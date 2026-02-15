# Modules Index

> 등록된 모듈의 메타 정보. Orchestrator가 라우팅 시 참조한다.

## 등록된 모듈

| Module ID | 고유 질문 축 | 입력 | 출력 | 토큰 예산 | 주요 Reference Trigger |
|-----------|-------------|------|------|-----------|----------------------|
| module.bundle-contract | 번들 9키 구조 설계와 optional 확장 계약 | domain, intent, constraints, workflow_profile | mental_model_bundle (JSON) | ~1,200 | "스키마", "검증", "RACI" |
| module.loading-policy | deltaQ 기반 참조 로딩 정책 설계 | domain 정보 밀도, 검증 요구 수준 | loading_policy + reference_loading_rule | ~1,200 | "토큰 비용", "deltaQ", "예산" |
| module.routing-kpi | 패턴 라우팅 규칙과 운영 KPI 목표 설계 | 도메인 패턴 분포, workflow class | routing_policy + kpi_targets + cost/utility model | ~1,200 | "비용 모델", "직교성", "RACI 매핑" |

## 패턴-모듈 조합 참고

| 패턴 | 조합 방식 | 모드 |
|------|----------|------|
| Evaluate | bundle-contract + loading-policy 병렬 | 각 렌즈 독립 판단 |
| Critique | bundle-contract 생성 → routing-kpi 검증 | 적대적 검증 |
| Translate | 한 모듈의 계약을 다른 모듈 관점으로 재해석 | 프레임 변환 |
| Prioritize | bundle-contract 단독 심층 | 깊이 분석 |
| Arbitrate | loading-policy vs routing-kpi 트레이드오프 | 상충점 추출 |
| Simulate | 3개 모듈 페르소나로 도메인 시나리오 | 병렬 시뮬레이션 |

## 직교성 검증

| 모듈 A | 모듈 B | 겹침 여부 | 비고 |
|--------|--------|----------|------|
| bundle-contract | loading-policy | 없음 | A=구조 설계, B=로딩 전략 |
| bundle-contract | routing-kpi | 없음 | A=계약 내용, B=운영 성능 |
| loading-policy | routing-kpi | 없음 | A=참조 관리, B=패턴/KPI |
