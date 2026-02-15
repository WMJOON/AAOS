# Loading Policy

## 기본 로딩 규칙

| Layer | 로딩 조건 |
|-------|----------|
| Core + Orchestrator | **항상** 로딩 |
| Modules | Phase별 온디맨드 (modules_index.md 참조) |
| Reference Packs | ΔQ 기반 조건부 로딩 |
| Legacy references/ | 템플릿으로서 모듈에서 참조 시 로딩 |

## ΔQ 기반 Pack 로딩

ΔQ = 관찰 복잡도 지표. 신호 다양성 + 심각도 + 제안 필요성의 함수.

| ΔQ | 허용 | 예시 상황 |
|----|------|----------|
| < 2 | Pack 로딩 금지 | 이상 신호 없는 단순 주간 리뷰 |
| >= 2 | 1개 pack 허용 | 이상 신호 감지, 프로파일 참조 필요 |
| >= 3 | 1-2개 pack 허용 | 개선 제안 생성 + agora 제출 포맷 필요 |

## Pack 레지스트리

| Pack | Trigger | Path |
|------|---------|------|
| `sql_queries` | 항상 (신호 수집 시) | `30.references/packs/pack.sql_queries.md` |
| `anomaly_profiles` | ΔQ >= 2 | `30.references/packs/pack.anomaly_profiles.md` |
| `proposal_templates` | ΔQ >= 2 | `30.references/packs/pack.proposal_templates.md` |
| `agora_format` | ΔQ >= 3 | `30.references/packs/pack.agora_format.md` |

## Legacy References

| File | 용도 | 참조 모듈 |
|------|------|----------|
| `references/sql_checks.sql` | 기본 SQL 쿼리 (pack.sql_queries에 흡수) | observation-policy |
| `references/weekly_review.template.md` | 주간 리뷰 템플릿 | hitl-interaction |
| `references/biweekly_review.template.md` | 격주 리뷰 템플릿 | hitl-interaction |
| `references/workflow_improvement_report.template.md` | 개선 보고서 템플릿 | improvement-proposal |
