# Routing Rules

## 패턴 세트 (라우팅 최상위 키)

| 패턴 | Phase | 설명 |
|------|-------|------|
| **Observe** | 1 | 데이터 소스에서 신호 수집 |
| **Classify** | 2 | 이상 신호 분류 및 심각도 판정 |
| **Interact** | 3 | 사용자에게 관찰 결과 제시 및 피드백 수집 |
| **Propose** | 4 | 구조화된 개선 제안 생성 |
| **Evolve** | 5 | 제안 환류 및 라이프사이클 추적 |
| **Report** | 5 | 주기적 리뷰 보고서 생성 |

---

## Phase → Module 매핑

| Phase | Required Module | Conditional Pack | Pack 조건 |
|-------|----------------|-----------------|-----------|
| 1 | observation-policy | sql_queries | 항상 |
| 2 | observation-policy | anomaly_profiles | ΔQ >= 2 |
| 3 | hitl-interaction | -- | -- |
| 4 | improvement-proposal | proposal_templates | ΔQ >= 2 |
| 5 | evolution-tracking | agora_format | ΔQ >= 3 |

---

## 의도 분류 규칙

사용자 요청 또는 시스템 트리거의 의도를 다음 기준으로 분류:

| 의도 신호 | 라우팅 | 시작 Phase |
|----------|--------|-----------|
| "리뷰해줘", "주간 점검" | Observe → full pipeline | Phase 1 |
| "이상 있어?", "문제 분석" | Observe + Classify | Phase 1-2 |
| 이벤트 알림 (critical AS) | Interact (event) | Phase 3 |
| "개선안 만들어", "제안해줘" | Propose | Phase 4 |
| "agora에 제출", "환류 상태" | Evolve | Phase 5 |
| "보고서 작성" | Report | Phase 5 |
| 모호한 입력 | Observe 기본값 | Phase 1 |

---

## ΔQ 산정 규칙

ΔQ = 관찰 복잡도 지표, 참조팩 로딩 임계값 결정.

```
ΔQ = signal_type_count + severity_weight + proposal_needed

signal_type_count: 감지된 AS 유형 수 (0~6)
severity_weight:   critical=2, warning=1, notice=0 (최고 심각도 기준)
proposal_needed:   제안 생성 필요 시 +1
```

**예시**:
- 이상 없음: ΔQ = 0+0+0 = 0 → pack 로딩 없음
- retry_spike(warning) 1건: ΔQ = 1+1+1 = 3 → pack 2개까지
- failure_cluster(critical) + bottleneck(warning): ΔQ = 2+2+1 = 5 → pack 전체

---

## 에스컬레이션 라우팅

| 조건 | 행동 |
|------|------|
| critical AS 감지 | Phase 3 Event Checkpoint으로 즉시 분기 |
| event_checkpoint 48h 무응답 | `halt_and_escalate_to_audit` |
| 동일 AS 3회 OW 연속 | severity 자동 승격 (warning → critical) |
| 상충 결론 (가설 경합) | 사용자 판단 요청 (when_unsure 정책) |
