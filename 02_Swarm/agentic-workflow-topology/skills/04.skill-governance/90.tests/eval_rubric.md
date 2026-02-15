# Eval Rubric

## 평가 축 (5점 척도)

| 축 | 5 (우수) | 3 (보통) | 1 (미흡) |
|----|---------|---------|---------|
| **Metadata 완전성** | 4개 governed skill 전체 FM/SC/4L 체크 PASS | 주요 항목 PASS, 일부 WARN | FAIL 항목 누락 또는 미점검 |
| **Contract Sync 정확성** | CC-01~CC-05 전체 점검, 결합 근거 명시 | 주요 결합점(CC-01, CC-02) 점검, 근거 일부 누락 | HIGH risk 결합점 미점검 |
| **Registry 정합성** | 로컬+Swarm 레지스트리 전수 대조, cross-swarm 중복 검사 완료 | 로컬 레지스트리만 대조 | 레지스트리 미점검 |
| **보고서 구조** | governance_check_report 템플릿 완전 사용, action_items 명확 | 템플릿 부분 사용 | 자유 형식 보고 |
| **When Unsure 적용** | 모호한 상황에서 severity 보수 처리 + 사용자 판단 요청 | when_unsure 적용하지만 일부 누락 | 모호한 상황을 무시하고 단정 |

## Pass 기준

- 5개 축 평균 >= 3.5
- Contract Sync 정확성 >= 3
- Metadata 완전성 >= 3

## 보너스 항목

- CC-05 feedback loop closure 검증 시 +0.5
- schema version drift 검사 수행 시 +0.5
- 이전 거버넌스 점검 결과와 비교 (regression 검출) 시 +0.5
