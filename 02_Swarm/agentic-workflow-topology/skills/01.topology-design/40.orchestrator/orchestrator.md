# Orchestrator — Workflow Topology Designer

## 5-Phase 프로세스

### Phase 1: Goal → DQ 분해 → RSV_total

1. Goal 문장을 받는다
2. "이 Goal을 달성하려면 어떤 질문들에 답해야 하는가?" → DQ 목록 도출
3. 각 DQ에 weight 부여 → RSV_total = Σ(weight)
4. 제약 조건/컨텍스트 확인

**산출물**: `decision_questions[]` + `rsv.rsv_total`

### Phase 2: Topology 선택

**모듈 로딩**: `topology_selection`

1. Goal 성격 → 기본 후보
2. SE 분포 → 보정
3. RSV 크기 → 병렬성/계층성 보정
4. 최종 선택 + rationale

**산출물**: `workflow_topology.type` + `workflow_topology.rationale`

### Phase 3: Task Graph 설계

**모듈 로딩**: `node_design`

1. Topology에 따라 노드 배치
2. 각 노드에 Explicit Output 정의
3. θ_GT band, rsv_target 설정
4. assigned_dqs 연결
5. 엣지(의존관계) 정의

**산출물**: `task_graph.nodes[]` + `task_graph.edges[]`

### Phase 4: 위험 분석 + Hand-off

**모듈 로딩**: `loop_risk` + (hand-off 포인트 존재 시) `handoff`

1. 그래프 구조에서 루프 위험 식별
2. 각 위험에 mitigation 방안 설정
3. Hand-off 포인트 식별 + 포맷 결정

**산출물**: `loop_risk_assessment[]` + `handoff_strategy`

### Phase 5: Workflow Spec 산출

1. Phase 1~4 결과를 통합하여 Workflow Spec JSON 생성
2. execution_policy 작성 (Continue/Reframe/Stop 규칙)
3. (선택) Mermaid 시각화

**산출물 골격**:

```json
{
  "goal": "...",
  "workflow_topology": {"type": "...", "rationale": ["..."]},
  "decision_questions": [{"id": "DQ1", "question": "...", "weight": 1.5}],
  "rsv": {"rsv_total": 6.5},
  "task_graph": {
    "nodes": [{"node_id": "T1", "explicit_output": {"type": "memo"}, "theta_gt_band": {"min": 0.4, "max": 0.8}, "rsv_target": 1.5, "assigned_dqs": ["DQ1"]}],
    "edges": [{"from": "T1", "to": "T2"}]
  },
  "loop_risk_assessment": [{"loop_type": "...", "risk": "high", "mitigation": ["..."]}],
  "handoff_strategy": {"handoff_points": []},
  "execution_policy": {
    "continue_reframe_stop_rules": [
      "Continue: theta_gt_actual ∈ [band.min, band.max] AND rsv < rsv_target",
      "Reframe: theta_gt_actual < band.min",
      "Stop: redundancy == true OR rsv >= rsv_target"
    ]
  }
}
```

전체 스키마 상세 → `30.references/packs/pack.output_contract.md`
완성 예시 → `90.tests/golden_outputs/examples.md`

---

## 패턴 감지 (라우팅 최상위 키)

| 패턴 | 적용 | 설명 |
|------|------|------|
| **Evaluate** | Phase 2 | Topology 후보 평가 |
| **Critique** | Phase 4 | 루프 위험 비판적 분석 |
| **Translate** | Phase 5 | 설계 → JSON 변환 |
| **Prioritize** | Phase 3 | DQ → 노드 할당 우선순위 |
| **Arbitrate** | Phase 2 | Topology 동점 시 중재 |
| **Simulate** | Phase 4 | 루프 시나리오 시뮬레이션 |

---

## Strategy/High-Risk 게이트 (v2.1+)

strategy 또는 high_risk 워크플로우 감지 시:

1. **PF1 preflight**: 첫 질문을 `멘탈모델 먼저 세팅할까요?`로 고정
2. **필수 노드**: `H1`(HITL finalization), `H2`(HITL review) 포함
3. **필수 엣지**: `T4 → C1 → H1` 경로 보장
4. **H1 finalization 전제**: web evidence + COWI artifacts 검증 필수

검증 스크립트: `scripts/validate_strategy_h1_gate.py`

---

## Runtime Feedback Loop (estimator 연동)

Phase 5 완료 후 실행 환경에서:

```
[설계] θ_GT band, rsv_target 설정
  ↓
[실행] 노드 반복마다 normalized_output 스냅샷 저장
  ↓
[측정] estimator.py --prev iter_N.json --curr iter_N+1.json
  ↓
[판단] Continue / Reframe / Stop
```

상세: `30.references/packs/pack.estimator.md`
