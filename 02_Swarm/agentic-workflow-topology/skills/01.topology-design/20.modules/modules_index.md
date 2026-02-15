# Modules Index

## 등록 모듈

| id | 파일 | 질문 축 | 트리거 패턴 | θ_GT 경향 |
|----|------|---------|------------|----------|
| topology_selection | module.topology_selection.md | "어떤 구조를 선택할 것인가?" | Phase 2 진입 시 항상 | — |
| node_design | module.node_design.md | "노드를 어떻게 분리하고 설정할 것인가?" | Phase 3 진입 시 항상 | 좁~넓 |
| loop_risk | module.loop_risk.md | "어떤 루프 위험이 있는가?" | Phase 4 진입 시 항상 | — |
| handoff | module.handoff.md | "Hand-off 시 컨텍스트 손실을 어떻게 최소화할 것인가?" | Phase 4, hand-off 포인트 존재 시 | — |

## 직교성 매트릭스

| | topology | node_design | loop_risk | handoff |
|---|---------|------------|-----------|--------|
| **topology** | — | 구조↔노드분리 약결합 | 구조→루프유형 선행 | 구조→handoff유무 선행 |
| **node_design** | | — | 노드설정→루프조건 | 노드Output→handoff포맷 |
| **loop_risk** | | | — | 독립 |
| **handoff** | | | | — |

겹침 점검: 공유 어휘(θ_GT, RSV, DQ, Explicit Output)는 모두 `10.core/core.md`에만 정의.
각 모듈은 고유 질문 축의 delta만 담는다.
