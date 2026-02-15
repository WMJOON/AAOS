---
name: cof-glob-indexing
description: Resolves the nearest COF /[n].index/ from a target directory, scans within that node boundary, and writes NODE_INDEX.md and ROLE_EVIDENCE.md under the resolved index. Use when the user needs COF context boundary detection, role directory inference, or anchor discovery.
---

# cof-glob-indexing

## Purpose
- 대상 경로의 COF 경계와 role evidence를 인덱싱한다.
- 상세 스캔/검증 규칙은 모듈 문서로 분리한다.

## Trigger
- nearest index 경계 탐지가 필요할 때
- NODE_INDEX.md / ROLE_EVIDENCE.md를 갱신할 때
- role 디렉토리 추론/anchor 탐색이 필요할 때

## Non-Negotiable Invariants
- 스캔 범위는 nearest index 경계 밖으로 확장하지 않는다.
- 산출물은 resolved index 노드 아래에만 기록한다.
- 숨김/예외 디렉토리 정책을 일관 적용한다.
- 경로 파싱 실패 시 fail-fast.

## Layer Index
| Layer | File | Role |
|---|---|---|
| 00.meta | `00.meta/manifest.yaml` | 스캔 정책 메타 |
| 10.core | `10.core/core.md` | 공통 스캔 계약 |
| 20.modules | `20.modules/modules_index.md` | 경계/산출/검증 모듈 |
| 30.references | `30.references/loading_policy.md` | 참조 로딩 규칙 |
| 40.orchestrator | `40.orchestrator/orchestrator.md` | 스캔 라우팅 |

## Quick Start
```bash
python3 02_Swarm/context-orchestrated-filesystem/skills/01.glob-indexing/scripts/cof_glob_indexing.py \
  --target "/path/to/node"
```

## When Unsure
- 경계 선택이 애매하면 `module.boundary-resolution.md` 기준으로 보수적으로 축소한다.
