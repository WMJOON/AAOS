# Module: Loop Risk

**질문 축**: "어떤 루프 위험이 있고 어떻게 방지할 것인가?"

---

## 정상 루프 (허용)

**Convergence Loop**: θ_GT(actual) > θ_GT(expected) 동안 반복은 정상.
max_iterations 설정으로 무한 반복만 방지.

---

## 병리적 루프 5종

### 1. Redundancy Accumulation

- **신호**: Output 길이↑, 새 DQ/claim 추가 없음
- **위험**: high
- **발생**: 합성 노드 (synthesis_centric의 S, fanout_fanin의 fanin)
- **mitigation**: Output 스키마 강화(Trade-off/Boundary 필수), DQ 카운트 체크, 길이 cap

### 2. Semantic Dependency Cycle

- **신호**: T1↔T2 순환 의존
- **위험**: high
- **발생**: 그래프 엣지 설계 오류
- **mitigation**: DAG 검증 → 중간 Synthesis 노드 삽입 또는 합치기

### 3. RSV Inflation

- **신호**: 전 노드 완료 후 RSV 미충족
- **위험**: med-high
- **발생**: Phase 1에서 Goal 과대 설정
- **mitigation**: DQ 재정의(scope-out), Goal 분할(2개 Workflow), Reframe 선언

### 4. Human-Deferral Loop

- **신호**: 판단이 계속 사람에게 미뤄짐
- **위험**: med
- **발생**: human_gate에 판단 기준 부재
- **mitigation**: gate에 판단 기준 명시, auto-approve 조건 설정

### 5. Exploration Spiral

- **신호**: diverge 노드에서 새 관점 추가만 계속, 수렴 불가
- **위험**: med
- **발생**: fanout 구간, hierarchical 상위 노드
- **mitigation**: max_axes 상한(5), 직교성 체크(< ε면 추가 거부), budget 강제 종료

---

## 판단 루브릭

```
{
  판단: "루프 유형 식별 + 위험도 + mitigation 방안",
  근거: "노드 구조와 SE 패턴에서 도출한 신호",
  트레이드오프: "mitigation 강도 vs 유연성 제한",
  확신도: "estimator 데이터 있으면 높음, 설계 시 추정이면 중간"
}
```
