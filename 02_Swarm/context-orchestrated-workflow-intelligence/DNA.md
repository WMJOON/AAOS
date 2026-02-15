---
name: "AAOS-COWI"
version: "0.3.1"
scope: "04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence"
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

intelligence_contracts:
  agent_namespace_contract:
    schema: "references/agent_namespace_contract.schema.yaml"
  relation_context_map:
    schema: "references/relation_context_map.schema.yaml"
  skill_usage_adaptation_report:
    schema: "references/skill_usage_adaptation_report.schema.yaml"
    template: "references/skill_usage_adaptation_report.template.md"

consumption_bridge:
  source: "02_Swarm/cortex-agora/records"
  source_format: "md_with_frontmatter"
  legacy_source: "02_Swarm/cortex-agora/change_archive/events"
  source_of_truth_key: "source_snapshot.agora_ref"
  trigger_policy:
    on_new_improvement_decision: "manual_pull_required"
    daily_manual_batch: true
  script: "02_Swarm/context-orchestrated-workflow-intelligence/skills/00.agora-consumption-bridge/scripts/pull_agora_feedback.py"
  cursor_state: "02_Swarm/context-orchestrated-workflow-intelligence/registry/AGORA_PULL_STATE.json"
  outputs:
    relation_context_map: "02_Swarm/context-orchestrated-workflow-intelligence/agents/<agent-family>/<version>/artifacts/relation_context_map/*.yaml"
    skill_usage_adaptation_report: "02_Swarm/context-orchestrated-workflow-intelligence/agents/<agent-family>/<version>/artifacts/skill_usage_adaptation_report/*.md"
    conversation_snapshot: "02_Swarm/context-orchestrated-workflow-intelligence/agents/<agent-family>/<version>/conversation_snapshots/*.md"
  h1_finalization_guard:
    required_artifacts:
      - relation_context_map
      - skill_usage_adaptation_report
    enforcement: "block_if_missing"

proposal_operations:
  enabled: true
  proposal_root: "04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/proposals"
  proposal_template: "04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/proposals/_TEMPLATE.md"
  owner_swarm: "context-orchestrated-workflow-intelligence"
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
  dashboard_contract:
    build_script: "04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/scripts/build_production_dashboards.py"
    production_proposals_json: "04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/dashboard/production-proposals.json"
    production_proposals_csv: "04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/dashboard/production-proposals.csv"
    user_inbox_json: "04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/dashboard/user-inbox.json"
    user_inbox_csv: "04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/dashboard/user-inbox.csv"
    archived_proposals_json: "04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/dashboard/archived-proposals.json"
    archived_proposals_csv: "04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/dashboard/archived-proposals.csv"
    default_filters:
      - "proposal_status != closed"
      - "visibility_tier == must_show"
      - "approval_required queue: hitl_stage == approval_required && checked == true"

natural_dissolution:
  purpose: "COF↔AWT 관계 맥락과 스킬 사용 패턴 개선 제안을 연결하는 COWI intelligence mediator 제공"
  termination_conditions:
    - "COF↔AWT intelligence 중재 기능이 상위 표준에 흡수될 때"
    - "동일 책임 범위를 갖는 대체 Swarm이 canonical로 승격될 때"
  dissolution_steps:
    - "계약 스키마와 템플릿을 후속 DNA로 승계"
    - "운영 산출물은 `_archive/`로 이전하고 요약본만 유지"
  retention:
    summary_required: true
    max_days: 180

resource_limits:
  max_files: 240
  max_folders: 60
  max_log_kb: 384

inquisitor:
  required: true
  audit_log: "../../01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md"
---
# AAOS Context-Orchestrated Workflow Intelligence DNA

COWI는 COF 운영 맥락과 AWT 설계 맥락을 연결하고, `cortex-agora` 관찰 출력을
현장 컨텍스트로 재맥락화하는 intelligence 계층이다.

## Mission

- COF↔AWT 관계 맵을 구조화된 계약(`relation_context_map`)으로 유지한다.
- `cortex-agora` 출력 우선 원칙으로 스킬 사용 패턴 개선 제안을 만든다.
- 자동 집행 없이 `skill_usage_adaptation_report`로 수동 반영 판단 근거를 제공한다.
- `IMPROVEMENT_DECISIONS` 신규 이벤트를 pull해 관계 맥락/적응 보고서 산출물을 materialize한다.
- 대화 메모리는 Hybrid 정책(외부 메모리 읽기 + 로컬 snapshot ref 저장)으로 연결한다.
- 전략/고위험 topology에서는 `T4 -> C1 -> H1` 구간의 C1 consumption step을 필수로 둔다.

## Proposal Hub Contract

- COWI는 Production 기관 proposal의 parent rollup 허브를 담당한다.
- 기본 사용자 뷰는 `proposal_status != closed` + `visibility_tier == must_show`만 표시한다.
- 승인 대기 큐는 `hitl_stage=approval_required && checked=true` 조건으로만 노출한다.
- 사용자 inbox에는 `must_show && user_action_required=true` 항목만 노출한다.
- 출력 포맷은 Obsidian 의존 없이 JSON/CSV를 기본으로 제공한다.

## Core Constraints

1. `cortex-agora` 원천 출력이 없는 임의의 전역 관찰 해석을 금지한다.
2. COF/AWT 실행 오케스트레이션 개입을 금지한다.
3. 자동 규칙 반영/자동 차단을 금지한다.
4. 계약 변경은 감사 가능한 문서 변경으로 남긴다.
5. COWI 산출물 누락 시 H1 finalization을 차단한다.

## Governance Boundary

- 전역 행동 원천 관찰은 `cortex-agora`가 담당한다.
- COWI는 관찰 결과를 받아 로컬 맥락으로 변환/제안만 수행한다.
- COWI는 `cortex-agora/change_archive`에서 전달된 feedback/decision을 `source_snapshot.agora_ref` 기준으로만 소비한다.
- COF 티켓 실행/Manifestation 바인딩은 COWI 범위가 아니다.
- 규칙/스킬 자동 집행은 수행하지 않는다.
- 전략/고위험 workflow의 H1 gate는 `relation_context_map` + `skill_usage_adaptation_report` 존재를 전제로 한다.

## Consumption Runbook

```bash
python3 04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/skills/00.agora-consumption-bridge/scripts/pull_agora_feedback.py \
  --proposal-id P-SWARM-V014-BATCH \
  --agent-family claude \
  --agent-version 4.0 \
  --conversation-session-id chat-2026-02-14
```

```bash
python3 04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/skills/00.agora-consumption-bridge/scripts/pull_agora_feedback.py \
  --proposal-id P-SWARM-V014-BATCH \
  --agent-family claude \
  --agent-version 4.0 \
  --conversation-session-id chat-2026-02-14 \
  --dry-run
```

## Related modules

- `02_Swarm/context-orchestrated-filesystem`: 티켓 운영 및 실행 맥락 관리
- `02_Swarm/agentic-workflow-topology`: topology/handoff/termination 설계
- `02_Swarm/cortex-agora`: 행동 관찰/요약/제안의 원천 출력
- `03_Manifestation/summon-agents`: 실행 바인딩 계층

## Version Note

- v0.2.1 : `cortex-agora/change_archive` 연계 경계(`agora_ref` 기준 feedback/decision 소비) 명시
- v0.2.2 : COWI pull bridge(`IMPROVEMENT_DECISIONS` trigger + 일일 수동 배치 + cursor state) 운영 계약 추가
- v0.2.3 : `agents/<agent-family>/<version>/` 네임스페이스 출력 강제 및 conversation snapshot(Hybrid) 계약 추가
- v0.3.0 : 전략/고위험 `T4 -> C1 -> H1` 구간의 consumption step 강제 및 H1 finalization artifact gate 추가
- v0.3.1 : Production proposal parent/child 운영 계약 및 사용자 액션 대시보드 필터 계약 추가
