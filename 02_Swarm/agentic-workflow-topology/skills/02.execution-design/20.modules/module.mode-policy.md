# module.mode-policy

## Purpose
- θ_GT 수준에 따라 각 노드의 실행 mode와 LLM 설정을 결정한다.
- 산출 키: `node_mode_policy`, `model_selection_policy`.

## Inputs
| Source | Key | Description |
|---|---|---|
| `workflow_topology_spec` | `nodes[].theta_gt` | 노드별 θ_GT 수준 (L0–L4) |
| `workflow_topology_spec` | `nodes[].risk_level` | `low | medium | high_risk | strategy` |
| `node_chart_map` | (from module.node-mapping) | 할당된 chart 정보 |

## θ_GT → Mode 기본 테이블

> 출처: `reference/workflow-cone-analyzer/CONE_PROFILES.md`

| θ_GT | Regime | Default Mode | HITL Gate |
|---|---|---|---|
| L0 (≈0) | Convergent | `bypassPermissions` | 없음 |
| L1 (0.1–0.3) | Convergent | `dontAsk` | 없음 |
| L2 (0.3–0.5) | Verificatory | `default` | 선택적 H1 |
| L3 (0.5–0.8) | Deliberative | `plan` | H1 필수 |
| L4 (0.8–1.0) | Deliberative | `plan` | H1 + H2 필수 |

## Steps

### Step 1 — θ_GT 읽기 및 보정
1. `nodes[].theta_gt`가 명시되어 있으면 그대로 사용한다.
2. 명시되지 않은 경우 `CONE_PROFILES.md`의 Domain Reference Table로 추정한다.
3. `risk_level`이 `high_risk` 또는 `strategy`이면 θ_GT를 최소 L3으로 상향 조정한다.

### Step 2 — Mode 배정
```yaml
node_mode_policy:
  N1:
    mode: "default"
    theta_gt: "L2"
    hitl_gates: ["H1_optional"]
    override_reason: null
  N2:
    mode: "plan"
    theta_gt: "L4"
    hitl_gates: ["H1", "H2"]
    override_reason: "strategy node — H1+H2 강제"
```

**Override 규칙** (기본 테이블보다 우선):
- `risk_level: strategy` → mode는 반드시 `plan`, H1+H2 필수.
- `risk_level: high_risk` → mode는 최소 `plan`, H1 필수.
- 사용자가 명시적으로 mode를 지정한 경우 해당 값을 사용하되, 이유를 `override_reason`에 기록한다.

### Step 3 — Model Selection
```yaml
model_selection_policy:
  default_model: "claude-sonnet-4-5-20250929"
  overrides:
    - node_ids: ["N2", "N5"]
      model: "claude-opus-4-6"
      reason: "strategy/high_risk 노드 — 높은 추론 능력 필요"
    - node_ids: ["N1", "N3"]
      model: "claude-haiku-4-5-20251001"
      reason: "L0-L1 수렴 노드 — 빠른 처리 우선"
```

**Model Selection 원칙**:
| θ_GT Regime | 권장 모델 티어 | 근거 |
|---|---|---|
| Convergent (L0–L1) | haiku/sonnet | 답이 수렴하므로 속도·비용 우선 |
| Verificatory (L2) | sonnet | 검증 필요하나 탐색 범위 제한적 |
| Deliberative (L3–L4) | opus/sonnet | 높은 불확실성에 깊은 추론 필요 |

### Step 4 — Checkpoint-Mode 정합성 검증
- `pre_h1` checkpoint 노드는 반드시 H1 gate가 있어야 한다.
- `pre_h2` checkpoint 노드는 반드시 H2 gate가 있어야 한다.
- mode가 `bypassPermissions`인 노드에 H1/H2 gate가 있으면 모순 → fail-fast.

## When Unsure
- θ_GT 추정이 불확실하면 한 단계 높은 mode를 적용한다 (보수 원칙).
- mode 간 경합 시 risk_level이 높은 쪽을 우선한다.
