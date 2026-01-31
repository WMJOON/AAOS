---
trigger: always_on
description: "COF의 모든 Node 생성 및 관리는 본 규칙을 따르며, 정의된 Skill을 통해서만 수행된다."
---

# COF v0.1.3 RULE

본 규칙은 **Rule Genome**에 해당하며, 에이전트가 COF 환경에서 행동하는 **실행 지침(Execution Guidelines)**이다.

## Canonical Location (v0.1.3+)

COF canonical 문서는 버전 폴더(`COF vX.Y.Z/`)가 아니라 아래 경로에 직접 위치한다.

- `04_Agentic_AI_OS/02_Swarm/01_context-orchestrated-filesystem/`

버전은 폴더명이 아니라 문서의 YAML Frontmatter(`version`) 및 아카이브(`_archive/`)로 관리한다.

## 0. COF Pointer Model Baseline (Core)

### 0.1 Core Design Principles

1. 모든 문서는 Context Pointer로 취급된다.
2. 디렉토리는 포인터 타입을 정의한다.
3. 파일명은 역할(Role)과 수명(State)을 선언한다.
4. 링크(`[[...]]`)는 값이 아닌 참조(pointer)이다.
5. ID는 불변이며, 경로는 가변이다.

### 0.2 Directory = Pointer Type Rule

모든 디렉토리는 다음 규칙을 반드시 따른다.

```
[NN].[ROLE]/
```

- `NN` : 사람을 위한 시각적 인덱스 (ordering only)
- `ROLE` : 시스템이 해석하는 포인터 타입

> 숫자 인덱스(`NN`)는 의미를 가지지 않으며  
> 어떠한 로직도 숫자에 의존해서는 안 된다.

표준 디렉토리 세트:

```
00.index/
01.reference/
02.working/
03.ticket/
04.runtime/
99.history/
```

| Directory | Pointer Semantics |
|---------|-------------------|
| index | Context Pointer Table |
| reference | const pointer |
| working | mutable pointer |
| ticket | stack pointer |
| runtime | execution context |
| history | freed / archived pointer |

### 0.3 Context Identity Model

모든 문서는 YAML Frontmatter에 다음을 포함해야 한다.

```
---
context_id: cof-xxxx
role: SKILL | RULE | WORKFLOW
state: const | mutable | active | frozen | archived
scope: immune | agora | nucleus | swarm
lifetime: ticket | persistent | archived
---
```

- `context_id`는 전역에서 유일해야 하며 변경 불가이다.
- 파일 이동이나 이름 변경은 context_id에 영향을 주지 않는다.

### 0.4 Pointerical Skill Creator (`00.cof-pointerical-tool-creator`)

`skills/00.cof-pointerical-tool-creator/`는 포인터 안전(pointer-safe)한 문서만을 생성하도록 강제하는 **메타 생성 Skill**이다.  
재귀적으로 Skill/Rule/Workflow를 만들 때의 기본 패턴으로 사용한다.

- 수행 범위: 포인터 안전한 문서 구조 생성, 참조 방향 및 수명 전이 명시, Immune/Agora 스캔 가능성 보장
- 수행 금지: 실행 코드 생성, 런타임 판단, 정책 강제

### 0.5 Document Generation Rules

- Workflow 문서: Entry Context, Transition Step, Exit Rule을 반드시 포함한다.
- Workflow 문서: 수명 전이가 명시되지 않으면 유효하지 않다.
- Rule 문서: 접근 제어와 위반 처리만을 정의하며 실행 로직은 포함하지 않는다.
- Skill 문서: 포인터 연산 능력(capability)만을 선언한다.

### 0.6 Compatibility Requirements

- Immune System: 정적 참조 무결성 검사 가능, 금지된 포인터 접근 명시, 위반 시 SEV 분류 가능
- Cortex Agora: 입력 로그 유형, 시간 축 사용 여부, 패턴/이상 탐지 산출물 유형 노출

### 0.7 Hard Constraints

다음 항목을 위반하는 문서는 생성 불가하다.

1. context_id 없는 문서
2. history context를 active로 참조
3. 디렉토리 ROLE과 state 불일치
4. 수명 전이가 명시되지 않은 Workflow
5. 숫자 인덱스(`NN`)에 의미를 부여한 규칙

## 1. Skill Usage Mandate (스킬 사용 의무)

COF 독트린의 "Skill-Mediated Creation Only" 원칙에 따라, 다음 작업은 반드시 지정된 Skill을 호출해야 한다.

| 목적 (Intent) | 대상 Node | 필수 Skill | 비고 |
|---|---|---|---|
| **작업 맥락 생성/초기화** | `task-manager/` | `cof-task-manager-node` | `bootstrap_node.py` 권장 (`create_node.py --all` 포함) |
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
- Skill Manual: `skills/02.cof-task-manager-node/SKILL.md`
- Pointerical Spec: `skills/00.cof-pointerical-tool-creator/SPEC.md`
