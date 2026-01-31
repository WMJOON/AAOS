#!/usr/bin/env python3
"""
01.agents-task-context/ 노드 생성 스크립트 (legacy: task-manager/)

Usage:
    python create_node.py <target_path>
    python create_node.py <target_path> --all
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

NODE_DIRNAME = "01.agents-task-context"
LEGACY_NODE_DIRNAME = "task-manager"


def read_template(template_name: str) -> str:
    """Read template file from ../templates directory"""
    script_dir = Path(__file__).parent
    template_path = script_dir.parent / "templates" / template_name
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
        
    return template_path.read_text(encoding="utf-8")


def create_rule_md(node_path: Path) -> None:
    """RULE.md 생성"""
    content = read_template("NODE_RULE.md")
    (node_path / "RULE.md").write_text(content, encoding="utf-8")


def create_troubleshooting_md(node_path: Path) -> None:
    """troubleshooting.md 생성"""
    content = read_template("TROUBLESHOOTING-TEMPLATE.md")
    (node_path / "troubleshooting.md").write_text(content, encoding="utf-8")


def create_issue_notes(node_path: Path) -> None:
    """issue_notes/ 디렉토리 및 RULE.md 생성"""
    issue_path = node_path / "issue_notes"
    issue_path.mkdir(exist_ok=True)

    content = read_template("ISSUE_NOTE_RULE.md")
    (issue_path / "RULE.md").write_text(content, encoding="utf-8")


def create_release_notes(node_path: Path) -> None:
    """release_notes/ 디렉토리 및 RULE.md 생성"""
    release_path = node_path / "release_notes"
    release_path.mkdir(exist_ok=True)

    content = read_template("RELEASE_NOTE_RULE.md")
    (release_path / "RULE.md").write_text(content, encoding="utf-8")


def create_task_context_node(
    target_path: str,
    with_issue_notes: bool = False,
    with_release_notes: bool = False
) -> dict:
    """
    01.agents-task-context/ 노드 생성

    Returns:
        dict: 생성 결과 {"success": bool, "path": str, "created": list, "errors": list}
    """
    result = {
        "success": False,
        "path": "",
        "created": [],
        "errors": []
    }

    target = Path(target_path).resolve()

    # 대상 경로 검증
    if not target.exists():
        result["errors"].append(f"Target path does not exist: {target}")
        return result

    if not target.is_dir():
        result["errors"].append(f"Target path is not a directory: {target}")
        return result

    node_path = target / NODE_DIRNAME
    result["path"] = str(node_path)

    # 이미 존재하는지 확인
    legacy_path = target / LEGACY_NODE_DIRNAME
    if legacy_path.exists():
        result["errors"].append(
            f"Legacy '{LEGACY_NODE_DIRNAME}/' already exists at: {legacy_path} "
            f"(expected '{NODE_DIRNAME}/')."
        )
        return result

    if node_path.exists():
        result["errors"].append(f"{NODE_DIRNAME}/ already exists at: {node_path}")
        return result

    try:
        # 기본 구조 생성
        node_path.mkdir()
        result["created"].append(f"{NODE_DIRNAME}/")

        (node_path / "tickets").mkdir()
        result["created"].append(f"{NODE_DIRNAME}/tickets/")

        create_rule_md(node_path)
        result["created"].append(f"{NODE_DIRNAME}/RULE.md")

        create_troubleshooting_md(node_path)
        result["created"].append(f"{NODE_DIRNAME}/troubleshooting.md")

        # 선택적 하위 노드
        if with_issue_notes:
            create_issue_notes(node_path)
            result["created"].append(f"{NODE_DIRNAME}/issue_notes/")
            result["created"].append(f"{NODE_DIRNAME}/issue_notes/RULE.md")

        if with_release_notes:
            create_release_notes(node_path)
            result["created"].append(f"{NODE_DIRNAME}/release_notes/")
            result["created"].append(f"{NODE_DIRNAME}/release_notes/RULE.md")

        result["success"] = True

    except PermissionError as e:
        result["errors"].append(f"Permission denied: {e}")
    except OSError as e:
        result["errors"].append(f"OS error: {e}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description=f"Create {NODE_DIRNAME}/ node structure"
    )
    parser.add_argument(
        "target_path",
        help=f"Path where {NODE_DIRNAME}/ will be created"
    )
    parser.add_argument(
        "--with-issue-notes",
        action="store_true",
        help="Include issue_notes/ directory"
    )
    parser.add_argument(
        "--with-release-notes",
        action="store_true",
        help="Include release_notes/ directory"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Include all optional directories"
    )

    args = parser.parse_args()

    with_issue = args.with_issue_notes or args.all
    with_release = args.with_release_notes or args.all

    result = create_task_context_node(
        args.target_path,
        with_issue_notes=with_issue,
        with_release_notes=with_release
    )

    if result["success"]:
        print(f"OK: Created {NODE_DIRNAME}/ at {result['path']}")
        print("\nCreated:")
        for item in result["created"]:
            print(f"  - {item}")
    else:
        print("FAILED:", file=sys.stderr)
        for error in result["errors"]:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
