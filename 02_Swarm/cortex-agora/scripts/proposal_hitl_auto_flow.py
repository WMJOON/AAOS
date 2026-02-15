#!/usr/bin/env python3
"""
Auto-progress proposal HITL state when approval is confirmed.

Rule:
  hitl_stage == "approval_required"
  checked == true
  auto_flow_enabled == true
  proposal_status != "closed"
"""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_frontmatter(path: Path) -> tuple[list[str], int]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        raise ValueError(f"{path}: missing frontmatter")
    end = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end == -1:
        raise ValueError(f"{path}: unterminated frontmatter")
    return lines, end


def get_field(lines: list[str], end: int, key: str) -> str | None:
    prefix = f"{key}:"
    for i in range(1, end):
        raw = lines[i].strip()
        if raw.startswith(prefix):
            value = raw[len(prefix):].strip()
            return value.strip('"')
    return None


def upsert_field(lines: list[str], end: int, key: str, value: str) -> tuple[list[str], int]:
    prefix = f"{key}:"
    rendered = f'{key}: "{value}"'
    for i in range(1, end):
        if lines[i].strip().startswith(prefix):
            lines[i] = rendered
            return lines, end
    lines.insert(end, rendered)
    return lines, end + 1


def as_bool(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"true", '"true"'}


def should_progress(lines: list[str], end: int) -> bool:
    stage = get_field(lines, end, "hitl_stage")
    checked = as_bool(get_field(lines, end, "checked"))
    enabled = as_bool(get_field(lines, end, "auto_flow_enabled"))
    proposal_status = (get_field(lines, end, "proposal_status") or "").strip().lower()
    return stage == "approval_required" and checked and enabled and proposal_status != "closed"


def process_file(path: Path, dry_run: bool) -> bool:
    lines, end = parse_frontmatter(path)
    if not should_progress(lines, end):
        return False

    now = iso_now()
    updates = [
        ("hitl_stage", "completed"),
        ("hitl_review_status", "reviewed"),
        ("hitl_approval_status", "approved"),
        ("auto_flow_status", "done"),
        ("hitl_last_action_at", now),
    ]

    checked_at = get_field(lines, end, "checked_at")
    if not checked_at:
        updates.append(("checked_at", now))

    for key, value in updates:
        lines, end = upsert_field(lines, end, key, value)

    if dry_run:
        print(f"[DRY-RUN] would auto-progress: {path}")
        return True

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"auto-progressed: {path}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Auto-progress proposal HITL states")
    parser.add_argument(
        "--proposals-dir",
        default="02_Swarm/cortex-agora/proposals",
        help="Directory containing proposal markdown files",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    proposals_dir = Path(args.proposals_dir).expanduser().resolve()
    if not proposals_dir.exists():
        raise SystemExit(f"proposals dir not found: {proposals_dir}")

    changed = 0
    checked = 0
    for md in sorted(proposals_dir.glob("*.md")):
        checked += 1
        try:
            if process_file(md, args.dry_run):
                changed += 1
        except ValueError as exc:
            print(f"skip: {exc}")

    print(f"checked={checked} changed={changed} dry_run={args.dry_run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
