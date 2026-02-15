# module.node-mapping

## Purpose
- topology 노드를 mental model chart에 할당하고, bundle 추적 참조를 생성한다.
- 산출 키: `bundle_ref`, `node_chart_map`, `task_to_chart_map`.

## Inputs
| Source | Key | Description |
|---|---|---|
| `workflow_topology_spec` | `nodes[]` | 토폴로지 노드 목록 (node_id, theta_gt, task_type 등) |
| `mental_model_bundle` | `charts[]` | 사용 가능한 chart 목록 (chart_id, domain, applicable_tasks) |
| `mental_model_bundle` | `execution_checkpoints` | checkpoint stage 정의 |

## Steps

### Step 1 — Bundle Reference 생성
```yaml
bundle_ref:
  id: <mental_model_bundle.id>
  version: <mental_model_bundle.version>
  generated_at: <현재 timestamp>
```
- bundle이 변경되면 execution plan 전체를 재생성해야 한다.

### Step 2 — Node → Chart 할당
각 topology 노드에 대해:

1. **태스크 유형 매칭**: `node.task_type`과 `chart.applicable_tasks`를 대조한다.
2. **도메인 적합성**: `chart.domain`이 노드의 작업 범위와 일치하는지 확인한다.
3. **다중 chart 허용**: 하나의 노드에 여러 chart를 할당할 수 있다 (예: 분석 노드에 정량 chart + 정성 chart).
4. **빈 할당 금지**: `chart_ids`가 빈 배열이면 fail-fast.

```yaml
node_chart_map:
  - node_id: "N1"
    chart_ids: ["chart-quantitative-analysis"]
    checkpoint_id: "preflight"
```

### Step 3 — Checkpoint 할당
| Checkpoint | 할당 기준 |
|---|---|
| `preflight` | 파이프라인 입구 노드 또는 입력 검증 노드 |
| `pre_h1` | strategy/high_risk 노드의 H1 gate 직전 |
| `pre_h2` | 최종 출력 노드의 H2 gate 직전 |

- 하나의 노드는 정확히 하나의 checkpoint에 매핑된다.
- checkpoint가 해당 없는 내부 노드는 가장 가까운 downstream gate의 checkpoint를 상속한다.

### Step 4 — Task-to-Chart 역참조 생성
```yaml
task_to_chart_map:
  - task_type: "data_analysis"
    chart_ids: ["chart-quantitative-analysis", "chart-statistical-inference"]
    node_ids: ["N1", "N3"]
```
- 특정 chart가 어떤 태스크/노드에서 사용되는지 역추적할 수 있게 한다.
- 디버깅·감사(audit)용이며 실행에는 영향 없다.

## Validation Rules
1. `node_chart_map`의 모든 `chart_ids`는 `mental_model_bundle.charts[].chart_id`에 존재해야 한다.
2. `node_chart_map`의 모든 `node_id`는 `workflow_topology_spec.nodes[].node_id`에 존재해야 한다.
3. topology의 모든 노드가 `node_chart_map`에 하나 이상 등장해야 한다 (누락 금지).
4. `checkpoint_id`는 `preflight | pre_h1 | pre_h2`만 허용.

## When Unsure
- chart 후보가 복수이면 θ_GT가 높은 노드에 더 넓은 chart 세트를 할당한다.
- 매칭 불가 시 가장 범용적인 chart를 할당하고 confidence: low를 기록한다.
