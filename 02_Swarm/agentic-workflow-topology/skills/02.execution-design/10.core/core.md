# Core — Execution Design 공통 규칙

## Purpose
- `workflow_topology_spec` + `mental_model_bundle` → `workflow_mental_model_execution_plan` 변환의 공통 용어·형식·실패 처리 원칙을 정의한다.
- 모듈 문서는 고유 판단 축(delta)만 기술하고 Core를 재정의하지 않는다.

## Key Terms
| Term | Definition |
|---|---|
| `node_chart_map` | 토폴로지 노드 → mental model chart 할당 테이블 |
| `bundle_ref` | mental_model_bundle 버전 추적 참조 (id + version + generated_at) |
| `checkpoint` | 실행 중 검증 게이트 (`preflight` · `pre_h1` · `pre_h2`) |
| `mode` | 노드 실행 권한 수준 (plan · default · dontAsk · bypassPermissions) |
| `handoff_contract` | 노드 간 데이터 전달 계약 (output_keys → input_keys) |
| `θ_GT` | cone-analyzer가 산출한 Ground Truth 불확실성 수준 (L0–L4) |

## Input Contract
```yaml
inputs:
  workflow_topology_spec:   # from 01.topology-design
    required: [goal, nodes, edges, topology_type]
  mental_model_bundle:       # from 00.mental-model-design
    required: [domain, charts, execution_checkpoints, output_contract]
```

## Output Contract — Schema Key Ownership
각 모듈이 산출하는 `workflow_mental_model_execution_plan` 키:

| Output Key | Owning Module | Description |
|---|---|---|
| `bundle_ref` | module.node-mapping | bundle 버전 추적 참조 |
| `node_chart_map` | module.node-mapping | 노드 → chart 할당 |
| `task_to_chart_map` | module.node-mapping | 태스크 → chart 역참조 |
| `node_mode_policy` | module.mode-policy | θ_GT 기반 모드 배정 |
| `model_selection_policy` | module.mode-policy | 노드별 LLM 설정 |
| `handoff_contract` | module.fallback-handoff | 노드 간 데이터 계약 |
| `fallback_rules` | module.fallback-handoff | 실패 시 대응 규칙 |

## Output Format (모듈 공통)
모든 모듈의 판단 산출물은 다음 구조를 따른다:
```yaml
decision: <판단 결과>
rationale: <근거 — 어떤 규칙/데이터에서 도출했는가>
tradeoff: <선택하지 않은 대안과 그 이유>
confidence: <high | medium | low>
```

## Global Invariants
1. **증거 없는 단정 금지** — 매핑 근거를 반드시 명시한다.
2. **계약 정합성** — `node_chart_map.chart_ids`의 모든 ID는 `mental_model_bundle.charts`에 존재해야 한다.
3. **checkpoint 일관성** — `node_chart_map.checkpoint_id`는 `preflight | pre_h1 | pre_h2`만 허용한다.
4. **빈 chart 금지** — `chart_ids`는 최소 1개 이상이어야 한다.
5. **fail-fast** — 입력 계약 불일치 시 즉시 중단하고 누락 필드를 보고한다.
6. **하위호환** — optional 확장 필드가 없어도 기본 소비 계약이 깨지지 않아야 한다.

## Cone-Analyzer 연결
- `θ_GT` 값은 `workflow_topology_spec.nodes[].theta_gt`에서 읽는다.
- θ_GT가 없는 노드는 cone-analyzer 참조(`reference/workflow-cone-analyzer/CONE_PROFILES.md`)로 추정한다.
- mode 배정 기본 테이블은 `module.mode-policy.md`에서 정의한다.
