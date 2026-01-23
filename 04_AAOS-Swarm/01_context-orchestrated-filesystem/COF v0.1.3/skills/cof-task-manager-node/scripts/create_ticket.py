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

TEMPLATE = """---
type: task-ticket
status: todo # todo, in-progress, done, blocked
priority: {priority} # P0 (Urgent), P1 (High), P2 (Normal), P3 (Low)
dependencies: {dependencies} # List of dependent ticket filenames
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

def create_ticket(
    target_dir: str,
    title: str,
    dependencies: list = None,
    priority: str = "P2"
) -> bool:
    target_path = Path(target_dir).resolve()
    
    # tickets/ 디렉토리 찾기
    tickets_dir = target_path / "tickets"
    if not tickets_dir.exists():
        # 혹시 현재 위치가 tickets/ 내부일 수도 있음
        if target_path.name == "tickets":
            tickets_dir = target_path
        elif target_path.name == "task-manager": # task-ticket -> task-manager
             tickets_dir = target_path / "tickets"
        else:
             # Try task-manager child
            tickets_dir = target_path / "task-manager" / "tickets"
            if not tickets_dir.exists():
                print(f"Error: 'tickets/' directory not found in {target_dir}. Expected 'task-manager/tickets/' or 'tickets/'", file=sys.stderr)
                return False

    if not tickets_dir.exists():
        print(f"Error: Tickets directory not found at {tickets_dir}", file=sys.stderr)
        return False
        
    # Validate dependencies
    if dependencies:
        missing_deps = []
        for dep in dependencies:
            # Check if dependency matches a filename in tickets_dir
            # We check partially because user might just type "Ticket Name" but file is "Ticket-Name.md"
            # For strictness, let's assume user provides exact or sanitized names, but we should help them.
            # Simple check: direct file existence or glob
            sanitized_dep = sanitize_filename(dep)
            possible_files = [
                tickets_dir / dep,
                tickets_dir / (dep + ".md"),
                tickets_dir / sanitized_dep,
                tickets_dir / (sanitized_dep + ".md")
            ]
            
            found = any(p.exists() for p in possible_files)
            if not found:
                 missing_deps.append(dep)
        
        if missing_deps:
            print(f"Warning: The following dependencies were not found as existing tickets: {missing_deps}", file=sys.stderr)
            print("Creating ticket anyway, but please verify dependencies.", file=sys.stderr)

    filename = sanitize_filename(title) + ".md"
    file_path = tickets_dir / filename
    
    if file_path.exists():
        print(f"Error: Ticket file already exists: {file_path}", file=sys.stderr)
        return False

    if dependencies is None:
        dependencies = []
    
    # YAML list format string
    deps_str = "[" + ", ".join([f'"{d}"' for d in dependencies]) + "]"
    
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
