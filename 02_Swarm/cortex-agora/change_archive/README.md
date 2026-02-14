---
name: cortex-agora-change-archive
description: cortex-agora 변경/비판/개선 이력을 append-only로 기록하고, 주기적으로 Nucleus record_archive로 봉인하는 브릿지 운영 장치.
status: canonical
updated: "2026-02-14"
---

# Cortex Agora Change Archive

`change_archive/`는 cortex-agora 제안 산출물의 변경 이력, 동료 비판, 개선 결정을 append-only로 기록하는 로컬 운영 계층이다.
장기 immutable SoT는 Nucleus `record_archive`이며, 본 경로는 봉인 전 staging/추적 계층으로 사용한다.

## Core Principles

- Append-only: 기존 이벤트 수정/삭제 금지
- Optional critique: 비판은 권장사항이며 상태 전환의 필수 차단 게이트는 아님
- Source-of-truth link: 모든 개선/비판은 `source_snapshot.agora_ref` 기반으로 추적
- Stage-then-seal: 로컬 기록 후 주기적으로 `record_archive`로 봉인

## Layout

```text
change_archive/
├── README.md
├── events/
│   ├── CHANGE_EVENTS.jsonl
│   ├── PEER_FEEDBACK.jsonl
│   └── IMPROVEMENT_DECISIONS.jsonl
├── indexes/
│   └── CHANGE_INDEX.md
└── templates/
    ├── CHANGE_EVENT.template.yaml
    ├── PEER_FEEDBACK.template.yaml
    └── IMPROVEMENT_DECISION.template.yaml
```

## Event Contracts

1. `events/CHANGE_EVENTS.jsonl`
- event_id, ts, proposal_id, change_type, actor, source_snapshot, artifact_ref, status

2. `events/PEER_FEEDBACK.jsonl`
- feedback_id, ts, proposal_id, reviewer, reviewer_model_family, reviewer_provider, stance, summary, linked_event_id

3. `events/IMPROVEMENT_DECISIONS.jsonl`
- decision_id, ts, proposal_id, decision, rationale, applied_event_ids, feedback_refs, next_action

## Bridge Runbook

1. 변경 기록
```bash
python3 04_Agentic_AI_OS/02_Swarm/cortex-agora/scripts/change_archive_bridge.py \
  record-change --proposal-id P-001 --change-type created --actor agent:cortex \
  --artifact-ref 02_Swarm/cortex-agora/skills/cortex-agora-instruction-nucleus/SKILL.md \
  --agora-ref agora://proposal/P-001 --captured-at 2026-02-14T10:00:00Z --status open
```

2. 비판 기록(선택)
```bash
python3 04_Agentic_AI_OS/02_Swarm/cortex-agora/scripts/change_archive_bridge.py \
  record-feedback --proposal-id P-001 --reviewer agent:cowi \
  --reviewer-model-family openai-gpt --reviewer-provider OpenAI \
  --stance critique --summary "handoff 조건이 모호함" --linked-event-id ce_...
```

3. 개선 결정 기록
```bash
python3 04_Agentic_AI_OS/02_Swarm/cortex-agora/scripts/change_archive_bridge.py \
  record-decision --proposal-id P-001 --decision accepted \
  --rationale "조건 분기 명확화 반영" --applied-event-ids ce_... \
  --feedback-refs fb_... --next-action "weekly seal batch"
```

4. 패키지 생성(staging)
```bash
python3 04_Agentic_AI_OS/02_Swarm/cortex-agora/scripts/change_archive_bridge.py \
  build-package --from-ts 2026-02-14T00:00:00Z --to-ts 2026-02-14T23:59:59Z \
  --out /tmp/cortex-agora-change-package
```

5. Nucleus record_archive 봉인(명시적 실행)
```bash
python3 04_Agentic_AI_OS/02_Swarm/cortex-agora/scripts/change_archive_bridge.py \
  seal-to-record-archive --package-dir /tmp/cortex-agora-change-package \
  --record-archive-root 04_Agentic_AI_OS/01_Nucleus/record_archive \
  --summary "cortex-agora weekly change review" \
  --targets "04_Agentic_AI_OS/02_Swarm/cortex-agora" \
  --notes "weekly seal"
```
