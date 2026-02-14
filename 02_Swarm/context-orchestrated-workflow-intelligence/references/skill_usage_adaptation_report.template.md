# skill_usage_adaptation_report

## source_snapshot
- agora_ref: `<cortex-agora output reference>`
- captured_at: `<ISO-8601>`
- period: `<optional>`
- notes: `<optional>`

## usage_patterns
- pattern: `<observed behavior pattern>`
  - evidence:
    - `<evidence item>`
  - confidence: `<0.0 ~ 1.0>`

## cof_awt_impact
- scope: `<COF|AWT|handoff>`
  - impact: `<impact summary>`
  - risk: `<optional>`

## proposed_adjustments
- id: `adj-001`
  - summary: `<adjustment proposal>`
  - guardrails:
    - `<guardrail>`

## expected_effect
- hypotheses:
  - `<expected effect>`
- success_signals:
  - `<signal>`
- review_cycle: `<weekly|biweekly|monthly>`

## rollback_rule
- trigger: `<rollback condition>`
- action: `<rollback action>`
- owner: `<responsible role>`
