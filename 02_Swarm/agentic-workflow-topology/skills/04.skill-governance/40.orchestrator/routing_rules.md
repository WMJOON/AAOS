# Routing Rules

## Phase -> Module 매핑

| Phase | Required Module | Reference | Reference 조건 |
|-------|----------------|-----------|----------------|
| 1. Metadata Validation | metadata-validation | skill_system_manifest.schema.yaml | manifest 검증 시 |
| 2. Contract Sync | contract-sync | 각 skill의 schema 파일 | 항상 (schema 교차 검증) |
| 3. Registry Runbook | registry-runbook | -- | -- |

## 의도 분류 규칙

| 의도 신호 | 라우팅 | 시작 Phase |
|----------|--------|-----------|
| "메타데이터 점검", "frontmatter 확인", "4-layer 검증" | Validate | Phase 1 |
| "계약 점검", "schema 결합", "coupling 확인", "drift 검사" | Sync | Phase 2 |
| "레지스트리 확인", "registry 재생성", "동기화" | Audit | Phase 3 |
| "전체 거버넌스 점검", "governance check" | Validate + Sync + Audit | Phase 1 (full pipeline) |
| "보고서 작성", "report" | Report | 가장 최근 점검 결과 기반 |
| 모호한 입력 | Validate 기본값 | Phase 1 |

## 에스컬레이션 규칙

| 조건 | 행동 |
|------|------|
| Phase 1에서 FAIL 발견 | Phase 2 진행 전 사용자에게 FAIL 보고 + 진행 여부 확인 |
| CC-01/CC-02 FAIL (HIGH risk) | 즉시 보고, contract-sync 결과를 상위 거버넌스로 에스컬레이션 |
| 3회 연속 거버넌스 점검에서 동일 WARN 미해결 | severity를 WARN -> FAIL로 승격 제안 |
