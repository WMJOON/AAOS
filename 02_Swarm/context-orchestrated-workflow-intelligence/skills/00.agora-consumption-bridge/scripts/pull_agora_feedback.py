#!/usr/bin/env python3
"""
Pull cortex-agora change_archive feedback/decisions and materialize COWI artifacts.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
COWI_ROOT = SKILL_ROOT.parent.parent

DEFAULT_EVENTS_ROOT = COWI_ROOT.parent / "cortex-agora" / "change_archive" / "events"
DEFAULT_NAMESPACE_ROOT = COWI_ROOT / "agents"


def parse_iso8601(value: str) -> dt.datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    parsed = dt.datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp must include timezone: {value}")
    return parsed.astimezone(dt.timezone.utc)


def stamp_from_iso(value: str) -> str:
    return parse_iso8601(value).strftime("%Y%m%dT%H%M%SZ")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        item = json.loads(line)
        if not isinstance(item, dict):
            raise ValueError(f"{path}:{lineno} must be a JSON object")
        rows.append(item)
    return rows


def sanitize_token(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip().lower())
    return cleaned.strip("-") or "item"

def sanitize_namespace_token(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-")

def parse_namespace_from_path(path: Path) -> tuple[str, str] | None:
    parts = path.parts
    for idx, part in enumerate(parts):
        if part == "agents" and idx + 2 < len(parts):
            family = sanitize_namespace_token(parts[idx + 1])
            version = sanitize_namespace_token(parts[idx + 2])
            if family and version:
                return family, version
    return None

def resolve_agent_namespace(
    namespace_root: Path,
    agent_family: str,
    agent_version: str,
) -> tuple[str, str, Path]:
    parsed = parse_namespace_from_path(namespace_root)
    from_args = None
    if agent_family or agent_version:
        if not (agent_family and agent_version):
            raise ValueError("both --agent-family and --agent-version are required together")
        family = sanitize_namespace_token(agent_family)
        version = sanitize_namespace_token(agent_version)
        if not family or not version:
            raise ValueError("invalid --agent-family/--agent-version")
        from_args = (family, version)

    if from_args and parsed and from_args != parsed:
        raise ValueError(
            "agent namespace mismatch between args and --namespace-root "
            f"(args={from_args[0]}/{from_args[1]}, path={parsed[0]}/{parsed[1]})"
        )

    if parsed and not from_args:
        family, version = parsed
        return family, version, namespace_root

    if from_args:
        family, version = from_args
        if parsed:
            return family, version, namespace_root
        return family, version, (namespace_root / family / version)

    raise ValueError("cannot resolve agent namespace from --namespace-root or args")


def shorten_for_single_line(value: str, max_chars: int) -> str:
    if max_chars <= 0:
        max_chars = 6000
    compact = value.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\\n")
    if len(compact) <= max_chars:
        return compact
    return compact[: max_chars - 3] + "..."


def load_conversation_notes(
    *,
    source: str,
    proposal_id: str,
    session_id: str,
    provided_notes: str,
    remembering_query: str,
    remembering_bin: str,
    remembering_max_chars: int,
) -> tuple[str, str]:
    if source != "remembering-conversations":
        return provided_notes, ""

    query = remembering_query.strip() or f"{proposal_id} {session_id}".strip()
    if not query:
        raise ValueError("remembering-conversations source requires non-empty query")

    cmd = [remembering_bin, "search", query]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip() or "unknown error"
        raise RuntimeError(f"remembering-conversations search failed: {stderr}")
    raw = (proc.stdout or "").strip()
    return shorten_for_single_line(raw, remembering_max_chars), query


def read_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": "1", "proposal_cursors": {}}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"invalid state payload: {path}")
    payload.setdefault("version", "1")
    payload.setdefault("proposal_cursors", {})
    if not isinstance(payload["proposal_cursors"], dict):
        payload["proposal_cursors"] = {}
    return payload


def write_state(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_cursor_ts(state: dict[str, Any], proposal_id: str, from_ts: str) -> dt.datetime | None:
    if from_ts:
        return parse_iso8601(from_ts)
    cursor = state.get("proposal_cursors", {}).get(proposal_id, {})
    cursor_ts = str(cursor.get("last_decision_ts", "")).strip()
    if not cursor_ts:
        return None
    return parse_iso8601(cursor_ts)


def find_source_snapshot(
    *,
    decision: dict[str, Any],
    proposal_changes: list[dict[str, Any]],
    change_by_id: dict[str, dict[str, Any]],
) -> dict[str, str]:
    for event_id in decision.get("applied_event_ids", []):
        row = change_by_id.get(str(event_id))
        if row:
            snap = row.get("source_snapshot", {})
            return {
                "agora_ref": str(snap.get("agora_ref", "")),
                "captured_at": str(snap.get("captured_at", "")),
            }

    decision_ts = parse_iso8601(str(decision.get("ts", "")))
    candidates = [
        row
        for row in proposal_changes
        if parse_iso8601(str(row.get("ts", ""))) <= decision_ts
    ]
    if candidates:
        snap = candidates[-1].get("source_snapshot", {})
        return {
            "agora_ref": str(snap.get("agora_ref", "")),
            "captured_at": str(snap.get("captured_at", "")),
        }
    return {"agora_ref": "", "captured_at": ""}


def build_relation_context_map(
    *,
    proposal_id: str,
    decision: dict[str, Any],
    source_snapshot: dict[str, str],
    feedback_rows: list[dict[str, Any]],
    conversation_context: dict[str, Any],
    agent_namespace: dict[str, str],
) -> dict[str, Any]:
    decision_id = str(decision.get("decision_id", "unknown"))
    decision_label = str(decision.get("decision", "unknown"))
    feedback_ids = [str(row.get("feedback_id", "")) for row in feedback_rows]
    return {
        "workflow_id": f"wf-{sanitize_token(proposal_id)}",
        "ticket_context_id": f"ctx-{sanitize_token(proposal_id)}",
        "topology_nodes": [
            {
                "node_id": "cortex-agora",
                "role": "observer",
                "purpose": "upstream behavior observation",
            },
            {
                "node_id": "cowi",
                "role": "mediator",
                "purpose": "context adaptation and local proposal shaping",
            },
            {
                "node_id": "awt-cof-handoff",
                "role": "handoff",
                "purpose": "bridge design intent and operating context",
            },
        ],
        "context_links": [
            {
                "from": "cortex-agora",
                "to": "cowi",
                "relation": "source_snapshot",
                "note": f"agora_ref={source_snapshot.get('agora_ref', '')}",
            },
            {
                "from": "cowi",
                "to": "awt-cof-handoff",
                "relation": "adaptation_report",
                "note": f"decision={decision_label}",
            },
        ],
        "handoff_rules": [
            {
                "source": "cortex-agora",
                "destination": "cowi",
                "condition": "new improvement_decision detected",
                "payload_contract": "source_snapshot.agora_ref + feedback_refs",
            },
            {
                "source": "cowi",
                "destination": "awt-cof-handoff",
                "condition": "manual mediation batch completed",
                "payload_contract": f"decision_id={decision_id}; feedback_refs={','.join(feedback_ids)}",
            },
        ],
        "conversation_context": conversation_context,
        "agent_namespace": agent_namespace,
        "conflict_resolution_rule": {
            "strategy": "cortex-agora-source-first",
            "escalation_path": "01_Nucleus/deliberation_chamber",
            "owner": "context-orchestrated-workflow-intelligence",
        },
    }


def build_adaptation_report_markdown(
    *,
    proposal_id: str,
    decision: dict[str, Any],
    source_snapshot: dict[str, str],
    feedback_rows: list[dict[str, Any]],
    conversation_context: dict[str, Any],
) -> str:
    feedback_lines: list[str] = []
    impact_lines: list[str] = []
    adjustment_lines: list[str] = []
    for index, row in enumerate(feedback_rows, start=1):
        feedback_id = str(row.get("feedback_id", ""))
        summary = str(row.get("summary", "")).strip()
        stance = str(row.get("stance", "critique"))
        confidence = "0.8" if stance == "critique" else "0.6"
        feedback_lines.append(f"- pattern: `{stance}` / `{feedback_id}`")
        feedback_lines.append("  - evidence:")
        feedback_lines.append(f"    - {summary or 'no summary'}")
        feedback_lines.append(f"  - confidence: {confidence}")
        impact_lines.append(f"- scope: `handoff-{index}`")
        impact_lines.append(f"  - impact: `{summary or 'n/a'}`")
        impact_lines.append("  - risk: `source contract drift`")
        adjustment_lines.append(f"- id: `adj-{index:03d}`")
        adjustment_lines.append(f"  - summary: `{summary or 'n/a'}`")
        adjustment_lines.append("  - guardrails:")
        adjustment_lines.append("    - `source_snapshot.agora_ref required`")

    if not feedback_lines:
        feedback_lines = [
            "- pattern: `decision-only`",
            "  - evidence:",
            "    - no feedback refs attached",
            "  - confidence: 0.5",
        ]
        impact_lines = [
            "- scope: `handoff`",
            "  - impact: `decision tracked without additional peer critique`",
            "  - risk: `under-specified adaptation scope`",
        ]
        adjustment_lines = [
            "- id: `adj-001`",
            "  - summary: `run next mediation cycle with richer feedback refs`",
            "  - guardrails:",
            "    - `require at least one critique ref for future major changes`",
        ]

    decision_id = str(decision.get("decision_id", ""))
    decision_label = str(decision.get("decision", ""))
    decision_ts = str(decision.get("ts", ""))
    rationale = str(decision.get("rationale", ""))

    lines = [
        "# skill_usage_adaptation_report",
        "",
        "## source_snapshot",
        f"- agora_ref: `{source_snapshot.get('agora_ref', '')}`",
        f"- captured_at: `{source_snapshot.get('captured_at', '')}`",
        f"- period: `{decision_ts}`",
        f"- notes: `proposal={proposal_id}; decision_id={decision_id}; decision={decision_label}`",
        "",
        "## usage_patterns",
        *feedback_lines,
        "",
        "## cof_awt_impact",
        *impact_lines,
        "",
        "## proposed_adjustments",
        *adjustment_lines,
        "",
        "## expected_effect",
        "- hypotheses:",
        f"  - `decision rationale applied: {rationale or 'n/a'}`",
        "  - `agora_ref-first consumption reduces interpretation drift`",
        "- success_signals:",
        "  - `relation_context_map generated for each decision`",
        "  - `feedback refs remain traceable to cortex-agora`",
        "- review_cycle: `daily-manual`",
        "",
        "## conversation_alignment",
        f"- source: `{conversation_context.get('source', '')}`",
        f"- session_id: `{conversation_context.get('session_id', '')}`",
        f"- snapshot_path: `{conversation_context.get('snapshot_path', '')}`",
        "- decision_refs:",
        *[f"  - `{ref}`" for ref in conversation_context.get("decision_refs", [])],
        f"- note: `captured_at={conversation_context.get('captured_at', '')}`",
        "",
        "## rollback_rule",
        "- trigger: `agora_ref missing or inconsistent with source_snapshot contract`",
        "- action: `discard generated artifact and rerun pull after source correction`",
        "- owner: `context-orchestrated-workflow-intelligence`",
        "",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Pull cortex-agora feedback/decisions for COWI")
    parser.add_argument("--proposal-id", required=True)
    parser.add_argument("--events-root", default=str(DEFAULT_EVENTS_ROOT))
    parser.add_argument("--namespace-root", default=str(DEFAULT_NAMESPACE_ROOT))
    parser.add_argument("--state-file", default="")
    parser.add_argument("--agent-family", default="")
    parser.add_argument("--agent-version", default="")
    parser.add_argument("--conversation-source", default="external-memory")
    parser.add_argument("--conversation-session-id", default="")
    parser.add_argument("--conversation-notes", default="")
    parser.add_argument("--remembering-query", default="")
    parser.add_argument("--remembering-bin", default="episodic-memory")
    parser.add_argument("--remembering-max-chars", type=int, default=6000)
    parser.add_argument("--from-ts", default="")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    events_root = Path(args.events_root).expanduser().resolve()
    namespace_root_input = Path(args.namespace_root).expanduser().resolve()
    family, version, namespace_root = resolve_agent_namespace(
        namespace_root_input,
        args.agent_family,
        args.agent_version,
    )
    out_root = namespace_root / "artifacts"
    state_file = (
        Path(args.state_file).expanduser().resolve()
        if args.state_file.strip()
        else (namespace_root / "registry" / "AGORA_PULL_STATE.json")
    )

    change_rows = load_jsonl(events_root / "CHANGE_EVENTS.jsonl")
    feedback_rows = load_jsonl(events_root / "PEER_FEEDBACK.jsonl")
    decision_rows = load_jsonl(events_root / "IMPROVEMENT_DECISIONS.jsonl")

    proposal_changes = [r for r in change_rows if str(r.get("proposal_id", "")) == args.proposal_id]
    proposal_feedback = [r for r in feedback_rows if str(r.get("proposal_id", "")) == args.proposal_id]
    proposal_decisions = [r for r in decision_rows if str(r.get("proposal_id", "")) == args.proposal_id]
    proposal_decisions.sort(key=lambda row: parse_iso8601(str(row.get("ts", ""))))

    state = read_state(state_file)
    cursor_ts = resolve_cursor_ts(state, args.proposal_id, args.from_ts)

    pending_decisions: list[dict[str, Any]] = []
    for row in proposal_decisions:
        row_ts = parse_iso8601(str(row.get("ts", "")))
        if cursor_ts is None or row_ts > cursor_ts:
            pending_decisions.append(row)

    relation_dir = out_root / "relation_context_map"
    report_dir = out_root / "skill_usage_adaptation_report"
    snapshot_dir = namespace_root / "conversation_snapshots"
    change_by_id = {str(r.get("event_id", "")): r for r in proposal_changes}
    feedback_by_id = {str(r.get("feedback_id", "")): r for r in proposal_feedback}

    if not pending_decisions:
        cursor_desc = args.from_ts or str(
            state.get("proposal_cursors", {}).get(args.proposal_id, {}).get("last_decision_ts", "")
        )
        print(f"no new improvement decisions for proposal={args.proposal_id} cursor={cursor_desc or 'none'}")
        return 0

    generated: list[tuple[Path, str]] = []
    snapshot_writes: list[tuple[Path, str]] = []
    latest_ts = ""
    latest_decision_id = ""
    session_id = args.conversation_session_id.strip() or f"session-{sanitize_token(args.proposal_id)}"
    conversation_notes, remembering_query = load_conversation_notes(
        source=args.conversation_source,
        proposal_id=args.proposal_id,
        session_id=session_id,
        provided_notes=args.conversation_notes,
        remembering_query=args.remembering_query,
        remembering_bin=args.remembering_bin,
        remembering_max_chars=args.remembering_max_chars,
    )
    namespace_payload = {
        "agent_family": family,
        "agent_version": version,
        "namespace_path": str(namespace_root),
    }

    for decision in pending_decisions:
        decision_id = str(decision.get("decision_id", "decision"))
        decision_ts = str(decision.get("ts", ""))
        stamp = stamp_from_iso(decision_ts)
        token = sanitize_token(args.proposal_id)
        decision_token = sanitize_token(decision_id)

        source_snapshot = find_source_snapshot(
            decision=decision,
            proposal_changes=proposal_changes,
            change_by_id=change_by_id,
        )
        feedback_refs = [str(item) for item in decision.get("feedback_refs", [])]
        feedback_for_decision = [feedback_by_id[item] for item in feedback_refs if item in feedback_by_id]
        snapshot_path = snapshot_dir / f"{stamp}__{token}__{decision_token}.md"
        conversation_context = {
            "source": args.conversation_source,
            "session_id": session_id,
            "captured_at": decision_ts,
            "snapshot_path": str(snapshot_path),
            "decision_refs": [decision_id, *feedback_refs],
        }
        snapshot_writes.append(
            (
                snapshot_path,
                "\n".join(
                    [
                        "# conversation_snapshot",
                        "",
                        f"- source: `{args.conversation_source}`",
                        f"- query: `{remembering_query}`",
                        f"- session_id: `{session_id}`",
                        f"- captured_at: `{decision_ts}`",
                        f"- proposal_id: `{args.proposal_id}`",
                        f"- decision_id: `{decision_id}`",
                        f"- feedback_refs: `{','.join(feedback_refs)}`",
                        f"- notes: `{conversation_notes}`",
                        "",
                    ]
                ),
            )
        )

        relation_payload = build_relation_context_map(
            proposal_id=args.proposal_id,
            decision=decision,
            source_snapshot=source_snapshot,
            feedback_rows=feedback_for_decision,
            conversation_context=conversation_context,
            agent_namespace=namespace_payload,
        )
        relation_path = relation_dir / f"{stamp}__{token}__{decision_token}.yaml"
        report_path = report_dir / f"{stamp}__{token}__{decision_token}.md"

        generated.append((relation_path, json.dumps(relation_payload, ensure_ascii=False, indent=2) + "\n"))
        generated.append(
            (
                report_path,
                build_adaptation_report_markdown(
                    proposal_id=args.proposal_id,
                    decision=decision,
                    source_snapshot=source_snapshot,
                    feedback_rows=feedback_for_decision,
                    conversation_context=conversation_context,
                ),
            )
        )

        latest_ts = decision_ts
        latest_decision_id = decision_id

    print(
        f"proposal={args.proposal_id} pending_decisions={len(pending_decisions)} generated_files={len(generated)}"
    )
    for path, _ in generated:
        print(f"- {path}")
    for path, _ in snapshot_writes:
        print(f"- {path}")

    if args.dry_run:
        print(
            f"[DRY-RUN] cursor would move to last_decision_ts={latest_ts} last_decision_id={latest_decision_id}"
        )
        return 0

    relation_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    for path, content in generated:
        path.write_text(content, encoding="utf-8")
    for path, content in snapshot_writes:
        path.write_text(content, encoding="utf-8")

    proposal_cursors = state.setdefault("proposal_cursors", {})
    if not isinstance(proposal_cursors, dict):
        proposal_cursors = {}
        state["proposal_cursors"] = proposal_cursors
    proposal_cursors[args.proposal_id] = {
        "last_decision_ts": latest_ts,
        "last_decision_id": latest_decision_id,
    }
    write_state(state_file, state)
    print(f"updated state: {state_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
