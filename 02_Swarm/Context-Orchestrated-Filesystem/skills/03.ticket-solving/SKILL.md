---
name: cof-ticket-solving
description: Dispatch tickets to AI CLI agents based on tag heuristics. Use when automating ticket-based agent workflows or coordinating multi-agent collaboration.
---

# cof-ticket-solving

## Purpose
- 티켓을 적절한 에이전트 그룹으로 라우팅하고 실행 결과를 반영한다.
- 상세 디스패치/에러 정책은 레이어 모듈에서 관리한다.

## Trigger
- `status: todo` 티켓을 실행해야 할 때
- 태그 기반 에이전트 선택/재시도가 필요할 때
- 실행 결과를 ticket frontmatter에 반영해야 할 때

## Non-Negotiable Invariants
- 티켓 frontmatter 파싱 실패 시 실행 중단.
- 상태 전이는 순서대로만 허용.
- dependencies 미충족 티켓은 실행 금지.
- 결과 로그는 추적 가능하게 저장.

## Layer Index
| Layer | File | Role |
|---|---|---|
| 00.meta | `00.meta/manifest.yaml` | 실행 메타 |
| 10.core | `10.core/core.md` | 공통 디스패치 원칙 |
| 20.modules | `20.modules/modules_index.md` | selection/flow/error 모듈 |
| 30.references | `30.references/loading_policy.md` | 참조 로딩 기준 |
| 40.orchestrator | `40.orchestrator/orchestrator.md` | 티켓 라우팅 |

## Quick Start
```bash
python3 02_Swarm/context-orchestrated-filesystem/skills/03.ticket-solving/scripts/solve_ticket.py \
  --ticket /path/to/tickets/TKT-0001.md
```

## When Unsure
- 에이전트 선택 확신이 낮으면 `module.agent-selection.md`의 보수 규칙을 적용한다.
- 오류 분류는 `module.error-policy.md` 우선.
