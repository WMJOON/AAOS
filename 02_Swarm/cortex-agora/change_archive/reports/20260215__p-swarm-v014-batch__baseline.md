---
proposal_id: "P-SWARM-V014-BATCH"
report_type: "baseline"
linked_proposal_id: "P-SWARM-V014-BATCH"
linked_proposal: "[[02_Swarm/cortex-agora/proposals/P-SWARM-V014-BATCH|P-SWARM-V014-BATCH Hub]]"
generated_at: "2026-02-15T08:03:40Z"
status_snapshot: "improving"
decision_snapshot: "accepted"
warnings_open: 6
---

# Baseline Snapshot: P-SWARM-V014-BATCH

## Linked Proposal
- [[02_Swarm/cortex-agora/proposals/P-SWARM-V014-BATCH|P-SWARM-V014-BATCH Hub]]

- generated_at: 2026-02-15T08:03:40Z
- proposal_id: P-SWARM-V014-BATCH
- latest_change_status: improving
- latest_decision: accepted
- change_events: 2
- peer_feedback_total: 7
- stance_distribution: critique=5, suggestion=1, endorsement=1

## Open Items (Before Closure)

- fb_20260214T100206Z_P-SWARM-V014-BATCH_agent-claude-opus-4: COWI 소비 메커니즘 미정의: cortex-agora output 우선 원칙을 선언했으나 실제 pull 트리거/주기/포맷이 명시되지 않음. 스킬 0개 상태에서 intelligence mediator 역할 수행 불가. relation_context_map과 adaptation_report 스키마는 존재하나 이를 호출하는 스킬이 없다.
- fb_20260214T120200Z_swarm-v014_awt-blindspot: AWT behavior_feed_export가 false(비활성). 설계 결정도 행동이며 cortex-agora가 AWT 패턴을 관찰할 경로가 차단됨. SQLite SoT에서 JSONL export로의 변환 정책/트리거가 부재하여 Agora-First 관찰 파이프라인에 사각지대 발생.
- fb_20260214T120300Z_swarm-v014_zero-operation: change_archive 3개 이벤트 로그(CHANGE_EVENTS/PEER_FEEDBACK/IMPROVEMENT_DECISIONS) 모두 비어 있음. 설계는 완성(bridge script, templates, index)되었으나 운영 검증 제로. 이 비판 기록 자체가 첫 실사용이 됨.
- fb_20260214T120400Z_swarm-v014_missing-context-id: cortex-agora SKILL.md(cortex-agora-instruction-nucleus) frontmatter에 context_id가 누락됨. COF Hard Constraint #1(context_id 없는 문서 생성 금지) 위반. name/description만 있고 context_id, role, state, scope, lifetime 필드 부재.
- fb_20260214T120500Z_swarm-v014_schema-mismatch: Behavior Feed 스키마 불일치: Swarm Root DNA 최소 이벤트에 group_id 필드가 있으나 cortex-agora DNA recommended_fields에는 group_id 대신 trace_id가 있음. 상위-하위 간 필드명 합의 부재로 파싱/집계 시 혼선 가능.
- fb_20260214T120600Z_swarm-v014_immune-ref-divergence: COF DNA immune_doctrine_reference가 자체 rules/cof-environment-set.md를 가리킴. 타 Swarm DNA(cortex-agora, AWT, COWI)는 01_Nucleus/immune_system/rules/README.md를 참조. 의도적 분기인지 불일치인지 명확화 필요. 의도적이라면 DNA에 주석 추가 권장.

## Current Record Files

- 02_Swarm/cortex-agora/records/change_events/CE-20260214T120000Z-ce_20260214T120000Z_swarm-v014-batch_created.md
- 02_Swarm/cortex-agora/records/change_events/CE-20260214T120800Z-ce_20260214T120800Z_swarm-v014-batch_updated.md
- 02_Swarm/cortex-agora/records/peer_feedback/FB-20260214T120100Z-fb_20260214T100206Z_P-SWARM-V014-BATCH_agent-claude-opus-4.md
- 02_Swarm/cortex-agora/records/peer_feedback/FB-20260214T120200Z-fb_20260214T120200Z_swarm-v014_awt-blindspot.md
- 02_Swarm/cortex-agora/records/peer_feedback/FB-20260214T120500Z-fb_20260214T120500Z_swarm-v014_schema-mismatch.md
- 02_Swarm/cortex-agora/records/peer_feedback/FB-20260214T120700Z-fb_20260214T120700Z_swarm-v014_endorsement-overall.md
- 02_Swarm/cortex-agora/records/peer_feedback/FB-20260214T120400Z-fb_20260214T120400Z_swarm-v014_missing-context-id.md
- 02_Swarm/cortex-agora/records/peer_feedback/FB-20260214T120600Z-fb_20260214T120600Z_swarm-v014_immune-ref-divergence.md
- 02_Swarm/cortex-agora/records/peer_feedback/FB-20260214T120300Z-fb_20260214T120300Z_swarm-v014_zero-operation.md
- 02_Swarm/cortex-agora/records/improvement_decisions/ID-20260214T120900Z-id_20260214T120900Z_swarm-v014-batch_accept.md
