---
name: cowi-agora-consumption-bridge
description: Pulls cortex-agora change_archive decisions by agora_ref and materializes relation_context_map plus skill_usage_adaptation_report artifacts for COWI manual mediation, including strategy/high-risk H1 gate support.
---

# cowi-agora-consumption-bridge

## Purpose
- Agora 개선 결정을 pull해 COWI 산출물로 물질화한다.
- 로더는 최소화하고 소비/산출/H1-guard 절차는 모듈 문서에서 실행한다.

## Trigger
- `IMPROVEMENT_DECISIONS` 신규 이벤트를 반영할 때
- `relation_context_map`/`skill_usage_adaptation_report`를 생성해야 할 때
- strategy/high_risk H1 finalization 증빙이 필요할 때

## Non-Negotiable Invariants
- source-of-truth 키는 `source_snapshot.agora_ref`.
- 자동 집행/자동 차단은 수행하지 않는다.
- COWI 산출물 누락 시 H1 finalization 허용 금지.
- cursor 상태(`registry/AGORA_PULL_STATE.json`)를 일관 유지.

## Layer Index
| Layer | File | Role |
|---|---|---|
| 00.meta | `00.meta/manifest.yaml` | 소비 계약 메타 |
| 10.core | `10.core/core.md` | 공통 소비 규칙 |
| 20.modules | `20.modules/modules_index.md` | pull/materialize/h1-guard 모듈 |
| 30.references | `30.references/loading_policy.md` | 참조 로딩 규칙 |
| 40.orchestrator | `40.orchestrator/orchestrator.md` | 소비 라우팅 |

## Quick Start
```bash
python3 02_Swarm/context-orchestrated-workflow-intelligence/skills/00.agora-consumption-bridge/scripts/pull_agora_feedback.py \
  --proposal-id P-SWARM-V014-BATCH --agent-family claude --agent-version 4.0
```

## When Unsure
- 이벤트 해석 불확실성은 낮은 확신도로 보고서에 표기하고 수동 검토로 넘긴다.
