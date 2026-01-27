---
name: managing-task-contexts
description: Creates and manages task-manager/ node structures for persistent agent context tracking. Use when initializing project workspaces, creating task tickets, or when the user mentions "task management", "context node", "COF", or needs sequential ticket dependency management.
---

# Task-Manager Node

task-manager/ 노드는 에이전트 작업 맥락을 저장하고 개별 작업 티켓을 관리하는 COF 노드이다.

## Node Creation Workflow

**One-Step Bootstrap (Recommended)**

```bash
python3 scripts/bootstrap_node.py <target_path>
```

This single command will:
1. Create the `task-manager/` structure (using `create_node.py --all`)
2. Verify the structure (using `verify_node.py`)
3. Report readiness

**Manual Creation (Legacy)**
If bootstrapping fails, you can fall back to the manual steps:
1. `python3 scripts/create_node.py <target_path> --all`
2. `python3 scripts/verify_node.py <target_path>/task-manager`

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


## Task Lifecyle Management

**Archiving Completed Tasks**

```bash
python3 scripts/archive_tasks.py <node_path>/task-manager
```

Moves `status: done` tickets to `archive/tickets/` and logs them in `archive/README.md`.
**Collision Safety**: Automatically appends timestamp if a file with the same name exists in archive.

**Node Validation**

```bash
python3 scripts/validate_node.py <node_path>/task-manager
```

Checks for `RULE.md` presence and broken ticket dependencies.

## Utility Scripts

| Script | Purpose |
|--------|---------|
| `bootstrap_node.py` | **[NEW]** 1-Click Node Creation & Verification |
| `create_node.py` | task-manager/ 노드 생성 (Low-level) |
| `create_ticket.py` | 표준화된 티켓 생성 |
| `verify_node.py` | 구조 검증 |
| `validate_node.py` | 노드 건강(Health) 진단 (의존성 등) |
| `add_optional.py` | 선택적 하위 노드 추가 |
| `archive_tasks.py` | 완료된 티켓 아카이빙 |

## Context Scope Rule

1. task-manager/ 노드의 **sibling 디렉토리는 repository로 정의한다.**
2. sibling 및 descendants 노드 맥락 저장
3. repository/ 참조 시 children 범위까지만 저장
4. 모든 기록은 후속 에이전트 재사용 가능하도록 명시적 서술

## Reference

- [NODE_RULE.md](templates/NODE_RULE.md): RULE.md 템플릿
- [TICKET-TEMPLATE.md](templates/TICKET-TEMPLATE.md): Ticket 템플릿
- [ISSUE_NOTE_RULE.md](templates/ISSUE_NOTE_RULE.md): issue_notes/ 템플릿
- [RELEASE_NOTE_RULE.md](templates/RELEASE_NOTE_RULE.md): release_notes/ 템플릿
