---
name: "AAOS-COO"
version: "0.1.0"
scope: "04_Agentic_AI_OS/04_AAOS-Swarm/02_context-orchestrated-ontology"
owner: "AAOS Swarm"
created: "2026-01-21"
status: draft

# Normative References (inherit Immune System)
canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/METADoctrine.md"
immune_doctrine_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/AAOS_DNA_DOCTRINE_RULE.md"
inquisitor_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/AUDIT_LOG.md"

natural_dissolution:
  purpose: "온톨로지 기반 Context/Knowledge Graph 구조를 표준화하기 위한 군체(Swarm) 계층(초기 스캐폴드)"
  termination_conditions:
    - "COO가 다른 표준으로 대체될 때"
    - "COO DNA/Rule가 별도 버전 폴더로 분리·승계될 때"
  dissolution_steps:
    - "정식 COO DNA/Rule 문서로 승계 후, 본 스캐폴드 폴더는 요약본만 남기고 `_archive/`로 이동"
    - "불필요 파일 삭제"
  retention:
    summary_required: true
    max_days: 90

resource_limits:
  max_files: 200
  max_folders: 40
  max_log_kb: 256

inquisitor:
  required: true
  audit_log: "../../02_AAOS-Immune_system/AUDIT_LOG.md"
---
# AAOS-COO DNA Blueprint (draft)

본 폴더는 COO 체계의 “시작점”이며, 정식 DNA/Rule 문서가 확정되면 별도 버전 구조로 승계한다.
