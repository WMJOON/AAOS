---
name: "AAOS-COF-Container"
version: "0.1.0"
scope: "04_Agentic_AI_OS/04_AAOS-Swarm/01_context-orchestrated-filesystem"
owner: "AAOS Swarm"
created: "2026-01-21"
status: canonical

# Normative References (inherit Immune System)
canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/METADoctrine.md"
immune_doctrine_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/AAOS_DNA_DOCTRINE_RULE.md"
inquisitor_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/AUDIT_LOG.md"

natural_dissolution:
  purpose: "COF 버전 폴더들을 보관/승계하는 컨테이너"
  termination_conditions:
    - "COF가 군체(Swarm) 표준에서 완전히 폐기될 때"
  dissolution_steps:
    - "최신 승계 버전만 남기고 구버전은 `_archive/`로 이동"
    - "컨테이너 README에 승계 경로를 남긴다"
  retention:
    summary_required: true
    max_days: 365

resource_limits:
  max_files: 1200
  max_folders: 200
  max_log_kb: 512

inquisitor:
  required: true
  audit_log: "../../02_AAOS-Immune_system/AUDIT_LOG.md"
---
# COF Container Blueprint

본 폴더는 COF 버전별 구현을 담는 컨테이너이며, 각 버전 폴더는 별도의 `DNA_BLUEPRINT.md`를 가진다.
