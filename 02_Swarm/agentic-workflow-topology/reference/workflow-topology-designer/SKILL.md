---
name: workflow-topology-designer
version: "2.0.0"
description: |
  Goal → Decision Questions → RSV 추정 → Topology 선택 → Task Graph 설계.
  θ_GT × RSV 기반으로 비용/루프/hand-off를 최소화하는 Workflow Topology를 산출한다.
  리포트를 생성하지 않는다. 리포트를 생성할 "그래프 구조 + 노드 명세"를 설계해 반환한다.

  트리거 상황:
  - "Topology 설계해줘", "태스크 그래프 만들어줘" 요청 시
  - "이 작업을 어떤 구조로 나눠야 하나?", "Topology 뭘로 해야 하나?" 질문 시
  - "노드 설계", "RSV 추정", "θ_GT 설정" 관련 요청 시
  - Goal이 주어지고 실행 가능한 Workflow Spec이 필요할 때
  - estimator.py로 Runtime 피드백 루프를 구성할 때

  cone-analyzer와의 차이:
  - 본 스킬 = "그래프 전체 구조" (노드 간 연결, Topology 유형)
  - cone-analyzer = "개별 노드 내부" (서브태스크 분할, 종료 전략)
  - 본 스킬 Phase 3 완료 후 → cone-analyzer로 노드 내부 상세 위임 가능
---

# Workflow Topology Designer v2.0

> **이 스킬은 리포트를 생성하지 않는다.**
> 리포트를 생성할 **"그래프 구조(Topology) + 노드 명세"**를 설계해 반환한다.

---

## 핵심 정의

| 개념 | 정의 |
|------|------|
| **Task Node 경계** | 외부에서 관측 가능한 **Explicit Output**으로 정의. 내부 추론/토큰은 경계 기준이 아님 |
| **θ_GT** | Node의 Explicit Output이 허용하는 의미적 분산도의 기대 범위 |
| **RSV** | Goal 달성에 필요한 의미 기여 총량 = Σ(DQ_weight) |
| **DQ** | Decision Question. RSV의 기본 단위. 닫히면 Goal에 의미 기여 완료 |

---

## 5-Phase 실행 프로세스

### Phase 1: Goal → DQ 분해 → RSV_total

1. Goal 문장을 받는다
2. "이 Goal을 달성하려면 어떤 질문들에 답해야 하는가?" → DQ 목록 도출
3. 각 DQ에 weight 부여 → **RSV_total = Σ(weight)**
4. 제약 조건/컨텍스트 확인

**when_unsure**: Goal이 모호하여 DQ 분해 불가 → "Goal을 구체화해 주세요" + 예시 DQ 제안

**산출물**:
```json
{
  "decision_questions": [
    {"id": "DQ1", "question": "...", "weight": 1.5}
  ],
  "rsv": {"rsv_total": 6.5, "estimation_method": "decision_questions_weighted_sum"}
}
```

---

### Phase 2: Topology 선택 (3-Signal 규칙)

**8가지 Topology 유형:**

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

**Signal 1 — Goal 성격 → 기본 후보:**
- 사실확인/규정준수/정답좁음 → `linear` / `state_transition`
- 조건 판단/케이스 분기 → `branching`
- 다각도 조사 → `parallel`
- 의도적 발산 후 결론 합성 → `fanout_fanin`
- 상위→하위 재귀 분해 → `hierarchical`
- 대부분의 의미가 최종 합성에서 결정 → `synthesis_centric`

**Signal 2 — SE(Semantic Entropy) 분포 → 보정:**
- 고SE 초반 집중 → `fanout_fanin` / `hierarchical`
- 고SE 합류 집중 → `synthesis_centric`
- 중간 분기 증가 → `branching`

**Signal 3 — RSV 크기 → 병렬성/계층성 보정:**
- RSV_total 작음 → `linear`로 충분
- RSV_total 중간 → `parallel` + 1회 synthesis
- RSV_total 큼 → `hierarchical` + 다단 synthesis

**when_unsure**: 후보 2개 이상 동점 → 두 후보의 트레이드오프를 제시하고 사용자 선택 요청

**산출물**: `workflow_topology: {type, rationale[]}`

---

### Phase 3: Task Graph 설계

**노드 분리 3-규칙:**

| 규칙 | 판단 테스트 |
|------|-----------|
| **Explicit Output 단위로 분리** | Output을 외부에서 독립 검증 가능? Yes → 노드 정당 |
| **합치기 판단** | 두 Output이 항상 함께 생성? Yes → 합치기 |
| **분리 유지** | Output이 다른 노드의 Input으로 명확히 사용? Yes → 분리 유지 |

**θ_GT band 설정:**

| SE 예상 | θ_GT band | 비고 |
|---------|-----------|------|
| 해석 자유도 큼 | 넓게 (0.4~0.9) | 합리적 다양성 허용 |
| 기준 명확 | 좁게 (0.0~0.2) | 수렴 보장 |
| 중복 증산 위험 | band 넓히지 말고 **Output 스키마 강화** | 구조로 통제 |

**Explicit Output 타입:**

| type | 용도 | θ_GT 경향 |
|------|------|----------|
| `memo` | 의사결정 배경 문서 | 중~넓음 |
| `table` | 구조화된 비교/정리 | 좁음~중간 |
| `checklist` | 항목별 확인 목록 | 좁음 |
| `spec` | 기술/요구사항 명세 | 좁음~중간 |
| `risk_register` | 위험+영향/확률/대응 | 중간 |
| `policy` | 정책/규칙 정의 | 중간~넓음 |
| `decision` | 최종 판단+근거 | 넓음 |
| `summary` | 요약 (hand-off 시에만) | 중간 |
| `state` | 상태 객체 | 좁음 |

**RSV 분배:**
- 각 노드는 "어떤 DQ를 닫는가" 명시 (`assigned_dqs`)
- **Σ(rsv_target) ≈ RSV_total (±10% 허용)**
- 합성 노드는 DQ 간 관계 정리 역할로 RSV 기여

**when_unsure**: θ_GT 추정이 불확실 → band를 넓게 설정 + "첫 반복 후 estimator로 보정 권장"

**산출물**: `task_graph: {nodes[], edges[]}`

---

### Phase 4: 위험 분석 + Hand-off

**병리적 루프 5종:**

| 유형 | 신호 | 위험 | 주발생지 | mitigation |
|------|------|------|---------|-----------|
| **Redundancy Accumulation** | Output 길이↑, 새 DQ 없음 | high | 합성 노드 | Output 스키마 강화, DQ 카운트 체크, 길이 cap |
| **Semantic Dependency Cycle** | T1↔T2 순환 의존 | high | 엣지 설계 오류 | DAG 검증 → 중간 Synthesis 삽입 또는 합치기 |
| **RSV Inflation** | 전 노드 완료 후 RSV 미충족 | med-high | Goal 과대 설정 | DQ 재정의, Goal 분할, Reframe 선언 |
| **Human-Deferral Loop** | 판단이 계속 사람에게 미뤄짐 | med | human_gate 판단기준 부재 | gate에 판단 기준 명시, auto-approve 조건 |
| **Exploration Spiral** | diverge 노드에서 수렴 불가 | med | fanout, hierarchical 상위 | max_axes 상한(5), 직교성 체크, budget 강제 종료 |

**Hand-off 원칙:**
- "중간 서브리포트 생성"을 기본값으로 두지 않는다
- 넘기는 것은 "요약"이 아니라 **"결정 가능한 구조"**

**허용 포맷**: Decision Memo, Risk Register, Constraint List, State Object, DQ Status
**금지 포맷**: 산문형 요약, "참고용" 리포트, 전체 로그 덤프

**Hand-off 로딩 조건**: parallel 노드, human_gate, agent 위임, 컨텍스트 초과 중 하나 이상 존재 시
→ 상세: `20_modules/module.handoff.md`

**산출물**: `loop_risk_assessment[]` + `handoff_strategy`

---

### Phase 5: Workflow Spec 산출

Phase 1~4 결과를 통합하여 **Workflow Spec JSON** 생성:

```json
{
  "workflow_topology": {"type": "...", "rationale": ["..."]},
  "decision_questions": [{"id": "DQ1", "question": "...", "weight": 1.5}],
  "rsv": {"rsv_total": 6.5},
  "task_graph": {
    "nodes": [{
      "node_id": "T1",
      "name": "노드 이름",
      "explicit_output": {"type": "memo", "required_sections": [], "acceptance_criteria": []},
      "inputs": [], "dependencies": [],
      "semantic_entropy_expected": 0.7,
      "theta_gt_band": {"min": 0.4, "max": 0.8},
      "rsv_target": 1.5,
      "assigned_dqs": ["DQ1"],
      "stop_condition": "..."
    }],
    "edges": [{"from": "T1", "to": "T2", "condition": "optional"}]
  },
  "loop_risk_assessment": [{"loop_type": "...", "where": "T5", "risk": "high", "mitigation": ["..."]}],
  "handoff_strategy": {"handoff_points": [], "minimize_context_loss_rules": []},
  "execution_policy": {
    "continue_reframe_stop_rules": [
      "Continue: theta_gt_actual ∈ [band.min, band.max] AND rsv < rsv_target",
      "Reframe: theta_gt_actual < band.min (과도 수렴)",
      "Stop: redundancy == true OR rsv >= rsv_target"
    ]
  }
}
```

**(선택) Mermaid 시각화** — 사용자가 요청하거나 composite Topology일 때 생성 권장.

**전체 JSON 스키마 상세** → `30_references/packs/pack.output_contract.md`

---

## 상세 파일 참조 가이드 (필요 시에만 로딩)

대부분의 설계 작업은 위 5-Phase만으로 완료 가능하다.
아래 파일은 **깊은 분석이 필요할 때만** 참조한다.

| 상황 | 파일 | 언제 |
|------|------|------|
| Topology 유형별 장단점 상세 비교 | `20_modules/module.topology_selection.md` | 후보 2개 이상 동점 시 |
| 노드 분리/Output 스키마 강화 상세 | `20_modules/module.node_design.md` | 중복 증산 위험 노드 설계 시 |
| 루프 위험 시뮬레이션 | `20_modules/module.loop_risk.md` | 위험 분석 세밀 작업 시 |
| Hand-off 포맷/최소화 패턴 상세 | `20_modules/module.handoff.md` | 복잡한 hand-off 설계 시 |
| 출력 JSON 전체 스키마 | `30_references/packs/pack.output_contract.md` | Phase 5 스키마 검증 시 |
| Runtime estimator 연동 | `30_references/packs/pack.estimator.md` | estimator.py 사용법 필요 시 |

---

## Runtime Feedback Loop (estimator 연동)

Phase 5 완료 후 실행 환경에서:

```
[설계] θ_GT band, rsv_target 설정
  → [실행] 노드 반복마다 normalized_output 스냅샷 저장
  → [측정] scripts/estimator.py --prev iter_N.json --curr iter_N+1.json
  → [판단] Continue / Reframe / Stop
```

estimator 사용법 상세 → `30_references/packs/pack.estimator.md`

---

## Quick Example

**Input**: "새로운 금융 규제 시행에 따른 자사 대응 전략 수립"

**Phase 1** → DQ 6개 (법적 제약, 운영 영향, 고객 리스크, 경쟁 현황, 전략, 타임라인), RSV_total = 6.5
**Phase 2** → Signal 1: 다각도 조사 → `parallel`. Signal 2: 합성 SE 높음 → `+synthesis_centric`. → **composite**
**Phase 3** → {T1법제약, T2운영, T3고객, T4경쟁} → T5합성 Decision Memo
**Phase 4** → T5에 redundancy_accumulation (high) → Output 스키마 강화
**Phase 5** → Workflow Spec JSON + Mermaid

추가 예시 → `90_tests/golden_outputs/examples.md`

---

## 관련 스킬

| 스킬 | 관계 |
|------|------|
| `workflow-cone-analyzer` | Phase 3 완료 후 → 개별 노드 내부 θ_GT 프로파일링 + 종료 전략 위임 |
| `skillpack-factory` | 이 4-Layer 구조의 패키징 원본 |
