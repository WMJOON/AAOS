---
name: "AAOS-COF"
version: "0.1.4"
scope: "04_Agentic_AI_OS/02_Swarm/context-orchestrated-filesystem"
owner: "AAOS Swarm"
created: "2026-01-22"
status: canonical

# Normative References (inherit Immune System)
canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/00_METADoctrine/DNA.md"
immune_doctrine_reference: "04_Agentic_AI_OS/01_Nucleus/immune_system/rules/cof-environment-set.md"
observability:
  behavior_feed:
    enabled: true
    required: true
    source: "swarm_runtime"
    path: "02_Swarm/context-orchestrated-filesystem/behavior/BEHAVIOR_FEED.jsonl"
    min_required_fields:
      - event_id
      - ts
      - swarm_id
      - actor
      - kind
      - context
      - outcome
      - scope
    retention_days: 180
    schema_version: "v1"
    sink: "02_Swarm/cortex-agora (Agora-First); 01_Nucleus/record_archive via change_archive seal"
inquisitor_reference: "04_Agentic_AI_OS/01_Nucleus/immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md"

natural_dissolution:
  purpose: "트리 기반 파일 워크스페이스에서 노드 구조/맥락/기록 규칙을 표준화하여 작업 연속성을 유지한다"
  termination_conditions:
    - "COF가 군체(Swarm) 표준에서 폐기/대체될 때"
    - "해당 COF 버전(v0.1.4)이 상위 버전으로 승계되어 더 이상 사용되지 않을 때"
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
  audit_log: "../../01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md"
---

# AAOS-COF DNA (v0.1.4)

본 DNA는 `COF v0.1.4` 군체(Swarm) 구조를 정의하는 핵심 유전체(Genome)이다.
META Doctrine(DNA.md) 및 **COF Doctrine**에 의거하여 작성되었다.

## 0. Doctrine Genome
- **Pointer**: `core-docs/COF_DOCTRINE.md`
- **Desc**: 4 Pillars of COF Philosophy (Locality, Self-Desc, Agent-First, Lifecycle)

## 1. Rule Genome
- **Pointer**: `rules/cof-environment-set.md`
- **Desc**: Skill-Mediated Creation Mandate

## 2. Skill Genome
- **Pointer**: `skills/`
- **Desc**: `cof-task-manager-node` (creation, ticket, archive, validate)

## 3. Lifecycle Genome
- **Pointer**: `DNA.md`
- **Desc**: Natural Dissolution & Resource Limits

## 4. Observability Routing Contract
- Behavior Feed는 Agora-First 경로(`02_Swarm/cortex-agora`)를 따른다.
- direct `record_archive` sink는 허용하지 않으며, 장기 immutable SoT는 `change_archive seal` 결과로 취급한다.

## Version Note
- v0.1.4 : observability sink를 Agora-First 정책으로 정렬하고 direct record_archive sink 금지 규칙을 추가

---
> "See referenced files for full definitions."
