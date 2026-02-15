---
name: "AAOS-Cortex-Agora"
version: "0.1.5"
scope: "04_Agentic_AI_OS/02_Swarm/cortex-agora"
owner: "AAOS Swarm"
created: "2026-01-30"
status: canonical

# Governance (homing instinct)
governance:
  voice: homing_instinct
  mother_ref: "04_Agentic_AI_OS/02_Swarm/DNA.md"
  precedence:
    - "AAOS Canon"
    - "META Doctrine"
    - "Immune Doctrine"
    - "Swarm Root DNA"
    - "This document"
  on_conflict: "halt_and_escalate_to_audit"

# Normative References (inherit Immune System)
canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/00_METADoctrine/DNA.md"
immune_doctrine_reference: "04_Agentic_AI_OS/01_Nucleus/immune_system/rules/README.md"
inquisitor_reference: "04_Agentic_AI_OS/01_Nucleus/immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md"

downstream_consumption:
  role: "workspace_observer"
  output_priority: "cortex_agora_output_first"
  transfer_mode: "pull_download"
  primary_consumer: "02_Swarm/context-orchestrated-workflow-intelligence"
  reusable_consumers:
    - "01_Nucleus/deliberation_chamber"
    - "02_Swarm/context-orchestrated-filesystem"
    - "02_Swarm/agentic-workflow-topology"
  required_source_snapshot_fields:
    - "agora_ref"
    - "captured_at"

change_archive:
  enabled: true
  append_only: true
  format: "md_with_frontmatter"
  format_version: "v2"
  optional_critique_gate: true
  bridge_mode: "stage_then_seal"
  paths:
    root: "02_Swarm/cortex-agora/records"
    change_events: "02_Swarm/cortex-agora/records/change_events/"
    peer_feedback: "02_Swarm/cortex-agora/records/peer_feedback/"
    improvement_decisions: "02_Swarm/cortex-agora/records/improvement_decisions/"
  legacy_paths:
    root: "02_Swarm/cortex-agora/change_archive"
    change_events: "02_Swarm/cortex-agora/change_archive/events/CHANGE_EVENTS.jsonl"
    peer_feedback: "02_Swarm/cortex-agora/change_archive/events/PEER_FEEDBACK.jsonl"
    improvement_decisions: "02_Swarm/cortex-agora/change_archive/events/IMPROVEMENT_DECISIONS.jsonl"
    change_index: "02_Swarm/cortex-agora/change_archive/indexes/CHANGE_INDEX.md"
  legacy_frozen: true
  bridge_script: "02_Swarm/cortex-agora/scripts/change_archive_bridge.py"
  record_writer: "02_Swarm/cortex-agora/scripts/record_writer.py"
  bases_views:
    default: "02_Swarm/cortex-agora/dashboard/cortex-agora-records.base"
    proposal_tracker: "02_Swarm/cortex-agora/dashboard/all-proposals.base"
    proposal_hitl_tracker: "02_Swarm/cortex-agora/dashboard/proposals.base"
    report_tracker: "02_Swarm/cortex-agora/dashboard/reports.base"
  proposal_hitl_policy:
    checked_field: "checked"
    hide_closed_in_dashboard: true
    auto_progress_condition: "hitl_stage=approval_required AND checked=true AND auto_flow_enabled=true"
    auto_progress_script: "02_Swarm/cortex-agora/scripts/proposal_hitl_auto_flow.py"
  record_archive_target: "01_Nucleus/record_archive/_archive/operations/<timestamp>__swarm-observability__cortex-agora-change-review/"

natural_dissolution:
  purpose: "Swarm 행동(Behavior Trace)을 관찰·요약하고 개선 제안을 생성하는 관찰/제안 군체"
  termination_conditions:
    - "Swarm 관찰 기능이 다른 표준 군체로 대체될 때"
    - "행동 수집 입력(Behavior Feed)이 중단되어 목적이 소멸할 때"
  dissolution_steps:
    - "관찰 산출물을 요약본으로 남기고, 필요 시 Nucleus Deliberation으로 승계한다"
    - "구 출력물은 `_archive/`로 이동 후 정리한다"
  retention:
    summary_required: true
    max_days: 365

resource_limits:
  max_files: 1200
  max_folders: 200
  max_log_kb: 512
observability:
  behavior_feed:
    enabled: true
    required: true
    source: "swarm_runtime"
    format: "md_with_frontmatter"
    format_version: "v2"
    path: "02_Swarm/cortex-agora/records/behavior/"
    legacy_path: "02_Swarm/cortex-agora/behavior/BEHAVIOR_FEED.jsonl"
    legacy_frozen: true
    record_writer: "02_Swarm/cortex-agora/scripts/record_writer.py"
    bases_view: "02_Swarm/cortex-agora/dashboard/cortex-agora-records.base"
    recommended_fields:
      - event_id
      - ts
      - swarm_id
      - group_id
      - actor
      - kind
      - context_task_id
      - outcome_status
      - trace_id   # optional; backward compatibility
    retention_days: 365
    schema_version: "v2"
    sink: "02_Swarm/cortex-agora/records (stage_then_seal -> 01_Nucleus/record_archive)"

inquisitor:
  required: true
  audit_log: "../../01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md"
---
# cortex-agora DNA

## Mission

cortex-agora는 Swarm들이 실제로 “어떻게 행동했는지”를 관찰하고,
반복되는 흐름을 **언어화된 제안**(자동화/룰화 후보)으로 만든다.
또한 workspace 중심 관찰자로서, downstream 계층(COWI 포함)의 재사용 가능한 출력 기준점을 제공한다.

## Hard Prohibitions (Non-Execution / Non-Enforcement)

- 실행(외부 도구/API/OS 바인딩) 금지
- 자동 반영(룰/스킬/권한 변경) 금지
- 규칙 수정(직접 편집/승격/배포) 금지
- 에이전트 호출(운영 Swarm 호출, fan-out, sub-agent orchestration) 금지
- record_archive 직접 조회 금지

## Inputs

### Behavior Feed (Behavior Trace)

cortex-agora의 입력은 “기록(증빙)”이 아니라 “행동(흐름)”이다.
Behavior Feed는 Agora-First 경로를 통해 수집하며, direct record_archive sink를 허용하지 않는다.

#### Standard Location (권장)

- Swarm별 권장 경로: `<swarm_root>/behavior/BEHAVIOR_FEED.jsonl`
- cortex-agora는 Swarm의 record_archive 증빙을 보지 않고, 위 Behavior Feed만을 관찰 입력으로 삼는다.

최소 이벤트(권장) 스키마:

```yaml
behavior_event:
  event_id: string
  ts: string               # ISO-8601
  swarm_id: string
  group_id: string
  actor: string            # agent_id | human | system
  kind: string             # plan|tool_call|subagent|model_select|gate|stop|retry|handoff
  context:
    task_id: string
    session_id: string
  outcome:
    status: string         # success|fail|halt|escalate
    human_intervention: boolean
```

스키마 정렬 원칙:

- canonical grouping key는 `group_id`를 사용한다.
- `trace_id`는 하위 호환(backward compatibility) 목적으로만 병행 허용한다.

## Outputs

cortex-agora의 출력은 항상 “관찰 → 해석 → 제안” 순서로만 산출한다.

- 관찰(Observation): 특정 조건에서 특정 선택이 반복됨
- 해석(Interpretation): 자동화/룰화 후보일 가능성(가설)
- 제안(Proposal): 고려할 수 있는 선택지(조건부 자동 호출, 예산 제한, 인간介入 기준 등)

### Consumption Contract (downstream)

- downstream 계층은 cortex-agora 출력 참조(`agora_ref`)를 source-of-truth로 취급한다.
- `context-orchestrated-workflow-intelligence`는 위 출력을 우선 입력으로 사용해
  `skill_usage_adaptation_report.source_snapshot`을 구성한다.
- cortex-agora는 출력만 제공하며, COF/AWT 실행/자동반영은 수행하지 않는다.

## Change Archive Policy

- cortex-agora는 변경/비판/개선 이벤트를 로컬 append-only로 기록한다.
- 비판은 optional이며 상태 전환의 필수 차단 게이트가 아니다.
- 장기 immutable 보존은 Nucleus `record_archive`가 담당하고,
  cortex-agora는 `change_archive_bridge.py`로 stage package를 봉인 요청한다.
- 기록 이벤트의 source snapshot은 `agora_ref`, `captured_at`를 포함해야 한다.
- `stage_then_seal`이 완료된 `record_archive` 엔트리만 장기 immutable SoT로 간주한다.

## Escalation Path

제안이 규칙/스킬/기관 DNA 변경을 요구하면, cortex-agora는 직접 반영하지 않고
Deliberation Chamber로 승격 입력을 제출한다.

## Version Note

- v0.1.3 : Agora-First 입력/봉인 정책 명문화 및 observability sink를 `change_archive -> record_archive seal` 경로로 정렬
- v0.1.4 : Behavior Feed canonical 필드를 `group_id`로 정렬하고 `trace_id`를 호환 필드로 격하
- v0.1.5 : Record Format v2(Obsidian Bases) — JSONL → 개별 .md + YAML frontmatter 전환, `.base` 뷰 도입, CHANGE_INDEX.md 제거
