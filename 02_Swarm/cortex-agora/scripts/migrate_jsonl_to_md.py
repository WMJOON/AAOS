#!/usr/bin/env python3
"""
One-time migration: JSONL records -> individual .md files (Obsidian Bases).

Reads existing JSONL behavior feeds and change_archive events,
flattens nested fields, and writes .md records via record_writer.

Usage:
    python3 migrate_jsonl_to_md.py [--dry-run]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Resolve script location to find record_writer
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import record_writer as rw  # noqa: E402

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

SWARM_ROOT = SCRIPT_DIR.parent.parent  # 02_Swarm/

SOURCES = [
    # (swarm_id, jsonl_path, record_type, id_field_remap)
    {
        "swarm_id": "context-orchestrated-filesystem",
        "jsonl": SWARM_ROOT / "context-orchestrated-filesystem" / "behavior" / "BEHAVIOR_FEED.jsonl",
        "record_type": "behavior_event",
        "records_root": SWARM_ROOT / "context-orchestrated-filesystem" / "records",
    },
    {
        "swarm_id": "agentic-workflow-topology",
        "jsonl": SWARM_ROOT / "agentic-workflow-topology" / "behavior" / "BEHAVIOR_FEED.jsonl",
        "record_type": "behavior_event",
        "records_root": SWARM_ROOT / "agentic-workflow-topology" / "records",
    },
    {
        "swarm_id": "cortex-agora",
        "jsonl": SWARM_ROOT / "cortex-agora" / "behavior" / "BEHAVIOR_FEED.jsonl",
        "record_type": "behavior_event",
        "records_root": SWARM_ROOT / "cortex-agora" / "records",
    },
    {
        "swarm_id": "cortex-agora",
        "jsonl": SWARM_ROOT / "cortex-agora" / "change_archive" / "events" / "CHANGE_EVENTS.jsonl",
        "record_type": "change_event",
        "records_root": SWARM_ROOT / "cortex-agora" / "records",
    },
    {
        "swarm_id": "cortex-agora",
        "jsonl": SWARM_ROOT / "cortex-agora" / "change_archive" / "events" / "PEER_FEEDBACK.jsonl",
        "record_type": "peer_feedback",
        "records_root": SWARM_ROOT / "cortex-agora" / "records",
    },
    {
        "swarm_id": "cortex-agora",
        "jsonl": SWARM_ROOT / "cortex-agora" / "change_archive" / "events" / "IMPROVEMENT_DECISIONS.jsonl",
        "record_type": "improvement_decision",
        "records_root": SWARM_ROOT / "cortex-agora" / "records",
    },
]


# ---------------------------------------------------------------------------
# Field remapping per record type
# ---------------------------------------------------------------------------


def remap_behavior_event(raw: dict) -> dict:
    """Flatten a behavior_event JSONL record."""
    flat = rw.flatten_nested(raw)
    # Ensure standard field names
    remap = {}
    for k, v in flat.items():
        remap[k] = v
    # Ensure event_id exists
    if "event_id" not in remap:
        remap["event_id"] = f"migrated:{remap.get('ts', 'unknown')}"
    return remap


def remap_change_event(raw: dict) -> dict:
    """Flatten a change_event JSONL record."""
    flat = rw.flatten_nested(raw)
    # Remap source_snapshot fields
    result = {}
    for k, v in flat.items():
        if k == "source_snapshot_agora_ref":
            result["source_agora_ref"] = v
        elif k == "source_snapshot_captured_at":
            result["source_captured_at"] = v
        else:
            result[k] = v
    return result


def remap_peer_feedback(raw: dict) -> dict:
    """Flatten a peer_feedback JSONL record."""
    return rw.flatten_nested(raw)


def remap_improvement_decision(raw: dict) -> dict:
    """Flatten an improvement_decision JSONL record."""
    return rw.flatten_nested(raw)


REMAP_FN = {
    "behavior_event": remap_behavior_event,
    "change_event": remap_change_event,
    "peer_feedback": remap_peer_feedback,
    "improvement_decision": remap_improvement_decision,
}


# ---------------------------------------------------------------------------
# Main migration
# ---------------------------------------------------------------------------


def migrate(dry_run: bool = False) -> int:
    total = 0
    errors = 0

    for source in SOURCES:
        jsonl_path = source["jsonl"]
        record_type = source["record_type"]
        swarm_id = source["swarm_id"]
        records_root = source["records_root"]

        if not jsonl_path.exists():
            print(f"SKIP (not found): {jsonl_path}")
            continue

        rows = rw.load_jsonl(jsonl_path)
        if not rows:
            print(f"SKIP (empty): {jsonl_path}")
            continue

        print(f"\n--- {jsonl_path.name} ({len(rows)} records) ---")

        remap_fn = REMAP_FN[record_type]

        for i, raw in enumerate(rows):
            try:
                record = remap_fn(raw)
                path = rw.write_record(
                    records_root=records_root,
                    record_type=record_type,
                    record=record,
                    swarm_id=swarm_id,
                    dry_run=dry_run,
                )
                total += 1
                if not dry_run:
                    print(f"  [{i+1}/{len(rows)}] {path.name}")
                else:
                    print(f"  [{i+1}/{len(rows)}] [DRY-RUN] {path.name}")
            except Exception as exc:
                errors += 1
                print(f"  [{i+1}/{len(rows)}] ERROR: {exc}", file=sys.stderr)

    print(f"\n=== Migration complete: {total} records, {errors} errors ===")
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migrate JSONL records to Obsidian Bases .md files"
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be written without writing")
    args = parser.parse_args()
    return migrate(dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
