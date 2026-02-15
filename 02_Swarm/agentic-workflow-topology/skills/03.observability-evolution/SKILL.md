---
name: awt-observability-evolution
description: >
  워크플로우 실행 로그를 관찰(Observe)하고, HITL 체크포인트와 이벤트 트리거로
  사용자와 상호작용(Interact)하며, 구조화된 개선 제안을 형제 스킬로 환류(Evolve)한다.
---

# awt-observability-evolution

## Purpose

- **Observe**: SQLite SoT + behavior feed에서 6종 이상 신호(AS)를 수집·분류한다.
- **Interact**: Scheduled/Event 체크포인트에서 사용자와 구조화된 피드백을 교환한다.
- **Evolve**: 증거 기반 개선 제안(IP)을 생성하여 cortex-agora를 통해 설계 스킬로 환류한다.
- 상세 절차는 레이어 모듈 문서에서 실행한다.

## Trigger

- 주간/격주 리뷰 수행 시 (scheduled)
- Critical 이상 신호 감지 시 (event)
- 사용자 명시 요청 시 (on_demand)
- behavior feed 수동 export 시

## Non-Negotiable Invariants

- 로그 SoT는 SQLite, export는 수동 경로만 (자동 반영 금지)
- 모든 개선 제안은 증거 + rollback rule 필수
- 실행 계층(COF/Manifestation) 직접 변경 금지
- Critical 이상 48h 무응답 시 halt_and_escalate_to_audit

## 5-Phase Process

```
Phase 1: Signal Collection   → observation-policy
Phase 2: Pattern Analysis     → observation-policy (분류)
Phase 3: HITL Checkpoint      → hitl-interaction
Phase 4: Improvement Proposal → improvement-proposal
Phase 5: Evolution Handoff    → evolution-tracking
```

## HITL Modes

| Mode | Trigger | 목적 |
|------|---------|------|
| Scheduled Checkpoint | OW 종료 시 | 누적 관찰 요약 + 피드백 수집 |
| Event Checkpoint | Critical AS 감지 | 즉시 알림 + 긴급 판단 요청 |

## Layer Index

| Layer | File | Role |
|---|---|---|
| 00.meta | `00.meta/manifest.yaml` | 운영 계약, 모듈/팩 레지스트리 |
| 10.core | `10.core/core.md` | 도메인 정의, 입력 인터페이스, when_unsure |
| 20.modules | `20.modules/modules_index.md` | 4개 직교 모듈 인덱스 |
| 30.references | `30.references/loading_policy.md` | ΔQ 기반 참조팩 로딩 |
| 40.orchestrator | `40.orchestrator/orchestrator.md` | 5-Phase 라우팅 |

## Quick Start

```bash
# Behavior feed export
python3 scripts/export_behavior_feed.py \
  --db-path 00.context/agent_log.db \
  --out-path behavior/BEHAVIOR_FEED.jsonl
```

## When Unsure

- 신호 분류 불확실 → 낮은 확신도로 기록 + 다음 SC에서 재검토
- 사용자 피드백 모호 → 구체화 질문 제시
- 근본 원인 경합 → 양쪽 가설 제시 + 사용자 판단 요청
- 심각도 불확실 → 보수적으로 한 단계 높은 심각도 적용
