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
from pathlib import Path

def sanitize_filename(name: str) -> str:
    name = name.replace(" ", "-")
    name = re.sub(r"[^a-zA-Z0-9\-_가-힣]", "", name)
    return name

def normalize_dependency(dep: str) -> str:
    dep = dep.strip()
    if dep.lower().endswith(".md"):
        dep = dep[:-3]
    return sanitize_filename(dep)

def get_dependencies(content: str) -> list[str]:
    """Extract dependencies from frontmatter."""
    match = re.search(r"^dependencies:\s*\[(.*?)\]", content, re.MULTILINE)
    if match:
        deps_str = match.group(1)
        # Parse "Dep-1", "Dep-2"
        return [d.strip().strip('"\'') for d in deps_str.split(",") if d.strip()]
    return []

def validate_node(node_path: str) -> bool:
    path = Path(node_path).resolve()
    print(f"Validating node: {path}")
    
    issues = []

    # 1. Essential Files
    if not (path / "RULE.md").exists():
        issues.append("[CRITICAL] Missing RULE.md")
    
    # 2. Tickets & Dependencies
    tickets_dir = path / "tickets"
    if tickets_dir.exists():
        ticket_files = {f.stem: f for f in tickets_dir.glob("*.md")}
        
        for name, file_path in ticket_files.items():
            content = file_path.read_text(encoding="utf-8")
            deps = [normalize_dependency(d) for d in get_dependencies(content)]
            
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
    parser.add_argument("path", help="Path to task-manager node")
    args = parser.parse_args()
    
    success = validate_node(args.path)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
