# Modules Index

## 모듈 레지스트리

| Module | 질문 축 | File |
|--------|---------|------|
| topology_selection | 어떤 Topology 구조를 선택할 것인가? | `module.topology_selection.md` |
| node_design | 노드를 어떻게 분리하고 θ_GT/RSV를 설정할 것인가? | `module.node_design.md` |
| loop_risk | 어떤 루프 위험이 있고 어떻게 방지할 것인가? | `module.loop_risk.md` |
| handoff | Hand-off 시 컨텍스트 손실을 어떻게 최소화할 것인가? | `module.handoff.md` |

## 직교성 매트릭스

각 모듈은 고유 질문 축만 소유하고 다른 모듈의 정의를 재정의하지 않는다.

| 개념 | topology_selection | node_design | loop_risk | handoff |
|------|--------------------|-------------|-----------|--------|
| Topology 유형 | **소유** | 참조 | 참조 | 참조 |
| 노드 분리/θ_GT | — | **소유** | 참조 | — |
| 루프 위험/mitigation | — | — | **소유** | — |
| Hand-off 포맷/최소화 | — | — | — | **소유** |
| DQ/RSV | Core 소유 | 할당 규칙 | RSV 검증 | DQ Status |

## 로딩 순서 (Phase별)

```
Phase 2 → topology_selection
Phase 3 → node_design
Phase 4 → loop_risk + (조건부) handoff
```
