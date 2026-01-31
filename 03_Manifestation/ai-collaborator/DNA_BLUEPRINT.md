---
name: "AAOS-Manifestation-AI-Collaborator"
version: "0.1.0"
scope: "04_Agentic_AI_OS/03_Manifestation/ai-collaborator"
owner: "AAOS Swarm"
created: "2026-01-31"
status: draft

governance:
  voice: homing_instinct
  mother_ref: "04_Agentic_AI_OS/03_Manifestation/DNA_BLUEPRINT.md"
  precedence: ["AAOS Canon", "META Doctrine", "Immune Doctrine", "Manifestation DNA", "This document"]
  on_conflict: "halt_and_escalate_to_audit"

# Normative References (inherit Immune System)
canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/METADoctrine.md"
immune_doctrine_reference: "04_Agentic_AI_OS/01_Nucleus/Immune_system/AAOS_DNA_DOCTRINE_RULE.md"
inquisitor_reference: "04_Agentic_AI_OS/01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/01_Nucleus/Immune_system/AUDIT_LOG.md"

natural_dissolution:
  purpose: "외부 AI CLI 실행을 표준 인터페이스로 묶어 Swarm의 검토/비교 작업을 현현하고 결과를 정규화한다"
  termination_conditions:
    - "대상 CLI(예: codex/claude/gemini) 인터페이스가 변경되어 유지 불가"
    - "보안/감사 요구를 만족하지 못해 Immune System에 의해 중단 판정"
  dissolution_steps:
    - "실행 결과/요약 산출물 경로를 Record Archive로 이관(필요 시)"
    - "로컬에 남은 progress/resume 파일 정리"
    - "실행 바인딩 문서/사용법을 요약 후 `_archive/`로 이동"
  retention:
    summary_required: true
    max_days: 30

resource_limits:
  max_files: 500
  max_folders: 80
  max_log_kb: 512

inquisitor:
  required: true
  audit_log: "../../01_Nucleus/Immune_system/AUDIT_LOG.md"
---
# DNA BLUEPRINT: AI Collaborator (Manifestation Component)

## Overview

AI Collaborator는 여러 AI CLI(Codex/Claude/Gemini 등)를 병렬 실행하고 결과를 정규화하는 Manifestation 컴포넌트이다.

- Canonical payload: `ai-collaborator_v0.3/`

## Hard Prohibitions

- 스스로 목표/정책을 생성하지 않는다(Non-Cognition).
- `AUDIT_LOG.md` 등 불변 로그를 수정하지 않는다(append-only 규범 준수).
- 토큰/키/민감정보를 문서에 하드코딩하지 않는다.

## Execution Contract

- Input: Swarm가 제공하는 `tasks/prompts/context file path`
- Output: 실행 결과(원문/정규화), 실패 사유, 재시도/중단 신호
- Reporting: 필요 시 상위 워크플로우가 Record Archive/Immune System에 증빙을 남긴다

