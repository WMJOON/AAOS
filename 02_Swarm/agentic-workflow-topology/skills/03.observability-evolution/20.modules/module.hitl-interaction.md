# module.hitl-interaction

## Question Axis

**관찰 결과를 사용자에게 어떻게 제시하고 피드백을 수집할 것인가?**

---

## HITL 체크포인트 2종

### 1. Scheduled Checkpoint (SC)

- **트리거**: Observation Window 종료 시 (weekly/biweekly/on_demand)
- **목적**: 누적된 관찰 결과를 요약 제시하고 사용자 방향성 수집

**제시 프로토콜**:

```markdown
## Observation Summary (OW: {start} ~ {end})

### 신호 요약
| Type | Count | Severity | Affected Nodes |
|------|-------|----------|----------------|
| {type} | {n} | {severity} | {nodes} |

### Top-3 패턴 상세
1. **{pattern_name}**
   - 근거: {evidence_excerpt}
   - 영향: {impact_description}

### 개선 제안 (auto_propose=true인 경우)
1. [{IP-id}] {proposed_change_summary} (확신도: {confidence})
2. ...

### 피드백 요청
다음 중 선택해 주세요:
a) 제안 승인/수정/거부
b) 추가 분석 요청
c) 이번 리뷰 건너뛰기
```

### 2. Event Checkpoint (EC)

- **트리거**: Critical 심각도 이상 신호 감지 시 즉시
- **목적**: 긴급 이상 상황에 대한 즉각적 사용자 판단 수집

**제시 프로토콜**:

```markdown
## ALERT: Critical Anomaly Detected

- **신호**: {signal_type} in {affected_node}
- **심각도**: CRITICAL
- **근거**: {evidence_summary}
- **감지 시점**: {timestamp}

### 즉시 선택지
a) 근본 원인 분석 요청
b) 즉시 개선안 생성
c) 워크플로우 일시 중단 + 에스컬레이션
d) 확인 후 모니터링 유지
```

---

## 사용자 피드백 스키마

```json
{
  "checkpoint_id": "HC-YYYY-MM-DD-NNN",
  "mode": "scheduled | event",
  "signals_reviewed": ["AS-001", "AS-002"],
  "user_assessment": {
    "signal_validity": "confirmed | disputed | needs_more_data",
    "priority_override": "high | medium | low (optional)",
    "additional_context": "free-text (optional)"
  },
  "proposal_decisions": [
    {
      "proposal_id": "IP-001",
      "decision": "approve | modify | reject",
      "modification_notes": "string (optional)"
    }
  ]
}
```

---

## 에스컬레이션 규칙

| 조건 | 행동 |
|------|------|
| event_checkpoint + 48h 무응답 | `halt_and_escalate_to_audit` (DNA 거버넌스) |
| 사용자가 signal_validity=disputed | 확신도 하향 + 다음 SC에서 추가 데이터로 재검토 |
| 사용자가 "에스컬레이션" 선택 | behavior feed에 escalation 이벤트 기록 + 워크플로우 일시 중단 |
| 동일 신호 3회 연속 SC에서 미해결 | warning → critical 자동 승격 |

---

## 피드백 기록 정책

- 모든 HC 결과는 SQLite SoT에 기록 (audit_logs에 `action='hitl_checkpoint'`)
- 피드백 원문은 behavior feed에 `kind='hitl_feedback'` 이벤트로 기록
- 미응답 SC는 `status='skipped'`로 기록하되, critical 미응답은 에스컬레이션

---

## 리뷰 템플릿 참조

| 주기 | 템플릿 |
|------|--------|
| weekly | `references/weekly_review.template.md` |
| biweekly | `references/biweekly_review.template.md` |
| improvement report | `references/workflow_improvement_report.template.md` |

SC 수행 시 해당 주기의 템플릿을 기반으로 리뷰 문서를 생성한다.
