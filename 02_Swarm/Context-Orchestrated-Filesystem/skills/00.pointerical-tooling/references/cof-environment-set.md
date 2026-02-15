---
name: cof-environment-set
description: COF 환경 설정 및 실행 지침. 에이전트가 COF 환경에서 작업할 때 반드시 참조해야 하는 규칙과 스킬 목록을 정의한다. Use when working in COF directories or creating/managing COF nodes.
trigger: always_on
version: "0.3.0"
created: "2026-01-31"
updated: "2026-02-15"
---

# COF Environment Set

에이전트가 COF 환경에서 행동하는 **실행 지침(Execution Guidelines)**.

---

## Quick Reference

### Available Skills

| Skill | Purpose | Invocation |
|-------|---------|------------|
| `cof-pointerical-tooling` | Skill/Rule/Workflow 문서 생성 | `@skill(cof-pointerical-tooling)` |
| `cof-glob-indexing` | Node 경계 탐색, 인덱싱 | `@skill(cof-glob-indexing)` |
| `cof-task-context-management` | `NN.agents-task-context/` 및 버전 브랜치 노드 관리 (legacy: `task-manager/`) | `@skill(cof-task-context-management)` |
| `cof-ticket-solving` | 티켓 → 에이전트 할당 | `@skill(cof-ticket-solving)` |
| `cof-skill-governance` | Swarm 스킬 레지스트리/관리 | `@skill(cof-skill-governance)` |

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
| `tickets/` | stack pointer |
| `runtime/` | execution context |
| `history/` | freed/archived pointer |

### 1.3 Agent Model Depth Strategy

에이전트 모델 버전이 증가하면 노드 하위 뎁스가 깊어질 수 있습니다. COF는 고정된 뎁스를 가정하지 않고, **경계 기반 탐색**으로 대응합니다.

- Canonical Anchor: 각 모델 패밀리의 기본 진입점은 항상 `NN.agents-task-context/` 입니다.
- 권장 확장: `NN.agents-task-context/<agent-family>/<version>/`
  - 예: `01.agents-task-context/claude/4.0/tickets/`
  - 예: `01.agents-task-context/gemini/2.5/working/`
- 탐색 규칙: 상대 깊이 숫자 대신 `AGENT.md`, `index/`, `reference/`, `tickets/` 같은 포인터 요소로 경계를 판별합니다.

---

## 2. Skill Usage Mandate

다음 작업은 **반드시 지정된 Skill**을 사용해야 한다.

| Intent | Node | Required Skill |
|--------|------|----------------|
| 작업 맥락 생성 | `NN.agents-task-context/` 또는 `NN.agents-task-context/<agent-family>/<version>/` (legacy: `task-manager/`) | `cof-task-context-management` |
| 티켓 발행 | `NN.agents-task-context/<branch>/tickets/` | `cof-task-context-management` |
| 티켓 해결 | 티켓 파일 → 적절한 에이전트 | `cof-ticket-solving` |
| 완료 작업 정리 | `archive/` | `cof-task-context-management` |
| 문서 생성 | Skill/Rule/Workflow | `cof-pointerical-tooling` |
| 컨텍스트 탐색 | Node boundary | `cof-glob-indexing` |

> **Warning**: `mkdir`/`touch`로 위 구조를 직접 생성하는 것은 **금지**. 모델 분기 브랜치 생성은 `cof-task-context-management`를 통해서만 진행합니다.

### 2.1 Agent Namespace Hard-Fail Policy

생성물(티켓/실행 로그/중간 산출물)은 반드시 아래 경로 하위로만 생성한다.

`NN.agents-task-context/<agent-family>/<version>/...`

- `agent-family`/`version`은 경로 또는 CLI 인자(`--agent-family`, `--agent-version`)에서 해석 가능해야 한다.
- 해석 불가 시 즉시 실패(exit code 1)한다.
- 비표준(shared) 경로 쓰기 시도는 즉시 실패하고 `[AUDIT] namespace_policy_violation` 로그를 출력한다.

### 2.2 Shared Path Exception (Governance Only)

아래 공용 경로는 문서 거버넌스 목적의 예외로 허용한다.

- `README.md`
- `DNA.md`
- `skills/`
- `registry/`

위 예외 외의 생성물은 모두 agent namespace 하위에서만 생성/갱신한다.

---

## 3. Agent Workflow

### 3.1 작업 시작 시

```
1. Check: `NN.agents-task-context/` 존재?
   ├─ No  → cof-task-context-management로 생성 (사용자 승인)
   └─ Yes → 적용 중인 브랜치의 `tickets/` 확인

2. Branching strategy:
   - 기본 브랜치: `NN.agents-task-context/tickets/`
   - 모델 분기: `NN.agents-task-context/<agent-family>/<version>/tickets/`
   - 브랜치는 기존 브랜치와 병행해 유지 가능

3. Check: 할당된 티켓 존재?
   ├─ No  → 새 티켓 발행
   └─ Yes → cof-ticket-solving(`@skill(cof-ticket-solving)`)로 처리
```

### 3.2 티켓 처리 흐름

```
ticket(todo) → cof-glob-indexing → agent selection → dispatch → result integration → ticket(done)
```

---

## 4. Hard Constraints

다음을 위반하는 문서는 **생성 불가**:

1. `history` context를 `active`로 참조
2. 디렉토리 ROLE과 state 불일치
3. 수명 전이가 명시되지 않은 Workflow
4. 숫자 인덱스(`NN`)에 의미를 부여한 규칙
5. 고정 노드 뎁스를 가정한 경로 하드코딩

---

## 5. Document Generation Rules

| Doc Type | Required Sections |
|----------|-------------------|
| **Skill** | Quick Start, Inputs/Outputs, Constraints |
| **Rule** | 접근 제어, 위반 처리 (실행 로직 금지) |
| **Workflow** | Entry Context, Transition Steps, Exit Rule, Lifetime Transition |
| **Agent** | Mission, Sub-Agent Delegation, Escalation |

### Skill Authoring (Best Practices)

- `name`: gerund form (`cof-ticket-solving`)
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

### 6.2 Resolution Order

1. **Local Config**: `.agent/config.yaml`의 `context_map`
2. **Swarm Registry**: 상위 COF의 `index/` 테이블
3. **Swarm Registry**: `02_Swarm/cortex-agora/registry/SWARM_SKILL_REGISTRY.md`와 각 Swarm의 `registry/SKILL_REGISTRY.md`
4. **Global Registry**: `02_Swarm/cortex-agora/registry/SWARM_SKILL_REGISTRY.md` + `02_Swarm/cortex-agora/registry/GLOBAL_SKILL_REGISTRY.json`

### 6.3 Config Example

```yaml
# .agent/config.yaml
cof_root: "@ref(context-orchestrated-filesystem)"
context_map:
  cof-doctrine: "${COF_ROOT}/core-docs/COF_DOCTRINE.md"
  cof-dna: "${COF_ROOT}/DNA.md"
  summon-agents: "03_Manifestation/summon-agents/"
```

---

## References

> **Note**: 모든 참조는 `context_id` 기반. 실제 경로는 agent config에서 resolve.

- **Doctrine**: `@ref(cof-doctrine)`
- **Skills**: `@ref(cof-pointerical-tooling)`, `@ref(cof-glob-indexing)`, `@ref(cof-task-context-management)`, `@ref(cof-ticket-solving)`, `@ref(cof-skill-governance)`
- **Best Practices**: `@ref(skill-authoring-best-practices)`
