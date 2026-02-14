---
name: cof-task-manager-node
description: "Creates and manages `NN.agents-task-context/` nodes (tickets, verification, validation, archiving) for persistent agent context tracking in COF. (legacy: `task-manager/`)"
---

# COF Task-Manager Node

NN.agents-task-context/ 노드는 에이전트 작업 맥락을 저장하고 개별 작업 티켓을 관리하는 COF 노드이다. (기본 생성: `01.agents-task-context/`, legacy: `task-manager/`)

> **설계 스펙**: [SPEC.md](SPEC.md) 참조

## When to Use

- 작업 시작 시 “작업 맥락(티켓/이슈/릴리즈/트러블슈팅)”을 표준 구조로 만들고 싶을 때
- 작업을 티켓 단위로 쪼개고 의존성을 추적해야 할 때
- 완료 티켓을 아카이브로 이동하고, 흔적을 남겨야 할 때

## Quick Start (Bootstrap)

```bash
python3 scripts/bootstrap_node.py <target_path>
```

수행 내용:
1. `01.agents-task-context/` 생성 (`create_node.py --all`)
2. 구조 검증 (`verify_node.py`)

## Node Creation (Manual)

```bash
python3 scripts/create_node.py <target_path> --all
python3 scripts/verify_node.py <target_path>/01.agents-task-context
```

## Ticket Creation

```bash
python3 scripts/create_ticket.py "Ticket Name" \
  --dir "<target_path>/01.agents-task-context" \
  --priority P1 \
  --deps "Prerequisite Ticket"
```

Options:
- `--dir`: `01.agents-task-context/` 또는 `tickets/` 기준 경로 (legacy: `task-manager/`)
- `--deps`: 의존 티켓 목록 (입력은 파일 stem 기준으로 정규화되어 기록됨)
- `--priority`: `P0|P1|P2|P3` (Default: `P2`)
- `create_ticket.py`는 특수문자-only 제목인 경우 안전하게 `untitled-ticket.md`로 생성하고,
  동일 파일명이 이미 존재하면 `-1`, `-2` ... 형태로 자동 회피합니다.

## Standard Ticket Format (Key Point)

All tickets MUST use this YAML Frontmatter:

```yaml
---
type: task-ticket
status: todo # todo, in-progress, done, blocked
priority: P2
dependencies: ["Ticket-A", "Ticket-B"] # ticket file stems (no .md)
created: "YYYY-MM-DD"
tags: []
---
```


## Task Lifecycle Management

**Archiving Completed Tasks**

```bash
python3 scripts/archive_tasks.py <node_path>/01.agents-task-context
```

Moves `status: done` tickets to `archive/tickets/` and logs them in `archive/README.md`.
**Collision Safety**: Automatically appends timestamp if a file with the same name exists in archive.

**Node Validation**

```bash
python3 scripts/validate_node.py <node_path>/01.agents-task-context
```

Checks for `cof-environment-set.md` presence and broken ticket dependencies.

## Utility Scripts

| Script | Purpose |
|--------|---------|
| `bootstrap_node.py` | **[NEW]** 1-Click Node Creation & Verification |
| `create_node.py` | 01.agents-task-context/ 노드 생성 (Low-level) |
| `create_ticket.py` | 표준화된 티켓 생성 |
| `verify_node.py` | 구조 검증 |
| `validate_node.py` | 노드 건강(Health) 진단 (의존성 등) |
| `add_optional.py` | 선택적 하위 노드 추가 |
| `archive_tasks.py` | 완료된 티켓 아카이빙 |

## Context Scope Rule

1. NN.agents-task-context/ 노드의 **sibling 디렉토리는 repository로 정의한다.**
2. sibling 및 descendants 노드 맥락 저장
3. repository/ 참조 시 children 범위까지만 저장
4. 모든 기록은 후속 에이전트 재사용 가능하도록 명시적 서술

## Reference

- [NODE_RULE.md](templates/NODE_RULE.md): cof-environment-set.md 템플릿
- [TICKET-TEMPLATE.md](templates/TICKET-TEMPLATE.md): Ticket 템플릿
- [ISSUE_NOTE_RULE.md](templates/ISSUE_NOTE_RULE.md): issue_notes/ 템플릿
- [RELEASE_NOTE_RULE.md](templates/RELEASE_NOTE_RULE.md): release_notes/ 템플릿
- Governance Guide: `../00.cof-pointerical-tool-creator/references/cof-environment-set.md`
