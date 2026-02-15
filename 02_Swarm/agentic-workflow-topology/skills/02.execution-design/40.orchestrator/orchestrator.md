# Orchestrator — Execution Design

## Responsibilities
- 요청 의도를 감지하여 적절한 모듈로 라우팅한다.
- 모듈 실행 순서(node-mapping → mode-policy → fallback-handoff)를 강제한다.
- 참조 로딩을 판단하고, 출력이 스키마 계약을 충족하는지 검증한다.

## Flow

### Phase 1 — Intent Classification
요청을 분석하여 실행 범위를 결정한다.

| Intent Pattern | Scope | Entry Module |
|---|---|---|
| 전체 execution plan 생성 | full | module.node-mapping → 순차 실행 |
| chart 할당만 변경 | partial | module.node-mapping 단독 |
| mode/model 정책 조정 | partial | module.mode-policy 단독 |
| handoff/fallback 수정 | partial | module.fallback-handoff 단독 |
| 기존 plan 검증/비평 | review | 전체 스키마 대조 (모듈 실행 없음) |

### Phase 2 — Prerequisite Check
- `workflow_topology_spec` 존재 확인 → 없으면 01.topology-design 선행 안내.
- `mental_model_bundle` 존재 확인 → 없으면 00.mental-model-design 선행 안내.
- 두 입력 모두 있으면 Phase 3 진행.

### Phase 3 — Module Dispatch
```
full scope:
  1. module.node-mapping   → bundle_ref, node_chart_map, task_to_chart_map
  2. module.mode-policy    → node_mode_policy, model_selection_policy
  3. module.fallback-handoff → handoff_contract, fallback_rules

partial scope:
  - 해당 모듈만 실행
  - 의존 모듈 결과가 없으면 기존 plan에서 읽음
```

### Phase 4 — Reference Loading Decision
| 조건 | 로딩 대상 |
|---|---|
| θ_GT 추정 불확실 | `reference/workflow-cone-analyzer/CONE_PROFILES.md` |
| termination 전략 필요 | `reference/workflow-cone-analyzer/TERMINATION_RULES.md` |
| 스키마 검증 필요 | `references/workflow_mental_model_execution_plan.schema.json` |
| mode override 근거 필요 | `module.mode-policy.md` 내부 Override 규칙 |

### Phase 5 — Contract Output Assembly
1. 7개 required 키가 모두 존재하는지 검증한다.
2. `node_chart_map`의 chart_ids가 bundle에 존재하는지 교차 검증한다.
3. `handoff_contract.edges`가 topology edges와 1:1 대응하는지 확인한다.
4. 모든 검증 통과 시 `workflow_mental_model_execution_plan`을 산출한다.
5. 검증 실패 시 실패 키와 원인을 보고하고 중단한다.
