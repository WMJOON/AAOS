# Routing Rules (Quick Reference)

## Phase → Module 매핑

| Phase | 필수 모듈 | 조건부 모듈 | Reference Pack |
|-------|----------|-----------|----------------|
| 1. Goal→DQ | — | — | — |
| 2. Topology | topology_selection | — | — |
| 3. Task Graph | node_design | — | output_contract (ΔQ≥2) |
| 4. Risk+Handoff | loop_risk | handoff (hand-off 존재 시) | — |
| 5. Spec 산출 | — | — | output_contract (스키마 검증) |

## ΔQ 로딩 규칙

| ΔQ | 허용 | 예시 |
|----|------|------|
| < 2 | Pack 로딩 금지 | 단순 linear 설계 |
| ≥ 2 | Pack 1개 | JSON 스키마 참조 필요 |
| ≥ 4 | Pack 1~2개 | 복합 설계 + estimator 연동 |

## handoff 모듈 트리거

```
parallel OR human_gate OR agent_delegation OR context_overflow → load handoff
```

## Strategy/High-Risk 추가 규칙

```
if strategy OR high_risk detected:
  → PF1 preflight 강제
  → H1, H2 노드 필수
  → T4→C1→H1 엣지 필수
  → H1 finalization 전 validate_strategy_h1_gate.py 실행
```
