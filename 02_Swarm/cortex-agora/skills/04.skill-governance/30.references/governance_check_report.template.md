# governance_check_report

## metadata_checks

- frontmatter_policy_ok: boolean
- missing_required_fields: [{skill_id, field, severity}]
- sidecar_consistency: [{skill_id, check_id, status: PASS|WARN|FAIL, detail}]
- four_layer_compliance: [{skill_id, missing_layers: [], severity, note}]

## archive_integrity_checks

- change_events_schema: [{check_id, status: PASS|WARN|FAIL, details}]
- peer_feedback_schema: [{check_id, status, details}]
- improvement_decisions_schema: [{check_id, status, details}]
- referential_integrity:
  - cc_01: [{from: "proposal.id", to: "CHANGE_EVENTS.proposal_id", status, details}]
  - cc_02: [{from: "PEER_FEEDBACK.linked_event_id", to: "CHANGE_EVENTS.event_id", status, details}]
  - cc_03: [{from: "IMPROVEMENT_DECISIONS.feedback_refs[]", to: "PEER_FEEDBACK.feedback_id", status, details}]
- bridge_command_coverage: [{check_id, command, status}]
- index_consistency: [{check_id, status, details}]
- append_only_invariant: [{check_id, status, details}]

## consumption_contract_checks

- behavior_feed_schema: [{check_id, status: PASS|WARN|FAIL, details}]
- cowi_pull_interface:
  - cc_05: [{from: "IMPROVEMENT_DECISIONS", to: "COWI pull_agora_feedback.py", status, details}]
  - checks: [{check_id, status, details}]
- cross_swarm_recording: [{check_id, status, details}]

## registry_sync_status

- local_registry: {path, skill_count, last_generated}
- swarm_registry: {path, cortex_agora_section_count}
- mismatches: [{type: missing_in_registry|missing_in_dir|name_mismatch, details}]
- generated_at: ISO8601

## action_items

1. [FAIL] {check_id}: {description} -> {remediation}
2. [WARN] {check_id}: {description} -> {remediation}
3. ...
