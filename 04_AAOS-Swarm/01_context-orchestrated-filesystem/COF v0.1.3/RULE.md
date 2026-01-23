---
trigger: always_on
description: "COF의 모든 Node 생성 및 관리는 본 규칙을 따르며, 정의된 Skill을 통해서만 수행된다."
---

# COF v0.1.3 RULE

본 규칙은 **Rule Genome**에 해당하며, 에이전트가 COF 환경에서 행동하는 **실행 지침(Execution Guidelines)**이다.

## 1. Skill Usage Mandate (스킬 사용 의무)

COF 독트린의 "Skill-Mediated Creation Only" 원칙에 따라, 다음 작업은 반드시 지정된 Skill을 호출해야 한다.

| 목적 (Intent) | 대상 Node | 필수 Skill | 비고 |
|---|---|---|---|
| **작업 맥락 생성/초기화** | `task-manager/` | `cof-task-manager-node` | `create_node.py` 실행 |
| **작업 티켓 발행** | `tickets/` | `cof-task-manager-node` | `create_ticket.py` 실행 |
| **완료 작업 정리** | `archive/` | `cof-task-manager-node` | `archive_tasks.py` 실행 |

> **Warning**: `mkdir`나 `touch` 명령어로 위 구조를 직접 생성하는 것은 **금지**된다.

## 2. Node Definitions

### 2.1. Task-Manager Node (`task-manager/`)
- **역할**: 에이전트의 작업 맥락(Context)을 저장하고 추적한다.
- **위치**: 작업 대상 디렉토리의 Sibling 위치
- **권한**:
  - 생성: `Using Skill` (O), `Manual` (X)
  - 수정: `Using Skill` (O), `Manual` (X) - 단, 내용(Content) 수정은 허용

## 3. Workflow Integration

모든 에이전트는 작업 시작 전 다음 순서를 따른다:

1. **Check**: 현재 디렉토리에 `task-manager/`가 있는가?
2. **If Missing**: `cof-task-manager-node` 스킬을 사용하여 노드를 생성한다. (사용자 승인 필요)
3. **If Present**: `tickets/`에서 할당된 티켓을 확인하거나, 새로운 티켓을 발행한다.

---
**Reference**:
- Doctrine: `COF_DOCTRINE.md`
- Skill Manual: `skills/cof-task-manager-node/SKILL.md`
