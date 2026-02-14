#!/usr/bin/env python3
"""
기존 agents-task-context 노드에 선택적 하위 노드 추가 (legacy: task-manager/)

Usage:
    python add_optional.py <node_path> --issue-notes
    python add_optional.py <node_path> --release-notes
    python add_optional.py <node_path> --all
"""

import argparse
import sys
from pathlib import Path

LEGACY_NODE_NAME = "task-manager"

def create_issue_notes(node_path: Path) -> list:
    """issue_notes/ 추가"""
    created = []
    issue_path = node_path / "issue_notes"

    if issue_path.exists():
        return ["issue_notes/ already exists (skipped)"]

    issue_path.mkdir()
    created.append("issue_notes/")

    content = """# issue_notes/ Rule

## Purpose
작업 수행 중 발생한 이슈·의사결정·논의 사항 기록.

## Rules
1. 발생 즉시 기록
2. 해결 시 방법 및 영향 범위 명시
3. 반복 이슈는 troubleshooting.md로 승격

## File Naming
{parentName}-issue_note-{YYYYMMDD-HHMM}.md
"""
    (issue_path / "RULE.md").write_text(content, encoding="utf-8")
    created.append("issue_notes/RULE.md")

    return created


def create_release_notes(node_path: Path) -> list:
    """release_notes/ 추가"""
    created = []
    release_path = node_path / "release_notes"

    if release_path.exists():
        return ["release_notes/ already exists (skipped)"]

    release_path.mkdir()
    created.append("release_notes/")

    content = """# release_notes/ Rule

## Purpose
작업 단위 완료 결과 요약 기록.

## Rules
1. 주요 변경 사항·산출물 간결히 정리
2. 후속 작업·의존 티켓 영향 사항 명시

## File Naming
{parentName}-release_note-{YYYYMMDD-HHMM}.md
"""
    (release_path / "RULE.md").write_text(content, encoding="utf-8")
    created.append("release_notes/RULE.md")

    return created


def main():
    parser = argparse.ArgumentParser(
        description="Add optional child nodes to NN.agents-task-context/ (or legacy: task-manager/)"
    )
    parser.add_argument(
        "node_path",
        help="Path to existing NN.agents-task-context/ (or legacy: task-manager/) directory"
    )
    parser.add_argument(
        "--issue-notes",
        action="store_true",
        help="Add issue_notes/ directory"
    )
    parser.add_argument(
        "--release-notes",
        action="store_true",
        help="Add release_notes/ directory"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Add all optional directories"
    )

    args = parser.parse_args()
    path = Path(args.node_path).resolve()

    # 검증
    if not path.exists():
        print(f"FAILED: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    if path.name == LEGACY_NODE_NAME:
        print(
            f"WARNING: Legacy node name detected: '{LEGACY_NODE_NAME}/' "
            "(recommended: 'NN.agents-task-context/')."
        )

    created = []

    if args.issue_notes or args.all:
        created.extend(create_issue_notes(path))

    if args.release_notes or args.all:
        created.extend(create_release_notes(path))

    if not (args.issue_notes or args.release_notes or args.all):
        print("No option specified. Use --issue-notes, --release-notes, or --all")
        sys.exit(1)

    print("OK: Optional nodes added")
    print("\nResult:")
    for item in created:
        print(f"  - {item}")


if __name__ == "__main__":
    main()
