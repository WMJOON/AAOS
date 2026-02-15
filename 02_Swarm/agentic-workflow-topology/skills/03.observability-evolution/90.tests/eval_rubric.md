# Eval Rubric -- Observability & Evolution

## 6축 평가 (5점 척도)

| 축 | 5 (우수) | 3 (보통) | 1 (미흡) |
|------|---------|---------|---------|
| **Signal Coverage** | 6종 AS 전부 감지 가능, SQL 쿼리 완비, 심각도 매트릭스 일관 | 주요 AS 유형 커버, 일부 쿼리 누락 | 핵심 AS 유형 누락 |
| **HITL Protocol** | SC+EC 모두 구현, 피드백 스키마 구조화, 에스컬레이션 완비 | 한 모드만 구현, 부분적 피드백 | HITL 메커니즘 없음 |
| **Proposal Quality** | 증거 기반, rollback rule 포함, 타깃 스킬 정확 | 제안 있으나 증거 약함 | 비구조적 제안 또는 없음 |
| **Evolution Loop** | agora 제출, 라이프사이클 추적, 폐루프 메트릭 | 부분적 추적 | 피드백 루프 없음 |
| **Orthogonality** | 4모듈 직교 분리, 재정의 없음 | 경미한 중복 | 모듈 간 내용 중복 |
| **when_unsure** | 모든 모호 상황에 구체적 행동 지침 | 주요 상황 커버 | 범용적이거나 없음 |

## 통과 기준

- 6축 평균 >= 3.5
- **Signal Coverage** >= 3 (필수)
- **HITL Protocol** >= 3 (필수)

## 구조 검증 (Pass/Fail)

| 항목 | 기준 |
|------|------|
| SKILL.md 줄 수 | <= 120줄 |
| 필수 레이어 존재 | 00.meta, 10.core, 20.modules, 30.references, 40.orchestrator |
| 모듈 4개 존재 | observation-policy, hitl-interaction, improvement-proposal, evolution-tracking |
| manifest에 모든 모듈 선언 | manifest.yaml modules[] 완비 |
| 참조팩 파일 존재 | 30.references/packs/ 내 선언된 팩 존재 |
