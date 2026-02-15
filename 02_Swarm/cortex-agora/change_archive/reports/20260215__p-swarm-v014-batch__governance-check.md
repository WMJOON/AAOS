---
proposal_id: "P-SWARM-V014-BATCH"
report_type: "governance_check"
linked_proposal_id: "P-SWARM-V014-BATCH"
linked_proposal: "[[02_Swarm/cortex-agora/proposals/P-SWARM-V014-BATCH|P-SWARM-V014-BATCH Hub]]"
generated_at: "2026-02-15T08:51:00Z"
status_snapshot: "closed"
decision_snapshot: "accepted"
phase_1: "pass"
phase_2: "pass"
phase_3: "pass"
warnings_open: 0
---

# governance_check_report

## Linked Proposal
- [[02_Swarm/cortex-agora/proposals/P-SWARM-V014-BATCH|P-SWARM-V014-BATCH Hub]]

- generated_at: 2026-02-15T08:51:00Z
- proposal_id: P-SWARM-V014-BATCH
- review_scope: post-closure refresh
- latest_change_event_id: ce_20260215T080432Z_swarm-v014-batch_closed
- latest_decision_id: id_20260215T080532Z_swarm-v014-batch_close-seal

## metadata_checks
- FM-01: PASS - frontmatter name present
- FM-02: PASS - frontmatter description present
- FM-06: PASS - context_id delegated to SKILL.meta.yaml (sidecar SoT)
- SC-01: PASS - SKILL.meta.yaml exists
- SC-02: PASS - context_id present: cortex-agora-instruction-nucleus
- SC-04: PASS - role=SKILL
- SC-05: PASS - state=const
- SC-06: PASS - scope=swarm
- SC-07: PASS - lifetime=persistent
- SC-08: PASS - consumers populated (3 entries)
- 4L-ALL: SKIP - instruction-nucleus is intentionally flat + sidecar structure

## archive_integrity_checks
- AE-01~AE-08: PASS - CHANGE_EVENTS rows=3, schema parse ok
- AF-01~AF-08: PASS - PEER_FEEDBACK rows=7, schema parse ok
- AD-01~AD-07: PASS - IMPROVEMENT_DECISIONS rows=2, schema parse ok
- CC-02: PASS - linked_event refs valid=True
- CC-03: PASS - feedback_refs valid=True
- AB-01~AB-05: PASS - bridge subcommands present (record-change/feedback/decision/build-package/seal-to-record-archive)
- AM-02: PASS - timestamps in each stream are monotonic non-decreasing
- AM-04: PASS - event/feedback/decision IDs are unique within streams

## consumption_contract_checks
- BF-01~BF-04: PASS - behavior feed required keys present=True, group_id canonical + trace_id optional observed
- CP-01: PASS - pull_agora_feedback.py exists
- CP-05: PASS - COWI runbook path documented in cortex-agora README
- CC-05: PASS - dry-run consumption succeeds with explicit agent namespace (proposal=P-SWARM-V014-BATCH, generated_files=4)
- XR-01: PASS - primary_consumer is context-orchestrated-workflow-intelligence
- XR-05: PASS - DNA recommended_fields aligned with emitted flattened behavior fields
- SUG-IMMUNE: PASS - COF immune_doctrine_reference divergence is documented as intentional in COF DNA/README

## registry_sync_status
- local_registry: 02_Swarm/cortex-agora/registry/SKILL_REGISTRY.md
- swarm_registry: 02_Swarm/cortex-agora/registry/SWARM_SKILL_REGISTRY.md
- mismatches: none observed in this pass

## action_items
- [PASS] No FAIL items in 3-phase validation.
- [PASS] No open WARN items.
- [INFO] Proposal is already closed and sealed.
