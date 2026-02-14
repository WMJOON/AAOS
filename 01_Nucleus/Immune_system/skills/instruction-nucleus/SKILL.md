---
name: validating-instruction-nucleus
description: "Immune System에서 instruction의 의미 계약(Nucleus: 5 types/contract/mode/validation)을 작성·검토·정규화한다. Use when instruction을 설계/작성하거나, 기존 instruction의 타입-필드-모드 정합성을 검토할 때."
---

# Inquisitor Instruction Nucleus Skill

이 스킬은 Instruction Nucleus spec을 "의미의 정본"으로 삼아, instruction을 **동일한 타입/필드/의미 체계**로 작성하거나 리뷰할 때 사용한다.

## Quick Start

1) Instruction Nucleus spec을 열고, "Type System / Field Schema / Constraints"를 기준으로 삼는다.
2) 대상 instruction의 타입을 5가지 중 하나로 확정한다.
3) 아래 Workflow를 따라 필드/모드/계약을 정규화한다.

## When to Use

- 새로운 instruction(:rule/:method/:workflow/:state/:policy)을 추가로 설계/작성할 때
- 기존 instruction 스니펫이 타입-필드 불일치, mode 불일치, contract 누락 등으로 흔들릴 때
- "이 내용이 Nucleus 범위인가?" 경계가 애매할 때(저장/정책/실행 침범 여부)

## Inputs

- `instruction` (required): 검토/정규화 대상 instruction 문서 또는 스니펫
- `nucleus_spec` (required): Instruction Nucleus spec 참조 경로

## Outputs

- 정규화된 instruction (아래 Output Template 형식)
- 타입/필드/모드 불일치 목록(있을 경우)
- Nucleus 범위 외 항목 분리 결과

### Output Template (권장 형식)

```clojure
(:instruction {
  :id "..."
  :version "1.0.0"
  :type :method
  :description "..."
  :contract {
    :input_schema {...}
    :output_schema {...}
  }
  :execution {
    :mode :executable
    :action "..."
  }
})
```

## Workflow (Checklist)

```
Instruction Validation Progress:
- [ ] Step 1: 정본 로드 — Instruction Nucleus spec 기준 확인
- [ ] Step 2: 타입 결정 — :rule / :method / :workflow / :state / :policy 중 확정
- [ ] Step 3: Execution Mode 고정 — :rule/:state/:policy → :reference_only, :method/:workflow → :executable
- [ ] Step 4: 필수 필드 채우기 — 공통(:id, :version, :type, :description, :execution.mode) + 타입별
- [ ] Step 5: 금지/부적합 필드 제거 — 타입에 맞지 않는 필드 정리
- [ ] Step 6: Contract(JSON Schema) 정리 — :method/:workflow/:state에 계약 정의
- [ ] Step 7: Trigger/Dependency 정합 — enum/구조만 맞추고 평가 로직 배제
```

### 타입별 필수 필드

- `:method` → `:execution.action`
- `:workflow` → `:execution.steps`(비어있으면 안 됨)
- `:state` → `:contract.schema`
- `:policy` → (권장) `:validation.level :policy_signal` + `:validation.criteria`

### 금지/부적합 필드

- `:rule`에 `:execution.action`/`:execution.steps`가 들어가면 제거
- `:method`에 `:execution.steps`가 들어가면 제거(워크플로우로 승격해야 함)
- `:policy`는 `:contract`를 두지 않는 것을 기본으로 한다

## Constraints

- 이 스킬은 의미론(semantic contract) 점검/작성 보조용이다. 집행/차단은 Inquisitor judgment 스킬이 담당한다.
- Nucleus 범위 밖 항목(저장/정책/실행)은 명시적으로 분리한다.
- `:type` 혼종(하나의 instruction에 복수 타입)은 허용하지 않는다.
- 트리거의 "평가 로직"은 작성하지 않는다 — enum/구조 정합만 담당한다.

## Non-Goals (명시적 범위 밖)

- 주소/저장/검색/리졸버/인덱스(= 외부 저장/해석 레이어)
- 트리거 평가, 실행 계획, 실패 시 행동, HITL 정책(= 오케스트레이션/정책 레이어)
- 실제 실행, 스키마 검증, 상태 영속화(= 런타임)

## References

- Nucleus spec (planning): Instruction Nucleus spec
- META Doctrine: `00_METADoctrine/DNA.md`
