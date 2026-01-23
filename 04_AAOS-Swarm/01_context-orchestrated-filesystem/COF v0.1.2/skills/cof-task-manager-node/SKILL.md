---
name: managing-task-contexts
description: Creates and manages task-manager/ node structures for persistent agent context tracking. Use when initializing project workspaces, creating task tickets, or when the user mentions "task management", "context node", "COF", or needs sequential ticket dependency management.
---

# Task-Manager Node

task-manager/ 노드는 에이전트 작업 맥락을 저장하고 개별 작업 티켓을 관리하는 COF 노드이다.

## Node Creation Workflow

Copy this checklist and track your progress:

```
Task Progress:
- [ ] Step 1: Confirm target path with user
- [ ] Step 2: Run create_node.py
- [ ] Step 3: Run verify_node.py
- [ ] Step 4: Report result to user
```

**Step 1: Confirm target path**

사용자에게 생성 위치 확인. 선택적 노드(issue_notes, release_notes) 필요 여부 질문.

**Step 2: Run create_node.py**

```bash
python3 scripts/create_node.py <target_path> [--all]
```

Output:
```
{targetPath}/
└── task-manager/
    ├── RULE.md
    ├── troubleshooting.md
    └── tickets/
```

**Step 3: Run verify_node.py**

```bash
python3 scripts/verify_node.py <target_path>/task-manager
```

검증 실패 시 에러 메시지 확인 후 수정.

**Step 4: Report result**

생성된 구조와 각 파일의 용도를 사용자에게 안내.

## Ticket Creation

```bash
python3 scripts/create_ticket.py "Ticket Name" --priority P1 --deps "Prerequisite Ticket"
```

Options:
- `--deps <ticket1> <ticket2>`: 의존성 티켓 지정
- `--priority <P0|P1|P2|P3>`: 우선순위 설정 (Default: P2)

## Standard Ticket Format

All tickets MUST use this YAML Frontmatter:

```yaml
---
type: task-ticket
status: todo # todo, in-progress, done, blocked
priority: P2
dependencies: ["ticket-A", "ticket-B"]
created: "2024-01-21"
tags: []
---
```

## Utility Scripts

| Script | Purpose |
|--------|---------|
| `create_node.py` | task-manager/ 노드 생성 |
| `create_ticket.py` | 표준화된 티켓 생성 |
| `verify_node.py` | 구조 검증 |
| `add_optional.py` | 선택적 하위 노드 추가 |

## Context Scope Rule

1. task-manager/ 노드의 **sibling 디렉토리는 repository로 정의한다.**
2. sibling 및 descendants 노드 맥락 저장
3. repository/ 참조 시 children 범위까지만 저장
4. 모든 기록은 후속 에이전트 재사용 가능하도록 명시적 서술

## Reference

- [RULE-TEMPLATE.md](templates/RULE-TEMPLATE.md): RULE.md 템플릿 상세
- [TICKET-TEMPLATE.md](templates/TICKET-TEMPLATE.md): Ticket 템플릿 상세
- [ISSUE-NOTES-SPEC.md](templates/ISSUE-NOTES-SPEC.md): issue_notes/ 스펙
- [RELEASE-NOTES-SPEC.md](templates/RELEASE-NOTES-SPEC.md): release_notes/ 스펙
