---
name: cortex-agora-skill-governance
description: >
  Govern cortex-agora's instruction-nucleus skill, change_archive infrastructure,
  and behavior feed by validating metadata, archive integrity, and consumption contracts.
  Policy + checklist based; no auto-enforcement.
  Use when skill structure changes, archive drift is suspected, or COWI interface needs verification.
---

# cortex-agora-skill-governance

## Purpose

- instruction-nucleus 스킬 메타데이터, change_archive 무결성, 소비 계약 정합성을 점검한다.
- 자동 수정 없이 정책+체크리스트 기반으로 운영한다.
- 본 문서는 최소 로더이며 점검 로직은 레이어 모듈 문서에서 수행한다.

## Trigger

- instruction-nucleus 스킬 구조(frontmatter/sidecar) 변경 후 정합성 점검이 필요할 때
- change_archive JSONL 스키마/참조 무결성 drift가 의심될 때
- BEHAVIOR_FEED 스키마 변경 또는 COWI 소비 계약 변경 시
- 새 스킬 추가 또는 아카이브 정책 변경 시 거버넌스 점검

## Non-Negotiable Invariants

- `SKILL.meta.yaml`의 `context_id`는 불변이며 frontmatter `name`과 일치해야 한다.
- change_archive 3개 JSONL은 append-only: 기존 행 수정/삭제 금지.
- `PEER_FEEDBACK.linked_event_id`는 반드시 `CHANGE_EVENTS.event_id`를 참조해야 한다 (CC-02).
- `IMPROVEMENT_DECISIONS` status는 COWI가 소비 가능해야 한다 (CC-05).
- 자동 수정/자동 차단 금지. 점검 결과를 governance_check_report로 산출한다.
- DNA 금지사항 계승: 실행, 자동반영, 규칙수정, 에이전트호출, record_archive 직접조회 금지.

## Layer Index

| Layer | File | Role |
|-------|------|------|
| 00.meta | `00.meta/manifest.yaml` | 거버넌스 메타, 대상/인프라/CC map |
| 10.core | `10.core/core.md` | 원칙, 정의, 출력 형식 |
| 20.modules | `20.modules/modules_index.md` | metadata-validation / archive-integrity / consumption-contract |
| 30.references | `30.references/loading_policy.md` | 참조 로딩 트리거 |
| 40.orchestrator | `40.orchestrator/orchestrator.md` | 3-Phase 거버넌스 라우팅 |
| 90.tests | `90.tests/test_cases.yaml` | 17개 테스트 케이스 |

## Quick Start

3-Phase 점검 파이프라인:

1. **Phase 1 -- Metadata Validation**: instruction-nucleus frontmatter/sidecar 체크리스트 실행
2. **Phase 2 -- Archive Integrity**: change_archive 3개 JSONL 스키마, CC-01~CC-03 참조 무결성, bridge 명령 coverage, append-only 불변조건 점검
3. **Phase 3 -- Consumption Contract**: BEHAVIOR_FEED 스키마, COWI pull interface CC-05, cross-swarm recording completeness 점검

레지스트리 재생성 시 (COF 스크립트 사용):

```bash
python3 02_Swarm/context-orchestrated-filesystem/skills/04.skill-governance/scripts/sync_swarms_skill_manager.py \
  --swarm-root 02_Swarm --dry-run
```

## When Unsure

- frontmatter vs sidecar 충돌 시 `SKILL.meta.yaml`을 SoT로 우선한다.
- JSONL 필드 존재하지만 값이 빈 경우 WARN으로 기록하고 사용자에게 확인 요청한다.
- group_id vs trace_id 불일치 시 canonical `group_id` 기준으로 판단한다 (DNA v0.1.4).
- COWI 소비 주기가 미확인이면 WARN + 수동 검증 요청을 기록한다.
