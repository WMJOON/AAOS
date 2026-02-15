# module.fallback-handoff

## Purpose
- 노드 간 데이터 전달 계약(handoff)과 실패 시 대응 규칙(fallback)을 설계한다.
- 산출 키: `handoff_contract`, `fallback_rules`.

## Inputs
| Source | Key | Description |
|---|---|---|
| `workflow_topology_spec` | `edges[]` | 노드 간 연결 (source → target, data_keys) |
| `workflow_topology_spec` | `topology_type` | linear · fan_out · conditional · loop |
| `node_chart_map` | (from module.node-mapping) | 노드별 chart 할당 |
| `node_mode_policy` | (from module.mode-policy) | 노드별 mode 배정 |

## Steps

### Step 1 — Handoff Contract 생성
각 edge에 대해 upstream 노드의 output과 downstream 노드의 input을 매핑한다.

```yaml
handoff_contract:
  edges:
    - source: "N1"
      target: "N2"
      output_keys: ["analysis_result", "confidence_score"]
      input_keys: ["upstream_analysis", "upstream_confidence"]
      format: "json"
      required: true
    - source: "N2"
      target: "N3"
      output_keys: ["recommendation"]
      input_keys: ["input_recommendation"]
      format: "markdown"
      required: true
  validation_rule: "strict"  # strict | permissive
```

**Handoff 설계 규칙**:
1. `output_keys`의 모든 키는 source 노드의 chart가 산출할 수 있어야 한다.
2. `input_keys`의 모든 키는 target 노드의 chart가 소비할 수 있어야 한다.
3. key 이름이 다르면 명시적 매핑을 제공한다.
4. `required: true`인 handoff가 누락되면 파이프라인 중단.

### Step 2 — Topology별 Handoff 패턴

| Topology | Handoff 특성 | 주의사항 |
|---|---|---|
| `linear` | 1:1 순차 전달 | 단순, key 정합성만 검증 |
| `fan_out` | 1:N 분기 전달 | 각 branch에 동일 output 복제 또는 부분 전달 명시 |
| `conditional` | 조건부 경로 | 조건 미충족 branch의 default output 정의 필요 |
| `loop` | 재진입 전달 | 루프 탈출 조건과 max_iterations 필수 명시 |

### Step 3 — Fallback Rules 설계
```yaml
fallback_rules:
  - trigger: "node_timeout"
    action: "retry_once"
    max_retries: 1
    escalation: "skip_with_default_output"
  - trigger: "output_validation_fail"
    action: "retry_with_lower_temperature"
    max_retries: 2
    escalation: "halt_pipeline_and_report"
  - trigger: "hitl_rejection"
    action: "revise_with_feedback"
    max_retries: 1
    escalation: "escalate_to_human"
  - trigger: "chart_mismatch"
    action: "fallback_to_generic_chart"
    max_retries: 0
    escalation: "halt_pipeline_and_report"
```

**Fallback 설계 원칙**:
1. 모든 fallback에 `max_retries`와 `escalation`이 있어야 한다 (무한 루프 방지).
2. `bypassPermissions` mode 노드는 자동 retry만 허용한다 (HITL fallback 불가).
3. `plan` mode 노드는 반드시 `escalate_to_human` 경로를 포함한다.
4. Retry 시 동일 입력으로 재시도하되 temperature를 낮추거나 prompt를 조정한다.

### Step 4 — Termination 연계
- cone-analyzer의 `TERMINATION_RULES.md`에서 정의된 종료 전략을 fallback과 연결한다.

| Regime | Termination 연계 | Fallback 동작 |
|---|---|---|
| Convergent | answer_match_n — 동일 답 n회 반복 시 종료 | retry 후에도 동일 답이면 확정 |
| Verificatory | checklist_pass_rate ≥ threshold | 미달 시 누락 항목 재처리 |
| Deliberative | decision_sufficiency + orthogonality | 새 축 없으면 종료, 있으면 확장 |

## Validation Rules
1. `handoff_contract.edges`는 `workflow_topology_spec.edges`와 1:1 대응해야 한다.
2. 모든 `fallback_rules`에 `escalation`이 명시되어야 한다.
3. `loop` topology에서 `max_iterations`가 없으면 fail-fast.

## When Unsure
- handoff key 매핑이 모호하면 가장 넓은 output을 전달하고 target에서 필터링한다 (permissive).
- fallback 전략이 불확실하면 `halt_pipeline_and_report`를 기본 escalation으로 설정한다.
