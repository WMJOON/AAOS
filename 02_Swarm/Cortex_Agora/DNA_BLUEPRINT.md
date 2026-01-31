---
name: "AAOS-Cortex-Agora"
version: "0.1.0"
scope: "04_Agentic_AI_OS/02_Swarm/Cortex_Agora"
owner: "AAOS Swarm"
created: "2026-01-30"
status: canonical

# Governance (homing instinct)
governance:
  voice: homing_instinct
  mother_ref: "04_Agentic_AI_OS/02_Swarm/DNA_BLUEPRINT.md"
  precedence:
    - "AAOS Canon"
    - "META Doctrine"
    - "Immune Doctrine"
    - "Swarm Root DNA"
    - "This document"
  on_conflict: "halt_and_escalate_to_audit"

# Normative References (inherit Immune System)
canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/METADoctrine.md"
immune_doctrine_reference: "04_Agentic_AI_OS/01_Nucleus/Immune_system/AAOS_DNA_DOCTRINE_RULE.md"
inquisitor_reference: "04_Agentic_AI_OS/01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/01_Nucleus/Immune_system/AUDIT_LOG.md"

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

inquisitor:
  required: true
  audit_log: "../../01_Nucleus/Immune_system/AUDIT_LOG.md"
---
# Cortex_Agora DNA Blueprint

## Mission

Cortex_Agora는 Swarm들이 실제로 “어떻게 행동했는지”를 관찰하고,
반복되는 흐름을 **언어화된 제안**(자동화/룰화 후보)으로 만든다.

## Hard Prohibitions (Non-Execution / Non-Enforcement)

- 실행(외부 도구/API/OS 바인딩) 금지
- 자동 반영(룰/스킬/권한 변경) 금지
- 규칙 수정(직접 편집/승격/배포) 금지
- 에이전트 호출(운영 Swarm 호출, fan-out, sub-agent orchestration) 금지
- Record_Archive 직접 조회 금지

## Inputs

### Behavior Feed (Behavior Trace)

Cortex_Agora의 입력은 “기록(증빙)”이 아니라 “행동(흐름)”이다.

#### Standard Location (권장)

- Swarm별 권장 경로: `<swarm_root>/behavior/BEHAVIOR_FEED.jsonl`
- Cortex_Agora는 Swarm의 Record_Archive 증빙을 보지 않고, 위 Behavior Feed만을 관찰 입력으로 삼는다.

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

## Outputs

Cortex_Agora의 출력은 항상 “관찰 → 해석 → 제안” 순서로만 산출한다.

- 관찰(Observation): 특정 조건에서 특정 선택이 반복됨
- 해석(Interpretation): 자동화/룰화 후보일 가능성(가설)
- 제안(Proposal): 고려할 수 있는 선택지(조건부 자동 호출, 예산 제한, 인간介入 기준 등)

## Escalation Path

제안이 규칙/스킬/기관 DNA 변경을 요구하면, Cortex_Agora는 직접 반영하지 않고
Deliberation Chamber로 승격 입력을 제출한다.
