# Eval Rubric

## 평가 축 (5점 척도)

| 축 | 5 (우수) | 3 (보통) | 1 (미흡) |
|----|---------|---------|---------|
| **Topology 적합성** | Goal/SE/RSV 3-Signal 모두 반영, 근거 명확 | 대체로 맞으나 근거 부족 | 부적합한 Topology 선택 |
| **DQ 완전성** | Goal 달성에 필요한 DQ 누락 없음 | 핵심 DQ 포함, 일부 누락 | 핵심 DQ 누락 |
| **Node 분리 품질** | Explicit Output 단위 분리, θ_GT/RSV 정당 | 분리는 맞으나 설정 근거 부족 | 내부 추론 기준 분리 |
| **Loop Risk 식별** | 해당 Topology의 위험 모두 식별 + mitigation | 주요 위험 식별, mitigation 일부 | 위험 누락 |
| **Hand-off 품질** | 허용 포맷 사용, 금지 포맷 없음 | 포맷 적절하나 최소화 미흡 | 산문형 요약 사용 |
| **RSV 일관성** | Σ(rsv_target) ≈ RSV_total (±10%) | 20% 이내 오차 | 불일치 |

## Pass 기준

- 6개 축 평균 ≥ 3.5
- Topology 적합성 ≥ 3
- RSV 일관성 ≥ 3
