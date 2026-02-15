#!/usr/bin/env python3
"""
Cortex Agora change archive bridge.

Records append-only change/feedback/decision events as individual .md
files with YAML frontmatter under 02_Swarm/cortex-agora/records/,
using the shared record_writer module for Obsidian Bases compatibility.

Can build/seal a package to 01_Nucleus/record_archive.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
CORTEX_ROOT = SCRIPT_DIR.parent
SCRIPTS_ROOT = CORTEX_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))
import record_writer as rw  # noqa: E402

RECORDS_ROOT = CORTEX_ROOT / "records"

# Legacy JSONL paths (kept for build-package backward compat reading)
CHANGE_ARCHIVE_ROOT = CORTEX_ROOT / "change_archive"
EVENTS_DIR = CHANGE_ARCHIVE_ROOT / "events"
LEGACY_CHANGE_EVENTS_PATH = EVENTS_DIR / "CHANGE_EVENTS.jsonl"
LEGACY_PEER_FEEDBACK_PATH = EVENTS_DIR / "PEER_FEEDBACK.jsonl"
LEGACY_IMPROVEMENT_DECISIONS_PATH = EVENTS_DIR / "IMPROVEMENT_DECISIONS.jsonl"

CHANGE_TYPES = {"created", "updated", "superseded", "withdrawn", "sealed"}
STATUSES = {"open", "improving", "closed", "sealed"}
FEEDBACK_STANCES = {"critique", "suggestion", "endorsement"}
DECISIONS = {"accepted", "partially_accepted", "deferred", "rejected"}


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso_now() -> str:
    return utc_now().strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp_now() -> str:
    return utc_now().strftime("%Y%m%dT%H%M%SZ")


def parse_iso8601(value: str) -> dt.datetime:
    try:
        normalized = value.strip()
        if normalized.endswith("Z"):
            normalized = normalized[:-1] + "+00:00"
        parsed = dt.datetime.fromisoformat(normalized)
    except Exception as exc:
        raise ValueError(f"invalid ISO-8601 timestamp: {value}") from exc

    if parsed.tzinfo is None:
        raise ValueError(f"timestamp must include timezone: {value}")
    return parsed.astimezone(dt.timezone.utc)


def sanitize_token(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip())
    return cleaned.strip("-") or "item"


def ensure_layout() -> None:
    for subdir in ["behavior", "change_events", "peer_feedback", "improvement_decisions"]:
        (RECORDS_ROOT / subdir).mkdir(parents=True, exist_ok=True)


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def ensure_event_exists(event_id: str) -> None:
    for row in rw.load_records_from_md(RECORDS_ROOT / "change_events", "change_event"):
        if str(row.get("event_id", "")) == event_id:
            return
    raise RuntimeError(f"linked change event not found: {event_id}")


def ensure_feedback_exists(feedback_id: str) -> None:
    for row in rw.load_records_from_md(RECORDS_ROOT / "peer_feedback", "peer_feedback"):
        if str(row.get("feedback_id", "")) == feedback_id:
            return
    raise RuntimeError(f"feedback ref not found: {feedback_id}")


def parse_csv_list(value: str) -> list[str]:
    if not value.strip():
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def cmd_record_change(args: argparse.Namespace) -> int:
    ensure_layout()

    if args.change_type not in CHANGE_TYPES:
        raise RuntimeError(f"invalid change_type: {args.change_type}")
    if args.status not in STATUSES:
        raise RuntimeError(f"invalid status: {args.status}")

    parse_iso8601(args.ts)
    parse_iso8601(args.captured_at)

    event_id = args.event_id or (
        f"ce_{stamp_now()}_{sanitize_token(args.proposal_id)}_{sanitize_token(args.change_type)}"
    )

    record = {
        "event_id": event_id,
        "ts": args.ts,
        "proposal_id": args.proposal_id,
        "change_type": args.change_type,
        "actor": args.actor,
        "source_agora_ref": args.agora_ref,
        "source_captured_at": args.captured_at,
        "artifact_ref": args.artifact_ref,
        "status": args.status,
    }

    path = rw.write_record(RECORDS_ROOT, "change_event", record, "cortex-agora")
    print(f"recorded change event: {event_id} -> {path.name}")
    return 0


def cmd_record_feedback(args: argparse.Namespace) -> int:
    ensure_layout()

    if args.stance not in FEEDBACK_STANCES:
        raise RuntimeError(f"invalid stance: {args.stance}")

    parse_iso8601(args.ts)
    ensure_event_exists(args.linked_event_id)

    feedback_id = args.feedback_id or (
        f"fb_{stamp_now()}_{sanitize_token(args.proposal_id)}_{sanitize_token(args.reviewer)}"
    )

    record = {
        "feedback_id": feedback_id,
        "ts": args.ts,
        "proposal_id": args.proposal_id,
        "reviewer": args.reviewer,
        "reviewer_model_family": args.reviewer_model_family,
        "reviewer_provider": args.reviewer_provider,
        "stance": args.stance,
        "summary": args.summary,
        "linked_event_id": args.linked_event_id,
    }

    path = rw.write_record(RECORDS_ROOT, "peer_feedback", record, "cortex-agora")
    print(f"recorded feedback event: {feedback_id} -> {path.name}")
    return 0


def cmd_record_decision(args: argparse.Namespace) -> int:
    ensure_layout()

    if args.decision not in DECISIONS:
        raise RuntimeError(f"invalid decision: {args.decision}")
    parse_iso8601(args.ts)

    applied_ids = parse_csv_list(args.applied_event_ids)
    feedback_refs = parse_csv_list(args.feedback_refs)

    for event_id in applied_ids:
        ensure_event_exists(event_id)
    for feedback_id in feedback_refs:
        ensure_feedback_exists(feedback_id)

    decision_id = args.decision_id or (
        f"id_{stamp_now()}_{sanitize_token(args.proposal_id)}_{sanitize_token(args.decision)}"
    )

    record = {
        "decision_id": decision_id,
        "ts": args.ts,
        "proposal_id": args.proposal_id,
        "decision": args.decision,
        "rationale": args.rationale,
        "applied_event_ids": applied_ids,
        "feedback_refs": feedback_refs,
        "next_action": args.next_action,
    }

    path = rw.write_record(RECORDS_ROOT, "improvement_decision", record, "cortex-agora")
    print(f"recorded improvement decision: {decision_id} -> {path.name}")
    return 0


def in_range(ts_value: str, start: dt.datetime, end: dt.datetime) -> bool:
    parsed = parse_iso8601(ts_value)
    return start <= parsed <= end


def cmd_build_package(args: argparse.Namespace) -> int:
    ensure_layout()

    start_ts = parse_iso8601(args.from_ts)
    end_ts = parse_iso8601(args.to_ts)
    if end_ts < start_ts:
        raise RuntimeError("to-ts must be greater than or equal to from-ts")

    out_dir = Path(args.out).expanduser().resolve()
    if out_dir.exists() and any(out_dir.iterdir()):
        raise RuntimeError(f"out directory must be empty: {out_dir}")
    out_dir.mkdir(parents=True, exist_ok=True)

    payload_dir = out_dir / "payload"
    payload_dir.mkdir(parents=True, exist_ok=True)

    # Read from .md record files
    change_rows = [
        r for r in rw.load_records_from_md(RECORDS_ROOT / "change_events", "change_event")
        if in_range(str(r.get("ts", "")), start_ts, end_ts)
    ]
    feedback_rows = [
        r for r in rw.load_records_from_md(RECORDS_ROOT / "peer_feedback", "peer_feedback")
        if in_range(str(r.get("ts", "")), start_ts, end_ts)
    ]
    decision_rows = [
        r for r in rw.load_records_from_md(RECORDS_ROOT / "improvement_decisions", "improvement_decision")
        if in_range(str(r.get("ts", "")), start_ts, end_ts)
    ]

    # Output still uses JSONL in the package payload (seal format unchanged)
    write_jsonl(payload_dir / "CHANGE_EVENTS.jsonl", change_rows)
    write_jsonl(payload_dir / "PEER_FEEDBACK.jsonl", feedback_rows)
    write_jsonl(payload_dir / "IMPROVEMENT_DECISIONS.jsonl", decision_rows)

    proposal_ids = sorted({str(r.get("proposal_id", "")) for r in change_rows if r.get("proposal_id")})

    summary_md = (
        "# cortex-agora change review summary\n\n"
        f"- from_ts: `{args.from_ts}`\n"
        f"- to_ts: `{args.to_ts}`\n"
        f"- change_events: `{len(change_rows)}`\n"
        f"- peer_feedback: `{len(feedback_rows)}`\n"
        f"- improvement_decisions: `{len(decision_rows)}`\n"
        f"- proposals: `{', '.join(proposal_ids) if proposal_ids else '-'}`\n"
    )
    (payload_dir / "SUMMARY.md").write_text(summary_md, encoding="utf-8")

    package_id = out_dir.name
    package_md = f"""---
timestamp: "{iso_now()}"
package_id: "{package_id}"
type: "swarm-observability"
status: "staged"
source_refs:
  - "04_Agentic_AI_OS/02_Swarm/cortex-agora/records/change_events/"
  - "04_Agentic_AI_OS/02_Swarm/cortex-agora/records/peer_feedback/"
  - "04_Agentic_AI_OS/02_Swarm/cortex-agora/records/improvement_decisions/"
targets:
  - "04_Agentic_AI_OS/02_Swarm/cortex-agora"
integrity:
  manifest: "MANIFEST.sha256"
created_by:
  actor: "change_archive_bridge"
  method: "tool"
notes: "cortex-agora local change archive package"
---
# Archive Package

## Summary

- Why this package exists: preserve local append-only change/feedback/decision history for record_archive sealing.
- What it proves: cortex-agora proposal evolution and downstream critique/improvement traces.
- What can be reproduced from it: exact event/feedback/decision payload and hashes.

## Contents

- `payload/CHANGE_EVENTS.jsonl`
- `payload/PEER_FEEDBACK.jsonl`
- `payload/IMPROVEMENT_DECISIONS.jsonl`
- `payload/SUMMARY.md`
"""
    (out_dir / "PACKAGE.md").write_text(package_md, encoding="utf-8")

    manifest_lines: list[str] = []
    for filename in [
        "CHANGE_EVENTS.jsonl",
        "PEER_FEEDBACK.jsonl",
        "IMPROVEMENT_DECISIONS.jsonl",
        "SUMMARY.md",
    ]:
        rel = f"payload/{filename}"
        file_hash = sha256_file(payload_dir / filename)
        manifest_lines.append(f"{file_hash}  {rel}")
    (out_dir / "MANIFEST.sha256").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    print(f"package built: {out_dir}")
    print(f"change_events={len(change_rows)} feedback={len(feedback_rows)} decisions={len(decision_rows)}")
    return 0


def cmd_seal_to_record_archive(args: argparse.Namespace) -> int:
    package_dir = Path(args.package_dir).expanduser().resolve()
    if not package_dir.is_dir():
        raise RuntimeError(f"package-dir not found: {package_dir}")

    required = [package_dir / "PACKAGE.md", package_dir / "MANIFEST.sha256", package_dir / "payload"]
    for req in required:
        if not req.exists():
            raise RuntimeError(f"missing required package component: {req}")

    record_archive_root = Path(args.record_archive_root).expanduser().resolve()
    ledger_script = record_archive_root / "scripts" / "ledger_keeper.py"
    if not ledger_script.exists():
        raise RuntimeError(f"ledger_keeper.py not found: {ledger_script}")

    ts = stamp_now()
    destination = (
        record_archive_root
        / "_archive"
        / "operations"
        / f"{ts}__swarm-observability__cortex-agora-change-review"
    )

    if args.dry_run:
        print(f"[DRY-RUN] would copy package to: {destination}")
        print(
            "[DRY-RUN] would run ledger seal command with --summary/--targets/--notes "
            "against staged package under record_archive/_archive/operations/"
        )
        print("[DRY-RUN] seal of .md records skipped")
        return 0
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(package_dir, destination)
    seal_target = destination

    cmd = [
        sys.executable,
        str(ledger_script),
        "seal",
        str(seal_target),
        "--summary",
        args.summary,
    ]
    if args.targets.strip():
        cmd.extend(["--targets", args.targets])
    if args.notes.strip():
        cmd.extend(["--notes", args.notes])

    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        raise RuntimeError("ledger seal failed")

    rel_pkg = destination.relative_to(record_archive_root).as_posix() + "/"

    # Read the sealed JSONL to identify time range, then seal source .md records
    packaged_changes = rw.load_jsonl(destination / "payload" / "CHANGE_EVENTS.jsonl")
    if packaged_changes:
        start_ts = parse_iso8601(str(packaged_changes[0].get("ts", "")))
        end_ts = parse_iso8601(str(packaged_changes[-1].get("ts", "")))

        for subdir in ["change_events", "peer_feedback", "improvement_decisions"]:
            records_dir = RECORDS_ROOT / subdir
            if not records_dir.exists():
                continue
            for md_file in sorted(records_dir.glob("*.md")):
                ts_val = rw._read_frontmatter_field(md_file, "ts")
                if ts_val and in_range(ts_val, start_ts, end_ts):
                    sealed = rw._read_frontmatter_field(md_file, "sealed")
                    if sealed != "true":
                        rw.seal_record(md_file, rel_pkg)

    print(f"sealed package: {rel_pkg}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="cortex-agora change archive bridge")
    sub = parser.add_subparsers(dest="command", required=True)

    p_change = sub.add_parser("record-change", help="append change event")
    p_change.add_argument("--proposal-id", required=True)
    p_change.add_argument("--change-type", required=True, choices=sorted(CHANGE_TYPES))
    p_change.add_argument("--actor", required=True)
    p_change.add_argument("--artifact-ref", required=True)
    p_change.add_argument("--agora-ref", required=True)
    p_change.add_argument("--captured-at", required=True)
    p_change.add_argument("--status", required=True, choices=sorted(STATUSES))
    p_change.add_argument("--ts", default=iso_now())
    p_change.add_argument("--event-id", default="")

    p_feedback = sub.add_parser("record-feedback", help="append peer feedback")
    p_feedback.add_argument("--proposal-id", required=True)
    p_feedback.add_argument("--reviewer", required=True)
    p_feedback.add_argument("--reviewer-model-family", required=True)
    p_feedback.add_argument("--reviewer-provider", required=True)
    p_feedback.add_argument("--stance", required=True, choices=sorted(FEEDBACK_STANCES))
    p_feedback.add_argument("--summary", required=True)
    p_feedback.add_argument("--linked-event-id", required=True)
    p_feedback.add_argument("--ts", default=iso_now())
    p_feedback.add_argument("--feedback-id", default="")

    p_decision = sub.add_parser("record-decision", help="append improvement decision")
    p_decision.add_argument("--proposal-id", required=True)
    p_decision.add_argument("--decision", required=True, choices=sorted(DECISIONS))
    p_decision.add_argument("--rationale", required=True)
    p_decision.add_argument("--applied-event-ids", default="")
    p_decision.add_argument("--feedback-refs", default="")
    p_decision.add_argument("--next-action", required=True)
    p_decision.add_argument("--ts", default=iso_now())
    p_decision.add_argument("--decision-id", default="")

    p_build = sub.add_parser("build-package", help="build staging package")
    p_build.add_argument("--from-ts", required=True)
    p_build.add_argument("--to-ts", required=True)
    p_build.add_argument("--out", required=True)

    p_seal = sub.add_parser("seal-to-record-archive", help="seal package to record_archive")
    p_seal.add_argument("--package-dir", required=True)
    p_seal.add_argument("--record-archive-root", required=True)
    p_seal.add_argument("--summary", required=True)
    p_seal.add_argument("--targets", default="")
    p_seal.add_argument("--notes", default="")
    p_seal.add_argument("--dry-run", action="store_true")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "record-change":
            return cmd_record_change(args)
        if args.command == "record-feedback":
            return cmd_record_feedback(args)
        if args.command == "record-decision":
            return cmd_record_decision(args)
        if args.command == "build-package":
            return cmd_build_package(args)
        if args.command == "seal-to-record-archive":
            return cmd_seal_to_record_archive(args)
        raise RuntimeError(f"unsupported command: {args.command}")
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
