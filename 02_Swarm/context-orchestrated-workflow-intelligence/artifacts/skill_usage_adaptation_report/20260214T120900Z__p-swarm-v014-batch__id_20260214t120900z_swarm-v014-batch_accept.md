# skill_usage_adaptation_report

## source_snapshot
- agora_ref: `agora://proposal/P-SWARM-V014-BATCH`
- captured_at: `2026-02-14T12:08:00Z`
- period: `2026-02-14T12:09:00Z`
- notes: `proposal=P-SWARM-V014-BATCH; decision_id=id_20260214T120900Z_swarm-v014-batch_accept; decision=accepted`

## usage_patterns
- pattern: `critique` / `fb_20260214T100206Z_P-SWARM-V014-BATCH_agent-claude-opus-4`
  - evidence:
    - COWI 소비 메커니즘 미정의: cortex-agora output 우선 원칙을 선언했으나 실제 pull 트리거/주기/포맷이 명시되지 않음. 스킬 0개 상태에서 intelligence mediator 역할 수행 불가. relation_context_map과 adaptation_report 스키마는 존재하나 이를 호출하는 스킬이 없다.
  - confidence: 0.8
- pattern: `critique` / `fb_20260214T120200Z_swarm-v014_awt-blindspot`
  - evidence:
    - AWT behavior_feed_export가 false(비활성). 설계 결정도 행동이며 cortex-agora가 AWT 패턴을 관찰할 경로가 차단됨. SQLite SoT에서 JSONL export로의 변환 정책/트리거가 부재하여 Agora-First 관찰 파이프라인에 사각지대 발생.
  - confidence: 0.8
- pattern: `critique` / `fb_20260214T120300Z_swarm-v014_zero-operation`
  - evidence:
    - change_archive 3개 이벤트 로그(CHANGE_EVENTS/PEER_FEEDBACK/IMPROVEMENT_DECISIONS) 모두 비어 있음. 설계는 완성(bridge script, templates, index)되었으나 운영 검증 제로. 이 비판 기록 자체가 첫 실사용이 됨.
  - confidence: 0.8
- pattern: `critique` / `fb_20260214T120400Z_swarm-v014_missing-context-id`
  - evidence:
    - cortex-agora SKILL.md(cortex-agora-instruction-nucleus) frontmatter에 context_id가 누락됨. COF Hard Constraint #1(context_id 없는 문서 생성 금지) 위반. name/description만 있고 context_id, role, state, scope, lifetime 필드 부재.
  - confidence: 0.8
- pattern: `critique` / `fb_20260214T120500Z_swarm-v014_schema-mismatch`
  - evidence:
    - Behavior Feed 스키마 불일치: Swarm Root DNA 최소 이벤트에 group_id 필드가 있으나 cortex-agora DNA recommended_fields에는 group_id 대신 trace_id가 있음. 상위-하위 간 필드명 합의 부재로 파싱/집계 시 혼선 가능.
  - confidence: 0.8

## cof_awt_impact
- scope: `handoff-1`
  - impact: `COWI 소비 메커니즘 미정의: cortex-agora output 우선 원칙을 선언했으나 실제 pull 트리거/주기/포맷이 명시되지 않음. 스킬 0개 상태에서 intelligence mediator 역할 수행 불가. relation_context_map과 adaptation_report 스키마는 존재하나 이를 호출하는 스킬이 없다.`
  - risk: `source contract drift`
- scope: `handoff-2`
  - impact: `AWT behavior_feed_export가 false(비활성). 설계 결정도 행동이며 cortex-agora가 AWT 패턴을 관찰할 경로가 차단됨. SQLite SoT에서 JSONL export로의 변환 정책/트리거가 부재하여 Agora-First 관찰 파이프라인에 사각지대 발생.`
  - risk: `source contract drift`
- scope: `handoff-3`
  - impact: `change_archive 3개 이벤트 로그(CHANGE_EVENTS/PEER_FEEDBACK/IMPROVEMENT_DECISIONS) 모두 비어 있음. 설계는 완성(bridge script, templates, index)되었으나 운영 검증 제로. 이 비판 기록 자체가 첫 실사용이 됨.`
  - risk: `source contract drift`
- scope: `handoff-4`
  - impact: `cortex-agora SKILL.md(cortex-agora-instruction-nucleus) frontmatter에 context_id가 누락됨. COF Hard Constraint #1(context_id 없는 문서 생성 금지) 위반. name/description만 있고 context_id, role, state, scope, lifetime 필드 부재.`
  - risk: `source contract drift`
- scope: `handoff-5`
  - impact: `Behavior Feed 스키마 불일치: Swarm Root DNA 최소 이벤트에 group_id 필드가 있으나 cortex-agora DNA recommended_fields에는 group_id 대신 trace_id가 있음. 상위-하위 간 필드명 합의 부재로 파싱/집계 시 혼선 가능.`
  - risk: `source contract drift`

## proposed_adjustments
- id: `adj-001`
  - summary: `COWI 소비 메커니즘 미정의: cortex-agora output 우선 원칙을 선언했으나 실제 pull 트리거/주기/포맷이 명시되지 않음. 스킬 0개 상태에서 intelligence mediator 역할 수행 불가. relation_context_map과 adaptation_report 스키마는 존재하나 이를 호출하는 스킬이 없다.`
  - guardrails:
    - `source_snapshot.agora_ref required`
- id: `adj-002`
  - summary: `AWT behavior_feed_export가 false(비활성). 설계 결정도 행동이며 cortex-agora가 AWT 패턴을 관찰할 경로가 차단됨. SQLite SoT에서 JSONL export로의 변환 정책/트리거가 부재하여 Agora-First 관찰 파이프라인에 사각지대 발생.`
  - guardrails:
    - `source_snapshot.agora_ref required`
- id: `adj-003`
  - summary: `change_archive 3개 이벤트 로그(CHANGE_EVENTS/PEER_FEEDBACK/IMPROVEMENT_DECISIONS) 모두 비어 있음. 설계는 완성(bridge script, templates, index)되었으나 운영 검증 제로. 이 비판 기록 자체가 첫 실사용이 됨.`
  - guardrails:
    - `source_snapshot.agora_ref required`
- id: `adj-004`
  - summary: `cortex-agora SKILL.md(cortex-agora-instruction-nucleus) frontmatter에 context_id가 누락됨. COF Hard Constraint #1(context_id 없는 문서 생성 금지) 위반. name/description만 있고 context_id, role, state, scope, lifetime 필드 부재.`
  - guardrails:
    - `source_snapshot.agora_ref required`
- id: `adj-005`
  - summary: `Behavior Feed 스키마 불일치: Swarm Root DNA 최소 이벤트에 group_id 필드가 있으나 cortex-agora DNA recommended_fields에는 group_id 대신 trace_id가 있음. 상위-하위 간 필드명 합의 부재로 파싱/집계 시 혼선 가능.`
  - guardrails:
    - `source_snapshot.agora_ref required`

## expected_effect
- hypotheses:
  - `decision rationale applied: Claude critique 1~5 반영: COWI pull bridge/AWT export 활성화/group_id canonical/context_id 보강/운영 의사결정 체인 기록 완료`
  - `agora_ref-first consumption reduces interpretation drift`
- success_signals:
  - `relation_context_map generated for each decision`
  - `feedback refs remain traceable to cortex-agora`
- review_cycle: `daily-manual`

## rollback_rule
- trigger: `agora_ref missing or inconsistent with source_snapshot contract`
- action: `discard generated artifact and rerun pull after source correction`
- owner: `context-orchestrated-workflow-intelligence`
