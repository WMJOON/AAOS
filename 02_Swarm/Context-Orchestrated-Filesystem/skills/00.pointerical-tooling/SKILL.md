---
name: cof-pointerical-tooling
description: Creates pointer-safe COF Skill/Rule/Workflow/Sub-Agent documents. Use when creating or updating COF docs.
---

# cof-pointerical-tooling

## Purpose
- COF 문서를 pointer-safe 규약으로 생성/정리한다.
- `SKILL.md`는 최소 로더이며 상세 생성 규칙은 레이어 모듈에서 관리한다.

## Trigger
- 새 SKILL/RULE/WORKFLOW/SUB-AGENT 문서를 만들 때
- `SKILL.md` + `SKILL.meta.yaml`를 함께 정합화해야 할 때
- COF 하드 제약 위반을 사전 차단해야 할 때

## Non-Negotiable Invariants
- `SKILL.md`는 표준 frontmatter만 허용(`name`, `description`, 선택 `allowed-tools`).
- COF 식별 메타는 `SKILL.meta.yaml`로 관리.
- `context_id`는 전역 유일, 불변.
- 직접 `mkdir/touch` 남용 대신 생성 스크립트를 우선 사용.

## Layer Index
| Layer | File | Role |
|---|---|---|
| 00.meta | `00.meta/manifest.yaml` | 생성 정책 메타 |
| 10.core | `10.core/core.md` | 공통 문서 계약 |
| 20.modules | `20.modules/modules_index.md` | script/template/guardrail 모듈 |
| 30.references | `30.references/loading_policy.md` | 참조 로딩 기준 |
| 40.orchestrator | `40.orchestrator/orchestrator.md` | 생성 흐름 라우팅 |

## Quick Start
```bash
python3 02_Swarm/context-orchestrated-filesystem/skills/00.pointerical-tooling/scripts/create_pointerical_doc.py \
  --type skill --title "My Skill" --out "/path/to/SKILL.md" \
  --context-id cof-my-skill --name "my-skill" --description "Use when ..."
```

## When Unsure
- 문서 타입이 불명확하면 `module.template-manual.md`를 먼저 확인한다.
- 메타 충돌 시 `SKILL.meta.yaml`를 식별 SoT로 고정한다.
