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

**산출물**: 완전한 Workflow Spec JSON

---

## 라우팅 규칙

### Phase별 모듈 선택

```
Phase 1 → (모듈 불필요, Core만으로 처리)
Phase 2 → topology_selection (필수)
Phase 3 → node_design (필수)
Phase 4 → loop_risk (필수) + handoff (조건부)
Phase 5 → (모듈 불필요, 통합만)
```

### handoff 모듈 로딩 조건

```
if task_graph에 다음 중 하나 이상:
  - parallel 노드 존재
  - human_gate 노드 존재
  - 다른 Agent/모델 위임 노드 존재
  - 컨텍스트 윈도우 초과 예상
then:
  load handoff
```

### Reference Pack 로딩 (ΔQ 규칙)

```
ΔQ < 2  → Reference Pack 로딩 금지
ΔQ ≥ 2  → 관련 pack 1개 로딩 고려
ΔQ ≥ 4  → pack 1~2개 로딩

트리거 예:
- "출력 JSON 스키마 전체 보여줘" → pack.output_contract (ΔQ ≥ 2)
- "estimator 사용법 알려줘" → pack.estimator (ΔQ ≥ 2)
- Phase 5 최종 산출 시 → pack.output_contract (ΔQ = 2, 스키마 검증용)
```

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

상세: `30_references/packs/pack.estimator.md`
