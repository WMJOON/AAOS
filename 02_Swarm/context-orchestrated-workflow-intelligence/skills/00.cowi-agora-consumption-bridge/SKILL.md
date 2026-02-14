---
name: cowi-agora-consumption-bridge
description: Pulls cortex-agora change_archive decisions by agora_ref and materializes relation_context_map plus skill_usage_adaptation_report artifacts for COWI manual mediation.
---

# COWI Agora Consumption Bridge

`00.cowi-agora-consumption-bridge`는 `cortex-agora/change_archive`를 pull해서
`relation_context_map`와 `skill_usage_adaptation_report` 초안을 생성한다.

## Purpose

- `cortex-agora output first` 원칙을 COWI 운영 루틴으로 고정
- `source_snapshot.agora_ref` 기준으로 feedback/decision 이벤트를 소비
- 수동 실행 기반 일일 배치(runbook) 제공
- 전략/고위험 워크플로우의 `T4 -> C1 -> H1` 구간에서 consumption step(`C1`)을 강제

## Inputs

- `02_Swarm/cortex-agora/change_archive/events/CHANGE_EVENTS.jsonl`
- `02_Swarm/cortex-agora/change_archive/events/PEER_FEEDBACK.jsonl`
- `02_Swarm/cortex-agora/change_archive/events/IMPROVEMENT_DECISIONS.jsonl`
- conversation source: `remembering-conversations` (optional, via `episodic-memory search`)

## Outputs

- `agents/<agent-family>/<version>/artifacts/relation_context_map/*.yaml`
- `agents/<agent-family>/<version>/artifacts/skill_usage_adaptation_report/*.md`
- `agents/<agent-family>/<version>/conversation_snapshots/*.md`

## Script

```bash
python3 04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/skills/00.cowi-agora-consumption-bridge/scripts/pull_agora_feedback.py \
  --proposal-id P-SWARM-V014-BATCH \
  --agent-family claude \
  --agent-version 4.0 \
  --conversation-source remembering-conversations \
  --conversation-session-id chat-2026-02-14 \
  --remembering-query "COWI COF AWT integration decisions"
```

### Dry-run

```bash
python3 04_Agentic_AI_OS/02_Swarm/context-orchestrated-workflow-intelligence/skills/00.cowi-agora-consumption-bridge/scripts/pull_agora_feedback.py \
  --proposal-id P-SWARM-V014-BATCH \
  --agent-family claude \
  --agent-version 4.0 \
  --conversation-session-id chat-2026-02-14 \
  --dry-run
```

## Trigger Policy

1. `IMPROVEMENT_DECISIONS` 신규 이벤트가 발생하면 즉시 수동 실행
2. 이벤트가 없더라도 일일 1회 수동 배치 실행

## H1 Finalization Guard

전략/고위험 워크플로우에서는 아래 산출물이 없으면 H1 finalization을 금지한다.

- `relation_context_map`
- `skill_usage_adaptation_report`

권장 검증 절차:

1. COWI pull bridge 실행
2. AWT H1 gate validator 실행
3. PASS일 때만 H1 승인 진행

## Guardrail

- COWI는 event pull/변환/보고서 생성까지만 수행한다.
- COF/AWT 실행 집행은 수행하지 않는다.
- 자동 스케줄러(cron)는 도입하지 않고 runbook 실행만 허용한다.
