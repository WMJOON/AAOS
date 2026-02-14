---
name: workflow-mental-model-execution-designer
description: Design how each workflow task node should apply mental models/charts at execution time. Produces `workflow_mental_model_execution_plan` from topology and mental model bundle.
---

# Workflow Mental Model Execution Designer

`02.workflow-topology-scaffolder` 산출물의 각 노드에 `01.mental-model-loader`의 멘탈모델/차트를 어떻게 적용할지 설계한다.

## Inputs

- `workflow_topology_spec`
- `mental_model_bundle`

## Output: `workflow_mental_model_execution_plan`

필수 키:
- `task_to_chart_map`
- `node_mode_policy`
- `model_selection_policy`
- `handoff_contract`
- `fallback_rules`

스키마: `references/workflow_mental_model_execution_plan.schema.json`

## Method

1. 노드별 판단 목적과 필요한 chart를 매핑한다.
2. node mode(`converge`, `diverge`, `validate`)를 실행 정책으로 연결한다.
3. handoff 시 필요한 최소 구조를 정의한다.
4. 과설명/과압축 리스크를 fallback 규칙으로 명시한다.

## Scope Boundary

- 실행 런너/자동 디스패치 구현은 포함하지 않는다.
- 설계 계약과 실행 방법론 문서화에 집중한다.
