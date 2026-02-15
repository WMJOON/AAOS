# Routing Rules (Quick Reference)

## Phase → Module 매핑

| Phase | 필수 모듈 | 조건부 모듈 | Reference Pack |
|-------|----------|-----------|----------------|
| 0. Preflight | — | — | — |
| 1. Goal→DQ | — | — | — |
| 2. Topology | topology_selection | — | — |
| 3. Task Graph | node_design | — | output_contract (ΔQ≥2) |
| 4. Risk+Handoff | loop_risk | handoff (hand-off 존재 시) | — |
| 5. H1 Gate | — | — | output_contract + web_evidence.template |
| 6. Spec 산출 | — | — | output_contract (스키마 검증) |

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

## Strategy/High-Risk Gate 트리거

아래 중 하나라도 참이면 `strategy_gate.enabled=true`:

- `workflow_profile.class in {strategy, high_risk}`
- `context.risk_tolerance=high`
- goal 키워드에 `전략`, `strategy`, `go-to-market`, `시장 진입` 포함

`strategy_gate.enabled=true`일 때 강제 규칙:

- `preflight.questions[0]`은 PF1 고정
- 노드 `H1`, `H2` 존재 필수
- 엣지 `T4 -> C1 -> H1` 필수
- H1 finalization 전에 `web_evidence_YYYY-MM-DD.md` + COWI 산출물 존재 필수
