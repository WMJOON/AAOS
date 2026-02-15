# Core -- Workflow Observability & Evolution

## 고정 문장

이 스킬은 워크플로우를 실행하지 않는다.
실행 로그를 **관찰(Observe)**하고, 사용자와 **상호작용(Interact)**하며, 설계 **개선 제안(Evolve)**을 산출한다.

---

## 핵심 정의

| 용어 | 약어 | 정의 |
|------|------|------|
| Observation Point | OP | 신호를 수집하는 워크플로우 생명주기 위치. **periodic**(주기적: weekly/biweekly) 또는 **event-triggered**(이상 감지 시 즉시). |
| Anomaly Signal | AS | 기대 동작으로부터의 측정 가능한 이탈. 6종: `performance_drift`, `failure_cluster`, `retry_spike`, `bottleneck`, `human_deferral_loop`, `rsv_inflation`. |
| Signal Severity | SS | 심각도 3단계. `notice`(정보) → `warning`(주의 필요) → `critical`(즉시 HITL 필요). |
| HITL Checkpoint | HC | 관찰 결과를 사용자에게 제시하고 구조화된 피드백을 수집하는 상호작용 지점. `scheduled_checkpoint` 또는 `event_checkpoint`. |
| Improvement Proposal | IP | 관찰 패턴 · 근본 원인 가설 · 제안 변경 · 타깃 스킬 · 기대 효과 · 롤백 규칙 · 확신도를 포함하는 구조화된 산출물. |
| Evolution Cycle | EC | IP의 전체 라이프사이클: `draft` → `user_reviewed` → `submitted_to_agora` → `accepted/rejected` → `applied/archived`. |
| Observation Window | OW | 단일 관찰 세션의 시간 범위. weekly=7일, biweekly=14일, event=실시간. |

---

## 공유 출력 스키마

모든 판단은 다음 4-tuple로 구조화한다:

```
{판단, 근거, 트레이드오프, 확신도}
```

- **판단**: 결론 또는 제안 내용
- **근거**: SQL 쿼리 결과, behavior feed 이벤트 ID 등 증거 참조
- **트레이드오프**: 해당 판단의 대안과 비교
- **확신도**: `high` / `medium` / `low`

---

## 입력 인터페이스

```json
{
  "mode": "scheduled | event | on_demand",
  "observation_window": {
    "start": "ISO8601",
    "end": "ISO8601"
  },
  "data_sources": {
    "sqlite_db_path": "string (required)",
    "behavior_feed_path": "string (optional)",
    "workflow_spec_ref": "string (optional, 기대 동작 기준선)"
  },
  "event_trigger": {
    "signal_type": "optional: failure_cluster | retry_spike | bottleneck | human_deferral_loop | rsv_inflation | performance_drift",
    "trigger_event_ids": ["optional"]
  },
  "user_preferences": {
    "review_depth": "summary | detailed",
    "auto_propose": "boolean (default: true)"
  }
}
```

---

## 책임 범위

### In-Scope

- SQLite SoT(`audit_logs`) + behavior feed(JSONL)에서 신호 수집
- 6종 이상 신호(AS) 분류 및 심각도(SS) 판정
- HITL 체크포인트 제시 및 구조화된 피드백 수집
- 구조화된 개선 제안(IP) 생성
- cortex-agora 제안 제출 스테이징
- Evolution Cycle 추적 및 폐루프 메트릭 산출

### Out-of-Scope

- 워크플로우 실행 (AWT 경계)
- topology/execution 직접 수정 (제안만 가능)
- 자동 반영 (수동 요약 export만, DNA 준수)
- behavior feed dual-write (수동 export만)
- COF 티켓 관리 (COF Swarm 영역)

---

## Global Invariants

1. 증거 없는 단정 금지
2. 모든 개선 제안은 `rollback_rule` 포함 필수
3. 로그 SoT는 SQLite, export는 수동 경로만 허용
4. Critical 이상 신호의 48h 무응답 시 `halt_and_escalate_to_audit` (DNA 거버넌스)
5. 실행 계층(COF/Manifestation) 직접 변경 금지
6. 경로/계약 불일치 시 fail-fast

---

## when_unsure 정책

| 상황 | 행동 |
|------|------|
| 이상 신호 분류 불확실 | 낮은 확신도로 기록 + 다음 scheduled checkpoint에서 재검토 |
| 사용자 피드백 모호 | 구체화 질문 제시 + 현 상태 보류 기록 |
| 근본 원인 가설 경합 | 두 가설 모두 제시 + 사용자 판단 요청 |
| 타깃 스킬 불확실 | `operational` 분류 + skill-governance에 메타 검토 요청 |
| 심각도 판단 불확실 | 보수적으로 한 단계 높은 심각도 적용 |
| 제안 효과 불확실 | `low` 확신도 + 사용자 검증 후 제출 조건 부여 |
