---
name: creating-task-ticket-node
description: Creates task-ticket/ node structure for agent context management. Use when initializing a new workspace, setting up task tracking, or when user mentions "task-ticket", "context node", or "COF node".
---

# Task-Ticket Node

task-ticket/ 노드는 에이전트 작업 맥락을 저장하는 COF 노드이다.

## Quick Start

```bash
python scripts/create_node.py /path/to/target
```

Output:
```
{targetPath}/
└── task-ticket/
    ├── RULE.md
    ├── troubleshooting.md
    └── tickets/
```

## Utility Scripts

**create_node.py**: task-ticket/ 노드 생성

```bash
# 기본 생성
python scripts/create_node.py <target_path>

# issue_notes/ 포함
python scripts/create_node.py <target_path> --with-issue-notes

# 모든 선택적 노드 포함
python scripts/create_node.py <target_path> --all
```

**verify_node.py**: 구조 검증

```bash
python scripts/verify_node.py <node_path>
# Returns: OK or INVALID with missing items
```

**add_optional.py**: 기존 노드에 선택적 하위 노드 추가

```bash
python scripts/add_optional.py <node_path> --issue-notes
python scripts/add_optional.py <node_path> --release-notes
python scripts/add_optional.py <node_path> --all
```

## Creation Workflow

Copy this checklist:

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
python scripts/create_node.py <target_path> [--all]
```

**Step 3: Run verify_node.py**

```bash
python scripts/verify_node.py <target_path>/task-ticket
```

검증 실패 시 에러 메시지 확인 후 수정.

**Step 4: Report result**

생성된 구조와 각 파일의 용도를 사용자에게 안내.

## Context Scope Rule

1. sibling 및 descendants 노드 맥락 저장
2. repository/ 참조 시 children 범위까지만 저장
3. 모든 기록은 후속 에이전트 재사용 가능하도록 명시적 서술

## Reference

- [RULE-TEMPLATE.md](RULE-TEMPLATE.md): RULE.md 템플릿 상세
- [ISSUE-NOTES-SPEC.md](ISSUE-NOTES-SPEC.md): issue_notes/ 스펙
- [RELEASE-NOTES-SPEC.md](RELEASE-NOTES-SPEC.md): release_notes/ 스펙
