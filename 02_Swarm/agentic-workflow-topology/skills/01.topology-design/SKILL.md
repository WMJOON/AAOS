---
name: awt-topology-design
description: Design workflow topology and scaffold specification from Goal→DQ→RSV→theta_GT. Enforces PF1 preflight and strategy/high-risk HITL gates (H1/H2, T4->C1->H1, H1 artifact checks).
---

# Workflow Topology Scaffolder v2.1

> 이 스킬은 리포트를 생성하지 않는다.
> 리포트를 생성할 "그래프 구조(Topology) + 노드 명세"를 설계해 반환한다.

Goal을 실행 가능한 `workflow_topology_spec`으로 변환한다.

## 책임 경계

- 포함: Goal→DQ→RSV→Topology→Task Graph 설계, 종료 정책 설계, 전략/고위험 H1 gate 설계
- 제외: 실제 티켓 실행/자동 디스패치/자동 반영
- PF1 preflight는 항상 강제된다.

## 입력

- `goal`
- `context`
- `quality_budget`
- `cost_budget`
- `constraints` (optional)
- `workflow_profile` (optional, 미지정 시 유추)

## 출력 계약: `workflow_topology_spec`

권장(canonical) 키:
- `goal`
- `preflight`
- `workflow_profile`
- `decision_questions`
- `workflow_topology`
- `rsv`
- `task_graph`
- `stop_policy`
- `execution_policy` (legacy alias 허용)
- `strategy_gate`

레거시(flat) 호환 키:
- `topology_type`
- `rsv_total`
- `nodes`
- `edges`

스키마: `references/workflow_topology_spec.schema.json`

## 핵심 정의

| 개념 | 정의 |
|------|------|
| **Task Node 경계** | 외부에서 관측 가능한 **Explicit Output**으로 정의. 내부 추론/토큰은 경계 기준이 아님 |
| **θ_GT** | Node의 Explicit Output이 허용하는 의미적 분산도의 기대 범위 |
| **RSV** | Goal 달성에 필요한 의미 기여 총량 = Σ(DQ_weight) |
| **DQ** | Decision Question. RSV의 기본 단위. 닫히면 Goal에 의미 기여 완료 |

## Non-Negotiable Invariants

- `preflight.questions[0]`는 반드시 PF1
- PF1 질문 텍스트는 반드시 `멘탈모델 먼저 세팅할까요?`
- `workflow_profile.class in {strategy, high_risk}` 또는 동등 조건이면:
  - `strategy_gate.enabled = true`
  - `H1`, `H2` 노드 필수
  - 필수 엣지 `T4 -> C1 -> H1`
  - H1 finalization 전 `web evidence + COWI artifacts` 검증
- `Σ(node.rsv_target) ≈ rsv.rsv_total` (±10% 권장)

## 6-Phase 실행 프로세스

### Phase 0: Mandatory Preflight

1. `preflight.questions[0]`를 PF1로 고정한다.
2. 고정 질문: `멘탈모델 먼저 세팅할까요?`
3. PF1 응답이 yes면 `00.mental-model-design` 산출물(`mental_model_bundle`) 선행을 권장한다.

산출물: `preflight.questions[]` + `workflow_profile`

### Phase 1: Goal → DQ 분해 → RSV_total

1. Goal 문장을 받는다.
2. "이 Goal을 달성하려면 어떤 질문들에 답해야 하는가?"로 DQ 목록을 도출한다.
3. 각 DQ에 weight를 부여하고 `rsv.rsv_total = Σ(weight)`로 계산한다.
4. 제약 조건/컨텍스트를 확인한다.

when_unsure:
- Goal이 모호하여 DQ 분해 불가면 Goal 구체화 질문 1~2개 + 임시 DQ 예시를 제시한다.

산출물 예시:
```json
{
  "decision_questions": [
    {"id": "DQ1", "question": "...", "weight": 1.5}
  ],
  "rsv": {
    "rsv_total": 6.5,
    "estimation_method": "decision_questions_weighted_sum"
  }
}
```

### Phase 2: Topology 선택 (3-Signal 규칙)

8가지 Topology 유형:

| type | 구조 | 적합 상황 |
|------|------|----------|
| `linear` | A→B→C | 사실확인, 정답좁음, RSV 작음 |
| `branching` | A→[조건]→B\|C | 조건분기 많음 |
| `parallel` | {A,B,C}→D | 다각도 독립 조사 |
| `fanout_fanin` | A→{B1,B2,B3}→C | 의도적 발산→합성 |
| `hierarchical` | Goal→Sub-Goals→Tasks→Synthesis | 재귀 분해, RSV 큼 |
| `synthesis_centric` | {T1,T2}→S1→{T3}→S2 | 합성이 핵심 가치 |
| `state_transition` | S0→[이벤트]→S1→S2 | 상태 기반 프로세스 |
| `composite` | 혼합 | 복합 목표 |

Signal 1 — Goal 성격:
- 사실확인/규정준수/정답좁음 → `linear` / `state_transition`
- 조건 판단/케이스 분기 → `branching`
- 다각도 조사 → `parallel`
- 의도적 발산 후 결론 합성 → `fanout_fanin`
- 상위→하위 재귀 분해 → `hierarchical`
- 대부분의 의미가 최종 합성에서 결정 → `synthesis_centric`

Signal 2 — SE(Semantic Entropy) 분포:
- 고SE 초반 집중 → `fanout_fanin` / `hierarchical`
- 고SE 합류 집중 → `synthesis_centric`
- 중간 분기 증가 → `branching`

Signal 3 — RSV 크기:
- RSV_total 작음 → `linear`
- RSV_total 중간 → `parallel` + 1회 synthesis
- RSV_total 큼 → `hierarchical` + 다단 synthesis

when_unsure:
- 후보 2개 이상 동점이면 트레이드오프를 제시하고 사용자 선택을 요청한다.

산출물: `workflow_topology: {type, rationale[]}`

### Phase 3: Task Graph 설계

노드 분리 3-규칙:

| 규칙 | 판단 테스트 |
|------|-----------|
| **Explicit Output 단위로 분리** | Output을 외부에서 독립 검증 가능? Yes → 노드 정당 |
| **합치기 판단** | 두 Output이 항상 함께 생성? Yes → 합치기 |
| **분리 유지** | Output이 다른 노드의 Input으로 명확히 사용? Yes → 분리 유지 |

θ_GT band 설정:

| SE 예상 | θ_GT band | 비고 |
|---------|-----------|------|
| 해석 자유도 큼 | 넓게 (0.4~0.9) | 합리적 다양성 허용 |
| 기준 명확 | 좁게 (0.0~0.2) | 수렴 보장 |
| 중복 증산 위험 | band를 넓히지 말고 Output 스키마 강화 | 구조로 통제 |

Explicit Output 타입:

| type | 용도 | θ_GT 경향 |
|------|------|----------|
| `memo` | 의사결정 배경 문서 | 중~넓음 |
| `table` | 구조화된 비교/정리 | 좁음~중간 |
| `checklist` | 항목별 확인 목록 | 좁음 |
| `spec` | 기술/요구사항 명세 | 좁음~중간 |
| `risk_register` | 위험+영향/확률/대응 | 중간 |
| `policy` | 정책/규칙 정의 | 중간~넓음 |
| `decision` | 최종 판단+근거 | 넓음 |
| `summary` | 요약 (handoff 시에만) | 중간 |
| `state` | 상태 객체 | 좁음 |

RSV 분배:
- 각 노드는 "어떤 DQ를 닫는가"(`assigned_dqs`)를 명시한다.
- `Σ(rsv_target) ≈ RSV_total (±10%)`를 유지한다.
- 합성 노드는 DQ 간 관계 정리 역할로 RSV에 기여한다.

전략/고위험 강제 규칙:
- `H1`, `H2` 노드 삽입
- `T4 -> C1 -> H1` 엣지 삽입

산출물: `task_graph: {nodes[], edges[]}`

### Phase 4: 위험 분석 + Hand-off

병리적 루프 5종:

| 유형 | 신호 | 위험 | 주발생지 | mitigation |
|------|------|------|---------|-----------|
| **Redundancy Accumulation** | Output 길이↑, 새 DQ 없음 | high | 합성 노드 | Output 스키마 강화, DQ 카운트 체크, 길이 cap |
| **Semantic Dependency Cycle** | T1↔T2 순환 의존 | high | 엣지 설계 오류 | DAG 검증 후 중간 synthesis 삽입 또는 노드 합치기 |
| **RSV Inflation** | 전 노드 완료 후 RSV 미충족 | med-high | Goal 과대 설정 | DQ 재정의, Goal 분할, Reframe 선언 |
| **Human-Deferral Loop** | 판단이 계속 사람에게 미뤄짐 | med | human gate 기준 부재 | gate 판단 기준 명시, auto-approve 조건 정의 |
| **Exploration Spiral** | diverge 노드에서 수렴 불가 | med | fanout/hierarchical 상위 | max_axes 상한, 직교성 체크, budget 강제 종료 |

Hand-off 원칙:
- "중간 서브리포트 생성"을 기본값으로 두지 않는다.
- 넘기는 것은 "요약"이 아니라 **결정 가능한 구조**다.

허용 포맷: Decision Memo, Risk Register, Constraint List, State Object, DQ Status
금지 포맷: 산문형 요약, 참고용 리포트, 전체 로그 덤프

산출물: `loop_risk_assessment[]` + `handoff_strategy`

### Phase 5: H1 Finalization Gate (strategy/high_risk only)

아래 3가지가 모두 충족되어야 H1 finalization 가능:
1. `web_evidence_YYYY-MM-DD.md` 존재
2. COWI artifacts 존재:
   - `relation_context_map`
   - `skill_usage_adaptation_report`
3. validator PASS

검증 명령:

```bash
python3 02_Swarm/agentic-workflow-topology/skills/01.topology-design/scripts/validate_strategy_h1_gate.py \
  --workflow-spec /path/to/workflow_topology_spec.json \
  --agent-family claude \
  --agent-version 4.0 \
  --proposal-id P-SWARM-XXXX \
  --evidence-date 2026-02-14
```

### Phase 6: Workflow Spec 통합 산출

Phase 0~5 결과를 통합해 최종 JSON을 만든다.

```json
{
  "goal": "...",
  "preflight": {"questions": [{"id": "PF1", "question": "멘탈모델 먼저 세팅할까요?", "required": true}]},
  "workflow_profile": {"class": "general", "risk_tolerance": "medium", "is_strategy_or_high_risk": false},
  "workflow_topology": {"type": "parallel", "rationale": ["..."]},
  "decision_questions": [{"id": "DQ1", "question": "...", "weight": 1.5}],
  "rsv": {"rsv_total": 6.5},
  "task_graph": {
    "nodes": [
      {
        "node_id": "T1",
        "name": "노드 이름",
        "explicit_output": {"type": "memo", "required_sections": [], "acceptance_criteria": []},
        "theta_gt_band": {"min": 0.4, "max": 0.8},
        "rsv_target": 1.5,
        "assigned_dqs": ["DQ1"]
      }
    ],
    "edges": [{"from": "T1", "to": "T2", "condition": "optional"}]
  },
  "stop_policy": {
    "continue_reframe_stop_rules": [
      "Continue: theta_gt_actual ∈ band and rsv < rsv_target",
      "Reframe: theta_gt_actual < band.min",
      "Stop: redundancy true or rsv target reached"
    ]
  },
  "strategy_gate": {"enabled": false}
}
```

## 상세 참조 로딩 가이드 (필요 시)

기본 로딩 순서:
1. `10.core/core.md`
2. `40.orchestrator/orchestrator.md`
3. phase별 모듈
   - Phase 2: `20.modules/module.topology_selection.md`
   - Phase 3: `20.modules/module.node_design.md`
   - Phase 4: `20.modules/module.loop_risk.md`, 필요 시 `20.modules/module.handoff.md`
4. ΔQ >= 2일 때만 reference pack
   - 출력 계약/스키마: `30.references/packs/pack.output_contract.md`
   - runtime estimator: `30.references/packs/pack.estimator.md`

## Runtime Feedback Loop (estimator 연동)

```
[설계] θ_GT band, rsv_target 설정
  → [실행] 노드 반복마다 normalized_output 스냅샷 저장
  → [측정] scripts/estimator.py --prev iter_N.json --curr iter_N+1.json
  → [판단] Continue / Reframe / Stop
```

상세: `30.references/packs/pack.estimator.md`

## Quick Example

Input: "새로운 금융 규제 시행에 따른 자사 대응 전략 수립"

- Phase 1: DQ 6개, RSV_total = 6.5
- Phase 2: `parallel + synthesis_centric` → `composite`
- Phase 3: `{T1,T2,T3,T4} -> C1 -> H1 -> H2 -> T5`
- Phase 4: T5 redundancy 위험 high → Output 스키마 강화
- Phase 5: `web_evidence + COWI artifacts + validator PASS`
- Phase 6: `workflow_topology_spec` JSON + (선택) mermaid

추가 예시: `90.tests/golden_outputs/examples.md`

## 관련 스킬

- `00.mental-model-design`: PF1에서 yes일 때 선행 번들 설계
- `02.execution-design`: topology 산출물의 노드별 모델 적용 설계
- `workflow-cone-analyzer` (`reference/workflow-cone-analyzer`): 개별 노드 내부 종료 전략 설계
