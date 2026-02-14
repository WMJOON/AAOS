# Context-Orchestrated Workflow Intelligence

Context-Orchestrated Workflow Intelligence(COWI)는
`agentic-workflow-topology`(설계)와 `context-orchestrated-filesystem`(운영) 사이의
관계 맥락을 정합성 있게 유지하고, `cortex-agora` 출력 기반으로 스킬 사용 패턴 개선안을
만드는 하이브리드 Swarm이다.

## Mission

- COF↔AWT 사이의 workflow context relation을 정규 계약으로 표준화한다.
- `cortex-agora` 관찰 결과를 우선 입력으로 받아, 로컬 맥락형 개선안으로 재해석한다.
- 자동 집행 없이 개선 제안/롤백 규칙 중심으로 운영한다.
- `IMPROVEMENT_DECISIONS` 기반 pull 소비 루틴으로 `relation_context_map`/`skill_usage_adaptation_report`를 생성한다.

## Boundary

### 포함 영역

- `relation_context_map` 설계/갱신
- `skill_usage_adaptation_report` 작성
- COF↔AWT handoff/context link/conflict rule 정의
- `cortex-agora` 제안의 국소 맥락 재적용
- feedback contract: `cortex-agora/change_archive` 이벤트(`PEER_FEEDBACK`, `IMPROVEMENT_DECISIONS`)를 `source_snapshot.agora_ref` 기준으로 수집/회송
- 수동 pull bridge 실행 및 cursor(`registry/AGORA_PULL_STATE.json`) 갱신

### 제외 영역

- 전역 행동 원천 관찰(= `cortex-agora` 소관)
- 티켓 실행/오케스트레이션(= COF/Manifestation 소관)
- 자동 규칙 반영/자동 차단

## Contract Outputs

1. `relation_context_map` (YAML/JSON)
- schema: `references/relation_context_map.schema.yaml`
- required keys:
  `workflow_id`, `ticket_context_id`, `topology_nodes`, `context_links`, `handoff_rules`, `conflict_resolution_rule`

2. `skill_usage_adaptation_report` (Markdown/JSON)
- schema: `references/skill_usage_adaptation_report.schema.yaml`
- template: `references/skill_usage_adaptation_report.template.md`
- required sections:
  `source_snapshot`, `usage_patterns`, `cof_awt_impact`, `proposed_adjustments`, `expected_effect`, `rollback_rule`

## Consumption Operations

- trigger:
  - `cortex-agora/change_archive/events/IMPROVEMENT_DECISIONS.jsonl` 신규 이벤트 발생 시
  - 신규 이벤트가 없더라도 일일 1회 수동 배치
- source-of-truth: `source_snapshot.agora_ref`
- outputs:
  - `artifacts/relation_context_map/*.yaml`
  - `artifacts/skill_usage_adaptation_report/*.md`
- cursor:
  - `registry/AGORA_PULL_STATE.json`

### Runbook

```bash
python3 04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/skills/00.cowi-agora-consumption-bridge/scripts/pull_agora_feedback.py \
  --proposal-id P-SWARM-V014-BATCH
```

```bash
python3 04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/skills/00.cowi-agora-consumption-bridge/scripts/pull_agora_feedback.py \
  --proposal-id P-SWARM-V014-BATCH \
  --dry-run
```

## Hard Guardrails

- `cortex-agora output` 우선이며, COWI는 직접 전역 관찰을 수행하지 않는다.
- COWI는 직접 실행/오케스트레이션/자동반영을 수행하지 않는다.
- COF/AWT 실행 자체를 대행하지 않는다.

## Canonical References

- Canon: `04_Agentic_AI_OS/README.md`
- META Doctrine: `04_Agentic_AI_OS/00_METADoctrine/DNA.md`
- Immune Doctrine: `04_Agentic_AI_OS/01_Nucleus/immune_system/rules/README.md`
- Swarm Root DNA: `04_Agentic_AI_OS/02_Swarm/DNA.md`
