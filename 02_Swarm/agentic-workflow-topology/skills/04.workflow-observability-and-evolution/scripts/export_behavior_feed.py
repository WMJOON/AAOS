#!/usr/bin/env python3
"""
Export AWT SQLite SoT logs into append-only Behavior Feed JSONL.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sqlite3
from pathlib import Path
from typing import Any


def parse_iso8601(value: str) -> dt.datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    parsed = dt.datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp must include timezone: {value}")
    return parsed.astimezone(dt.timezone.utc)


def to_iso_z(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_row_timestamp(created_at: str | None, date_value: str | None) -> dt.datetime:
    if created_at:
        normalized = created_at.strip().replace(" ", "T")
        try:
            parsed = dt.datetime.fromisoformat(normalized)
        except ValueError:
            parsed = dt.datetime.strptime(created_at.strip(), "%Y-%m-%d %H:%M:%S")
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)

    if not date_value:
        return dt.datetime.now(dt.timezone.utc)
    parsed_date = dt.datetime.strptime(date_value.strip(), "%Y-%m-%d")
    return parsed_date.replace(tzinfo=dt.timezone.utc)


def load_existing_event_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    ids: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        row = json.loads(line)
        if isinstance(row, dict):
            event_id = str(row.get("event_id", ""))
            if event_id:
                ids.add(event_id)
    return ids


def map_kind(mode: str, action: str, transition_repeated: int) -> str:
    probe = f"{mode} {action}".lower()
    if "handoff" in probe:
        return "handoff"
    if "retry" in probe or transition_repeated == 1:
        return "retry"
    if "tool" in probe:
        return "tool_call"
    if "model" in probe:
        return "model_select"
    if "stop" in probe or "halt" in probe:
        return "stop"
    return "plan"


def map_outcome_status(raw_status: str) -> str:
    status = raw_status.strip().lower()
    if status == "success":
        return "success"
    if status == "fail":
        return "fail"
    return "halt"


def detect_human_intervention(notes: str, continuation_hint: str) -> bool:
    note_probe = f"{notes} {continuation_hint}".lower()
    if continuation_hint.strip():
        return True
    keywords = ("human", "manual", "승인", "검토", "개입")
    return any(token in note_probe for token in keywords)


def export_behavior_feed(
    *,
    db_path: Path,
    out_path: Path,
    from_ts: str,
    limit: int,
    dry_run: bool,
) -> int:
    if not db_path.exists():
        raise RuntimeError(f"db-path not found: {db_path}")

    lower_bound = parse_iso8601(from_ts) if from_ts else None

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute(
            """
            SELECT
                id,
                date,
                task_name,
                mode,
                action,
                status,
                notes,
                continuation_hint,
                transition_repeated,
                created_at
            FROM audit_logs
            ORDER BY
                CASE
                    WHEN created_at IS NULL OR trim(created_at) = '' THEN date || ' 00:00:00'
                    ELSE created_at
                END ASC,
                id ASC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cursor.fetchall()
    finally:
        conn.close()

    existing_ids = load_existing_event_ids(out_path)
    to_append: list[dict[str, Any]] = []
    skipped_duplicates = 0
    skipped_before_from_ts = 0

    for row in rows:
        audit_id = str(row["id"])
        timestamp = parse_row_timestamp(row["created_at"], row["date"])
        if lower_bound is not None and timestamp < lower_bound:
            skipped_before_from_ts += 1
            continue

        event_id = f"awt:{audit_id}"
        if event_id in existing_ids:
            skipped_duplicates += 1
            continue

        mode = str(row["mode"] or "")
        action = str(row["action"] or "")
        status = str(row["status"] or "")
        notes = str(row["notes"] or "")
        continuation_hint = str(row["continuation_hint"] or "")
        transition_repeated = int(row["transition_repeated"] or 0)

        group_id = f"{mode or 'default'}:{str(row['date'] or 'undated')}"
        event = {
            "event_id": event_id,
            "ts": to_iso_z(timestamp),
            "swarm_id": "agentic-workflow-topology",
            "group_id": group_id,
            "trace_id": group_id,  # backward compatibility
            "actor": "agent:awt",
            "kind": map_kind(mode, action, transition_repeated),
            "context": {
                "task_id": audit_id,
                "session_id": f"awt-{str(row['date'] or 'session')}",
                "task_name": str(row["task_name"] or ""),
                "mode": mode,
                "action": action,
            },
            "outcome": {
                "status": map_outcome_status(status),
                "human_intervention": detect_human_intervention(notes, continuation_hint),
            },
        }
        to_append.append(event)

    print(
        "rows_scanned={} to_append={} skipped_duplicates={} skipped_before_from_ts={}".format(
            len(rows),
            len(to_append),
            skipped_duplicates,
            skipped_before_from_ts,
        )
    )
    print(f"out_path={out_path}")

    if dry_run:
        print("[DRY-RUN] no file changes")
        return 0

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("a", encoding="utf-8") as f:
        for row in to_append:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"appended_events={len(to_append)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Export AWT SQLite logs to Behavior Feed JSONL")
    parser.add_argument("--db-path", required=True)
    parser.add_argument("--out-path", required=True)
    parser.add_argument("--from-ts", default="")
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        return export_behavior_feed(
            db_path=Path(args.db_path).expanduser().resolve(),
            out_path=Path(args.out_path).expanduser().resolve(),
            from_ts=args.from_ts,
            limit=args.limit,
            dry_run=args.dry_run,
        )
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
