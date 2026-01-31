---
name: cof-environment-set
description: COF 환경 설정 및 실행 지침. 에이전트가 COF 환경에서 작업할 때 반드시 참조해야 하는 규칙과 스킬 목록을 정의한다. Use when working in COF directories or creating/managing COF nodes.
trigger: always_on
context_id: cof-environment-set
role: RULE
state: const
scope: swarm
lifetime: persistent
version: "0.2.0"
created: "2026-01-31"
references:
  doctrine: cof-doctrine
  blueprint: cof-dna-blueprint
  skills:
    - cof-pointerical-tool-creator
    - cof-glob-indexing
    - cof-task-manager-node
    - solving-tickets
  agents:
    - cof-pointerical-tool-creator-agent
    - cof-task-manager-agent
  external:
    - summon-agents
---

# COF Environment Set

에이전트가 COF 환경에서 행동하는 **실행 지침(Execution Guidelines)**.

---

## Quick Reference

### Available Skills

| Skill | Purpose | Invocation |
|-------|---------|------------|
| `cof-pointerical-tool-creator` | Skill/Rule/Workflow 문서 생성 | `@skill(cof-pointerical-tool-creator)` |
| `cof-glob-indexing` | Node 경계 탐색, 인덱싱 | `@skill(cof-glob-indexing)` |
| `cof-task-manager-node` | task-manager/ 노드 관리 | `@skill(cof-task-manager-node)` |
| `solving-tickets` | 티켓 → 에이전트 할당 | `@skill(solving-tickets)` |

### Available Agents

| Agent | Purpose |
|-------|---------|
| `cof-pointerical-tool-creator` | 포인터 안전 문서 생성 오케스트레이터 |
| `cof-task-manager` | 티켓 관리 오케스트레이터 |

---

## 1. Pointer Model Baseline

### 1.1 Core Principles

1. 모든 문서는 **Context Pointer**로 취급된다
2. 디렉토리는 **포인터 타입**을 정의한다
3. 파일명은 **역할(Role)**과 **상태(State)**를 선언한다
4. 링크는 값이 아닌 **참조(pointer)**이다
5. **ID는 불변**, 경로는 가변이다

### 1.2 Directory = Pointer Type

```
[NN].[ROLE]/
```

- `NN`: 시각적 인덱스 (ordering only, 의미 없음)
- `ROLE`: 시스템이 해석하는 포인터 타입

**Standard Set:**

| Directory | Pointer Semantics |
|-----------|-------------------|
| `index/` | Context Pointer Table |
| `reference/` | const pointer |
| `working/` | mutable pointer |
| `ticket/` | stack pointer |
| `runtime/` | execution context |
| `history/` | freed/archived pointer |

### 1.3 Context Identity

모든 문서는 YAML Frontmatter에 다음을 포함:

```yaml
---
context_id: cof-xxxx          # Global unique, immutable
role: SKILL | RULE | WORKFLOW
state: const | mutable | active | frozen | archived
scope: immune | agora | nucleus | swarm
lifetime: ticket | persistent | archived
---
```

---

## 2. Skill Usage Mandate

다음 작업은 **반드시 지정된 Skill**을 사용해야 한다.

| Intent | Node | Required Skill |
|--------|------|----------------|
| 작업 맥락 생성 | `task-manager/` | `cof-task-manager-node` |
| 티켓 발행 | `tickets/` | `cof-task-manager-node` |
| 티켓 해결 | ticket → agent | `solving-tickets` |
| 완료 작업 정리 | `archive/` | `cof-task-manager-node` |
| 문서 생성 | Skill/Rule/Workflow | `cof-pointerical-tool-creator` |
| 컨텍스트 탐색 | Node boundary | `cof-glob-indexing` |

> **Warning**: `mkdir`/`touch`로 위 구조를 직접 생성하는 것은 **금지**.

---

## 3. Agent Workflow

### 3.1 작업 시작 시

```
1. Check: task-manager/ 존재?
   ├─ No  → cof-task-manager-node로 생성 (사용자 승인)
   └─ Yes → tickets/ 확인

2. Check: 할당된 티켓 존재?
   ├─ No  → 새 티켓 발행
   └─ Yes → solving-tickets로 처리
```

### 3.2 티켓 처리 흐름

```
ticket(todo) → cof-glob-indexing → agent selection → dispatch → result integration → ticket(done)
```

---

## 4. Hard Constraints

다음을 위반하는 문서는 **생성 불가**:

1. `context_id` 없는 문서
2. `history` context를 `active`로 참조
3. 디렉토리 ROLE과 state 불일치
4. 수명 전이가 명시되지 않은 Workflow
5. 숫자 인덱스(`NN`)에 의미를 부여한 규칙

---

## 5. Document Generation Rules

| Doc Type | Required Sections |
|----------|-------------------|
| **Skill** | Quick Start, Inputs/Outputs, Constraints |
| **Rule** | 접근 제어, 위반 처리 (실행 로직 금지) |
| **Workflow** | Entry Context, Transition Steps, Exit Rule, Lifetime Transition |
| **Agent** | Mission, Sub-Agent Delegation, Escalation |

### Skill Authoring (Best Practices)

- `name`: gerund form (`solving-tickets`)
- `description`: 3rd person, "Use when..." 포함
- Quick Start 먼저
- 500줄 이내
- References는 one level deep

> See: `@ref(skill-authoring-best-practices)`

---

## 6. Context Reference Protocol

### 6.1 Reference Syntax

| Syntax | Purpose | Example |
|--------|---------|---------|
| `@ref(context_id)` | 문서 참조 | `@ref(cof-doctrine)` |
| `@skill(context_id)` | 스킬 호출 | `@skill(cof-glob-indexing)` |
| `@agent(context_id)` | 에이전트 호출 | `@agent(cof-task-manager)` |

### 6.2 Resolution Order

1. **Local Config**: `.agent/config.yaml`의 `context_map`
2. **Swarm Registry**: 상위 COF의 `index/` 테이블
3. **Global Registry**: (미구현) 전역 context_id 레지스트리

### 6.3 Config Example

```yaml
# .agent/config.yaml
cof_root: "@ref(context-orchestrated-filesystem)"
context_map:
  cof-doctrine: "${COF_ROOT}/COF_DOCTRINE.md"
  cof-dna-blueprint: "${COF_ROOT}/DNA_BLUEPRINT.md"
  summon-agents: "03_Manifestation/Summon-Agents/"
```

---

## References

> **Note**: 모든 참조는 `context_id` 기반. 실제 경로는 agent config에서 resolve.

- **Doctrine**: `@ref(cof-doctrine)`
- **Blueprint**: `@ref(cof-dna-blueprint)`
- **Skills**: `@ref(cof-pointerical-tool-creator)`, `@ref(cof-glob-indexing)`, `@ref(cof-task-manager-node)`, `@ref(solving-tickets)`
- **Agents**: `@ref(cof-pointerical-tool-creator-agent)`, `@ref(cof-task-manager-agent)`
- **Best Practices**: `@ref(skill-authoring-best-practices)`
