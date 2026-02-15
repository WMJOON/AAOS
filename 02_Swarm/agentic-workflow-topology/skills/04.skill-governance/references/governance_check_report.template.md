# governance_check_report

## metadata_checks

- frontmatter_policy_ok: boolean  # true if all FM-* checks PASS
- missing_required_fields: [{skill_id, field, severity}]
- disallowed_frontmatter_keys: [{skill_id, key}]
- frontmatter_key_count_violations: [{skill_id, actual, max}]
- four_layer_compliance: [{skill_id, missing_layers: [], severity}]
- sidecar_consistency: [{skill_id, check_id, status, detail}]

## dependency_checks

- coupling_results: [{cc_id, from_skill, to_skill, status: PASS|WARN|FAIL, details}]
- broken_links: [{cc_id, description}]
- incompatible_contracts: [{cc_id, field, expected_type, actual_type}]
- schema_version_drift: [{skill_id, current_version, last_checked_version}]

## compatibility_checks

- legacy_aliases_present: [{old_name, new_name, locations_found}]
- routing_notes: [string]
- deprecation_status: [{skill_id, status, sunset_condition}]

## registry_sync_status

- local_registry: {path, skill_count, last_generated}
- swarm_registry: {path, awt_section_count, last_generated}
- mismatches: [{type: missing_in_registry|missing_in_dir|name_mismatch, details}]
- cross_swarm_duplicates: [{context_id, swarms: []}]
- generated_at: ISO8601

## action_items

1. [FAIL] {check_id}: {description} -> {remediation}
2. [WARN] {check_id}: {description} -> {remediation}
3. ...
