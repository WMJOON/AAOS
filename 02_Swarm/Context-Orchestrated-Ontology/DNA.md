---
name: "AAOS-COO"
version: "0.1.0"
scope: "04_Agentic_AI_OS/02_Swarm/context-orchestrated-ontology"
owner: "AAOS Swarm"
created: "2026-02-14"
status: canonical

# Governance (homing instinct)
governance:
  voice: homing_instinct
  mother_ref: "04_Agentic_AI_OS/02_Swarm/"
  precedence:
    - "AAOS Canon"
    - "META Doctrine"
    - "Immune Doctrine"
    - "Swarm Root DNA"
    - "This document"
  on_conflict: "halt_and_escalate_to_audit"

# Normative References
canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/00_METADoctrine/DNA.md"
immune_doctrine_reference: "04_Agentic_AI_OS/01_Nucleus/immune_system/rules/README.md"
inquisitor_reference: "04_Agentic_AI_OS/01_Nucleus/immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md"

natural_dissolution:
  purpose: "Context-Orchestrated Ontology(CoO) 표준을 통해 Swarm 컨텍스트 정합성과 추론 연결 고리의 기준점을 제공"
  termination_conditions:
    - "COO가 독립된 고도화 버전으로 대체될 때"
    - "상위 군체/모듈이 정식 Ontology 표준을 흡수할 때"
  dissolution_steps:
    - "대체 DNA로 승격 및 본 문서에 참조 요약 추가"
    - "필수 규칙은 축약본으로 남기고 나머지 산출물은 `_archive/`로 이전"
  retention:
    summary_required: true
    max_days: 180

resource_limits:
  max_files: 120
  max_folders: 30
  max_log_kb: 256

inquisitor:
  required: true
  audit_log: "../../01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md"
---
# AAOS Context-Orchestrated Ontology DNA

COO는 Swarm에서 발생하는 실무 맥락을 단순 파일·문서 단위를 넘어
관계형 의미 구조로 유지하기 위한 규범 기반 모듈이다.

## Mission

- Context node와 relation의 생명주기를 일관되게 표현한다.
- 판단 근거의 반복성과 추적성을 높이는 용어·구조 사전을 유지한다.
- Manifestation·Immune 판단이 공유할 수 있는 의미 경로를 제공한다.

## Core Constraints

1. Context 정합성 없는 정의 확장은 허용하지 않는다.
2. 동일 개념에 대한 이중 정의를 줄이고, 동일성 규약을 우선한다.
3. 실행/자동반영을 위한 코드 변경보다 의미 정의 우선으로 설계한다.
4. 감사 가능성이 있는 변경은 Nucleus 감사 루프 경유 후 반영한다.

## Governance Boundary

- 실행 관여는 하지 않는다.
- 레코드 보존은 `record_archive` 또는 Nucleus 운영 절차를 따른다.
- 규칙 변경은 기존 승인/상향 체계(`immune_system`)를 통해 반영한다.

## Related modules

- `02_Swarm/context-orchestrated-filesystem`: 구조 실행 규칙의 하위 운용
- `02_Swarm/cortex-agora`: 행동 관찰 기반 제안 생성
- `03_Manifestation/summon-agents`: 실행 바인딩과의 정합성 교차점
