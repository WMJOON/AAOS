#!/usr/bin/env python3
"""
Validate SKILL.md frontmatter contract and SKILL.meta.yaml sidecar contract.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict, List, Tuple
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
SHARED_DIR = SCRIPT_DIR.parent.parent / "_shared"
if str(SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_DIR))

from frontmatter import FrontmatterParseError, split_frontmatter_and_body


ALLOWED_SKILL_MD_KEYS = {"name", "description", "allowed-tools"}
FORBIDDEN_SKILL_MD_KEYS = {
    "context_id",
    "role",
    "state",
    "scope",
    "lifetime",
    "trigger",
    "created",
}
REQUIRED_META_KEYS = {"context_id", "role", "state", "scope", "lifetime", "created"}


def read_frontmatter(md_path: Path) -> Tuple[Dict[str, Any], List[str]]:
    try:
        text = md_path.read_text(encoding="utf-8")
    except OSError as exc:
        return {}, [f"{md_path}: cannot read - {exc}"]

    try:
        fm, _ = split_frontmatter_and_body(text)
    except FrontmatterParseError as exc:
        return {}, [f"{md_path}: frontmatter parse error - {exc}"]

    if not fm:
        return {}, [f"{md_path}: missing/invalid frontmatter"]
    return fm, []


def read_sidecar_yaml(meta_path: Path) -> Tuple[Dict[str, Any], List[str]]:
    try:
        raw = meta_path.read_text(encoding="utf-8")
    except OSError as exc:
        return {}, [f"{meta_path}: cannot read - {exc}"]

    wrapped = f"---\n{raw.strip()}\n---\n"
    try:
        fm, _ = split_frontmatter_and_body(wrapped)
    except FrontmatterParseError as exc:
        return {}, [f"{meta_path}: parse error - {exc}"]
    if not fm:
        return {}, [f"{meta_path}: empty or invalid yaml"]
    return fm, []


def iter_skill_docs(swarm_root: Path) -> List[Path]:
    docs: List[Path] = []
    for path in sorted(swarm_root.rglob("SKILL.md")):
        if "skills" in path.parts:
            docs.append(path)
    return docs


def validate_skill_contracts(
    swarm_root: Path,
    *,
    strict: bool = True,
    allow_legacy_frontmatter: bool = False,
) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    for skill_md in iter_skill_docs(swarm_root):
        skill_dir = skill_md.parent
        meta_path = skill_dir / "SKILL.meta.yaml"

        fm, fm_errors = read_frontmatter(skill_md)
        if fm_errors:
            errors.extend(fm_errors)
            continue

        keys = set(fm.keys())
        forbidden = sorted(keys.intersection(FORBIDDEN_SKILL_MD_KEYS))
        unknown = sorted(keys.difference(ALLOWED_SKILL_MD_KEYS).difference(FORBIDDEN_SKILL_MD_KEYS))

        if forbidden:
            msg = f"{skill_md}: forbidden keys in SKILL.md -> {', '.join(forbidden)}"
            if strict and not allow_legacy_frontmatter:
                errors.append(msg)
            else:
                warnings.append(f"WARN(legacy_frontmatter): {msg}")

        if unknown and strict:
            errors.append(f"{skill_md}: unknown keys in SKILL.md -> {', '.join(unknown)}")

        if meta_path.exists():
            meta_fm, meta_errors = read_sidecar_yaml(meta_path)
            if meta_errors:
                errors.extend(meta_errors)
                continue
            missing_required = sorted(REQUIRED_META_KEYS.difference(set(meta_fm.keys())))
            if missing_required:
                errors.append(f"{meta_path}: missing required keys -> {', '.join(missing_required)}")
        else:
            if forbidden:
                warnings.append(f"WARN(legacy_frontmatter): {skill_md} uses inline legacy metadata")
            else:
                warnings.append(f"WARN(missing_skill_meta): {meta_path} not found")

    return errors, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate SKILL frontmatter and SKILL.meta sidecars.")
    parser.add_argument("--swarm-root", required=True)
    parser.add_argument("--allow-legacy-frontmatter", action="store_true")
    parser.add_argument("--strict", action="store_true", default=False)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    swarm_root = Path(args.swarm_root).expanduser().resolve()
    strict = bool(args.strict)
    errors, warnings = validate_skill_contracts(
        swarm_root,
        strict=strict,
        allow_legacy_frontmatter=args.allow_legacy_frontmatter,
    )

    if warnings:
        print("WARNINGS:")
        for item in warnings:
            print(f"- {item}")
    if errors:
        print("ERRORS:")
        for item in errors:
            print(f"- {item}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
