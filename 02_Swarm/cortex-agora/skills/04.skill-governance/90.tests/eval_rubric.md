# Eval Rubric

## 평가 축 (5점 척도)

| 축 | 5 (우수) | 3 (보통) | 1 (미흡) |
|----|---------|---------|---------|
| **Metadata 완전성** | instruction-nucleus FM/SC 전체 PASS | 주요 항목 PASS, 일부 WARN | FAIL 항목 누락/미점검 |
| **Archive Integrity** | 3 JSONL 전체 스키마 + CC-01~CC-03 참조 무결성 + append-only 확인 | 주요 JSONL 체크 + 일부 CC 점검 | JSONL 스키마 미점검 |
| **Consumption Contract** | BF 스키마 + COWI pull CC-05 + cross-swarm completeness 전체 점검 | BF 스키마 + CC-05 일부 | BF/COWI 미점검 |
| **보고서 구조** | governance_check_report 템플릿 완전 사용, action_items 명확 | 템플릿 부분 사용 | 자유 형식 보고 |
| **When Unsure 적용** | 모호한 상황에서 severity 보수 처리 + 사용자 판단 요청 | when_unsure 일부 적용 | 모호한 상황 무시/단정 |

## Pass 기준

- 5개 축 평균 >= 3.5
- Archive Integrity >= 3
- Consumption Contract >= 3

## 보너스 항목

- CC-02 `linked_event_id` referential integrity 완전 검증 시 +0.5
- Bridge script `monotonic_ts` + `unique_id` enforcement 확인 시 +0.5
- `group_id` vs `trace_id` canonical alignment 검증 시 +0.5
