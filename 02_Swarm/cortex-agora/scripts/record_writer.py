#!/usr/bin/env python3
"""
Unified Obsidian-Bases-optimized record writer for AAOS Swarms.

Each record becomes an individual .md file with YAML frontmatter,
queryable by Obsidian Bases (.base) views.

File naming: {PREFIX}-{YYYYMMDDTHHMMSSZ}-{slug}.md
Frontmatter: flat top-level YAML (no nesting — Bases limitation).
Policy: append-only (files are never modified after creation,
except sealed: false -> true one-way transition).
"""

from __future__ import annotations

import datetime as dt
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

RECORD_TYPES = {
    "behavior_event",
    "change_event",
    "peer_feedback",
    "improvement_decision",
}

PREFIX_MAP = {
    "behavior_event": "BEV",
    "change_event": "CE",
    "peer_feedback": "FB",
    "improvement_decision": "ID",
}

SUBDIRECTORY_MAP = {
    "behavior_event": "behavior",
    "change_event": "change_events",
    "peer_feedback": "peer_feedback",
    "improvement_decision": "improvement_decisions",
}

ID_FIELD_MAP = {
    "behavior_event": "event_id",
    "change_event": "event_id",
    "peer_feedback": "feedback_id",
    "improvement_decision": "decision_id",
}

REQUIRED_FIELDS: dict[str, list[str]] = {
    "behavior_event": [
        "event_id", "ts", "swarm_id", "actor", "kind",
    ],
    "change_event": [
        "event_id", "ts", "proposal_id", "change_type", "actor",
        "source_agora_ref", "source_captured_at", "artifact_ref", "status",
    ],
    "peer_feedback": [
        "feedback_id", "ts", "proposal_id", "reviewer", "stance",
        "summary", "linked_event_id",
    ],
    "improvement_decision": [
        "decision_id", "ts", "proposal_id", "decision", "rationale",
        "next_action",
    ],
}

SWARM_SHORT_NAMES = {
    "context-orchestrated-filesystem": "cof",
    "agentic-workflow-topology": "awt",
    "cortex-agora": "cortex-agora",
    "context-orchestrated-workflow-intelligence": "cowi",
}

# ---------------------------------------------------------------------------
# Timestamp helpers
# ---------------------------------------------------------------------------


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso_now() -> str:
    return utc_now().strftime("%Y-%m-%dT%H:%M:%SZ")


def stamp_now() -> str:
    return utc_now().strftime("%Y%m%dT%H%M%SZ")


def parse_iso8601(value: str) -> dt.datetime:
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = dt.datetime.fromisoformat(normalized)
    except Exception as exc:
        raise ValueError(f"invalid ISO-8601 timestamp: {value}") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp must include timezone: {value}")
    return parsed.astimezone(dt.timezone.utc)


def ts_to_stamp(ts_str: str) -> str:
    """Convert ISO-8601 ts to filename-safe stamp YYYYMMDDTHHMMSSZ."""
    parsed = parse_iso8601(ts_str)
    return parsed.strftime("%Y%m%dT%H%M%SZ")


# ---------------------------------------------------------------------------
# String helpers
# ---------------------------------------------------------------------------


def sanitize_token(value: str, max_len: int = 60) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip())
    cleaned = cleaned.strip("-") or "item"
    return cleaned[:max_len]


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_record(record_type: str, record: dict[str, Any]) -> None:
    if record_type not in RECORD_TYPES:
        raise ValueError(f"unknown record_type: {record_type}")

    missing = [
        f for f in REQUIRED_FIELDS[record_type]
        if f not in record or record[f] is None or record[f] == ""
    ]
    if missing:
        raise ValueError(
            f"missing required fields for {record_type}: {missing}"
        )

    ts_value = str(record.get("ts", ""))
    if ts_value:
        parse_iso8601(ts_value)


# ---------------------------------------------------------------------------
# Frontmatter & body rendering
# ---------------------------------------------------------------------------


def _yaml_value(value: Any) -> str:
    """Render a single YAML value."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        if not value:
            return "[]"
        items = "\n".join(f"  - {json.dumps(v, ensure_ascii=False) if isinstance(v, str) else v}" for v in value)
        return f"\n{items}"
    if isinstance(value, str):
        if "\n" in value or ":" in value or value.startswith(("{", "[", '"')):
            return json.dumps(value, ensure_ascii=False)
        return f'"{value}"'
    return json.dumps(value, ensure_ascii=False)


def render_frontmatter(record: dict[str, Any]) -> str:
    lines = ["---"]
    for key, value in record.items():
        rendered = _yaml_value(value)
        if rendered.startswith("\n"):
            lines.append(f"{key}:{rendered}")
        else:
            lines.append(f"{key}: {rendered}")
    lines.append("---")
    return "\n".join(lines)


def render_body(record_type: str, record: dict[str, Any]) -> str:
    id_field = ID_FIELD_MAP[record_type]
    record_id = str(record.get(id_field, "unknown"))
    heading = f"# {record_id}"

    body_parts = [heading, ""]

    if record_type == "behavior_event":
        goal = record.get("context_goal", "")
        if goal:
            body_parts.append(goal)

    elif record_type == "change_event":
        change_type = record.get("change_type", "")
        proposal_id = record.get("proposal_id", "")
        body_parts.append(
            f"Change event: Proposal {proposal_id} {change_type}."
        )

    elif record_type == "peer_feedback":
        summary = record.get("summary", "")
        if summary:
            body_parts.append("## Summary")
            body_parts.append("")
            body_parts.append(summary)

    elif record_type == "improvement_decision":
        decision = record.get("decision", "")
        rationale = record.get("rationale", "")
        body_parts.append(f"## Decision: {decision}")
        body_parts.append("")
        if rationale:
            body_parts.append("## Rationale")
            body_parts.append("")
            body_parts.append(rationale)

    return "\n".join(body_parts) + "\n"


# ---------------------------------------------------------------------------
# Tag generation
# ---------------------------------------------------------------------------


def generate_tags(
    record_type: str,
    swarm_id: str,
    record: dict[str, Any],
    extra_tags: list[str] | None = None,
) -> list[str]:
    short = SWARM_SHORT_NAMES.get(swarm_id, sanitize_token(swarm_id))
    tags = [
        f"aaos/record/{record_type.replace('_', '-')}",
        f"aaos/swarm/{short}",
    ]

    proposal_id = record.get("proposal_id")
    if proposal_id:
        tags.append(f"aaos/proposal/{sanitize_token(str(proposal_id))}")

    stance = record.get("stance")
    if stance:
        tags.append(f"aaos/stance/{stance}")

    decision = record.get("decision")
    if decision:
        tags.append(f"aaos/decision/{decision}")

    kind = record.get("kind")
    if kind:
        tags.append(f"aaos/kind/{kind}")

    if extra_tags:
        tags.extend(extra_tags)

    return sorted(set(tags))


# ---------------------------------------------------------------------------
# Filename generation
# ---------------------------------------------------------------------------


def generate_filename(
    record_type: str,
    record: dict[str, Any],
) -> str:
    prefix = PREFIX_MAP[record_type]
    ts_str = str(record.get("ts", ""))
    stamp = ts_to_stamp(ts_str) if ts_str else stamp_now()

    id_field = ID_FIELD_MAP[record_type]
    slug = sanitize_token(str(record.get(id_field, "unknown")))

    filename = f"{prefix}-{stamp}-{slug}.md"
    if len(filename) > 120:
        filename = filename[:116] + ".md"
    return filename


# ---------------------------------------------------------------------------
# Monotonic timestamp & unique ID enforcement
# ---------------------------------------------------------------------------


def _read_frontmatter_field(path: Path, field: str) -> str | None:
    """Read a single frontmatter field from an .md file."""
    in_frontmatter = False
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    break
            if in_frontmatter and ":" in stripped:
                key, _, val = stripped.partition(":")
                if key.strip() == field:
                    return val.strip().strip('"').strip("'")
    return None


def assert_monotonic_ts(directory: Path, new_ts: str) -> None:
    if not directory.exists():
        return
    md_files = sorted(directory.glob("*.md"))
    if not md_files:
        return
    last_file = md_files[-1]
    last_ts = _read_frontmatter_field(last_file, "ts")
    if last_ts:
        last_dt = parse_iso8601(last_ts)
        new_dt = parse_iso8601(new_ts)
        if new_dt <= last_dt:
            raise RuntimeError(
                f"non-monotonic ts: {new_ts} <= {last_ts} (in {last_file.name})"
            )


def assert_unique_id(
    directory: Path,
    id_field: str,
    identifier: str,
) -> None:
    if not directory.exists():
        return
    for md_file in directory.glob("*.md"):
        existing_id = _read_frontmatter_field(md_file, id_field)
        if existing_id == identifier:
            raise RuntimeError(
                f"duplicate {id_field}: {identifier} (in {md_file.name})"
            )


# ---------------------------------------------------------------------------
# Core write function
# ---------------------------------------------------------------------------


def write_record(
    records_root: Path,
    record_type: str,
    record: dict[str, Any],
    swarm_id: str,
    extra_tags: list[str] | None = None,
    dry_run: bool = False,
) -> Path:
    """
    Write a single record as an .md file with YAML frontmatter.

    Args:
        records_root: Path to the Swarm's records/ directory
        record_type: One of RECORD_TYPES
        record: Flat dict of record fields (no nesting)
        swarm_id: Swarm identifier for tag generation
        extra_tags: Additional tags to include
        dry_run: If True, print what would be written but don't write

    Returns:
        Path to the created .md file
    """
    validate_record(record_type, record)

    subdir = SUBDIRECTORY_MAP[record_type]
    target_dir = records_root / subdir
    target_dir.mkdir(parents=True, exist_ok=True)

    id_field = ID_FIELD_MAP[record_type]
    identifier = str(record[id_field])

    ts_str = str(record.get("ts", ""))
    assert_monotonic_ts(target_dir, ts_str)
    assert_unique_id(target_dir, id_field, identifier)

    tags = generate_tags(record_type, swarm_id, record, extra_tags)

    full_record = {
        "record_type": record_type,
        **record,
        "tags": tags,
        "sealed": record.get("sealed", False),
        "seal_ref": record.get("seal_ref", ""),
    }

    frontmatter = render_frontmatter(full_record)
    body = render_body(record_type, record)
    content = f"{frontmatter}\n{body}"

    filename = generate_filename(record_type, record)
    target_path = target_dir / filename

    if dry_run:
        print(f"[DRY-RUN] would write: {target_path}")
        print(content)
        return target_path

    tmp_fd, tmp_path = tempfile.mkstemp(
        dir=str(target_dir), suffix=".md.tmp"
    )
    try:
        with open(tmp_fd, "w", encoding="utf-8") as f:
            f.write(content)
        Path(tmp_path).rename(target_path)
    except Exception:
        Path(tmp_path).unlink(missing_ok=True)
        raise

    return target_path


# ---------------------------------------------------------------------------
# Seal mutation (the only allowed mutation)
# ---------------------------------------------------------------------------


def seal_record(path: Path, seal_ref: str) -> None:
    """
    One-way mutation: set sealed=true and seal_ref on a record file.
    Raises if already sealed.
    """
    if not path.exists():
        raise FileNotFoundError(f"record not found: {path}")

    text = path.read_text(encoding="utf-8")

    current_sealed = _read_frontmatter_field(path, "sealed")
    if current_sealed == "true":
        raise RuntimeError(f"record already sealed: {path}")

    text = re.sub(
        r'^sealed:\s*false\s*$',
        'sealed: true',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r'^seal_ref:\s*""?\s*$',
        f'seal_ref: "{seal_ref}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )

    path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Bulk read helpers (for scripts that consume records)
# ---------------------------------------------------------------------------


def load_records_from_md(
    directory: Path,
    record_type: str | None = None,
) -> list[dict[str, Any]]:
    """
    Read all .md record files in a directory and return their frontmatter
    as a list of dicts, sorted by ts.
    """
    if not directory.exists():
        return []

    records: list[dict[str, Any]] = []
    for md_file in sorted(directory.glob("*.md")):
        record = parse_md_frontmatter(md_file)
        if record is None:
            continue
        if record_type and record.get("record_type") != record_type:
            continue
        records.append(record)

    return records


def parse_md_frontmatter(path: Path) -> dict[str, Any] | None:
    """Parse YAML frontmatter from an .md file into a dict."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None

    end_idx = text.index("---", 3)
    fm_text = text[3:end_idx].strip()

    record: dict[str, Any] = {}
    current_key: str | None = None
    list_values: list[str] = []

    for line in fm_text.split("\n"):
        stripped = line.strip()

        # List continuation
        if stripped.startswith("- ") and current_key is not None:
            val = stripped[2:].strip().strip('"').strip("'")
            list_values.append(val)
            continue

        # Flush previous list
        if current_key and list_values:
            record[current_key] = list_values
            list_values = []
            current_key = None

        if ":" not in stripped:
            continue

        key, _, val = stripped.partition(":")
        key = key.strip()
        val = val.strip()

        if not val:
            # Might be a list starting on next line
            current_key = key
            list_values = []
            continue

        # Inline list: [a, b, c]
        if val.startswith("[") and val.endswith("]"):
            items = [
                v.strip().strip('"').strip("'")
                for v in val[1:-1].split(",")
                if v.strip()
            ]
            record[key] = items
            current_key = None
            continue

        # Scalar
        val = val.strip('"').strip("'")
        if val == "true":
            record[key] = True
        elif val == "false":
            record[key] = False
        else:
            try:
                record[key] = int(val)
            except ValueError:
                try:
                    record[key] = float(val)
                except ValueError:
                    record[key] = val
        current_key = None

    # Flush trailing list
    if current_key and list_values:
        record[current_key] = list_values

    return record


# ---------------------------------------------------------------------------
# JSONL compatibility helpers (for migration / fallback)
# ---------------------------------------------------------------------------


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for lineno, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{lineno} invalid JSONL") from exc
            if not isinstance(item, dict):
                raise ValueError(f"{path}:{lineno} expected JSON object")
            rows.append(item)
    return rows


def flatten_nested(
    record: dict[str, Any],
    parent_key: str = "",
    sep: str = "_",
) -> dict[str, Any]:
    """
    Flatten nested dicts for Bases compatibility.
    e.g. {"context": {"task_id": "x"}} -> {"context_task_id": "x"}
    Lists are preserved as-is.
    """
    items: list[tuple[str, Any]] = []
    for k, v in record.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_nested(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# ---------------------------------------------------------------------------
# CLI (for direct invocation / testing)
# ---------------------------------------------------------------------------


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="AAOS Swarm record writer (Obsidian Bases)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_write = sub.add_parser("write", help="write a record from JSON stdin")
    p_write.add_argument("--records-root", required=True)
    p_write.add_argument("--record-type", required=True, choices=sorted(RECORD_TYPES))
    p_write.add_argument("--swarm-id", required=True)
    p_write.add_argument("--dry-run", action="store_true")

    p_read = sub.add_parser("read", help="read records from a directory")
    p_read.add_argument("--directory", required=True)
    p_read.add_argument("--record-type", default=None)

    args = parser.parse_args()

    try:
        if args.command == "write":
            record = json.load(sys.stdin)
            path = write_record(
                records_root=Path(args.records_root),
                record_type=args.record_type,
                record=record,
                swarm_id=args.swarm_id,
                dry_run=args.dry_run,
            )
            print(f"wrote: {path}")
            return 0

        if args.command == "read":
            records = load_records_from_md(
                Path(args.directory),
                args.record_type,
            )
            for r in records:
                print(json.dumps(r, ensure_ascii=False, default=str))
            return 0

    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
