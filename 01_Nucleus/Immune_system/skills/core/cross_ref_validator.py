#!/usr/bin/env python3
"""
Cross-reference validator for AAOS doctrine/docs.

Checks:
- markdown links whose target paths should exist
- inline code paths that look like AAOS paths
- minimal doctrine file presence
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


@dataclass
class BrokenRef:
    file: str
    line: int
    ref: str
    reason: str


_MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
_AAOS_PATH_RE = re.compile(r"`(0[0-3]_[A-Za-z0-9._\-/]+)`")


def _iter_md_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*.md"):
        if any(part.startswith(".") for part in p.parts):
            continue
        if "_archive" in p.parts:
            continue
        if "00_METADoctrine" in p.parts:
            continue
        if p.name in {"AUDIT_LOG.md", "META_AUDIT_LOG.md"}:
            continue
        yield p


def _resolve_ref(current_file: Path, raw_ref: str, root: Path) -> Path | None:
    ref = raw_ref.strip()
    if not ref or ref.startswith("http://") or ref.startswith("https://") or ref.startswith("mailto:") or ref.startswith("file://"):
        return None
    if any(tok in ref for tok in ("...", "*", "path/to/")):
        return None
    ref = ref.split("#", 1)[0]
    if not ref:
        return None

    # Absolute path in repo-style
    if ref.startswith("04_Agentic_AI_OS/"):
        candidate = root / ref.removeprefix("04_Agentic_AI_OS/")
        return candidate

    # Relative markdown path
    return (current_file.parent / ref).resolve()


def validate(root: Path, *, check_inline_paths: bool = False) -> dict:
    broken: list[BrokenRef] = []

    for md in _iter_md_files(root):
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            broken.append(BrokenRef(str(md), 1, "", f"failed to read file: {e}"))
            continue

        lines = text.splitlines()
        for i, line in enumerate(lines, start=1):
            # Markdown links
            for m in _MD_LINK_RE.finditer(line):
                raw = m.group(1)
                target = _resolve_ref(md, raw, root)
                if target is not None and not target.exists():
                    broken.append(BrokenRef(str(md), i, raw, "markdown link target missing"))

            if check_inline_paths:
                # Inline AAOS-style path mentions in code ticks only
                for m in _AAOS_PATH_RE.finditer(line):
                    raw = m.group(1)
                    if any(tok in raw for tok in ("...", "*", "path/to/")):
                        continue
                    candidate = root / raw
                    if not candidate.exists():
                        if "/" in raw and raw.count("/") >= 1:
                            broken.append(BrokenRef(str(md), i, raw, "inline path target missing"))

    meta_doctrine_path = root / "00_METADoctrine" / "DNA.md"
    required_meta_doctrine = meta_doctrine_path

    required = [
        root / "README.md",
        required_meta_doctrine,
        root / "01_Nucleus" / "immune_system" / "rules" / "README.md",
    ]
    missing_required = [str(p) for p in required if not p.exists()]

    return {
        "root": str(root),
        "ok": len(broken) == 0 and len(missing_required) == 0,
        "broken_links": [asdict(x) for x in broken],
        "missing_required": missing_required,
        "summary": {
            "broken_links": len(broken),
            "missing_required": len(missing_required),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate cross references in AAOS docs")
    parser.add_argument("--root", required=True, help="Path to 04_Agentic_AI_OS")
    parser.add_argument("--format", choices=["json", "text"], default="json")
    parser.add_argument(
        "--check-inline-paths",
        action="store_true",
        help="Also validate inline AAOS paths wrapped in backticks",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    report = validate(root, check_inline_paths=args.check_inline_paths)

    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"root: {report['root']}")
        print(f"ok: {report['ok']}")
        print(f"broken_links: {report['summary']['broken_links']}")
        print(f"missing_required: {report['summary']['missing_required']}")
        for row in report["broken_links"][:50]:
            print(f"- {row['file']}:{row['line']} -> {row['ref']} ({row['reason']})")
        if len(report["broken_links"]) > 50:
            print(f"... {len(report['broken_links']) - 50} more")

    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
