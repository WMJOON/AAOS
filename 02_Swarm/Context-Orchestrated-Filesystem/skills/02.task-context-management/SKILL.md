---
name: cof-task-context-management
description: "Creates and manages `NN.agents-task-context/` nodes (tickets, verification, validation, archiving) for persistent agent context tracking in COF. (legacy: `task-manager/`)"
---

# cof-task-context-management

## Purpose
- 작업 맥락 노드와 티켓 라이프사이클을 관리한다.
- 로더는 최소화하고 실제 절차는 모듈 문서로 위임한다.

## Trigger
- 새 task-context 노드를 생성할 때
- 티켓 발행/검증/아카이브를 수행할 때
- legacy `task-manager` 경로를 마이그레이션할 때

## Non-Negotiable Invariants
- 표준 노드/티켓 템플릿과 frontmatter 규약을 준수한다.
- 상태 전이(`todo -> in-progress -> done|blocked`)는 추적 가능해야 한다.
- 검증 실패 티켓은 완료 처리 금지.
- 경로/의존성 누락은 즉시 오류로 처리.

## Layer Index
| Layer | File | Role |
|---|---|---|
| 00.meta | `00.meta/manifest.yaml` | 라이프사이클 메타 |
| 10.core | `10.core/core.md` | 공통 컨텍스트 규칙 |
| 20.modules | `20.modules/modules_index.md` | bootstrap/lifecycle/archive 모듈 |
| 30.references | `30.references/loading_policy.md` | 참조 로딩 기준 |
| 40.orchestrator | `40.orchestrator/orchestrator.md` | 작업 흐름 라우팅 |

## Quick Start
```bash
python3 02_Swarm/context-orchestrated-filesystem/skills/02.task-context-management/scripts/create_node.py \
  --path "/target/directory"
```

## When Unsure
- 템플릿 선택이 애매하면 `module.node-bootstrap.md`를 우선 적용한다.
- 라이프사이클 충돌은 `module.ticket-lifecycle.md` 규칙을 따른다.
