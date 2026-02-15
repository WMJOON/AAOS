# Module: Consumption Contract (Phase 3)

## 목적

BEHAVIOR_FEED.jsonl 스키마 준수, COWI pull interface 계약(CC-05),
cross-swarm recording completeness를 점검한다.

## 입력

- `behavior/BEHAVIOR_FEED.jsonl`
- cortex-agora `DNA.md` (observability / downstream_consumption 섹션)
- cortex-agora `README.md` (Output Consumption Model)
- COWI `skills/00.agora-consumption-bridge/SKILL.md`
- COWI `skills/00.agora-consumption-bridge/scripts/pull_agora_feedback.py`

---

## Checklist: BEHAVIOR_FEED.jsonl 스키마

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| BF-01 | 각 행이 유효한 JSON | parseable | FAIL |
| BF-02 | Required fields: `event_id`, `ts`, `swarm_id`, `group_id`, `actor`, `kind`, `context`, `outcome` | DNA recommended_fields 기준 | FAIL |
| BF-03 | `group_id` 존재 | canonical grouping key (v0.1.4) | FAIL |
| BF-04 | `trace_id` 처리 | optional backward-compat, primary 아님 | WARN |
| BF-05 | `kind` enum 준수 | plan / tool_call / subagent / model_select / gate / stop / retry / handoff | WARN |
| BF-06 | `outcome.status` enum 준수 | success / fail / halt / escalate | WARN |
| BF-07 | `outcome.human_intervention` 타입 | boolean | WARN |
| BF-08 | `context.task_id` 및 `context.session_id` 존재 | structural completeness | WARN |
| BF-09 | `event_id` 파일 내 고유 | no duplicates | FAIL |
| BF-10 | `ts` ISO-8601 형식 | valid timestamp | WARN |

---

## Checklist: COWI Pull Interface 계약 (CC-05)

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| CP-01 | COWI `pull_agora_feedback.py` 스크립트 존재 | 파일 present | FAIL |
| CP-02 | COWI 스크립트가 `IMPROVEMENT_DECISIONS`를 입력 소스로 참조 | documented dependency | FAIL |
| CP-03 | COWI cursor 메커니즘 존재 | `AGORA_PULL_STATE.json` 또는 equivalent | WARN |
| CP-04 | cortex-agora README에 COWI pull trigger 정의 | "IMPROVEMENT_DECISIONS 신규 + 일일 배치 1회" | WARN |
| CP-05 | cortex-agora README에 COWI runbook 경로 명시 | 실제 경로와 일치 | WARN |
| CP-06 | `IMPROVEMENT_DECISIONS`의 `source_snapshot.agora_ref`가 COWI 소비 가능 형식 | format compatibility **(CC-05)** | FAIL |
| CP-07 | COWI `cowi-agora-consumption-bridge` SKILL.md 존재 | skill present | WARN |
| CP-08 | COWI skill trigger가 agora output 주기와 정렬 | documented alignment | WARN |

---

## Checklist: Cross-Swarm Recording Completeness

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| XR-01 | DNA `downstream_consumption.primary_consumer` = COWI | `context-orchestrated-workflow-intelligence` | FAIL |
| XR-02 | DNA `downstream_consumption.reusable_consumers`에 알려진 소비자 포함 | deliberation_chamber, COF, AWT | WARN |
| XR-03 | BEHAVIOR_FEED에 최소 1개 이벤트 존재 (또는 multi-swarm 대응 준비) | bootstrap entry 이상 | WARN |
| XR-04 | behavior_feed 활성화된 swarm에 대한 cortex-agora 기록 존재 | observable coverage | WARN |
| XR-05 | DNA `observability.behavior_feed.recommended_fields`와 실제 피드 스키마 일치 | field match | WARN |
| XR-06 | `schema_version`이 DNA와 실제 피드 형식 간 일치 | `v1` | WARN |

---

## 산출물

`governance_check_report.consumption_contract_checks` 섹션에 기록.

## When Unsure

- COWI pull 주기가 문서화되었지만 실행 증빙이 없는 경우: WARN + "manual verification required".
- BEHAVIOR_FEED가 cortex-agora 자체만 기록하고 타 swarm 이벤트가 없는 경우: WARN + "multi-swarm collection not yet initiated".
- COWI 스크립트가 존재하지만 agora_ref 형식을 명시적으로 파싱하지 않는 경우: WARN + 형식 호환성 수동 확인 요청.
