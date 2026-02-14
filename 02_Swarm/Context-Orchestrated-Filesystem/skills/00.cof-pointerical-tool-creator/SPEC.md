# COF.Pointerical-Tool-Creator.skill
Meta Spec (v0.2)

---

## 0. Purpose

본 문서는 COF(Context-Orchestrated Filesystem)의 **포인터 모델(pointer model)**을 기반으로
Workflow, Rule, Skill, Sub-Agent 문서를 생성하기 위한 메타 생성기
`COF.Pointerical-Tool-Creator.skill`의 공식 스펙을 정의한다.

이 스킬의 목적은 다음을 만족하는 것이다.

1. 포인터 안전(pointer-safe)한 COF 문서 구조를 강제한다.
2. 참조 방향 및 수명 전이를 명시적으로 선언하게 한다.
3. COF Scanner / Immune System / Cortex Agora에서 해석 가능한 구조를 보장한다.
4. 문서 생성 시 Hard Constraints 위반을 사전에 탐지하고 차단한다.

---

## 1. Scope

- 대상: COF 규칙을 따르는 문서(SKILL, RULE, WORKFLOW, SUB-AGENT)
- 산출물 위치: 사용자가 지정한 경로 (COF 디렉토리 구조 준수 권장)
- 생성 대상: 실제 문서 또는 템플릿 스켈레톤
- 정책: `SKILL.md`는 표준 스킬 frontmatter만 유지하고, COF 식별 메타는 `SKILL.meta.yaml` sidecar에 저장한다.

---

## 2. Definitions

### 2.1 Core Design Principles

1. 모든 문서는 Context Pointer로 취급된다.
2. 디렉토리는 포인터 타입을 정의한다.
3. 파일명은 역할(Role)과 수명(State)을 선언한다.
4. 모든 참조는 값이 아닌 논리적 포인터(pointer)로 취급된다.
5. ID는 불변이며, 경로는 가변이다.

### 2.2 Directory Naming Convention

모든 디렉토리는 다음 규칙을 반드시 따른다.

```
[NN].[ROLE]/
```

- `NN` : 사람을 위한 시각적 인덱스 (ordering only)
- `ROLE` : 시스템이 해석하는 포인터 타입

> 숫자 인덱스(`NN`)는 의미를 가지지 않으며
> **어떠한 로직도 숫자에 의존해서는 안 된다.**

### 2.3 Standard Directory Set

```
00.index/
01.reference/
02.working/
03.ticket/
04.runtime/
99.history/
```

| Directory | Pointer Semantics |
|-----------|-------------------|
| index | Context Pointer Table |
| reference | const pointer |
| working | mutable pointer |
| ticket | stack pointer |
| runtime | execution context |
| history | freed / archived pointer |

### 2.4 Document Types

| Type | Role Value | Description |
|------|------------|-------------|
| SKILL | `SKILL` (in `SKILL.meta.yaml`) | 포인터 연산 능력(capability) 선언 |
| RULE | `RULE` | 접근 제어와 위반 처리 정의 |
| WORKFLOW | `WORKFLOW` | 상태 전이 및 수명 관리 정의 |
| SUB-AGENT | `SKILL` + `agent_kind: sub-agent` | 하위 에이전트 역할 선언 |

### 2.5 Context Identity Model

`RULE`/`WORKFLOW`/`SUB-AGENT` 문서는 YAML Frontmatter에 다음을 포함해야 한다.

```yaml
---
context_id: cof-xxxx
role: SKILL | RULE | WORKFLOW
state: const | mutable | active | frozen | archived
scope: immune | agora | nucleus | swarm
lifetime: ticket | persistent | archived
created: "YYYY-MM-DD"
---
```

| Field | Mutability | Description |
|-------|------------|-------------|
| `context_id` | 불변 | 전역 유일 식별자, 변경 불가 |
| `role` | 불변 | 문서 타입 선언 |
| `state` | 가변 | 현재 포인터 상태 |
| `scope` | 가변 | 가시성 범위 |
| `lifetime` | 가변 | 수명 정책 |
| `created` | 불변 | 생성일 |

### 2.6 SKILL Sidecar Metadata (`SKILL.meta.yaml`)

`SKILL.md`는 최소 frontmatter만 사용하고, COF 식별 메타는 sidecar 파일에 저장한다.

```yaml
context_id: cof-xxxx
role: SKILL
state: const | mutable | active | frozen | archived
scope: immune | agora | nucleus | swarm
lifetime: ticket | persistent | archived
created: "YYYY-MM-DD"
trigger: always_on | model_decision | using_instruction | data_state_change   # optional
consumers: []                                                                  # optional
notes: ""                                                                      # optional
```

---

## 3. Inputs

### 3.1 필수 입력

| 파라미터 | 타입 | 설명 |
|---------|------|------|
| `doc_type` | `enum` | 문서 타입: `skill` \| `rule` \| `workflow` \| `sub-agent` |
| `output_path` | `string` | 산출물 저장 경로 (절대 경로 권장) |
| `context_id` | `string` | 전역 유일 식별자. 패턴: `cof-[a-z0-9-]+` |
| `title` | `string` | 문서 제목 |

### 3.2 선택 입력

| 파라미터 | 타입 | 기본값 | 설명 |
|---------|------|--------|------|
| `state` | `enum` | `const` | 초기 상태: `const` \| `mutable` \| `active` \| `frozen` |
| `scope` | `enum` | `swarm` | 가시성: `immune` \| `agora` \| `nucleus` \| `swarm` |
| `lifetime` | `enum` | `persistent` | 수명: `ticket` \| `persistent` \| `archived` |
| `created` | `string` | 현재 날짜 | ISO 8601 형식 (YYYY-MM-DD) |
| `references` | `string[]` | `[]` | 관련 Rule/Skill/Workflow 링크 목록 |
| `template_only` | `boolean` | `false` | true이면 빈 템플릿만 생성 |

### 3.3 입력 검증 규칙

| 규칙 | 검증 조건 | 실패 시 에러 코드 |
|------|----------|------------------|
| context_id 형식 | `/^cof-[a-z0-9-]+$/` 매칭 | `INVALID_CONTEXT_ID` |
| context_id 유일성 | 기존 문서와 중복 없음 | `DUPLICATE_CONTEXT_ID` |
| output_path 유효성 | 부모 디렉토리 존재 | `INVALID_OUTPUT_PATH` |
| doc_type 유효성 | 허용된 enum 값 | `INVALID_DOC_TYPE` |

---

## 4. Outputs

### 4.1 산출물 구조

선택된 `doc_type`에 따라 다음 구조의 문서를 생성한다.

#### SKILL 문서 예시 (`SKILL.md`)

```markdown
---
name: my-skill
description: Use when creating or updating pointer-safe COF documents.
---

# My Skill Title

## 0. Purpose
- 목적과 범위를 간결히 서술한다.

## 1. Capability Declaration
- allowed_contexts: [...]
- forbidden_contexts: [...]
- consumers: immune | agora | agent

## 2. Inputs / Outputs
- inputs: [...]
- outputs: [...]

## 3. Constraints
- 금지된 포인터 접근 명시
- 실행 코드 포함 금지

## 4. References
- 관련 Rule/Workflow 링크
```

#### SKILL 메타 예시 (`SKILL.meta.yaml`)

```yaml
context_id: cof-my-skill
role: SKILL
state: const
scope: swarm
lifetime: persistent
created: "2025-05-20"
trigger: model_decision
consumers: ["agent"]
notes: ""
```

#### RULE 문서 예시

```markdown
---
context_id: cof-my-rule
role: RULE
state: const
scope: immune
lifetime: persistent
created: "2025-05-20"
---

# My Rule Title

## 0. Purpose
- 이 규칙이 보호하는 대상과 목적

## 1. Access Control
| Subject | Target Pointer Type | Condition | Permission |
|---------|---------------------|-----------|------------|
| agent | history | always | read-only |

## 2. Violation Handling
| Violation | SEV | Action |
|-----------|-----|--------|
| history write attempt | SEV-2 | reject + log |

## 3. References
- 관련 Skill/Workflow 링크
```

#### WORKFLOW 문서 예시

```markdown
---
context_id: cof-my-workflow
role: WORKFLOW
state: active
scope: swarm
lifetime: ticket
created: "2025-05-20"
---

# My Workflow Title

## 0. Purpose
- 이 워크플로우가 해결하는 문제

## 1. Entry Context
- entry_pointer: [입력 포인터 타입]
- preconditions: [선행 조건]

## 2. Transition Steps
| Step | Action | State Before | State After |
|------|--------|--------------|-------------|
| 1 | ... | mutable | active |
| 2 | ... | active | frozen |

## 3. Exit Rule
- exit_state: frozen | archived
- postconditions: [후행 조건]

## 4. Lifetime Transition
- 수명 전이 경로를 반드시 명시한다.

## 5. References
- 관련 Rule/Skill 링크
```

### 4.2 반환 구조

```json
{
  "status": "success" | "partial" | "error",
  "error_code": null | "INVALID_CONTEXT_ID" | "DUPLICATE_CONTEXT_ID" | ...,
  "warnings": [
    {"field": "...", "reason": "..."}
  ],
  "artifacts": {
    "document": "path/to/OUTPUT.md",
    "validation_result": {
      "passed": true | false,
      "violations": []
    }
  }
}
```

---

## 5. Core Workflow

### Step 1) Validate Inputs

- 필수 입력 파라미터 존재 여부 확인
- `context_id` 형식 및 유일성 검증
- `output_path` 유효성 검증
- 검증 실패 시 즉시 에러 반환, 문서 생성 중단

### Step 2) Resolve Template

- `doc_type`에 따른 템플릿 선택:
  - `skill` → `templates/SKILL_TEMPLATE.md`
  - `rule` → `templates/RULE_TEMPLATE.md`
  - `workflow` → `templates/WORKFLOW_TEMPLATE.md`
  - `sub-agent` → `templates/SUB_AGENT_TEMPLATE.md`
- 템플릿 파일 존재 여부 확인

### Step 3) Render Frontmatter

- `skill`:
  - `SKILL.md` frontmatter는 `name`, `description`, `allowed-tools`만 생성
  - COF 식별 메타는 `SKILL.meta.yaml`로 생성
- `rule/workflow/sub-agent`:
  - 기존 COF frontmatter(`context_id`, `role`, `state`, `scope`, `lifetime`, `created`) 생성
  - `sub-agent`의 경우 `agent_kind: sub-agent` 추가

### Step 4) Render Body

- 템플릿의 플레이스홀더를 입력값으로 치환:
  - `[Skill Title]` → `title`
  - `cof-xxxx` → `context_id`
  - `YYYY-MM-DD` → `created`
- `references` 배열이 있으면 References 섹션에 추가

### Step 5) Validate Pointer Safety

- Hard Constraints 준수 여부 검증:
  - `context_id` 존재 확인 (`skill`은 `SKILL.meta.yaml`에서 확인)
  - `role`과 디렉토리 ROLE 일치 여부 (경로에서 추론 가능 시)
  - `history` 컨텍스트를 `active`로 참조하는지 검사
  - WORKFLOW의 경우 수명 전이 명시 여부 확인
- 위반 발견 시 `warnings[]`에 기록, 심각도에 따라 중단 또는 경고 후 계속

### Step 6) Write Document

- 렌더링된 문서를 `output_path`에 저장
- 기존 파일 존재 시:
  - `context_id`가 동일하면 갱신 (덮어쓰기)
  - `context_id`가 다르면 `CONTEXT_ID_MISMATCH` 에러, 중단
- 쓰기 성공 시 반환 구조 생성

---

## 6. Generation Rules by Document Type

### 6.1 Skill Generation Rules

Skill은 **포인터 연산 능력(capability)** 만을 선언한다.

- 허용된 Context 접근
- 금지된 Context 접근
- 예상 소비자(COF Runtime / Immune System / Cortex Agora / Agent)

**금지 사항:**
- 실행 코드 생성
- 런타임 판단
- 정책 강제

### 6.2 Rule Generation Rules

Rule 문서는 오직 **접근 제어와 위반 처리**만을 정의한다.

- 누가 (Subject)
- 어떤 포인터 타입을 (Target)
- 어떤 조건에서 (Condition)
- 접근 가능한가 (Permission)

**금지 사항:**
- 실행 로직 포함

### 6.3 Workflow Generation Rules

Workflow 문서는 반드시 다음을 포함해야 한다.

1. Entry Context (입력 포인터)
2. Transition Steps (포인터 상태 전이)
3. Exit Rule (종료 상태)
4. **Lifetime Transition (수명 전이) - 필수**

**금지 사항:**
- 수명 전이가 명시되지 않은 Workflow는 유효하지 않다.

### 6.4 Sub-Agent Generation Rules

Sub-Agent는 SKILL 문서의 변형이다.

- `role`은 `SKILL`로 유지
- `agent_kind: sub-agent` 필드 추가
- 위임 가능한 capability 범위 명시

---

## 7. Error Handling

### 7.1 입력 검증 에러

| 에러 유형 | 에러 코드 | 동작 |
|----------|----------|------|
| context_id 형식 불일치 | `INVALID_CONTEXT_ID` | 즉시 중단, 에러 반환 |
| context_id 중복 | `DUPLICATE_CONTEXT_ID` | 즉시 중단, 에러 반환 |
| output_path 부모 디렉토리 없음 | `INVALID_OUTPUT_PATH` | 즉시 중단, 에러 반환 |
| doc_type 유효하지 않음 | `INVALID_DOC_TYPE` | 즉시 중단, 에러 반환 |

### 7.2 템플릿 에러

| 에러 유형 | 에러 코드 | 동작 |
|----------|----------|------|
| 템플릿 파일 없음 | `TEMPLATE_NOT_FOUND` | 즉시 중단, 에러 반환 |
| 템플릿 파싱 실패 | `TEMPLATE_PARSE_ERROR` | 즉시 중단, 에러 반환 |

### 7.3 포인터 안전성 위반

| 위반 유형 | 에러 코드 | SEV | 동작 |
|----------|----------|-----|------|
| context_id 누락 | `MISSING_CONTEXT_ID` | SEV-1 | 즉시 중단 |
| history를 active로 참조 | `INVALID_HISTORY_REF` | SEV-2 | 경고 후 계속, `warnings[]`에 기록 |
| role과 디렉토리 불일치 | `ROLE_DIR_MISMATCH` | SEV-3 | 경고 후 계속, `warnings[]`에 기록 |
| Workflow 수명 전이 누락 | `MISSING_LIFETIME_TRANSITION` | SEV-2 | 즉시 중단 |
| 숫자 인덱스에 의미 부여 | `INDEX_SEMANTIC_VIOLATION` | SEV-3 | 경고 후 계속 |

### 7.4 파일시스템 에러

| 에러 유형 | 에러 코드 | 동작 |
|----------|----------|------|
| 쓰기 권한 없음 | `WRITE_PERMISSION_DENIED` | 즉시 중단, 에러 반환 |
| 디스크 공간 부족 | `DISK_FULL` | 즉시 중단, 에러 반환 |
| 기존 파일 context_id 불일치 | `CONTEXT_ID_MISMATCH` | 즉시 중단, 에러 반환 |

### 7.5 반환 구조 (에러 시)

```json
{
  "status": "error",
  "error_code": "DUPLICATE_CONTEXT_ID",
  "error_message": "context_id 'cof-my-skill' already exists at '/path/to/existing.md'",
  "warnings": [],
  "artifacts": null
}
```

---

## 8. Compatibility

### 8.1 Immune System Compatibility

본 Skill이 생성한 문서는 다음을 만족해야 한다.

- 정적 참조 무결성 검사 가능
- 금지된 포인터 접근 명시
- 위반 시 SEV 분류 가능

### 8.2 Cortex Agora Compatibility

본 Skill이 생성한 문서는 다음을 노출해야 한다.

- 입력 로그 유형
- 시간 축 사용 여부
- 패턴 / 이상 탐지 산출물 유형

---

## 9. Hard Constraints

다음 항목을 위반하는 문서는 생성 불가하다.

| # | 제약 | 검증 방법 | 위반 시 에러 코드 |
|---|-----|----------|------------------|
| 1 | `context_id` 없는 문서 금지 | Frontmatter 파싱 후 필드 존재 확인 | `MISSING_CONTEXT_ID` |
| 2 | `history` 컨텍스트를 `active`로 참조 금지 | state 필드 검사 + 참조 경로 분석 | `INVALID_HISTORY_REF` |
| 3 | 디렉토리 ROLE과 state 불일치 금지 | output_path에서 ROLE 추출 후 비교 | `ROLE_DIR_MISMATCH` |
| 4 | 수명 전이 누락된 Workflow 금지 | WORKFLOW 타입일 때 Lifetime Transition 섹션 존재 확인 | `MISSING_LIFETIME_TRANSITION` |
| 5 | 숫자 인덱스(`NN`)에 의미 부여 금지 | 문서 내용에서 `[0-9]+\.` 패턴 참조 시 의미 부여 여부 휴리스틱 검사 | `INDEX_SEMANTIC_VIOLATION` |

---

## 10. Non-goals

본 Skill은 다음을 수행하지 않는다.

- 실행 코드(Python/JS 등) 생성
- 런타임 판단 또는 동적 의사결정
- 정책 강제(권한 판단/위반 처리 실행)
- 전역 인덱스 또는 문서 레지스트리 관리
- 기존 문서의 마이그레이션 또는 일괄 변환

---

## 11. Tool-Specific Extension Policy

본 스펙은 COF(Core) 기준으로 작성되었으며,
특정 편집기나 툴(예: 옵시디언)에 종속된 규칙은 포함하지 않는다.

툴 특화 규칙은 다음 원칙을 따른다.

- COF 스펙을 수정하지 않는다.
- 별도의 확장 레이어로 정의한다.
- 확장 스펙은 `co-*` 네임스페이스를 사용한다.

예:
- `co-obsidian.Pointer-Link-Resolver`
- `co-obsidian.Backlink-Indexer`

---

## 12. References

본 스킬이 참조하는 문서들.

| 문서 | 경로 | 설명 |
|------|------|------|
| Skill Normative | `references/skill-normative-interpretation.md` | Skill 문서 작성/해석 규범 |
| Rule Normative | `references/rule-normative-interpretation.md` | Rule 문서 작성/해석 규범 |
| Workflow Normative | `references/workflow-normative-interpretation.md` | Workflow 문서 작성/해석 규범 |
| Sub-Agent Normative | `references/subagent-normative-interpretation.md` | Sub-Agent 문서 작성/해석 규범 |
| Glob Patterns | `references/glob-patterns.md` | Glob 패턴 문법 정의 |
| COF Governance Guide | `references/cof-environment-set.md` | COF 전체 규칙 정의 (skill-based) |

---

## Appendix A. Changelog

| 버전 | 날짜 | 변경 사항 |
|------|------|----------|
| v0.1 | - | 초안 작성 |
| v0.2 | - | 구조 전면 개편: Scope/Inputs/Outputs/Core Workflow/Error Handling 섹션 신설, Hard Constraints 검증 방법 및 에러 코드 매핑 추가, 산출물 템플릿 예시 추가, Non-goals 명시, References 정형화 |
