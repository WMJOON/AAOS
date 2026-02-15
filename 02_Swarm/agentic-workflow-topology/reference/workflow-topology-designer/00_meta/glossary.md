# Glossary

| 용어 | 정의 | 사용처 |
|------|------|--------|
| **Workflow** | Task Node들의 유향 그래프(Task Graph) | 전체 |
| **Task Node** | Explicit Output으로 경계가 정의되는 작업 단위 | 전체 |
| **Explicit Output** | 외부에서 관측 가능한 명시적 산출물. 노드 경계의 유일한 기준 | core, node_design |
| **θ_GT** | Node-level Expected Entropy Band. Explicit Output의 의미적 분산도 기대 범위 | core, topology, node_design |
| **SE** | Semantic Entropy. 해석 자유도. θ_GT 설정의 입력 | core, node_design |
| **RSV** | Required Semantic Value. Goal 달성에 필요한 의미 기여 총량 | core, node_design |
| **DQ** | Decision Question. RSV의 기본 단위. 닫히면 Goal에 의미 기여 완료 | core, orchestrator |
| **RSV_total** | Σ(DQ_weight). 워크플로우 전체의 RSV | core, orchestrator |
| **rsv_target** | 개별 노드에 할당된 RSV 목표 | node_design |
| **Topology** | Task Graph의 연결 구조. 8종: linear, branching, parallel, fanout_fanin, hierarchical, synthesis_centric, state_transition, composite | topology_selection |
| **Hand-off** | 노드 간 컨텍스트 전달 지점. 비용(암묵지 손실)이 발생 | handoff |
| **Redundancy** | "정보량은 늘었지만 의미 공간은 안 늘어난" 상태. 중복 증산 루프의 신호 | loop_risk, estimator |
| **Convergence Loop** | θ_GT(actual) > θ_GT(expected) 동안의 정상 반복 | loop_risk |
| **normalized_output** | estimator 입력용 정규화 JSON. 6개 섹션(DQ, claims, assumptions, constraints, risks, tradeoffs) | estimator |
