#!/usr/bin/env python3
"""
Verify a SKILL folder meets minimal AAOS requirements.

Usage:
  python3 verify_skill.py <skill_dir>
"""

from __future__ import annotations

import argparse
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from core.yaml_validator import YAMLValidator


def verify_skill_dir(skill_dir: Path) -> tuple[bool, list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not skill_dir.exists():
        return False, [f"Missing directory: {skill_dir}"], []
    if not skill_dir.is_dir():
        return False, [f"Not a directory: {skill_dir}"], []

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return False, ["Missing required file: SKILL.md"], []

    text = skill_md.read_text(encoding="utf-8")
    validator = YAMLValidator(text)
    if not validator.is_valid():
        return False, [validator.parse_error or "Invalid YAML frontmatter"], []

    required = ["name", "description"]
    for k in required:
        if not validator.has_non_empty(k):
            errors.append(f"Missing or empty `{k}` in SKILL.md frontmatter")

    trigger = validator.get("trigger")
    if trigger is None:
        warnings.append("Missing `trigger` in SKILL.md frontmatter (recommended)")
    elif trigger not in ["on_request", "always_on"]:
        warnings.append(f"Unexpected trigger value: {trigger} (expected: on_request|always_on)")

    name = validator.get("name")
    if isinstance(name, str) and " " in name.strip():
        warnings.append("`name` should be kebab-case (no spaces)")

    return len(errors) == 0, errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify AAOS SKILL folder")
    parser.add_argument("skill_dir", help="Path to skill folder containing SKILL.md")
    args = parser.parse_args()

    ok, errors, warnings = verify_skill_dir(Path(args.skill_dir).expanduser().resolve())

    if ok:
        print("OK: SKILL folder is valid")
    else:
        print("INVALID: SKILL folder failed checks")

    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  - {e}")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  - {w}")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

