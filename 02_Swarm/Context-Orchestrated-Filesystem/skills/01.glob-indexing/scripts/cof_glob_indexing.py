#!/usr/bin/env python3
import argparse
import errno
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Tuple


STANDARD_ROLE_TOKENS: Set[str] = {
    "index",
    "reference",
    "working",
    "ticket",
    "runtime",
    "history",
}

INDEX_DIR_RE = re.compile(r"^(?P<n>\d+)\.index$")
ROLE_DIR_RE = re.compile(r"^(?P<n>\d+)\.(?P<token>[a-z0-9_-]+)$")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _parse_index_dirname(name: str) -> Optional[Tuple[int, str]]:
    m = INDEX_DIR_RE.match(name)
    if not m:
        return None
    return int(m.group("n")), name


def _parse_role_dirname(name: str) -> Optional[Tuple[int, str, str]]:
    m = ROLE_DIR_RE.match(name)
    if not m:
        return None
    return int(m.group("n")), m.group("token"), name


def _should_skip_dir(name: str, include_hidden: bool) -> bool:
    return (not include_hidden) and name.startswith(".")


def _resolve_nearest_index(target_dir: str) -> Tuple[Optional[str], List[Dict[str, str]]]:
    warnings: List[Dict[str, str]] = []
    current = os.path.abspath(target_dir)

    while True:
        index_candidates: List[Tuple[int, str]] = []
        try:
            with os.scandir(current) as it:
                for entry in it:
                    if not entry.is_dir(follow_symlinks=False):
                        continue
                    parsed = _parse_index_dirname(entry.name)
                    if parsed:
                        n, name = parsed
                        index_candidates.append((n, entry.path))
        except PermissionError:
            warnings.append({"path": current, "reason": "permission_denied"})
        except OSError:
            warnings.append({"path": current, "reason": "read_error"})

        if index_candidates:
            index_candidates.sort(key=lambda x: (x[0], os.path.basename(x[1])))
            return index_candidates[0][1], warnings

        parent = os.path.dirname(current)
        if parent == current:
            return None, warnings
        current = parent


@dataclass(frozen=True)
class RoleDir:
    role: str
    rel_path: str
    abs_path: str
    confidence: str
    evidence: str


def _collect_role_dirs(
    node_root: str, primary_index_abs: str, include_hidden: bool
) -> Tuple[List[RoleDir], List[Dict[str, str]], List[Dict[str, str]]]:
    roles: List[RoleDir] = []
    unknown: List[Dict[str, str]] = []
    warnings: List[Dict[str, str]] = []

    try:
        with os.scandir(node_root) as it:
            for entry in it:
                if not entry.is_dir(follow_symlinks=False):
                    continue
                if _should_skip_dir(entry.name, include_hidden):
                    continue

                # index directory counts as role=index
                parsed_index = _parse_index_dirname(entry.name)
                if parsed_index:
                    rel = os.path.relpath(entry.path, node_root) + os.sep
                    roles.append(
                        RoleDir(
                            role="index",
                            rel_path=rel,
                            abs_path=entry.path,
                            confidence="certain",
                            evidence="matches /[n].index/ pattern (standard role token)",
                        )
                    )
                    continue

                parsed_role = _parse_role_dirname(entry.name)
                if not parsed_role:
                    continue

                _, token, _ = parsed_role
                rel = os.path.relpath(entry.path, node_root) + os.sep
                if token in STANDARD_ROLE_TOKENS:
                    roles.append(
                        RoleDir(
                            role=token,
                            rel_path=rel,
                            abs_path=entry.path,
                            confidence="certain",
                            evidence="matches /[n].[role]/ pattern (standard role token)",
                        )
                    )
                else:
                    unknown.append(
                        {
                            "token": token,
                            "path": rel,
                            "note": "non-standard token; consider renaming to a standard role token",
                        }
                    )
    except PermissionError:
        warnings.append({"path": node_root, "reason": "permission_denied"})
    except OSError:
        warnings.append({"path": node_root, "reason": "read_error"})

    # Keep stable ordering: index first (primary first), then token, then path
    roles.sort(
        key=lambda r: (
            0 if r.role == "index" and os.path.abspath(r.abs_path) == os.path.abspath(primary_index_abs) else 1,
            0 if r.role == "index" else 1,
            r.role,
            r.rel_path,
        )
    )
    unknown.sort(key=lambda x: (x.get("token", ""), x.get("path", "")))
    return roles, unknown, warnings


def _discover_index_anchors(
    node_root: str,
    include_hidden: bool,
    follow_symlinks: bool,
    max_depth: int,
) -> Tuple[List[str], List[Dict[str, str]]]:
    warnings: List[Dict[str, str]] = []
    anchors: List[str] = []

    visited_real: Set[str] = set()
    stack: List[Tuple[str, int]] = [(node_root, 0)]

    while stack:
        current, depth = stack.pop()
        try:
            with os.scandir(current) as it:
                for entry in it:
                    if not entry.is_dir(follow_symlinks=follow_symlinks):
                        continue
                    if _should_skip_dir(entry.name, include_hidden):
                        continue

                    if follow_symlinks and entry.is_symlink():
                        real = os.path.realpath(entry.path)
                        if real in visited_real:
                            warnings.append({"path": entry.path, "reason": "symlink_cycle"})
                            continue
                        visited_real.add(real)

                    if _parse_index_dirname(entry.name):
                        anchors.append(os.path.relpath(entry.path, node_root) + os.sep)

                    if depth < max_depth:
                        stack.append((entry.path, depth + 1))
        except PermissionError:
            warnings.append({"path": current, "reason": "permission_denied"})
        except OSError:
            warnings.append({"path": current, "reason": "read_error"})

    anchors = sorted(set(anchors))
    return anchors, warnings


def _write_text(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _render_node_index_md(
    *,
    target_dir_abs: str,
    node_root_abs: str,
    primary_index_abs: str,
    max_depth: int,
    include_hidden: bool,
    follow_symlinks: bool,
    role_dirs: List[RoleDir],
    anchor_paths_rel: List[str],
    warnings: List[Dict[str, str]],
) -> str:
    scanned_at = _utc_now_iso()
    primary_rel = os.path.relpath(primary_index_abs, node_root_abs) + os.sep
    secondary = [p for p in anchor_paths_rel if os.path.normpath(p) != os.path.normpath(primary_rel)]

    lines: List[str] = []
    lines.append("# Node Index")
    lines.append("> Auto-generated by cof-glob-indexing")
    lines.append("")
    lines.append("## Meta")
    lines.append(f"- **Node Root (absolute)**: `{node_root_abs}{os.sep}`")
    lines.append(f"- **Target Dir (absolute)**: `{target_dir_abs}{os.sep}`")
    lines.append(
        f"- **Scanned At (UTC)**: {scanned_at}"
    )
    lines.append(
        f"- **Parameters**: max_depth={max_depth}, include_hidden={str(include_hidden).lower()}, follow_symlinks={str(follow_symlinks).lower()}"
    )
    lines.append("")
    lines.append("## Role Directories")
    lines.append("| Role | Path | Status |")
    lines.append("|------|------|--------|")
    for rd in role_dirs:
        status = "primary" if os.path.normpath(rd.rel_path) == os.path.normpath(primary_rel) else "✓"
        lines.append(f"| {rd.role} | `{rd.rel_path}` | {status} |")
    lines.append("")
    lines.append("## Anchors")
    lines.append(f"- **Primary**: `{primary_rel}`")
    lines.append("- **Secondary**:")
    if secondary:
        for p in secondary:
            lines.append(f"  - `{p}`")
    else:
        lines.append("  - (none)")

    if warnings:
        lines.append("")
        lines.append("## Warnings")
        for w in warnings:
            lines.append(f"- `{w.get('path','')}`: {w.get('reason','')}")

    lines.append("")
    return "\n".join(lines)


def _render_role_evidence_md(
    *,
    role_dirs: List[RoleDir],
    primary_index_abs: str,
    node_root_abs: str,
    anchor_paths_rel: List[str],
    unknown_dirs: List[Dict[str, str]],
    warnings: List[Dict[str, str]],
) -> str:
    primary_rel = os.path.relpath(primary_index_abs, node_root_abs) + os.sep
    anchors: List[Dict[str, str]] = []
    for p in anchor_paths_rel:
        anchors.append(
            {
                "kind": "primary" if os.path.normpath(p) == os.path.normpath(primary_rel) else "secondary",
                "path": p,
                "confidence": "certain",
                "evidence": "matches /[n].index/ pattern within node boundary",
            }
        )

    roles_json = [
        {
            "role": rd.role,
            "path": rd.rel_path,
            "confidence": rd.confidence,
            "evidence": rd.evidence,
        }
        for rd in role_dirs
    ]

    lines: List[str] = []
    lines.append("# Role Evidence")
    lines.append("> Auto-generated by cof-glob-indexing")
    lines.append("")
    lines.append("## Detected Roles")
    lines.append("```json")
    lines.append(json.dumps(roles_json, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    lines.append("## Anchors")
    lines.append("```json")
    lines.append(json.dumps(anchors, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    lines.append("## Unknown Directories")
    lines.append("> `/[n].[token]/` 패턴이지만 표준 role token set이 아닌 디렉토리")
    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(unknown_dirs, ensure_ascii=False, indent=2))
    lines.append("```")

    if warnings:
        lines.append("")
        lines.append("## Warnings")
        lines.append("```json")
        lines.append(json.dumps(warnings, ensure_ascii=False, indent=2))
        lines.append("```")

    lines.append("")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="COF nearest-index resolver and node index artifact generator.")
    parser.add_argument("--target-dir", required=True, help="Absolute path used as the resolution starting point.")
    parser.add_argument("--max-depth", type=int, default=10, help="Max subtree depth to scan from node root.")
    parser.add_argument("--include-hidden", action="store_true", help="Include dot-prefixed directories.")
    parser.add_argument("--follow-symlinks", action="store_true", help="Follow symlinks while scanning.")
    args = parser.parse_args(argv)

    target_dir_abs = os.path.abspath(args.target_dir)
    max_depth = max(0, int(args.max_depth))
    include_hidden = bool(args.include_hidden)
    follow_symlinks = bool(args.follow_symlinks)

    nearest_index_abs, resolve_warnings = _resolve_nearest_index(target_dir_abs)
    if not nearest_index_abs:
        result = {
            "status": "error",
            "error_code": "INDEX_NOT_FOUND",
            "warnings": resolve_warnings,
            "artifacts": {"node_index": None, "role_evidence": None},
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2

    node_root_abs = os.path.abspath(os.path.dirname(nearest_index_abs))

    role_dirs, unknown_dirs, role_warnings = _collect_role_dirs(
        node_root_abs, nearest_index_abs, include_hidden
    )
    anchor_paths_rel, anchor_warnings = _discover_index_anchors(
        node_root_abs, include_hidden, follow_symlinks, max_depth
    )

    all_warnings = resolve_warnings + role_warnings + anchor_warnings

    node_index_path = os.path.join(nearest_index_abs, "NODE_INDEX.md")
    role_evidence_path = os.path.join(nearest_index_abs, "ROLE_EVIDENCE.md")

    try:
        _write_text(
            node_index_path,
            _render_node_index_md(
                target_dir_abs=target_dir_abs,
                node_root_abs=node_root_abs,
                primary_index_abs=nearest_index_abs,
                max_depth=max_depth,
                include_hidden=include_hidden,
                follow_symlinks=follow_symlinks,
                role_dirs=role_dirs,
                anchor_paths_rel=anchor_paths_rel,
                warnings=all_warnings,
            ),
        )
        _write_text(
            role_evidence_path,
            _render_role_evidence_md(
                role_dirs=role_dirs,
                primary_index_abs=nearest_index_abs,
                node_root_abs=node_root_abs,
                anchor_paths_rel=anchor_paths_rel,
                unknown_dirs=unknown_dirs,
                warnings=all_warnings,
            ),
        )
    except PermissionError:
        result = {
            "status": "error",
            "error_code": "WRITE_PERMISSION_DENIED",
            "warnings": all_warnings,
            "artifacts": {"node_index": None, "role_evidence": None},
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 3
    except OSError as e:
        error_code = "DISK_FULL" if getattr(e, "errno", None) == errno.ENOSPC else "WRITE_PERMISSION_DENIED"
        result = {
            "status": "error",
            "error_code": error_code,
            "warnings": all_warnings,
            "artifacts": {"node_index": None, "role_evidence": None},
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 4

    result = {
        "status": "success" if not all_warnings else "partial",
        "error_code": None,
        "warnings": all_warnings,
        "artifacts": {"node_index": node_index_path, "role_evidence": role_evidence_path},
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
