#!/usr/bin/env python3
"""
Export AWT SQLite SoT logs into append-only Behavior Feed records (.md).

Output uses the unified record_writer (Obsidian Bases format).
Legacy JSONL mode is preserved when --out-path ends in .jsonl.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_AWT_ROOT = SCRIPT_DIR.parent.parent.parent.parent

# record_writer lives at 02_Swarm/cortex-agora/scripts/record_writer.py
SWARM_SCRIPTS = Path(__file__).resolve().parents[4] / "cortex-agora" / "scripts"  # 02_Swarm/cortex-agora/scripts/
sys.path.insert(0, str(SWARM_SCRIPTS))
import record_writer as rw  # noqa: E402


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
    *,
    out_path: Path | None,
    agent_family: str,
    agent_version: str,
) -> tuple[str, str]:
    from_path = parse_namespace_from_path(out_path) if out_path is not None else None
    from_args = None
    if agent_family or agent_version:
        if not (agent_family and agent_version):
            raise ValueError("both --agent-family and --agent-version are required together")
        family = sanitize_namespace_token(agent_family)
        version = sanitize_namespace_token(agent_version)
        if not family or not version:
            raise ValueError("invalid --agent-family/--agent-version")
        from_args = (family, version)

    if from_args and from_path and from_args != from_path:
        raise ValueError(
            "agent namespace mismatch between args and --out-path "
            f"(args={from_args[0]}/{from_args[1]}, path={from_path[0]}/{from_path[1]})"
        )
    if from_args:
        return from_args
    if from_path:
        return from_path
    raise ValueError("cannot resolve agent namespace from --out-path or args")


def _is_jsonl_path(raw: str) -> bool:
    """Return True if the user explicitly requested legacy JSONL output."""
    return raw.strip().lower().endswith(".jsonl")


def resolve_out_path(
    raw_out_path: str,
    awt_root: Path,
    agent_family: str,
    agent_version: str,
) -> tuple[Path, bool]:
    """Resolve the output destination.

    Returns:
        (path, is_jsonl) -- *path* is either a JSONL file (legacy) or
        the records root directory (new .md mode).
    """
    if raw_out_path.strip():
        out_path = Path(raw_out_path).expanduser().resolve()
        if _is_jsonl_path(raw_out_path):
            # Legacy JSONL mode
            parsed = parse_namespace_from_path(out_path)
            if parsed is None:
                raise ValueError(
                    "--out-path must include namespace segment "
                    "'agents/<agent-family>/<version>'"
                )
            return out_path, True
        # New directory mode -- treat as records root
        return out_path, False

    # Default: records root inside the AWT swarm
    return awt_root / "records", False


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


def load_existing_event_ids_jsonl(path: Path) -> set[str]:
    """Load event IDs from a legacy JSONL file."""
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


def load_existing_event_ids_md(records_root: Path) -> set[str]:
    """Load event IDs from .md records in records_root/behavior/."""
    behavior_dir = records_root / "behavior"
    if not behavior_dir.exists():
        return set()
    ids: set[str] = set()
    for rec in rw.load_records_from_md(behavior_dir, record_type="behavior_event"):
        event_id = str(rec.get("event_id", ""))
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


SWARM_ID = "agentic-workflow-topology"


def _build_event(
    row: sqlite3.Row,
    agent_family: str,
    agent_version: str,
) -> dict[str, Any]:
    """Build a behavior event dict from a SQLite row (unchanged logic)."""
    audit_id = str(row["id"])
    timestamp = parse_row_timestamp(row["created_at"], row["date"])

    mode = str(row["mode"] or "")
    action = str(row["action"] or "")
    status = str(row["status"] or "")
    notes = str(row["notes"] or "")
    continuation_hint = str(row["continuation_hint"] or "")
    transition_repeated = int(row["transition_repeated"] or 0)

    group_id = f"{mode or 'default'}:{str(row['date'] or 'undated')}"
    event = {
        "event_id": f"awt:{audit_id}",
        "ts": to_iso_z(timestamp),
        "swarm_id": SWARM_ID,
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
            "agent_namespace": {
                "agent_family": agent_family,
                "agent_version": agent_version,
            },
        },
        "outcome": {
            "status": map_outcome_status(status),
            "human_intervention": detect_human_intervention(notes, continuation_hint),
        },
    }
    return event


def export_behavior_feed(
    *,
    db_path: Path,
    out_path: Path,
    is_jsonl: bool,
    agent_family: str,
    agent_version: str,
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

    # Load existing IDs for deduplication
    if is_jsonl:
        existing_ids = load_existing_event_ids_jsonl(out_path)
    else:
        existing_ids = load_existing_event_ids_md(out_path)

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

        event = _build_event(row, agent_family, agent_version)
        to_append.append(event)

    print(
        "rows_scanned={} to_append={} skipped_duplicates={} skipped_before_from_ts={}".format(
            len(rows),
            len(to_append),
            skipped_duplicates,
            skipped_before_from_ts,
        )
    )
    print(f"out_path={out_path}  mode={'jsonl' if is_jsonl else 'md'}")

    if dry_run:
        print("[DRY-RUN] no file changes")
        return 0

    if is_jsonl:
        # Legacy JSONL append mode
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open("a", encoding="utf-8") as f:
            for ev in to_append:
                f.write(json.dumps(ev, ensure_ascii=False) + "\n")
        print(f"appended_events={len(to_append)}")
    else:
        # New .md record mode via record_writer
        written = 0
        for ev in to_append:
            flat = rw.flatten_nested(ev)
            rw.write_record(
                records_root=out_path,
                record_type="behavior_event",
                record=flat,
                swarm_id=SWARM_ID,
                dry_run=False,
            )
            written += 1
        print(f"written_records={written}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Export AWT SQLite logs to Behavior Feed records. "
            "Default output is .md (Obsidian Bases). "
            "Use --out-path *.jsonl for legacy JSONL mode."
        ),
    )
    parser.add_argument("--db-path", required=True)
    parser.add_argument(
        "--out-path",
        default="",
        help=(
            "Output destination. If a .jsonl file path, uses legacy append mode. "
            "If a directory path, uses as records root for .md output. "
            "Defaults to <awt-root>/records/."
        ),
    )
    parser.add_argument("--awt-root", default=str(DEFAULT_AWT_ROOT))
    parser.add_argument("--agent-family", default="")
    parser.add_argument("--agent-version", default="")
    parser.add_argument("--from-ts", default="")
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--dry-run", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        awt_root = Path(args.awt_root).expanduser().resolve()
        is_jsonl = _is_jsonl_path(args.out_path) if args.out_path.strip() else False

        if is_jsonl:
            # Legacy JSONL mode requires agent namespace resolution
            candidate_out_path = Path(args.out_path).expanduser().resolve()
            family, version = resolve_agent_namespace(
                out_path=candidate_out_path,
                agent_family=args.agent_family,
                agent_version=args.agent_version,
            )
        else:
            # .md mode -- agent namespace is still useful for the record context
            # but we don't require it from the path
            family = args.agent_family or "awt"
            version = args.agent_version or "default"

        out_path, out_is_jsonl = resolve_out_path(
            args.out_path, awt_root, family, version,
        )
        return export_behavior_feed(
            db_path=Path(args.db_path).expanduser().resolve(),
            out_path=out_path,
            is_jsonl=out_is_jsonl,
            agent_family=family,
            agent_version=version,
            from_ts=args.from_ts,
            limit=args.limit,
            dry_run=args.dry_run,
        )
    except Exception as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
