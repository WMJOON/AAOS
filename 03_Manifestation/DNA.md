---
name: "aaos-manifestation"
version: "0.1.0"
scope: "04_Agentic_AI_OS/03_Manifestation"
created: "2026-01-27"
status: draft

governance:
  voice: homing_instinct
  mother_ref: "04_Agentic_AI_OS/01_Nucleus/immune_system/"
  supremacy: "Manifestation은 Canon/META/Immune 규범을 위반할 수 없다"
  precedence: ["AAOS Canon", "META Doctrine", "Immune Doctrine", "This document"]
  on_conflict: "halt_and_escalate_to_audit"

canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/00_METADoctrine/DNA.md"
immune_doctrine_reference: "04_Agentic_AI_OS/01_Nucleus/immune_system/rules/README.md"
inquisitor_reference: "04_Agentic_AI_OS/01_Nucleus/immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md"

natural_dissolution:
  purpose: "Swarm 의도를 실행 가능한 형태로 현현/접속하고 결과를 환류한다"
  termination_conditions:
    - "해당 Manifestation 런타임/프로바이더가 더 이상 사용되지 않음"
    - "보안/감사 요구를 만족하지 못해 Immune System에 의해 중단 판정"
  dissolution_steps:
    - "실행 로그/결과 요약을 Record Archive로 이관"
    - "권한/토큰/키/세션 등 민감정보 폐기"
    - "런타임/프로세스 종료 및 작업공간 정리"
  retention:
    summary_required: true
    max_days: 30

resource_limits:
  max_files: 200
  max_folders: 50
  max_log_kb: 512

inquisitor:
  required: true
  audit_log: "../01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md"
---
# DNA: Manifestation (Draft)

## Overview

Manifestation은 Swarm의 의도를 **실행 가능한 인터페이스/런타임**으로 변환하고, 그 결과를 Nucleus로 환류한다.

- Must never do:
  - 스스로 목적/정책을 정의하거나 변경하지 않는다.
  - 감사/권한/보존 규범을 우회하지 않는다.

## Execution Contract

- Input: Swarm의 계획/Skill/요청(권한 요청 포함)
- Output: 실행 결과(성공/실패), 로그 요약, 증빙 링크
- Reporting: Record Archive + (필요 시) Immune System/Inquisitor

## Components (Draft)

- Call CLI Agents: `summon-agents/skill/sa-call-cli-agents/DNA.md`
- MCP Manifestations: `summon-agents/mcp/README.md`
