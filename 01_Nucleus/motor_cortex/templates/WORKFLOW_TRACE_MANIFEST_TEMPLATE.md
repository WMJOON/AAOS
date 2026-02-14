---
name: aaos-workflow-trace-manifest-template
scope: "04_Agentic_AI_OS/01_Nucleus"
version: "0.1.0"
---

workflow_id: TASK-NUC-YYYYMMDD-XXX
issue_proposer: human:requester
issue_signature: "<이슈 증상/범위/KPI 1문장>"
goal_statement: "<최종 목표 1문장>"
dq_index: "DQ1|DQ2|DQ3"
rsv_total: 3.0
topology_type: "linear"
topology_rationale: "<Goal 성격/SE 분포/RSV 규모 기반 선택 이유>"
task_graph_signature: "T1->T2->T3"
model_consensus: "multi-agent-consensus"
plan_critic_model_id: "agent-<provider>-<name>"
plan_critic_provider: "provider-A"
plan_critic_model_family: "Codex"
criticality_separation_required: true
criticality_model_family_separated: true
direction_signature: "<개선방향: 대안 2개 이상 비교 + 승인 방향 1개>"
record_path: "_archive/workflow/TASK-NUC-YYYYMMDD-XXX"
cross_ref_validation: "pending"
dissolution_monitor_status: "not-applicable"

plan_author: "agent-A"
plan_critic: "agent-B"
plan_critic_status: no-critical-objection

decomposition_author: "agent-B"
decomposition_critic: "agent-C"
decomposition_critic_status: no-critical-objection
decomposition_critic_model_id: "agent-<provider>-<name>"
decomposition_critic_provider: "provider-B"
decomposition_critic_model_family: "Claude"
