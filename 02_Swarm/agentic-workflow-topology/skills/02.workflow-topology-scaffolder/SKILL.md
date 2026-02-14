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
- `preflight`
- `workflow_profile`
- `decision_questions`
- `rsv_total`
- `topology_type`
- `nodes`
- `edges`
- `stop_policy`
- `strategy_gate`

스키마: `references/workflow_topology_spec.schema.json`

## Mandatory Preflight

워크플로우 생성 전에 아래 질문을 첫 질문으로 고정한다.

- `PF1`: `멘탈모델 먼저 세팅할까요?`

`preflight.questions[0]`는 반드시 PF1이어야 하며, 전략/고위험 분류 시 생략할 수 없다.

## Strategy/High-Risk Gate Rule

`workflow_profile.class`가 `strategy` 또는 `high_risk`로 분류되면 다음을 강제한다.

- Mermaid/Task graph에 `H1`, `H2` 노드 포함
- 필수 엣지: `T4 -> C1 -> H1`
- H1 finalization 전 `web evidence + COWI artifacts` 존재 검증

H1 gate 검증 스크립트:

```bash
python3 02_Swarm/agentic-workflow-topology/skills/02.workflow-topology-scaffolder/scripts/validate_strategy_h1_gate.py \
  --workflow-spec /path/to/workflow_topology_spec.json \
  --agent-family claude \
  --agent-version 4.0 \
  --proposal-id P-SWARM-XXXX \
  --evidence-date 2026-02-14
```

## Design Flow

1. PF1 preflight를 수행하고 멘탈모델 선설정 여부를 확정한다.
2. Goal을 DQ 세트로 분해하고 RSV를 산정한다.
3. Semantic Entropy 분포와 theta_GT band를 추정한다.
4. topology type을 선택하고 task graph를 구성한다.
5. 전략/고위험이면 HITL/H1 gate를 task graph에 삽입한다.
6. cone 기반 termination 전략을 각 노드에 선언한다.
7. scaffold 산출 규격(JSON + optional mermaid)을 정의한다.

## Bundled Assets

- 기존 topology assets: `00_meta/`, `10_core/`, `20_modules/`, `30_references/`, `40_orchestrator/`, `90_tests/`
- cone references/scripts: `50_cone_analyzer/`
