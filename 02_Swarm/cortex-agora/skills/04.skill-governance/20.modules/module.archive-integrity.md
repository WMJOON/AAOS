# Module: Archive Integrity (Phase 2)

## 목적

change_archive 3개 JSONL 이벤트 로그의 스키마 준수, 참조 무결성(CC-01~CC-03),
bridge script 명령 coverage, CHANGE_INDEX 일관성, append-only/단조증가 불변조건을 점검한다.

## 입력

- `change_archive/events/CHANGE_EVENTS.jsonl`
- `change_archive/events/PEER_FEEDBACK.jsonl`
- `change_archive/events/IMPROVEMENT_DECISIONS.jsonl`
- `change_archive/indexes/CHANGE_INDEX.md`
- `scripts/change_archive_bridge.py`
- `change_archive/templates/` (3개 YAML 템플릿)

---

## Checklist: CHANGE_EVENTS.jsonl 스키마

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| AE-01 | 각 행이 유효한 JSON | parseable | FAIL |
| AE-02 | Required fields 존재: `event_id`, `ts`, `proposal_id`, `change_type`, `actor`, `source_snapshot`, `artifact_ref`, `status` | 템플릿 기준 전체 존재 | FAIL |
| AE-03 | `change_type` enum 준수 | created / updated / superseded / withdrawn / sealed | FAIL |
| AE-04 | `status` enum 준수 | open / improving / closed / sealed | FAIL |
| AE-05 | `source_snapshot.agora_ref` 존재 | DNA mandate: required | FAIL |
| AE-06 | `source_snapshot.captured_at` ISO-8601 | valid timestamp | FAIL |
| AE-07 | `event_id` 파일 내 고유 | no duplicates | FAIL |
| AE-08 | `ts` ISO-8601 형식 | valid | WARN |

---

## Checklist: PEER_FEEDBACK.jsonl 스키마

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| AF-01 | 각 행이 유효한 JSON | parseable | FAIL |
| AF-02 | Required fields 존재: `feedback_id`, `ts`, `proposal_id`, `reviewer`, `reviewer_model_family`, `reviewer_provider`, `stance`, `summary`, `linked_event_id` | 전체 존재 | FAIL |
| AF-03 | `stance` enum 준수 | critique / suggestion / endorsement | FAIL |
| AF-04 | `linked_event_id` → `CHANGE_EVENTS.event_id` 참조 존재 **(CC-02)** | referential integrity | FAIL |
| AF-05 | `feedback_id` 파일 내 고유 | no duplicates | FAIL |
| AF-06 | `reviewer_model_family` 비어있지 않음 | populated | WARN |
| AF-07 | `reviewer_provider` 비어있지 않음 | populated | WARN |
| AF-08 | `ts` 단조 증가 | monotonic within file | WARN |

---

## Checklist: IMPROVEMENT_DECISIONS.jsonl 스키마

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| AD-01 | 각 행이 유효한 JSON | parseable | FAIL |
| AD-02 | Required fields 존재: `decision_id`, `ts`, `proposal_id`, `decision`, `rationale`, `applied_event_ids`, `feedback_refs`, `next_action` | 전체 존재 | FAIL |
| AD-03 | `decision` enum 준수 | accepted / partially_accepted / deferred / rejected | FAIL |
| AD-04 | `feedback_refs[]` 각 항목 → `PEER_FEEDBACK.feedback_id` 참조 존재 **(CC-03)** | referential integrity | WARN |
| AD-05 | `applied_event_ids[]` 각 항목 → `CHANGE_EVENTS.event_id` 참조 존재 | referential integrity | WARN |
| AD-06 | `decision_id` 파일 내 고유 | no duplicates | FAIL |
| AD-07 | `ts` 단조 증가 | monotonic within file | WARN |

---

## Checklist: Bridge Script 명령 Coverage

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| AB-01 | `record-change` 서브커맨드 정의 | bridge에 존재 | FAIL |
| AB-02 | `record-feedback` 서브커맨드 정의 | bridge에 존재 | FAIL |
| AB-03 | `record-decision` 서브커맨드 정의 | bridge에 존재 | FAIL |
| AB-04 | `build-package` 서브커맨드 정의 | bridge에 존재 | FAIL |
| AB-05 | `seal-to-record-archive` 서브커맨드 정의 | bridge에 존재 | FAIL |
| AB-06 | `assert_monotonic_ts` 및 `assert_unique_id` 함수 존재 | invariant enforcement 구현 | WARN |

---

## Checklist: CHANGE_INDEX.md 일관성

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| AI-01 | 각 `proposal_id`가 CHANGE_EVENTS에 존재 | referential integrity | WARN |
| AI-02 | `latest_change_event_id`가 해당 proposal의 최신 이벤트와 일치 | consistent | WARN |
| AI-03 | `feedback_count`가 PEER_FEEDBACK 실제 카운트와 일치 | count match | WARN |
| AI-04 | `last_decision`이 IMPROVEMENT_DECISIONS 최신 결정과 일치 | consistent | WARN |
| AI-05 | 기존 항목 변조 없음 (append-only) | no mutation | FAIL |

---

## Checklist: Append-Only / 단조증가 불변조건

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| AM-01 | 3개 JSONL 파일 행 수 >= 이전 점검 시점 | non-decreasing | FAIL |
| AM-02 | 3개 JSONL 파일 `ts` 단조 증가 | ts_n >= ts_{n-1} | WARN |
| AM-03 | CHANGE_INDEX 항목 수 >= 이전 점검 시점 | non-decreasing | WARN |
| AM-04 | `event_id` / `feedback_id` / `decision_id` 전역 재사용 없음 | global uniqueness | FAIL |

---

## 산출물

`governance_check_report.archive_integrity_checks` 섹션에 기록.

## When Unsure

- JSONL 필드가 존재하지만 값이 빈 문자열/null인 경우: WARN + "empty value" 명시.
- 이전 점검 시점 데이터가 없는 경우 (최초 점검): AM-01/AM-03 SKIP, 현재 값 기록.
- bridge에 미사용 서브커맨드가 있는 경우: WARN + "untested command path" 기록.
