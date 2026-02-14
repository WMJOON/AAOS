---
name: "aaos-manifestation-summon-agents"
version: "0.1.0"
scope: "04_Agentic_AI_OS/03_Manifestation/summon-agents"
owner: "AAOS Manifestation"
created: "2026-02-14"
status: canonical

# Governance
precedence:
  - "AAOS Canon"
  - "META Doctrine"
  - "Immune Doctrine"
  - "03_Manifestation/DNA.md"
  - "This document"

governance:
  voice: homing_instinct
  mother_ref: "04_Agentic_AI_OS/03_Manifestation/"
  on_conflict: "halt_and_escalate_to_audit"

# Normative References
canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/00_METADoctrine/DNA.md"
immune_doctrine_reference: "04_Agentic_AI_OS/01_Nucleus/immune_system/rules/README.md"
inquisitor_reference: "04_Agentic_AI_OS/01_Nucleus/immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md"

natural_dissolution:
  purpose: "외부 런타임/CLI/MCP를 통해 Manifestation 집행을 제공하는 경계 모듈"
  termination_conditions:
    - "런타임 바인딩이 전면 대체되거나 중단될 때"
    - "보안/권한 준수가 장기 위반되어 감사로 중지될 때"
  dissolution_steps:
    - "실행 바인딩을 `_archive/`로 이전"
    - "감사/토큰/세션 흔적 정리 및 재발 방지 체크리스트 이행"
  retention:
    summary_required: true
    max_days: 90

resource_limits:
  max_files: 80
  max_folders: 30
  max_log_kb: 256

inquisitor:
  required: true
  audit_log: "../../01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md"
observability:
  behavior_feed:
    enabled: true
    required: true
    source: "manifestation_runtime"
    path: "03_Manifestation/summon-agents/behavior/BEHAVIOR_FEED.jsonl"
    required_fields:
      - event_id
      - ts
      - swarm_id
      - actor
      - kind
      - context
      - outcome
      - severity
    retention_days: 90
    schema_version: "v1"
    sink: "01_Nucleus/record_archive"
---
# summon-agents DNA

`summon-agents`는 Manifestation 계층에서 외부 실행 바인딩을 제공하는 모듈이다.
Skill/MCP 경로를 통해 에이전트 인스턴스화, 실행 호출, 결과 환류를 수행한다.

## Mission

- 외부 실행 런타임을 안전하게 호출한다.
- 실행 바인딩을 관측 가능한 방식으로 설계해 결과를 Nucleus에 환류한다.
- `README.md`, `SKILL.md`, `MCP` 실행 산출물 간 정합성을 유지한다.

## Core Obligations

1. 실행은 Canon/META/Immune 규약 외부로 나가지 않는다.
2. 외부 바인딩 변경은 감사 로그와 인수인계 기록을 남긴다.
3. Skill은 실행 중심이 아니라 운영 재현성 중심으로 설계한다.
4. Record archive로 돌아가는 결과는 추적 가능해야 한다.

## Boundaries

- 자동으로 규칙/권한을 수정하지 않는다.
- 실행 실패/중단 시 Escalation Path를 통해 Nucleus/Immune로 상향한다.
- 외부 시스템 호출 전후 상태는 각 구성요소가 각자의 문서(frontmatter/로그)에서 입증한다.

## Components

- `skill/sa-call-cli-agents`: CLI 호출/작업 분배 바인딩
- `mcp/sa-call-cli-agents-mcp`: MCP 인터페이스 바인딩
- `mcp/MCP-MANIFESTATION-TEMPLATE.md`: 실행 계약 템플릿
