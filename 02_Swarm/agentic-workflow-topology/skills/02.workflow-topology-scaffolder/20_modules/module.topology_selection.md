# Module: Topology Selection

**질문 축**: "어떤 Topology 구조를 선택할 것인가?"

---

## 8가지 Topology 유형

| type | 구조 | 적합 상황 | θ_GT 패턴 |
|------|------|----------|----------|
| linear | A→B→C | 사실확인, 정답좁음, RSV 작음 | 전 구간 좁음 |
| branching | A→[조건]→B\|C | 조건분기 많음 | 분기점에서 SE 갈라짐 |
| parallel | {A,B,C}→D | 다각도 독립 조사 | 각 노드 θ_GT 독립 |
| fanout_fanin | A→{B1,B2,B3}→C | 의도적 발산→합성 | fanout θ_GT 넓음→수렴 |
| hierarchical | Goal→Sub-Goals→Tasks→Synthesis | 재귀 분해, RSV 큼 | 상위 넓음→하위 좁음 |
| synthesis_centric | {T1,T2}→S1→{T3}→S2 | 합성이 핵심 가치 | 수집 좁음, 합성 넓음 |
| state_transition | S0→[이벤트]→S1→S2 | 상태 기반 프로세스 | 전이마다 변동 |
| composite | 혼합 | 복합 목표 | 구간별 상이 |

---

## 3-Signal 선택 규칙

### Signal 1: Goal 성격 → 기본 후보

- 사실확인/규정준수/정답좁음 → `linear` / `state_transition`
- 조건 판단/케이스 분기 → `branching`
- 다각도 조사 (법/시장/기술/운영) → `parallel`
- 의도적 발산 후 결론 합성 → `fanout_fanin`
- 상위→하위 재귀 분해 → `hierarchical`
- 대부분의 의미가 최종 합성에서 결정 → `synthesis_centric`
- 복합 목표/혼재 → `composite`

### Signal 2: SE 분포 → 보정

- 고SE 초반 집중 → `fanout_fanin` 또는 `hierarchical`(상위 탐색 분리)
- 고SE 합류 집중 → `synthesis_centric`
- 중간 분기 증가 → `branching`(분기 기준 Explicit Output 필수)

### Signal 3: RSV 크기 → 병렬성/계층성 보정

- RSV_total 작음 → `linear`로 충분
- RSV_total 중간 → `parallel` + 1회 synthesis
- RSV_total 큼 → `hierarchical` + 다단 synthesis

---

## 판단 루브릭

```
1. Goal 성격으로 기본 Topology 1~2개 후보 선정
2. SE 분포로 보정
3. RSV 크기로 병렬성/계층성 보정
4. 후보 2개 이상 → composite 검토
5. 최종 선택 + rationale 기록
```

---

## 유형별 주의사항

| type | 장점 | 핵심 위험 |
|------|------|----------|
| linear | hand-off 0, 조율 비용 최소 | RSV 크면 단일 노드 과부하 |
| branching | 불필요 경로 회피 | 분기 조건 모호 시 잘못된 경로 |
| parallel | 시간 단축, 독립 실행 | 합류 노드 SE 폭등 |
| fanout_fanin | 탐색 다양성 확보 | fanin에서 redundancy |
| hierarchical | 복잡도 분산 | 계층 간 hand-off cost |
| synthesis_centric | 합성 품질 집중 | 합성 노드 과부하 |
| state_transition | 명확한 진행, 재시작 용이 | 상태 폭발, 예외 복잡 |
| composite | 유연성 | 설계 복잡도 증가 |
