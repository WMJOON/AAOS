# Token Budget

## v2.2 아키텍처: SKILL.md 최소 로더 + 레이어 온디맨드

| Layer | 대상 | Soft Limit | 로딩 조건 |
|---|---|---:|---|
| SKILL.md | 초경량 로더 | <= 120 lines | 항상 |
| 10.core | 핵심 정의, 입력 인터페이스, when_unsure | ~1,500 tok | 항상 |
| 40.orchestrator | 5-Phase 프로세스, 라우팅, strategy gate | ~1,300 tok | 항상 |
| 20.modules | 상세 모듈 1개 | ~1,200 tok | 필요 시 |
| 30.references | 참조 1개 | ~2,000 tok | 필요 시 |

## 예상 시나리오별 토큰 사용

| 시나리오 | 로딩 구성 | 예상 토큰 | 추가 view 호출 |
|---|---|---:|---:|
| 단순 linear 설계 | loader + core + orchestrator | ~2,800 | 0~1 |
| 표준 parallel/composite | 위 + modules 1~2개 | ~4,000~5,200 | 1~2 |
| 동점 Topology 비교 | 위 + topology_selection | ~4,000 | 1 |
| 복합 + 루프 강화 | 위 + node/loop 모듈 | ~5,200 | 2 |
| 풀 분석 + estimator | 위 + handoff + estimator 참조 | ~8,800 | 3+

## 운영 원칙
- `SKILL.md`는 단독 runbook가 아니라 라우팅 엔트리포인트다.
- 상세 규칙은 레이어 문서로 분해해 필요할 때만 읽는다.
- self-contained 정책은 폐기한다.
