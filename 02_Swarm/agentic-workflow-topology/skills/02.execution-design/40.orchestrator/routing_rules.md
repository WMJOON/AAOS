# Routing Rules — Execution Design

## Intent Patterns

| Pattern | Description | Target Module(s) | Reference Loading |
|---|---|---|---|
| `design_full` | 전체 execution plan 생성 | node-mapping → mode-policy → fallback-handoff | 필요 시 |
| `map_charts` | 노드-chart 할당 설계/수정 | node-mapping | bundle schema |
| `assign_modes` | θ_GT 기반 mode 배정 | mode-policy | CONE_PROFILES |
| `select_models` | 노드별 LLM 모델 선택 | mode-policy | CONE_PROFILES |
| `design_handoff` | 노드 간 데이터 계약 설계 | fallback-handoff | topology edges |
| `design_fallback` | 실패 대응 규칙 설계 | fallback-handoff | TERMINATION_RULES |
| `validate_plan` | 기존 plan 스키마 검증 | (모듈 없음, 스키마 대조) | schema.json |
| `critique_plan` | 기존 plan 비평 | 전체 모듈 기준 대조 | 전체 |

## Routing Precedence Rules

1. **모호한 입력** → `design_full`로 기본 라우팅 (전체 plan 생성).
2. **부분 수정 요청** → 해당 모듈만 실행하되, 의존 모듈 결과가 없으면 오류 보고.
3. **상충 의도** (예: "mode를 바꾸면서 handoff도 다시") → 의존 순서대로 순차 실행.
4. **strategy/high_risk 노드 포함** → mode-policy에서 HITL gate 강제 적용 확인.
5. **검증/비평 요청** → 모듈 실행 없이 스키마 + 규칙 대조만 수행.

## Cross-Module Dependency Enforcement
```
module.node-mapping (독립)
       ↓ node_chart_map
module.mode-policy (node_chart_map 필요)
       ↓ node_mode_policy
module.fallback-handoff (node_chart_map + node_mode_policy 필요)
```
- 상위 모듈 결과 없이 하위 모듈을 실행하면 오류.
- 부분 실행 시 기존 plan에서 상위 결과를 읽어 주입할 수 있다.
