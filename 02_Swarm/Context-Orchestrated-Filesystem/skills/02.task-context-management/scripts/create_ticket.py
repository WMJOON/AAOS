#!/usr/bin/env python3
"""
Ticket 생성 스크립트

Usage:
    python create_ticket.py <ticket_name>
    python create_ticket.py <ticket_name> --deps ticket-A ticket-B
    python create_ticket.py <ticket_name> --priority P1
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import re

NODE_DIRNAMES = ("01.agents-task-context", "task-manager")

TEMPLATE = """---
type: task-ticket
status: todo # todo, in-progress, done, blocked
priority: {priority} # P0 (Urgent), P1 (High), P2 (Normal), P3 (Low)
dependencies: {dependencies} # List of dependent ticket file stems (no .md)
proposal_id: "{proposal_id}"
user_action_required: {user_action_required}
visibility_tier: "{visibility_tier}"
owner_swarm: "context-orchestrated-filesystem"
created: "{created}"
tags: []
---

# {title}

## Description
<!-- 상세 작업 내용을 기술합니다. -->


## Action Items
<!-- 구체적인 실행 단계를 리스트업합니다. 순차적 의존성이 있다면 숫자로, 병렬 가능하면 불릿으로 작성합니다. -->
- [ ] 


## Definition of Done
<!-- 완료 조건을 명확히 정의합니다. -->
- [ ] 
"""

def sanitize_filename(name: str) -> str:
    """파일명으로 사용할 수 있도록 문자열 정제"""
    # 공백을 하이픈으로 변경
    name = name.replace(" ", "-")
    # 알파벳, 숫자, 하이픈, 언더스코어, 한글만 허용 (나머지 삭제)
    name = re.sub(r"[^a-zA-Z0-9\-_가-힣]", "", name)
    if not name:
        return ""
    # 연속 구분자 정리
    name = re.sub(r"[-_]{2,}", "-", name)
    # 양끝 구분자 정리
    name = name.strip("-_")
    return name

def normalize_dependency(dep: str) -> str:
    """
    dependencies에는 '파일 stem(확장자 .md 제외)'을 저장한다.
    사용자가 '.md'를 포함해 입력해도 일관되게 stem으로 정규화한다.
    """
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

def resolve_node_root(target_path: Path) -> Path | None:
    cursor = target_path
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

def resolve_namespace(target_path: Path, node_root: Path, agent_family: str, agent_version: str) -> tuple[str, str]:
    from_path = parse_namespace_from_path(target_path) or parse_namespace_from_path(node_root)
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
            "agent namespace mismatch between args and target path "
            f"(args={from_args[0]}/{from_args[1]}, path={from_path[0]}/{from_path[1]})"
        )
    if from_args:
        return from_args
    if from_path:
        return from_path
    raise ValueError("cannot resolve agent namespace from path or args")

def create_ticket(
    target_dir: str,
    title: str,
    dependencies: list = None,
    priority: str = "P2",
    agent_family: str = "",
    agent_version: str = "",
    proposal_id: str = "UNASSIGNED",
    user_action_required: bool = False,
    visibility_tier: str = "internal",
) -> bool:
    target_path = Path(target_dir).resolve()
    node_root = resolve_node_root(target_path)
    if node_root is None:
        print(
            f"Error: Could not locate '{NODE_DIRNAMES[0]}/' or '{NODE_DIRNAMES[1]}/' from {target_path}",
            file=sys.stderr
        )
        print(f"[AUDIT] namespace_policy_violation path={target_path}", file=sys.stderr)
        return False

    try:
        family, version = resolve_namespace(target_path, node_root, agent_family, agent_version)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        print(f"[AUDIT] namespace_policy_violation path={target_path}", file=sys.stderr)
        return False

    tickets_dir = node_root / family / version / "tickets"

    if not tickets_dir.exists():
        print(
            f"Error: Namespace ticket path not found: {tickets_dir}. "
            "Expected 'NN.agents-task-context/<agent-family>/<version>/tickets/'.",
            file=sys.stderr
        )
        print(f"[AUDIT] namespace_policy_violation path={tickets_dir}", file=sys.stderr)
        return False

    normalized_dependencies: list[str] = []
    if dependencies:
        normalized_dependencies = [normalize_dependency(d) for d in dependencies if d and d.strip()]

        existing = {p.stem for p in tickets_dir.glob("*.md")}
        missing = [d for d in normalized_dependencies if d not in existing]
        if missing:
            print(
                "Warning: The following dependencies were not found as existing ticket stems:",
                missing,
                file=sys.stderr
            )
            print("Creating ticket anyway; verify dependencies later.", file=sys.stderr)

    filename = sanitize_filename(title)
    if not filename:
        filename = "untitled-ticket"

    # 동일 이름이 이미 존재하면 자동으로 번호를 붙여 충돌 회피
    suffix = 0
    candidate = filename
    while True:
        file_path = tickets_dir / f"{candidate}.md"
        if not file_path.exists():
            break
        suffix += 1
        candidate = f"{filename}-{suffix}"
        if suffix > 1000:
            print("Error: Unable to allocate unique ticket filename (too many collisions).", file=sys.stderr)
            return False

    # YAML list format string (dependencies = ticket stems)
    deps_str = "[" + ", ".join([f'"{d}"' for d in normalized_dependencies]) + "]"
    
    content = TEMPLATE.format(
        title=title,
        priority=priority,
        dependencies=deps_str,
        proposal_id=proposal_id,
        user_action_required=str(user_action_required).lower(),
        visibility_tier=visibility_tier,
        created=datetime.now().strftime("%Y-%m-%d")
    )

    try:
        file_path.write_text(content, encoding="utf-8")
        print(f"Created ticket: {file_path} (namespace={family}/{version})")
        return True
    except Exception as e:
        print(f"Error creating ticket: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Create a new task ticket based on COF standard.")
    parser.add_argument("name", help="Ticket title/name")
    parser.add_argument("--dir", default=".", help="Target directory (must resolve to agent namespace)")
    parser.add_argument("--deps", nargs="*", help="List of dependent ticket names")
    parser.add_argument("--priority", default="P2", choices=["P0", "P1", "P2", "P3"], help="Priority level")
    parser.add_argument("--agent-family", default="", help="Agent family namespace key")
    parser.add_argument("--agent-version", default="", help="Agent version namespace key")
    parser.add_argument("--proposal-id", default="UNASSIGNED", help="proposal identifier for generated ticket")
    parser.add_argument(
        "--visibility-tier",
        default="internal",
        choices=["must_show", "optional", "internal"],
        help="visibility metadata for generated ticket",
    )
    parser.add_argument(
        "--user-action-required",
        action="store_true",
        help="mark ticket as requiring explicit user action",
    )

    args = parser.parse_args()

    success = create_ticket(
        args.dir,
        args.name,
        dependencies=args.deps,
        priority=args.priority,
        agent_family=args.agent_family,
        agent_version=args.agent_version,
        proposal_id=args.proposal_id,
        user_action_required=args.user_action_required,
        visibility_tier=args.visibility_tier,
    )

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
