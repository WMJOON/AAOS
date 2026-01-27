---
name: "AAOS-Swarm"
version: "0.1.1"
scope: "04_Agentic_AI_OS/02_Swarm"
owner: "AAOS Canon"
created: "2026-01-21"
status: canonical

# Governance (homing instinct)
governance:
  voice: homing_instinct
  mother_ref: "04_Agentic_AI_OS/01_Nucleus/Immune_system/"
  precedence:
    - "AAOS Canon"
    - "META Doctrine"
    - "Immune Doctrine"
    - "This document"
  on_conflict: "halt_and_escalate_to_audit"

# Normative References (inherit Immune System)
canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/METADoctrine.md"
immune_doctrine_reference: "04_Agentic_AI_OS/01_Nucleus/Immune_system/AAOS_DNA_DOCTRINE_RULE.md"
inquisitor_reference: "04_Agentic_AI_OS/01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/01_Nucleus/Immune_system/AUDIT_LOG.md"

natural_dissolution:
  purpose: "군체(Swarm) 하위 체계(COF/COO 등)가 생성·성장하는 실행 계층의 컨테이너"
  termination_conditions:
    - "AAOS 군체(Swarm) 계층이 구조적으로 대체될 때"
  dissolution_steps:
    - "하위 체계별로 승계 Blueprint/DNA를 확정하고, 본 컨테이너는 요약본만 남긴다"
    - "구 군체(Swarm) 트리는 `_archive/`로 이동 후 정리"
  retention:
    summary_required: true
    max_days: 365

resource_limits:
  max_files: 2000
  max_folders: 300
  max_log_kb: 1024

inquisitor:
  required: true
  audit_log: "../01_Nucleus/Immune_system/AUDIT_LOG.md"
---
# AAOS 군체(Swarm) DNA Blueprint

본 폴더는 군체(Swarm) 계층의 “루트 컨테이너”이며, 하위 체계는 각자 `DNA_BLUEPRINT.md`를 통해 면역체계를 계승한다.

## Version Note

- v0.1.0 : 군체(Swarm) 루트 컨테이너 DNA Blueprint 최초 성문화
- v0.1.1 : governance.voice=homing_instinct 및 mother_ref(모체) 기반 귀속 규칙 추가
