#!/usr/bin/env python3
"""
Validate COF Task Manager Node Health.

Checks:
1. Existence of RULE.md
2. Broken dependencies in tickets
"""

import argparse
import sys
import re
from typing import Any, Dict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SHARED_DIR = SCRIPT_DIR.parent.parent / "_shared"
if str(SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_DIR))

from frontmatter import FrontmatterParseError, split_frontmatter_and_body

NODE_DIRNAMES = ("01.agents-task-context", "task-manager")


def sanitize_filename(name: str) -> str:
    name = name.replace(" ", "-")
    name = re.sub(r"[^a-zA-Z0-9\-_가-힣]", "", name)
    return name

def normalize_dependency(dep: str) -> str:
    dep = dep.strip()
    if dep.lower().endswith(".md"):
        dep = dep[:-3]
    return sanitize_filename(dep)

def sanitize_namespace_token(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-")

def parse_namespace_from_path(path: Path) -> tuple[str, str] | None:
    parts = path.parts
    for i, part in enumerate(parts):
        if part in NODE_DIRNAMES and i + 2 < len(parts):
            family = sanitize_namespace_token(parts[i + 1])
            version = sanitize_namespace_token(parts[i + 2])
            if family and version:
                return family, version
    return None

def resolve_node_root(path: Path) -> Path | None:
    cursor = path
    while True:
        if cursor.name in NODE_DIRNAMES:
            return cursor
        for dirname in NODE_DIRNAMES:
            candidate = cursor / dirname
            if candidate.exists():
                return candidate
        if cursor.parent == cursor:
            break
        cursor = cursor.parent
    return None

def resolve_namespace(path: Path, node_root: Path, agent_family: str, agent_version: str) -> tuple[str, str]:
    from_path = parse_namespace_from_path(path) or parse_namespace_from_path(node_root)
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
            "agent namespace mismatch between args and path "
            f"(args={from_args[0]}/{from_args[1]}, path={from_path[0]}/{from_path[1]})"
        )
    if from_args:
        return from_args
    if from_path:
        return from_path
    raise ValueError("cannot resolve agent namespace from path or args")

def get_dependencies(frontmatter: Dict[str, Any]) -> list[str]:
    """Extract dependencies from parsed frontmatter."""
    raw_deps = frontmatter.get("dependencies")
    if raw_deps is None:
        return []
    if isinstance(raw_deps, list):
        values = raw_deps
    else:
        values = [raw_deps]

    return [normalize_dependency(str(dep)) for dep in values if str(dep).strip()]

def validate_node(node_path: str, agent_family: str = "", agent_version: str = "") -> bool:
    path = Path(node_path).resolve()
    node_root = resolve_node_root(path)
    if node_root is None:
        print(f"[ERROR] Could not locate node root from: {path}")
        print(f"[AUDIT] namespace_policy_violation path={path}")
        return False
    try:
        family, version = resolve_namespace(path, node_root, agent_family, agent_version)
    except ValueError as exc:
        print(f"[ERROR] Namespace resolution failed: {exc}")
        print(f"[AUDIT] namespace_policy_violation path={path}")
        return False

    namespace_path = node_root / family / version
    print(f"Validating namespace node: {namespace_path} (namespace={family}/{version})")
    
    issues = []

    # 1. Essential Files
    if not namespace_path.exists():
        issues.append(f"[CRITICAL] Namespace path missing: {namespace_path}")
    if not (namespace_path / "RULE.md").exists():
        issues.append("[CRITICAL] Missing RULE.md")
    
    # 2. Tickets & Dependencies
    tickets_dir = namespace_path / "tickets"
    if tickets_dir.exists():
        ticket_files = {f.stem: f for f in tickets_dir.glob("*.md")}
        
        for name, file_path in ticket_files.items():
            content = file_path.read_text(encoding="utf-8")
            try:
                frontmatter, _ = split_frontmatter_and_body(content)
            except FrontmatterParseError as exc:
                issues.append(f"[ERROR] Ticket '{name}' has invalid frontmatter: {exc}")
                continue

            deps = get_dependencies(frontmatter)
            
            for dep in deps:
                if dep not in ticket_files:
                    issues.append(f"[ERROR] Ticket '{name}' has broken dependency: '{dep}' not found.")
    else:
        issues.append("[WARNING] 'tickets' directory missing.")

    # Report
    if issues:
        print("\nValidation failed with issues:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("\nNode is healthy.")
        return True

def main():
    parser = argparse.ArgumentParser(description="Validate COF node health.")
    parser.add_argument("path", help="Path to NN.agents-task-context node (or legacy: task-manager)")
    parser.add_argument("--agent-family", default="", help="Agent family namespace key")
    parser.add_argument("--agent-version", default="", help="Agent version namespace key")
    args = parser.parse_args()
    
    success = validate_node(args.path, agent_family=args.agent_family, agent_version=args.agent_version)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
