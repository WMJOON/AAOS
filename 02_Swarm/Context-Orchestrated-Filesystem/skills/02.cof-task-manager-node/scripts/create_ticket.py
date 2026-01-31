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

def create_ticket(
    target_dir: str,
    title: str,
    dependencies: list = None,
    priority: str = "P2"
) -> bool:
    target_path = Path(target_dir).resolve()

    # tickets/ 디렉토리 해석:
    # - <...>/01.agents-task-context/tickets (or legacy: task-manager/tickets)
    # - <...>/01.agents-task-context (or legacy: task-manager)
    # - <...>/tickets
    # - <...>/ (상위에서 <node>/tickets 탐색)
    if target_path.name == "tickets":
        tickets_dir = target_path
    elif target_path.name in NODE_DIRNAMES:
        tickets_dir = target_path / "tickets"
    else:
        candidates = [target_path / "tickets"]
        candidates.extend([target_path / d / "tickets" for d in NODE_DIRNAMES])
        tickets_dir = next((p for p in candidates if p.exists()), candidates[0])

    if not tickets_dir.exists():
        print(
            f"Error: 'tickets/' directory not found in {target_dir}. "
            "Expected '01.agents-task-context/tickets/', 'task-manager/tickets/', or 'tickets/'.",
            file=sys.stderr
        )
        return False

    if not tickets_dir.exists():
        print(f"Error: Tickets directory not found at {tickets_dir}", file=sys.stderr)
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

    filename = sanitize_filename(title) + ".md"
    file_path = tickets_dir / filename
    
    if file_path.exists():
        print(f"Error: Ticket file already exists: {file_path}", file=sys.stderr)
        return False

    # YAML list format string (dependencies = ticket stems)
    deps_str = "[" + ", ".join([f'"{d}"' for d in normalized_dependencies]) + "]"
    
    content = TEMPLATE.format(
        title=title,
        priority=priority,
        dependencies=deps_str,
        created=datetime.now().strftime("%Y-%m-%d")
    )

    try:
        file_path.write_text(content, encoding="utf-8")
        print(f"Created ticket: {file_path}")
        return True
    except Exception as e:
        print(f"Error creating ticket: {e}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Create a new task ticket based on COF standard.")
    parser.add_argument("name", help="Ticket title/name")
    parser.add_argument("--dir", default=".", help="Target directory (task-manager root or tickets/ dir)")
    parser.add_argument("--deps", nargs="*", help="List of dependent ticket names")
    parser.add_argument("--priority", default="P2", choices=["P0", "P1", "P2", "P3"], help="Priority level")

    args = parser.parse_args()

    success = create_ticket(
        args.dir,
        args.name,
        dependencies=args.deps,
        priority=args.priority
    )

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
