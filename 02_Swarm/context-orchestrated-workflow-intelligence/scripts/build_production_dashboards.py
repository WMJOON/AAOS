#!/usr/bin/env python3
"""
Build portable production proposal dashboards (JSON/CSV) from proposal markdown files.

This script is intentionally Obsidian-independent so any markdown-capable workflow can consume it.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

DEFAULT_PROPOSAL_DIRS = [
    "02_Swarm/agentic-workflow-topology/proposals",
    "02_Swarm/context-orchestrated-filesystem/proposals",
    "02_Swarm/context-orchestrated-workflow-intelligence/proposals",
]


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value.startswith('"') and value.endswith('"') and len(value) >= 2:
        return value[1:-1]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        try:
            # parse as CSV tokens to preserve quoted commas
            row = next(csv.reader([inner], skipinitialspace=True))
            parsed = []
            for token in row:
                parsed.append(parse_scalar(token))
            return parsed
        except Exception:
            return [part.strip().strip('"') for part in inner.split(",") if part.strip()]
    return value


def parse_frontmatter(path: Path) -> dict[str, Any]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}

    data: dict[str, Any] = {}
    current_list_key: str | None = None

    for line in lines[1:]:
        stripped = line.rstrip()
        if stripped.strip() == "---":
            break

        list_match = re.match(r"^\s*-\s+(.*)$", stripped)
        if list_match and current_list_key:
            data.setdefault(current_list_key, [])
            data[current_list_key].append(parse_scalar(list_match.group(1)))
            continue

        key_match = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", stripped)
        if not key_match:
            current_list_key = None
            continue

        key = key_match.group(1)
        raw_val = key_match.group(2)
        if raw_val == "":
            data[key] = []
            current_list_key = key
        else:
            data[key] = parse_scalar(raw_val)
            current_list_key = None

    return data


def infer_owner_swarm(path: Path) -> str:
    p = str(path.as_posix())
    if "agentic-workflow-topology" in p:
        return "agentic-workflow-topology"
    if "context-orchestrated-filesystem" in p:
        return "context-orchestrated-filesystem"
    if "context-orchestrated-workflow-intelligence" in p:
        return "context-orchestrated-workflow-intelligence"
    return "unknown"


def to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() == "true"


def normalize_record(path: Path, record: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    out: dict[str, Any] = {}
    out["proposal_id"] = str(record.get("proposal_id") or path.stem)
    out["parent_proposal_id"] = str(record.get("parent_proposal_id") or "")
    out["proposal_title"] = str(record.get("proposal_title") or path.stem)
    out["owner_swarm"] = str(record.get("owner_swarm") or infer_owner_swarm(path))
    out["proposal_status"] = str(record.get("proposal_status") or "draft").strip().lower()
    out["hitl_required"] = to_bool(record.get("hitl_required"))
    out["hitl_stage"] = str(record.get("hitl_stage") or "not_required")
    out["checked"] = to_bool(record.get("checked"))
    out["user_action_required"] = to_bool(record.get("user_action_required"))
    out["visibility_tier"] = str(record.get("visibility_tier") or "internal")

    linked_reports = record.get("linked_reports")
    if not isinstance(linked_reports, list):
        linked_reports = []
    out["linked_reports"] = [str(x) for x in linked_reports]

    linked_artifacts = record.get("linked_artifacts")
    if not isinstance(linked_artifacts, list):
        linked_artifacts = []
    out["linked_artifacts"] = [str(x) for x in linked_artifacts]

    out["file_path"] = str(path.relative_to(repo_root).as_posix())
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    columns = [
        "proposal_id",
        "parent_proposal_id",
        "proposal_title",
        "owner_swarm",
        "proposal_status",
        "hitl_required",
        "hitl_stage",
        "checked",
        "user_action_required",
        "visibility_tier",
        "linked_reports",
        "linked_artifacts",
        "file_path",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            out["linked_reports"] = ";".join(out.get("linked_reports", []))
            out["linked_artifacts"] = ";".join(out.get("linked_artifacts", []))
            writer.writerow({k: out.get(k, "") for k in columns})


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_dashboards(repo_root: Path, dashboard_dir: Path, proposal_dirs: list[str]) -> int:
    proposals: list[dict[str, Any]] = []

    for raw_dir in proposal_dirs:
        pdir = (repo_root / raw_dir).resolve()
        if not pdir.exists():
            continue
        for md in sorted(pdir.glob("*.md")):
            if md.name.startswith("_"):
                continue
            parsed = parse_frontmatter(md)
            proposals.append(normalize_record(md, parsed, repo_root))

    proposals.sort(key=lambda x: (x["proposal_id"], x["file_path"]))

    production = [
        p for p in proposals
        if p["proposal_status"] != "closed" and p["visibility_tier"] == "must_show"
    ]
    approval_queue = [
        p for p in proposals
        if p["proposal_status"] != "closed"
        and p["hitl_stage"] == "approval_required"
        and p["checked"] is True
    ]
    user_inbox = [
        p for p in proposals
        if p["proposal_status"] != "closed"
        and p["visibility_tier"] == "must_show"
        and p["user_action_required"] is True
    ]
    archived = [p for p in proposals if p["proposal_status"] == "closed"]

    production_payload = {
        "generated_at": iso_now(),
        "source_proposal_dirs": proposal_dirs,
        "counts": {
            "all": len(proposals),
            "production": len(production),
            "approval_queue": len(approval_queue),
            "archived": len(archived),
        },
        "items": production,
        "approval_queue": approval_queue,
        "archived": archived,
    }

    inbox_payload = {
        "generated_at": iso_now(),
        "source_proposal_dirs": proposal_dirs,
        "count": len(user_inbox),
        "items": user_inbox,
    }

    archived_payload = {
        "generated_at": iso_now(),
        "source_proposal_dirs": proposal_dirs,
        "count": len(archived),
        "items": archived,
    }

    write_json(dashboard_dir / "production-proposals.json", production_payload)
    write_csv(dashboard_dir / "production-proposals.csv", production)
    write_json(dashboard_dir / "user-inbox.json", inbox_payload)
    write_csv(dashboard_dir / "user-inbox.csv", user_inbox)
    write_json(dashboard_dir / "archived-proposals.json", archived_payload)
    write_csv(dashboard_dir / "archived-proposals.csv", archived)

    print(
        "built dashboards: all={} production={} approval_queue={} user_inbox={} archived={}".format(
            len(proposals),
            len(production),
            len(approval_queue),
            len(user_inbox),
            len(archived),
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Build portable production proposal dashboards (JSON/CSV)")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--dashboard-dir",
        default="02_Swarm/context-orchestrated-workflow-intelligence/dashboard",
    )
    parser.add_argument(
        "--proposal-dir",
        action="append",
        default=[],
        help="Proposal directory (can be passed multiple times)",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).expanduser().resolve()
    dashboard_dir = (repo_root / args.dashboard_dir).resolve()
    proposal_dirs = args.proposal_dir if args.proposal_dir else DEFAULT_PROPOSAL_DIRS
    return build_dashboards(repo_root, dashboard_dir, proposal_dirs)


if __name__ == "__main__":
    raise SystemExit(main())
