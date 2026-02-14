---
name: cowi-agora-consumption-bridge
description: Pulls cortex-agora change_archive decisions by agora_ref and materializes relation_context_map plus skill_usage_adaptation_report artifacts for COWI manual mediation.
context_id: cowi-agora-consumption-bridge
trigger: model_decision
role: SKILL
state: const
scope: swarm
lifetime: persistent
created: "2026-02-14"
---

# COWI Agora Consumption Bridge

`00.cowi-agora-consumption-bridge`는 `cortex-agora/change_archive`를 pull해서
`relation_context_map`와 `skill_usage_adaptation_report` 초안을 생성한다.

## Purpose

- `cortex-agora output first` 원칙을 COWI 운영 루틴으로 고정
- `source_snapshot.agora_ref` 기준으로 feedback/decision 이벤트를 소비
- 수동 실행 기반 일일 배치(runbook) 제공

## Inputs

- `02_Swarm/cortex-agora/change_archive/events/CHANGE_EVENTS.jsonl`
- `02_Swarm/cortex-agora/change_archive/events/PEER_FEEDBACK.jsonl`
- `02_Swarm/cortex-agora/change_archive/events/IMPROVEMENT_DECISIONS.jsonl`

## Outputs

- `artifacts/relation_context_map/*.yaml`
- `artifacts/skill_usage_adaptation_report/*.md`

## Script

```bash
python3 04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/skills/00.cowi-agora-consumption-bridge/scripts/pull_agora_feedback.py \
  --proposal-id P-SWARM-V014-BATCH
```

### Dry-run

```bash
python3 04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/skills/00.cowi-agora-consumption-bridge/scripts/pull_agora_feedback.py \
  --proposal-id P-SWARM-V014-BATCH \
  --dry-run
```

## Trigger Policy

1. `IMPROVEMENT_DECISIONS` 신규 이벤트가 발생하면 즉시 수동 실행
2. 이벤트가 없더라도 일일 1회 수동 배치 실행

## Guardrail

- COWI는 event pull/변환/보고서 생성까지만 수행한다.
- COF/AWT 실행 집행은 수행하지 않는다.
- 자동 스케줄러(cron)는 도입하지 않고 runbook 실행만 허용한다.
