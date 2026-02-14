---
name: structuring-nucleus-instructions
description: "Deliberation 세션에서 Swarm 초기 설계(규칙/메서드/워크플로우/상태/정책)를 Nucleus 의미 계약(5 types/필드/모드/contract)에 맞춰 구조화한다. Use when Swarm 부팅 설계 세션이나 Deliberation Packet 작성/리뷰가 필요할 때."
---

# Deliberation Skill: Instruction Nucleus

Swarm을 처음 시작할 때(구조/규칙/워크플로우를 설계하는 시점) 가장 자주 터지는 문제는:

- "이 문장이 룰인가, 메서드인가, 정책인가?"가 섞여버리는 것
- 실행 가능한 것과 참조 전용이 뒤섞여 contract가 무너지는 것
- 트리거/의존성에 "평가 로직(정책)"이 섞여 Nucleus 범위를 침범하는 것

이 스킬은 Deliberation Packet 안에서 위 문제를 **사전에 구조화**하기 위한 "의미 계약 체크리스트"다.

## Quick Start

1) Instruction Nucleus spec을 기준으로 5 types/필드/제약을 확인한다.
2) Deliberation Packet에 아래 섹션을 추가해서 Swarm 초기 설계를 정규화한다.
3) 집행/검증이 필요하면 Immune 쪽 스킬을 호출한다:
   - Inquisitor Instruction Nucleus 스킬(Immune System)

## When to Use

- Swarm 부팅(초기 구조/규칙/워크플로우) 설계 세션에서 의미 계약을 정리할 때
- Deliberation Packet 작성/리뷰 시 instruction 타입 혼종을 제거할 때

## Inputs

- `deliberation_packet` (required): 구조화 대상 Deliberation Packet 경로
- `nucleus_spec` (required): Instruction Nucleus Spec 참조 경로
- `instruction_candidates` (optional): 사전 정리된 후보 instruction 목록

## Outputs

- Deliberation Packet에 추가되는 구조화 섹션:
  - **Instruction Inventory**: 후보 instruction 한 줄 요약 + `:type` 태그
  - **Type Assignment**: 5 types 확정 결과
  - **Mode Lock**: reference_only vs executable 분류
  - **Contract Check**: JSON Schema 최소 정의
  - **Boundary Check**: Nucleus 범위 외 과제 분리 결과

## Workflow (Checklist)

```
Structuring Progress:
- [ ] Step 1: Instruction Inventory — 후보 instruction 나열 + 임시 :type 태깅
- [ ] Step 2: Type Assignment — :rule / :method / :workflow / :state / :policy 확정
- [ ] Step 3: Mode Lock — :rule/:state/:policy → :reference_only, :method/:workflow → :executable
- [ ] Step 4: Contract Check — :method/:workflow에 input/output schema 정의
- [ ] Step 5: Boundary Check — Nucleus 밖(저장/정책/실행) 항목 분리
```

### Deliberation Packet Add-on (권장 섹션)

#### 1) Instruction Inventory (초기 목록)

- 후보 instruction들을 "한 줄 요약"으로 나열하고, 각 항목에 `:type`을 임시로 붙인다.
- 합의 목표는 "타입 혼종 제거"다.

#### 2) Type Assignment (5 types)

- `:rule` — 항상 성립해야 하는 제약(비실행)
- `:method` — 단일 책임 실행 단위
- `:workflow` — 단계 오케스트레이션(steps 보유)
- `:state` — 공유 상태 스키마(비실행)
- `:policy` — HITL/검토 기준(비실행)

#### 3) Mode Lock (reference_only vs executable)

- `:rule/:state/:policy`는 `:reference_only` 고정
- `:method/:workflow`는 기본 `:executable`

#### 4) Contract Check (JSON Schema)

- `:method`/`:workflow`: input/output schema 최소 정의
- `:state`: schema 정의 필수

#### 5) Boundary Check (Nucleus Litmus)

아래가 필요해지면 Nucleus 밖이다(Deliberation에서 "다른 레이어 과제"로 분리):

- 저장/주소/검색/인덱스/리졸버(= 외부 저장/해석 레이어)
- 트리거 평가 로직/실패 시 행동/HITL 정책(= 오케스트레이션/정책)
- 실제 실행/검증/영속화/재시도(= 런타임)

## Constraints

- Deliberation Chamber는 합의/근거 구조화 기관이며, 집행 권한이 없다.
- 최종 판정/차단/감사는 Immune System(Inquisitor)을 따른다.
- `:type` 혼종(하나의 instruction에 복수 타입)은 허용하지 않는다.
- `:rule`에 `:execution.action`/`:execution.steps`를 넣지 않는다.
- `:method`에 `:execution.steps`를 넣지 않는다(워크플로우로 승격).

## References

- Nucleus spec (planning): Instruction Nucleus spec
- Immune skill (authoring aid): Inquisitor Instruction Nucleus
