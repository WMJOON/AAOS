---
name: workflow-cone-analyzer
description: |
  Convergence Cone 프레임워크 기반 AI 워크플로우 설계 스킬.
  태스크의 θ_GT를 프로파일링하여 노드 분할, mode 배정, 종료 전략을 체계적으로 결정한다.

  v1.0 → v1.1 핵심 변경:
  - Termination을 1급 산출물로 승격 (부록 → Phase 3 주연)
  - Orthogonality를 명시적 종료 트리거로 격상
  - θ_GT regime별 종료 철학 분리 (decision_sufficiency 신설)
  - 비선형 DAG 토폴로지 지원
  - Phase별 구조화된 중간 산출물 형식(JSON) 명시

  트리거 상황:
  - "워크플로우 설계해줘", "파이프라인 구조 잡아줘" 요청 시
  - "이 태스크를 나눠야 할까?", "노드 몇 개로 분할?" 질문 시
  - "workflow.md 만들어줘", "워크플로우 스캐폴딩" 요청 시
  - "cone 분석", "θ_GT 프로파일링" 요청 시
  - "종료 조건 설계", "언제 멈춰야 하나" 질문 시
  - 복잡한 LLM 파이프라인의 구조 최적화가 필요할 때
---
# Workflow Cone Analyzer v1.1

Convergence Cone 프레임워크로 태스크를 분석하고, 최적 분할된 워크플로우와 디렉토리를 생성한다.

**설계 철학**: 이 스킬은 "어떻게 나눌 것인가"와 "왜 여기서 멈춰도 되는가"를 동등하게 다룬다. 종료는 실패가 아니라 설계 결과이며, 판단의 포기가 아니라 판단의 완성이다.

## 실행 프로세스 (6-Phase)

### Phase 1: θ_GT 프로파일링

태스크를 서브태스크로 분해하고, 각각의 θ_GT를 판정한다.

**θ_GT 스펙트럼** (상세: [references/CONE_PROFILES.md](references/CONE_PROFILES.md))

| θ_GT           | 특성             | mode                 | 종료 철학           |
| -------------- | ---------------- | -------------------- | ------------------- |
| 극히 좁음 (L0) | 정답 하나        | `validate`           | 정답 판정           |
| 좁음 (L1)      | 소수 허용 출력   | `converge`           | 정답 판정           |
| 중간 (L2)      | 다수 합리적 출력 | `diverge`→`converge` | 검증 통과           |
| 넓음 (L3)      | 광범위 정답 영역 | `diverge`            | **의사결정 충분성** |
| 정의 불가 (L4) | 정답 cone 없음   | ⚠️ hybrid             | **의사결정 충분성** |

**판정 절차 — 출력 형식:**

```json
{
  "subtasks": [
    {
      "name": "extract_entities",
      "theta_gt": "L1",
      "theta_gt_label": "narrow",
      "rationale": "출력이 3개 이내 후보로 수렴",
      "logical_axes": ["entity_matching", "boundary_detection"]
    }
  ],
  "split_candidates": [
    {"between": ["extract_entities", "reason_causes"], "delta_theta": 0.4, "split": true}
  ]
}
```

**분할 판단 기준:**

- `|Δθ_GT| < 0.1` → 분할 불필요
- `|Δθ_GT| 0.1~0.3` → 분할 검토
- `|Δθ_GT| > 0.3` → 분할 강력 권장

### Phase 2: 노드 분할 + 토폴로지 설계

**Cone Boundary Principle**: θ_GT가 불연속적으로 변하는 지점에서만 분할.
**직교성 원칙**: 새 노드는 기존 노드와 독립적인 판단 축(logical axis)을 추가하지 못하면 생성 금지.

노드 수 가이드:

- **1개**: θ_GT 전 구간 균일, 단순 태스크
- **2~3개**: θ_GT 변화 지점 1~2개. 가장 흔한 최적 구간.
- **4~5개**: 복합 파이프라인. 조율 비용 관리 필요.
- **6+**: 거의 불필요. 조율 비용 > 분할 이득.

**토폴로지 유형** (v1.1 신규):

- `linear`: A→B→C (기본)
- `fan_out`: A→{B,C}→D (병렬 분기 후 합류)
- `conditional`: A→[조건]→B|C (θ_GT에 따른 라우팅)
- `loop`: A→B→[종료판정]→A (diverge 반복)

**출력 형식:**

```json
{
  "nodes": [
    {"id": "n1", "name": "classify", "mode": "converge", "theta_gt": "L1",
     "logical_axes": ["intent_matching"]},
    {"id": "n2", "name": "analyze", "mode": "diverge", "theta_gt": "L3",
     "logical_axes": ["risk_evaluation", "feasibility", "stakeholder_impact"]}
  ],
  "edges": [
    {"from": "n1", "to": "n2", "type": "sequential"},
    {"from": "n2", "to": "n2", "type": "loop", "condition": "termination_check"}
  ],
  "topology": "loop"
}
```

### Phase 3: 종료 전략 설계 ⭐

> **v1.1 핵심 변경**: Termination은 부수 규칙이 아니라, 각 노드의 1급 산출물이다.

종료 전략은 θ_GT regime에 따라 **완전히 다른 철학**을 따른다.

상세: [references/TERMINATION_RULES.md](references/TERMINATION_RULES.md)

| Regime       | θ_GT   | 종료 타입              | 종료의 의미                     |
| ------------ | ------ | ---------------------- | ------------------------------- |
| Convergent   | L0, L1 | `answer_convergence`   | 정답에 수렴함                   |
| Verificatory | L2     | `verification_pass`    | 검증 기준을 통과함              |
| Deliberative | L3, L4 | `decision_sufficiency` | 의사결정에 충분한 근거를 확보함 |

**모든 노드는 반드시 종료 선언(Termination Declaration)을 출력해야 한다:**

```json
{
  "termination_status": "terminate",
  "termination_type": "decision_sufficiency",
  "termination_rationale": {
    "orthogonality_score": 0.12,
    "semantic_expansion_delta": 0.05,
    "decision_sensitivity": "low",
    "axes_explored": ["risk", "feasibility", "cost", "timeline", "stakeholder"],
    "axes_remaining_estimate": 0
  },
  "justification": "5개 독립 축 탐색 완료. 추가 축의 한계직교성 < ε. 의사결정 충분."
}
```

**Deliberative regime (L3, L4) 종료 공식:**

```
Terminate_deliberative(k) =
  D(k) ≥ D_min(θ_GT)                           ← 최소 차원 확보
  AND orthogonality(n_k, {n_1..n_{k-1}}) < ε    ← ⭐ 직교성 0 수렴
  AND (ΔC(k) < δ_cov  OR  Δsem(k) < δ_dec)     ← 커버리지 or 결정 안정성
```

핵심 차이: 직교성 0 수렴이 **핵심 트리거**이지 부수 조건이 아니다.

### Phase 4: Mode 배정 + LLM 설정

각 노드에 mode를 배정하고, 종료 전략과 정합성을 검증한다.

| Mode               | θ_GT Regime        | 종료 타입              | LLM 설정                |
| ------------------ | ------------------ | ---------------------- | ----------------------- |
| `validate`         | Convergent (L0)    | `answer_convergence`   | temp=0, boolean 출력    |
| `converge`         | Convergent (L1)    | `answer_convergence`   | temp 0~0.3, 구조화 출력 |
| `diverge→converge` | Verificatory (L2)  | `verification_pass`    | 탐색 0.5~0.7 → 수렴 0.2 |
| `diverge`          | Deliberative (L3+) | `decision_sufficiency` | temp 0.7~1.0, 자유 출력 |

**`diverge→converge` 구현 가이드** (v1.1 신규):

- 단일 노드 내 2-phase 실행: 동일 프롬프트에서 `## Explore` → `## Synthesize` 섹션 분리
- 또는 Phase 2에서 자동 2-노드 분할 (coordination cost가 낮을 때)
- 판단 기준: 중간 산출물을 다른 노드가 참조하면 2-노드, 아니면 단일 노드

### Phase 5: 비용-품질 시뮬레이션

분할 전후를 비교하여 경제적 정당성을 검증한다.

**토큰 비용 추정:**

```
node_cost = avg_input_tokens × input_price + avg_output_tokens × output_price
total_cost = Σ(node_cost × expected_calls_per_task)

# diverge 노드는 반복 횟수를 고려
diverge_cost = node_cost × avg_iterations_to_terminate
```

**비교표:**

```
| 지표               | 기존(단일) | 분할 후 | 변화 |
| ------------------ | ---------- | ------- | ---- |
| 종합 F1            |            |         |      |
| 평균 토큰/건       |            |         |      |
| 예상 월비용        |            |         |      |
| 종료까지 평균 반복 |            |         |      |
| 조율 오버헤드      | 0          |         |      |
```

**채택 기준:**

```
split_quality / split_cost > baseline_quality / baseline_cost × 1.1
(10% 마진은 조율 비용의 안전장치)
```

스킬 패키징 판단:

- 노드 간 컨텍스트 의존도 낮으면 → 별도 스킬 패키징 (coordination cost → 0)
- 높으면 → 단일 스킬 내 mode 분기

### Phase 6: workflow.md + 디렉토리 스캐폴딩

`scripts/scaffold_workflow.py`를 실행하여 최종 산출물을 생성한다.

```bash
# 선형 체인
python3 scripts/scaffold_workflow.py \
  --name <workflow_name> \
  --nodes "node1:converge:L1,node2:diverge:L3,node3:validate:L0" \
  --output <output_path>

# 비선형 토폴로지 (v1.1)
python3 scripts/scaffold_workflow.py \
  --name <workflow_name> \
  --nodes "classify:converge:L1,analyze:diverge:L3,validate:validate:L0" \
  --edges "classify->analyze,analyze->analyze:loop,analyze->validate" \
  --output <output_path>
```

생성되는 구조:

```
<workflow_name>/
├── workflow.md                 # 전체 워크플로우 정의서
├── nodes/
│   └── node_NN_<name>.md      # 노드별 상세 (mode, θ_GT, 종료 선언 형식)
├── prompts/
│   └── node_NN_<name>.prompt  # 노드별 프롬프트 템플릿
├── termination/                # ⭐ v1.1: 종료 전용 디렉토리
│   ├── strategy.md            # regime별 종료 전략 정의
│   ├── terminate_check.md     # 종료 판정 프롬프트
│   └── perspective_forcing.md # D_min 미달 시 관점 주입 프롬프트
├── validation/
│   └── quality_criteria.md    # 품질 기준 정의
└── analysis/
    ├── cone_profile.md        # θ_GT 프로파일링 결과
    └── cost_simulation.md     # 비용-품질 시뮬레이션
```

## 핵심 규칙

1. **Cone Boundary Principle**: θ_GT가 변하는 지점에서만 분할. 감이 아니라 Δθ로 판단.
2. **직교성 원칙**: 새 노드는 기존 노드와 독립적인 logical axis를 추가하지 못하면 생성 금지.
3. **종료는 설계 결과**: 종료 선언(Termination Declaration)은 모든 노드의 필수 출력이다.
4. **Regime 분리**: θ_GT regime이 다르면 종료 철학이 다르다. 혼용 금지.
5. **D_min 사전조건**: deliberative regime에서는 최소 차원 확보 전 종료 불가.
6. **직교성 0 수렴**: deliberative regime의 핵심 종료 트리거는 새 독립 축의 소진이다.
7. **쿨다운 윈도우**: 종료 조건은 연속 w회 포화 확인 후에만 허용.
8. **스킬 패키징 우선**: coordination cost를 0으로 만들 수 있으면 단일 스킬 내 mode 분기.
