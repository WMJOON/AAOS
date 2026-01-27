#!/usr/bin/env python3
"""
task-manager/ 노드 생성 스크립트

Usage:
    python create_node.py <target_path>
    python create_node.py <target_path> --all
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime


def create_rule_md(node_path: Path) -> None:
    """RULE.md 생성"""
    content = """# task-manager/ Node Rule

## Object
에이전트가 sibling 및 descendants 노드의 맥락을 참조하며 작업을 이어갈 수 있도록 지원.

## Context Scope
1. sibling 및 descendants 노드 맥락 저장
2. repository/ 참조 시 children 범위까지만 저장
3. 모든 기록은 명시적이고 구조화된 서술 유지

## Troubleshooting Rule
반복 발생 문제는 troubleshooting.md에 누적 기록.

## tickets/ Rule
- 동시 활성 티켓: 최대 3개
- 각 티켓: 단일 명확한 목표
- 완료 시: 즉시 종료 처리, 결과 상위 맥락 반영
"""
    (node_path / "RULE.md").write_text(content, encoding="utf-8")


def create_troubleshooting_md(node_path: Path) -> None:
    """troubleshooting.md 생성"""
    content = """# Troubleshooting

반복 발생 문제와 해결 방안 누적 기록.

## Format

### [문제 제목]
- **발생 상황**:
- **원인**:
- **해결 방법**:
- **재발 방지**:

---

<!-- 아래에 항목 추가 -->
"""
    (node_path / "troubleshooting.md").write_text(content, encoding="utf-8")


def create_issue_notes(node_path: Path) -> None:
    """issue_notes/ 디렉토리 및 RULE.md 생성"""
    issue_path = node_path / "issue_notes"
    issue_path.mkdir(exist_ok=True)

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


def create_release_notes(node_path: Path) -> None:
    """release_notes/ 디렉토리 및 RULE.md 생성"""
    release_path = node_path / "release_notes"
    release_path.mkdir(exist_ok=True)

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


def create_task_manager_node(
    target_path: str,
    with_issue_notes: bool = False,
    with_release_notes: bool = False
) -> dict:
    """
    task-manager/ 노드 생성

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

    node_path = target / "task-manager"
    result["path"] = str(node_path)

    # 이미 존재하는지 확인
    if node_path.exists():
        result["errors"].append(f"task-manager/ already exists at: {node_path}")
        return result

    try:
        # 기본 구조 생성
        node_path.mkdir()
        result["created"].append("task-manager/")

        (node_path / "tickets").mkdir()
        result["created"].append("task-manager/tickets/")

        create_rule_md(node_path)
        result["created"].append("task-manager/RULE.md")

        create_troubleshooting_md(node_path)
        result["created"].append("task-manager/troubleshooting.md")

        # 선택적 하위 노드
        if with_issue_notes:
            create_issue_notes(node_path)
            result["created"].append("task-manager/issue_notes/")
            result["created"].append("task-manager/issue_notes/RULE.md")

        if with_release_notes:
            create_release_notes(node_path)
            result["created"].append("task-manager/release_notes/")
            result["created"].append("task-manager/release_notes/RULE.md")

        result["success"] = True

    except PermissionError as e:
        result["errors"].append(f"Permission denied: {e}")
    except OSError as e:
        result["errors"].append(f"OS error: {e}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Create task-manager/ node structure"
    )
    parser.add_argument(
        "target_path",
        help="Path where task-manager/ will be created"
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

    result = create_task_manager_node(
        args.target_path,
        with_issue_notes=with_issue,
        with_release_notes=with_release
    )

    if result["success"]:
        print(f"OK: Created task-manager/ at {result['path']}")
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
