---
name: mental-model-loader
description: Design domain mental models and loading policy based on Semantic Atlas local charts. Produces a `mental_model_bundle` contract for downstream workflow execution design.
---

# Mental Model Loader

도메인에 맞는 멘탈 모델을 정의하고, Local Chart 선택/로딩 규칙을 설계한다.

## Input

- `domain`
- `intent`
- `constraints`
- `required_chart_types`

## Output: `mental_model_bundle`

필수 키:
- `domain`
- `bundle_ref`
- `core_axioms`
- `local_charts`
- `module_index`
- `node_chart_map`
- `execution_checkpoints`
- `loading_policy`
- `output_contract`

스키마: `references/mental_model_bundle.schema.yaml`

## Workflow

1. 도메인 목적을 `judgability` 기준으로 해석한다.
2. 4-Layer 구조(Core/Modules/References/Orchestrator)로 모델을 정렬한다.
3. Local Chart 후보를 정의하고 선택 조건을 명시한다.
4. 노드별 차트 연결(`node_chart_map`)과 checkpoint(`execution_checkpoints`)를 정의한다.
5. 정보 과부하를 피하도록 로딩 정책(when/why/how much)을 고정한다.
6. 표준 산출물(`mental_model_bundle`)로 반환한다.

## Standard Checkpoints

- `preflight`: PF1 응답 직후 `bundle_ref`와 기본 chart load 검증
- `pre_h1`: H1 전 `node_chart_map` 적용 상태 검증
- `pre_h2`: H2 전 최종 chart consistency 검증

## Notes

- 상세 scaffolding 생성은 기존 `scripts/scaffold.py`를 활용할 수 있다.
- 이 스킬은 실행 런너가 아니라 설계 계약을 제공한다.
