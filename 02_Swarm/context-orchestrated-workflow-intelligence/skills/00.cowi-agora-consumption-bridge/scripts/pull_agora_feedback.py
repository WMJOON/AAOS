#!/usr/bin/env python3
"""
Pull cortex-agora change_archive feedback/decisions and materialize COWI artifacts.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
COWI_ROOT = SKILL_ROOT.parent.parent

DEFAULT_EVENTS_ROOT = COWI_ROOT.parent / "cortex-agora" / "change_archive" / "events"
DEFAULT_OUT_ROOT = COWI_ROOT / "artifacts"
DEFAULT_STATE_FILE = COWI_ROOT / "registry" / "AGORA_PULL_STATE.json"


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
    parser.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT))
    parser.add_argument("--state-file", default=str(DEFAULT_STATE_FILE))
    parser.add_argument("--from-ts", default="")
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    events_root = Path(args.events_root).expanduser().resolve()
    out_root = Path(args.out_root).expanduser().resolve()
    state_file = Path(args.state_file).expanduser().resolve()

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
    change_by_id = {str(r.get("event_id", "")): r for r in proposal_changes}
    feedback_by_id = {str(r.get("feedback_id", "")): r for r in proposal_feedback}

    if not pending_decisions:
        cursor_desc = args.from_ts or str(
            state.get("proposal_cursors", {}).get(args.proposal_id, {}).get("last_decision_ts", "")
        )
        print(f"no new improvement decisions for proposal={args.proposal_id} cursor={cursor_desc or 'none'}")
        return 0

    generated: list[tuple[Path, str]] = []
    latest_ts = ""
    latest_decision_id = ""

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

        relation_payload = build_relation_context_map(
            proposal_id=args.proposal_id,
            decision=decision,
            source_snapshot=source_snapshot,
            feedback_rows=feedback_for_decision,
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

    if args.dry_run:
        print(
            f"[DRY-RUN] cursor would move to last_decision_ts={latest_ts} last_decision_id={latest_decision_id}"
        )
        return 0

    relation_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    for path, content in generated:
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
