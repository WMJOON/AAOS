---
name: "AAOS-COF"
version: "0.1.3"
scope: "04_Agentic_AI_OS/02_Swarm/01_context-orchestrated-filesystem/COF v0.1.3"
owner: "AAOS Swarm"
created: "2026-01-22"
status: canonical

# Normative References (inherit Immune System)
canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/METADoctrine.md"
immune_doctrine_reference: "04_Agentic_AI_OS/01_Nucleus/Immune_system/AAOS_DNA_DOCTRINE_RULE.md"
inquisitor_reference: "04_Agentic_AI_OS/01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/01_Nucleus/Immune_system/AUDIT_LOG.md"

natural_dissolution:
  purpose: "트리 기반 파일 워크스페이스에서 노드 구조/맥락/기록 규칙을 표준화하여 작업 연속성을 유지한다"
  termination_conditions:
    - "COF가 군체(Swarm) 표준에서 폐기/대체될 때"
    - "해당 COF 버전(v0.1.3)이 상위 버전으로 승계되어 더 이상 사용되지 않을 때"
  dissolution_steps:
    - "상위 버전/대체 군체(Swarm)로 마이그레이션 가이드 작성"
    - "필수 규칙/템플릿 요약을 `README.md`에 남기고 `_archive/`로 아카이브"
    - "구버전 스킬/스크립트는 `_archive/`로 이동 후 삭제"
  retention:
    summary_required: true
    max_days: 180

resource_limits:
  max_files: 800
  max_folders: 120
  max_log_kb: 512

inquisitor:
  required: true
  audit_log: "../../../01_Nucleus/Immune_system/AUDIT_LOG.md"
---
# AAOS-COF DNA Blueprint (v0.1.3)

## Overview

- What it is: Context-Orchestrated Filesystem (COF) 규칙/스킬 묶음
- Doctrine: `COF_DOCTRINE.md` (4 Pillars of COF)
- DNA: `DNA.md` (Rule/Skill/Lifecycle 통합 정의)
- Rule: `rule/context-orchestrated-filesystem.md`
- Skills: `skills/` (예: task-manager node 생성/티켓 발행/아카이빙)

## Growth Rules

- 새로운 노드 구조/티켓 스키마 추가는 `rule/`의 규칙과 함께 업데이트한다.
- 신규 자동화 스크립트 추가 시 `resource_limits`를 초과하지 않도록 한다.

## Dissolution Procedure

Natural Dissolution에 따라 구버전이 되면:
1. 상위 버전으로 승계 문서화
2. 핵심 규칙/사용법 요약 후 아카이브
3. 구버전 파일 정리
