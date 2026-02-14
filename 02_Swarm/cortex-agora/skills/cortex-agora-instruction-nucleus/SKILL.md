---
name: structuring-cortex-agora-proposals
description: Structures cortex-agora observation proposals into reusable semantic contract format for COWI/Nucleus downstream consumers (5 types/fields/modes/contract). Use when formalizing behavior patterns as instruction candidates.
---

# Cortex Agora Instruction Nucleus

cortex-agora에서 Behavior Feed를 관찰하고 제안(Proposal)을 생성할 때, 그 제안을 **Nucleus 의미 계약**에 맞춰 구조화하는 스킬.

---

## Capability Declaration

| Category | Value |
|----------|-------|
| allowed_contexts | `ticket`, `reference`, `working` |
| forbidden_contexts | `history` (read-only), `runtime` (execution) |
| consumers | `context-orchestrated-workflow-intelligence`, `deliberation_chamber`, `agent` |
| execution_mode | `:reference_only` (proposals only) |

---

## Quick Use

1. Behavior Feed 관찰 결과가 "패턴화 후보"로 식별되면 이 스킬을 적용한다.
2. 제안(Proposal)을 아래 **Proposal Nucleus Template**에 따라 구조화한다.
3. Type Assignment Guide를 참고하여 적절한 `:type`을 부여한다.
4. Boundary Check를 수행하여 Nucleus 범위 외 요소를 분리한다.
5. 규칙/스킬 변경이 필요한 제안은 Escalation Path를 따른다.
6. COWI 전달 시 `source_snapshot.agora_ref`, `source_snapshot.captured_at`를 함께 제공한다.

---

## Workflow Checklist

제안 작성 시 이 체크리스트를 복사하여 사용한다.

```
Proposal Structuring Progress:
- [ ] Step 1: 관찰 패턴 식별 (observation/interpretation 작성)
- [ ] Step 2: Type 결정 (:rule/:state/:policy 또는 위임)
- [ ] Step 3: Type-Field Cardinality 검증
- [ ] Step 4: Trigger/Dependencies 정의
- [ ] Step 5: Contract 정의 (해당 type만)
- [ ] Step 6: Boundary Check (Nucleus 외 요소 분리)
- [ ] Step 7: Validation Checklist 통과
- [ ] Step 8: 승격 필요 시 Escalation Request 작성
```

---

## Proposal Nucleus Template

cortex-agora의 제안은 다음 구조를 따른다.

```yaml
proposal:
  # === Identity (REQUIRED) ===
  id: "proposal-[swarm]-[pattern-name]"
  version: "0.1.0"

  # === Origin (cortex-agora 관찰 출처) ===
  origin:
    observation: "[관찰 요약: 특정 조건에서 특정 선택이 반복됨]"
    interpretation: "[해석: 자동화/룰화 후보일 가능성(가설)]"
    evidence:
      - behavior_feed: "[source_path]"
        event_ids: ["evt-001", "evt-002"]
        pattern_frequency: "[n회/기간]"

  # === Proposed Instruction ===
  instruction:
    # -- Identity (REQUIRED) --
    id: "[instruction-id]"
    version: "1.0.0"
    type: [:rule | :state | :policy]  # cortex-agora 권한 내
    description: "[250자 이내 요약]"

    # -- Execution (REQUIRED) --
    execution:
      mode: :reference_only           # 필수 (비실행)

    # -- Trigger (OPTIONAL) --
    trigger:
      type: [:always_on | :model_decision | :using_instruction | :data_state_change]
      condition: "[선언적 조건]"
      dependencies:
        - id: "[instruction-id]"
          type: [:prerequisite | :watch | :reference]

    # -- Contract (TYPE-DEPENDENT) --
    contract:
      input_schema: {}                # :method/:workflow (위임 시)
      output_schema: {}               # :method/:workflow (위임 시)
      schema: {}                      # :state only

    # -- Validation (TYPE-DEPENDENT) --
    validation:
      level: [:hard | :soft | :policy_signal]
      pre_conditions: []              # :rule
      post_conditions: []             # :rule
      criteria: []                    # :policy only

  # === Delegation (cortex-agora 권한 외) ===
  delegation:
    requires_execution: false         # true면 다른 Swarm 위임
    target_swarm: null                # 위임 대상 (있을 경우)
    escalation_required: false        # true면 Deliberation으로 승격

  # === Out of Scope (Nucleus 범위 외) ===
  out_of_scope:
    cof: []                           # 저장/주소/인덱스/리졸버
    orchestration: []                 # 트리거 평가 로직
    policy: []                        # 실패 시 행동/HITL 정책
    runtime: []                       # 실제 실행/검증/재시도

  # === Metadata (OPTIONAL) ===
  metadata:
    proposed_by: "cortex-agora"
    proposed_at: "[ISO-8601]"
    category: "[architecture | workflow | validation | state-management | documentation]"
    priority: [:critical | :high | :medium | :low]
    tags: []
```

---

## Proposal Type Assignment

cortex-agora는 **실행 권한이 없으므로**, 제안은 아래 타입으로 제한된다.

### cortex-agora 권한 내 (직접 제안 가능)

| Type | 사용 조건 | Mode | 예시 |
|------|----------|------|------|
| `:rule` | 반복 패턴이 "항상 성립해야 하는 제약"일 때 | `:reference_only` | "tool_call 실패 3회 시 반드시 halt" |
| `:state` | 반복 패턴이 "공유 상태 스키마"를 요구할 때 | `:reference_only` | "retry_count 상태 추적 필요" |
| `:policy` | 반복 패턴이 "HITL/검토 기준"을 제안할 때 | `:reference_only` | "예산 80% 초과 시 인간 승인 권장" |

### cortex-agora 권한 외 (위임 표시 필요)

| Type | 사용 조건 | 위임 표시 |
|------|----------|----------|
| `:method` | 반복 패턴이 "재사용 가능한 실행 단위"일 때 | `delegation.requires_execution: true` |
| `:workflow` | 반복 패턴이 "단계별 오케스트레이션"일 때 | `delegation.requires_execution: true` |

#### 위임 예시

```yaml
proposal:
  instruction:
    type: :method  # cortex-agora 권한 외
    description: "retry-with-backoff 패턴 자동화"
  delegation:
    requires_execution: true
    target_swarm: "Operator_Swarm"  # 실행 권한 보유 Swarm
    escalation_required: true       # Deliberation 승인 필요
```

---

## Type-Field Cardinality

Nucleus 스펙(§2.2)에 따른 Type별 필드 요구사항.

| Field | `:rule` | `:method` | `:workflow` | `:state` | `:policy` |
|-------|---------|-----------|-------------|----------|-----------|
| `:id` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `:version` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `:type` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `:description` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `:execution.mode` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `:execution.action` | ❌ | ✅ | ❌ | ❌ | ❌ |
| `:execution.steps` | ❌ | ❌ | ✅ | ❌ | ❌ |
| `:contract` | ⚠️ | ✅ | ✅ | ✅ | ❌ |
| `:validation` | ✅ | ⚠️ | ⚠️ | ❌ | ✅ |
| `:trigger` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |

**Legend**: ✅ Required | ⚠️ Recommended | ❌ Not allowed

### cortex-agora 권한 내 Type 요약

```
:rule   → validation ✅, contract ⚠️, execution.mode = :reference_only
:state  → contract.schema ✅, validation ❌, execution.mode = :reference_only
:policy → validation.criteria ✅, contract ❌, execution.mode = :reference_only
```

---

## Contract Check

### JSON Schema 사용 규칙

Nucleus는 **JSON Schema**를 contract 언어로 사용한다.

#### :state 타입 (cortex-agora 권한 내)

```yaml
contract:
  schema:
    type: "object"
    properties:
      field_name:
        type: "string"
        description: "[필드 설명]"
    required: ["field_name"]
```

#### :method/:workflow 타입 (위임 시)

```yaml
contract:
  input_schema:
    type: "object"
    properties:
      param_name:
        type: "string"
    required: ["param_name"]
  output_schema:
    type: "object"
    properties:
      result_name:
        type: "string"
    required: ["result_name"]
```

### Contract 필수 여부

| Type | Contract 필수 | 내용 |
|------|--------------|------|
| `:rule` | ⚠️ Recommended | pre/post condition이 참조하는 스키마 |
| `:state` | ✅ Required | `contract.schema` 필수 |
| `:policy` | ❌ Not allowed | 검토 기준만 문서화 |
| `:method` | ✅ Required (위임) | `input_schema`, `output_schema` |
| `:workflow` | ✅ Required (위임) | 전체 흐름의 I/O |

---

## Mode Lock

### Mode 결정 기준

| Type | Mode | 이유 |
|------|------|------|
| `:rule` | `:reference_only` | 제약은 평가되지, 실행되지 않음 |
| `:state` | `:reference_only` | 스키마 선언만 함 |
| `:policy` | `:reference_only` | 검토 기준 문서화만 함 |
| `:method` | `:executable` | cortex-agora가 직접 제안 불가 |
| `:workflow` | `:executable` | cortex-agora가 직접 제안 불가 |

### cortex-agora의 Hard Constraint

```
cortex-agora 제안의 :execution.mode는 반드시 :reference_only여야 한다.
:executable 제안은 delegation 블록에 위임 표시 후 다른 Swarm으로 넘긴다.
```

---

## Boundary Check

### Nucleus 범위 내 (이 스킬로 구조화)

제안이 답하는 질문: **"이 instruction은 무엇을 '의미'하는가?"**

- Type 정의 (5 types)
- Field 스키마
- Semantic constraints
- Validation level (`:hard`, `:soft`, `:policy_signal`)

### Nucleus 범위 외 (분리 필요)

제안에 아래가 포함되면 해당 부분을 별도 섹션으로 분리한다.

| 범위 외 요소 | 담당 레이어 | 분리 위치 |
|-------------|------------|----------|
| 저장/주소/인덱스/리졸버 | COF | `proposal.out_of_scope.cof` |
| COF↔AWT 관계 맥락 맵/적응 리포트 작성 | COWI | `proposal.out_of_scope.cowi` |
| 트리거 평가 로직 | Antigravity (오케스트레이션) | `proposal.out_of_scope.orchestration` |
| 실패 시 행동/HITL 트리거 | Antigravity (정책) | `proposal.out_of_scope.policy` |
| 실제 실행/검증/재시도 | Runtime | `proposal.out_of_scope.runtime` |

#### 분리 예시

```yaml
proposal:
  instruction:
    type: :rule
    description: "tool_call 실패 3회 시 halt"
    validation:
      level: :hard
      pre_conditions:
        - "retry_count >= 3"

  out_of_scope:
    orchestration:
      - "retry_count 상태를 누가 증가시키는가"
      - "halt 후 어떤 agent가 이어받는가"
    policy:
      - "halt 시 인간 알림 여부"
      - "자동 복구 정책"
    runtime:
      - "halt 명령 실제 구현"
```

---

## Escalation Path

### Deliberation Chamber 승격 조건

제안이 다음 중 하나에 해당하면 Deliberation Chamber로 승격한다.

1. **규칙 신설/변경**: 기존 Swarm DNA에 없는 새 규칙 제안
2. **스킬 신설 요청**: 새로운 SKILL.md 생성 필요
3. **기관 DNA 수정**: DNA.md 변경 요구
4. **권한 변경**: permissions 확장/축소 제안
5. **Cross-Swarm 영향**: 다른 Swarm의 행동에 영향

### 승격 형식

```yaml
escalation_request:
  from: "cortex-agora"
  to: "deliberation_chamber"
  type: "proposal_escalation"

  proposal_summary:
    id: "proposal-xxx"
    instruction_type: ":rule"
    description: "[250자 요약]"

  escalation_reason:
    - "[승격 조건 해당 항목]"

  evidence:
    observation: "[관찰 요약]"
    behavior_feed_ref: "[source_path]"
    event_count: n

  requested_action:
    - "Deliberation Packet 작성"
    - "합의 후 Nucleus 정식 등록"
```

---

## Validation Checklist

제안 작성 후 아래를 점검한다.

### Required Fields

- [ ] `proposal.id` 형식: `proposal-[swarm]-[pattern-name]`
- [ ] `proposal.origin.observation` 작성됨
- [ ] `proposal.instruction.type` 5 types 중 하나
- [ ] `proposal.instruction.execution.mode` 설정됨
- [ ] `proposal.instruction.description` 250자 이내

### Type-Specific Checks

| Type | 필수 점검 |
|------|----------|
| `:rule` | `validation.level` 설정됨 |
| `:state` | `contract.schema` 정의됨 |
| `:policy` | `validation.criteria` 목록 있음 |

### Boundary Checks

- [ ] `:executable` 제안은 `delegation` 블록 있음
- [ ] Nucleus 범위 외 요소는 `out_of_scope`에 분리됨
- [ ] 승격 필요 시 `escalation_request` 형식 준수

---

## Canonical Anchors

- Nucleus Spec: `04_Agentic_AI_OS/00_METADoctrine/DNA.md`
- cortex-agora DNA: `04_Agentic_AI_OS/02_Swarm/cortex-agora/DNA.md`
- Deliberation Skill: `04_Agentic_AI_OS/01_Nucleus/deliberation_chamber/skills/deliberation-instruction-nucleus/SKILL.md`
