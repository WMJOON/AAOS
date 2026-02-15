# pack.agora_format

> **로딩 조건**: ΔQ >= 3 (cortex-agora 제출 포맷 필요 시)

승인된 Improvement Proposal을 cortex-agora change event로 변환하기 위한 포맷 명세.

---

## Change Event 스키마

```json
{
  "change_id": "P-AWT-OE-{YYYYMMDD}-{NNN}",
  "source_skill": "awt-observability-evolution",
  "source_context_id": "awt-observability-evolution",
  "target_skill": "awt-{skill-name}",
  "classification": "topology | execution | policy | operational",
  "proposal_summary": "string: 1-2문장 요약",
  "evidence_digest": "string: 핵심 증거 3줄 이내 요약",
  "proposed_action": {
    "action": "string: action type",
    "detail": "string: 구체적 변경 내용",
    "affected_artifacts": ["string[]"]
  },
  "expected_effect": "string",
  "rollback_rule": "string",
  "confidence": "high | medium",
  "observation_window": {
    "start": "ISO8601",
    "end": "ISO8601"
  },
  "checkpoint_id": "HC-YYYY-MM-DD-NNN",
  "user_decision": "approve | modify",
  "submitted_at": "ISO8601",
  "status": "pending_review"
}
```

---

## 필드 매핑: IP → Change Event

| IP 필드 | Change Event 필드 |
|---------|------------------|
| `proposal_id` | `change_id` (접두사 변환: IP → P-AWT-OE) |
| `target_skill` | `target_skill` (접두사 추가: awt-) |
| `classification` | `classification` (동일) |
| `observed_pattern` + `root_cause_hypothesis` | `proposal_summary` (축약) |
| `evidence_refs` | `evidence_digest` (요약) |
| `proposed_change` | `proposed_action` (동일 구조) |
| `expected_effect` | `expected_effect` (동일) |
| `rollback_rule` | `rollback_rule` (동일) |
| `confidence` | `confidence` (동일, low는 제출 불가) |
| `user_feedback.checkpoint_id` | `checkpoint_id` |
| `user_feedback.decision` | `user_decision` |

---

## 제출 조건 체크리스트

제출 전 반드시 확인:

- [ ] `confidence >= medium` (low는 제출 불가)
- [ ] `user_decision` = approve 또는 modify (reject는 제출 불가)
- [ ] `rollback_rule` 비어있지 않음
- [ ] `evidence_digest` 비어있지 않음
- [ ] `target_skill`이 유효한 AWT 스킬 ID
- [ ] `change_id` 형식: `P-AWT-OE-YYYYMMDD-NNN`

---

## COWI 연동

제출된 change event는 cortex-agora CHANGE_INDEX에 추가되며:

1. `cowi-agora-consumption-bridge`가 CHANGE_INDEX를 주기적으로 확인
2. 수용된 change는 COWI 아티팩트로 물질화
3. 타깃 스킬이 COWI 아티팩트를 참조하여 실제 반영
4. 반영 완료 시 change event status → `accepted` → `applied`

evolution-tracking 모듈이 이 라이프사이클을 추적한다.
