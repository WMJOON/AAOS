---
name: "AAOS-Deliberation-Chamber"
version: "0.1.1"
scope: "04_Agentic_AI_OS/03_AAOS-Deliberation_Chamber"
owner: "AAOS Canon"
created: "2026-01-22"
status: canonical

# Governance (homing instinct)
governance:
  voice: homing_instinct
  mother_ref: "04_Agentic_AI_OS/METADoctrine.md"
  sibling_ref: "04_Agentic_AI_OS/02_AAOS-Immune_system/"
  precedence:
    - "AAOS Canon"
    - "Record Archive"
    - "META Doctrine"
    - "This document (Deliberation Chamber)"
    - "Immune Doctrine (sibling, not parent)"
  on_conflict: "halt_then_home_to_meta_doctrine"

# Normative References
canon_reference: "04_Agentic_AI_OS/README.md"
record_archive_reference: "04_Agentic_AI_OS/01_AAOS-Record_Archive/"
meta_doctrine_reference: "04_Agentic_AI_OS/METADoctrine.md"
immune_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/"
immune_doctrine_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/AAOS_DNA_DOCTRINE_RULE.md"
inquisitor_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/AUDIT_LOG.md"
meta_audit_log_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/META_AUDIT_LOG.md"

natural_dissolution:
  purpose: "Multi-Agent 합의와 인간 승인(서명)의 '숙의/정리/증빙'을 담당하는 기관. 결론을 강제하지 않고, Immune System/Inquisitor의 판정 입력을 정리한다."
  termination_conditions:
    - "META Doctrine이 합의/숙의 절차를 다른 기관으로 이관할 때"
  dissolution_steps:
    - "숙의 산출물(요약/결론/근거)을 Record Archive로 이관한다"
    - "활성 세션을 종료하고, 잔여 초안은 time_bound에 따라 폐기한다"
  retention:
    summary_required: true
    max_days: 365

resource_limits:
  max_files: 500
  max_folders: 50
  max_log_kb: 512

inquisitor:
  required: true
  audit_log: "../02_AAOS-Immune_system/AUDIT_LOG.md"
---

# AAOS Deliberation Chamber (DNA Blueprint)

## Overview

Deliberation Chamber는 “합의가 어떻게 만들어졌는지”를 구조화하는 기관이다.
기본 적용 범위: 군체(Swarm) 이상 상위기관의 DNA 변경 및 META Doctrine 변경(상위 변경 게이트).

- Input: 변경 제안(DNA_BLUEPRINT), 위험/영향 분석, 각 Agent의 verdict/rationale
- Output: 합의 요약(승인/거부/수정요청), 근거, 증빙 링크(Record Archive), 최종 승인 요청 패킷

권장 산출물 형식:
- `multi-agent-consensus` 기록 (verdict/rationale/model_id 포함; Immune Doctrine의 기록 스키마와 정렬)
- `permission-request` 또는 `blueprint-judgment` 요청 패킷 (집행/판정은 Immune System/Inquisitor)

## Hard Rules

- 본 기관은 집행/차단 권한을 갖지 않는다. (심판/집행은 Immune System/Inquisitor)
- 모든 산출물은 Record Archive에 보존 가능한 형태로 남겨야 한다.
- 충돌/불명확/권한 경계 감지 시 META Doctrine(METADoctrine.md)으로 귀속한다(homing_instinct).
- Immune System과는 동급 기관(sibling)이며, 상호 참조는 가능하나 상하 관계가 아니다.

## Version Note

- v0.1.0 : Deliberation Chamber DNA Blueprint 최초 성문화
- v0.1.1 : governance 구조 수정 - mother_ref를 META Doctrine으로 변경, Immune System은 sibling으로 명시, on_conflict를 halt_then_home_to_meta_doctrine으로 변경
