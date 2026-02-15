---
name: "AAOS-Agentic-Workflow-Topology"
version: "0.2.1"
scope: "04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology"
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

observability:
  log_sot:
    type: "sqlite"
    path: "00.context/agent_log.db"
    schema_contract: "agent-audit-log@1.3.0"
  behavior_feed_export:
    enabled: true
    mode: "manual_summary_export"
    format: "md_with_frontmatter"
    format_version: "v2"
    trigger_policy:
      on_new_review_batch: "manual_run"
      daily_manual_batch: true
    script: "04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/skills/03.observability-evolution/scripts/export_behavior_feed.py"
    path: "04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/records/behavior/"
    legacy_path: "04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/agents/<agent-family>/<version>/behavior/BEHAVIOR_FEED.jsonl"
    legacy_frozen: true
    record_writer: "04_Agentic_AI_OS/02_Swarm/cortex-agora/scripts/record_writer.py"
    bases_view: "02_Swarm/cortex-agora/dashboard/agentic-workflow-topology-records.base"
    append_only: true
    canonical_group_field: "group_id"
    backward_compatibility_field: "trace_id"
    retention_days: 30

strategy_gate:
  scope: "strategy_or_high_risk_only"
  preflight_first_question:
    id: "PF1"
    question: "멘탈모델 먼저 세팅할까요?"
  required_nodes: ["H1", "H2"]
  required_edges:
    - "T4->C1"
    - "C1->H1"
  h1_requirements:
    web_evidence_path: "04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/agents/<agent-family>/<version>/artifacts/web_evidence/web_evidence_YYYY-MM-DD.md"
    cowi_artifacts:
      - relation_context_map
      - skill_usage_adaptation_report
  validator_script: "04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/skills/01.topology-design/scripts/validate_strategy_h1_gate.py"
  enforcement: "block_h1_finalization_if_missing"

proposal_operations:
  enabled: true
  proposal_root: "04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/proposals"
  proposal_template: "04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/proposals/_TEMPLATE.md"
  owner_swarm: "agentic-workflow-topology"
  required_frontmatter:
    - proposal_id
    - parent_proposal_id
    - proposal_status
    - hitl_required
    - hitl_stage
    - checked
    - user_action_required
    - visibility_tier
    - owner_swarm
    - linked_reports
    - linked_artifacts
  status_enum:
    - draft
    - review_pending
    - approval_required
    - in_progress
    - done
    - closed
  visibility_enum:
    - must_show
    - optional
    - internal
  artifact_metadata_policy:
    workflow_generation_outputs:
      - proposal_id
      - visibility_tier
    scaffold_script: "04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/skills/01.topology-design/50.cone-analyzer/scripts/scaffold_workflow.py"

natural_dissolution:
  purpose: "워크플로우 토폴로지 설계 표준을 제공하고 COF/실행 계층과 경계를 유지"
  termination_conditions:
    - "상위 Swarm 표준이 본 스웜의 설계 기능을 흡수할 때"
    - "대체되는 전용 설계 Swarm이 canonical로 승격될 때"
  dissolution_steps:
    - "핵심 설계 규약을 후속 DNA로 이전"
    - "기존 스킬/실험 산출물은 `_archive/`로 이전"
  retention:
    summary_required: true
    max_days: 180

resource_limits:
  max_files: 400
  max_folders: 80
  max_log_kb: 512

inquisitor:
  required: true
  audit_log: "../../01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md"
---
# AAOS Agentic Workflow Topology DNA

본 Swarm은 업무 실행이 아니라 "설계 결정"을 담당한다.

## Mission

- Goal을 실행 가능한 workflow graph로 변환한다.
- theta_GT/RSV 기반으로 node split, topology, termination을 설계한다.
- COF 티켓 운영 계층과 책임 경계를 분리한다.
- 실행 런너가 아닌 설계 계약 중심으로 운영한다.
- 실행 로그 SoT는 SQLite로 유지하고, behavior feed는 필요 시 요약 export만 허용한다.
- 전략/고위험 워크플로우에는 PF1/H1/H2/H1 gate를 강제한다.

## Proposal Operations Contract

- AWT는 workflow 생성/관리 산출물을 proposal 단위로 추적한다.
- proposal 문서는 `proposals/` 경로에서 운영하며, frontmatter는 `proposal_operations.required_frontmatter`를 따른다.
- workflow 스캐폴드 산출물은 `proposal_id`, `visibility_tier` 메타를 포함해야 한다.
- 사용자 기본 노출 대상은 `visibility_tier=must_show` 항목으로 제한한다.
- proposal 산출 포맷은 표준 Markdown 기반이며 Obsidian 전용 포맷을 요구하지 않는다.

## Behavior Feed Export Runbook

```bash
python3 04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/skills/03.observability-evolution/scripts/export_behavior_feed.py \
  --db-path 04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/00.context/agent_log.db \
  --agent-family claude \
  --agent-version 4.0
```

## Boundary

- `context-orchestrated-filesystem`는 티켓 생성/관리/로컬 운영을 담당한다.
- `agentic-workflow-topology`는 workflow 설계 산출물을 제공한다.
- `context-orchestrated-workflow-intelligence`는 AWT 설계 출력과 COF 운영 맥락을 중재한다.
- 실행 바인딩은 `03_Manifestation/` 계층 또는 실행 Swarm에 위임한다.
- AWT는 직접 실행/오케스트레이션/자동반영을 수행하지 않는다.

## Seed Skills

- `04.skill-governance`
- `00.mental-model-design`
- `01.topology-design`
- `02.execution-design`
- `03.observability-evolution`

## Version Note

- v0.1.2 : COWI mediation contract 및 비실행 경계(직접 실행/자동반영 금지) 명시
- v0.1.3 : Behavior Feed 수동 export 활성화(`enabled: true`) 및 group_id canonical 필드 명시
- v0.1.4 : Behavior Feed 기본 출력 경로를 `agents/<agent-family>/<version>/behavior/` 네임스페이스로 전환
- v0.2.0 : 전략/고위험 PF1/H1/H2 강제 및 web evidence + COWI artifact 기반 H1 finalization gate 도입
- v0.2.1 : Production proposal 운영 계약(frontmatter/status/visibility) 및 workflow 산출물 proposal 메타 부착 정책 추가
