# Token Budget

## v2.0 아키텍처: SKILL.md 중심 실행

| Layer | 대상 | Soft Limit | 로딩 조건 |
|-------|------|-----------|----------|
| **SKILL.md** | 5-Phase 전체 runbook | **~3,500** | **항상 (단독 실행 가능)** |
| module | module.*.md 1개 | 1,200 | 상세 분석 필요 시에만 |
| reference | pack.*.md 1개 | 2,000 | ΔQ ≥ 2 |

## 예상 시나리오별 토큰 사용

| 시나리오 | 로딩 구성 | 예상 토큰 | 추가 view 호출 |
|----------|----------|----------|---------------|
| 단순 linear 설계 | **SKILL.md만** | ~3,500 | **0회** |
| 표준 parallel/composite | **SKILL.md만** | ~3,500 | **0회** |
| 동점 Topology 비교 | SKILL.md + topology_selection | ~4,700 | 1회 |
| 복합 + 스키마 강화 | SKILL.md + node_design + loop_risk | ~5,900 | 2회 |
| 풀 분석 + estimator | SKILL.md + handoff + output_contract + estimator | ~9,500 | 3회 |

## v1.0 대비 개선

| 지표 | v1.0 | v2.0 |
|------|------|------|
| 최소 view 호출 | 2~3회 (core + orch + module) | **0회** (SKILL.md 1회 읽기로 충분) |
| 단순 설계 토큰 | ~2,700 (core+orch+topo) | ~3,500 (SKILL.md, 약간 증가) |
| 단순 설계 총 비용 | tool call 3회 + 2,700 tok | **tool call 0회 + 3,500 tok** |
| 복합 설계 토큰 | ~5,100 | ~5,900 (비슷하지만 tool call 감소) |
