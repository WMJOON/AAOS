---
name: workflow-topology-scaffolder
description: Design workflow topology and scaffold specification from Goal→DQ→RSV→theta_GT. Integrates topology design and convergence cone termination strategy into one design contract.
---

# Workflow Topology Scaffolder

Goal을 실행 가능한 topology/task graph/scaffold spec으로 변환한다.

## Input

- `goal`
- `context`
- `quality_budget`
- `cost_budget`

## Output: `workflow_topology_spec`

필수 키:
- `goal`
- `decision_questions`
- `rsv_total`
- `topology_type`
- `nodes`
- `edges`
- `stop_policy`

스키마: `references/workflow_topology_spec.schema.json`

## Design Flow

1. Goal을 DQ 세트로 분해하고 RSV를 산정한다.
2. Semantic Entropy 분포와 theta_GT band를 추정한다.
3. topology type을 선택하고 task graph를 구성한다.
4. cone 기반 termination 전략을 각 노드에 선언한다.
5. scaffold 산출 규격(JSON + optional mermaid)을 정의한다.

## Bundled Assets

- 기존 topology assets: `00_meta/`, `10_core/`, `20_modules/`, `30_references/`, `40_orchestrator/`, `90_tests/`
- cone references/scripts: `50_cone_analyzer/`
