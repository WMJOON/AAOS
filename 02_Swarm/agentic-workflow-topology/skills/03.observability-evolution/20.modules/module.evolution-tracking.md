# module.evolution-tracking

## Question Axis

**제안이 설계 스킬로 어떻게 환류되고 피드백 루프가 어떻게 추적되는가?**

---

## Evolution Cycle 상태 전이

```
draft
  → user_reviewed      (HITL checkpoint에서 사용자가 검토)
    → submitted_to_agora (cortex-agora CHANGE_INDEX에 제출)
      → accepted        (agora에서 수용 결정)
        → applied        (타깃 스킬이 실제 반영)
      → rejected        (agora에서 거부)
        → archived       (거부 사유와 함께 보관)
      → deferred        (보류, 다음 리뷰에서 재검토)
    → archived          (사용자가 reject → 직접 아카이브)
```

**상태 전이 규칙**:
- `draft → user_reviewed`: Phase 3 HITL checkpoint 완료 필수
- `user_reviewed → submitted_to_agora`: `confidence >= medium` 필수, `low`는 추가 검증 후
- `submitted_to_agora → accepted/rejected`: agora 거버넌스 프로세스에 위임
- `accepted → applied`: 타깃 스킬 측에서 실제 반영 확인 시

---

## 타깃 스킬 라우팅

| Classification | Target Skill | 제안 유형 예시 |
|---------------|-------------|---------------|
| `topology` | 01.topology-design | 노드 분할, topology 전환, θ_GT 재보정 |
| `execution` | 02.execution-design | mode/model 전환, fallback 규칙, handoff 계약 |
| `policy` | 04.skill-governance | 거버넌스 규칙, 스킬 메타데이터 업데이트 |
| `operational` | DNA.md / 스웜 설정 | 리소스 한도, 행동 feed 정책 |

---

## Cortex-Agora 제출 프로토콜

승인된 제안을 agora change event로 포맷:

```json
{
  "change_id": "P-AWT-OE-{YYYYMMDD}-{NNN}",
  "source_skill": "awt-observability-evolution",
  "target_skill": "awt-topology-design",
  "classification": "topology",
  "proposal_summary": "string",
  "evidence_digest": "string (핵심 증거 요약)",
  "proposed_action": {
    "action": "split_node",
    "detail": "T3 → T3a + T3b",
    "affected_artifacts": ["workflow_topology_spec"]
  },
  "expected_effect": "string",
  "rollback_rule": "string",
  "confidence": "high | medium",
  "submitted_at": "ISO8601",
  "status": "pending_review"
}
```

**제출 조건**:
- `confidence >= medium` (low는 제출 불가, 추가 검증 필요)
- `user_feedback.decision = approve` 또는 `modify` (reject는 제출 불가)
- `rollback_rule` 비어있지 않음

---

## 폐루프 메트릭

### 주기적 산출 메트릭 (biweekly 이상)

| Metric | 정의 | 목표 |
|--------|------|------|
| `closure_rate_30d` | 30일 내 `applied` 도달 비율 | >= 50% |
| `avg_cycle_days` | `draft` → `applied` 평균 일수 | <= 14일 |
| `active_cycles` | 현재 `draft`~`submitted` 상태 IP 수 | 모니터링 |
| `rejection_rate` | `rejected` / 전체 제출 비율 | <= 30% |
| `stale_proposals` | 14일 이상 `submitted` 상태 유지 IP 수 | 0 목표 |

### Evolution Summary 산출물

```json
{
  "period": { "start": "...", "end": "..." },
  "evolution_metrics": {
    "total_proposals": 8,
    "active_cycles": 3,
    "closure_rate_30d": 0.67,
    "avg_cycle_days": 12,
    "rejection_rate": 0.12,
    "stale_proposals": 0
  },
  "cycle_details": [
    {
      "proposal_id": "IP-2026-02-01-001",
      "current_state": "applied",
      "target_skill": "01.topology-design",
      "days_in_cycle": 10
    }
  ]
}
```

---

## 피드백 루프 닫기

1. **제안 제출 후**: agora CHANGE_INDEX 상태를 주기적으로 확인
2. **수용 시**: 타깃 스킬에서 실제 반영 여부 확인 (다음 OW에서 해당 AS 재발 감소 기대)
3. **반영 효과 측정**: 제안 적용 후 다음 2~3 OW에서 동일 AS 발생률 비교
4. **효과 검증 실패 시**: `rollback_rule` 적용 여부를 다음 SC에서 사용자에게 제시
5. **아카이브**: 효과 검증 완료 또는 롤백 완료 시 `archived` 전이
