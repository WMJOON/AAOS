---
name: cof-skill-governance
description: Manage skills across each Swarm by scanning skill directories, generating per-swarm registries, detecting duplicate context IDs, and warning when a Swarm has overloaded skill sets. Use when you need to reduce skill sprawl and keep skill inventories reliable.
---

# cof-skill-governance

## Purpose
- Swarm 스킬 레지스트리 생성/검증을 수행한다.
- 4-Layer 정합성 검사를 단계적으로 강제한다(Warn -> Error).

## Trigger
- 스킬 구조 변경 이후 레지스트리 동기화가 필요할 때
- frontmatter/sidecar 계약 검증이 필요할 때
- Swarm 과적재/중복 context_id를 탐지할 때

## Non-Negotiable Invariants
- `SKILL.md` frontmatter 정책을 준수한다.
- `SKILL.meta.yaml` required keys 누락 금지.
- 4-Layer 필수 디렉토리 누락은 Phase A 경고, Phase B 오류.
- 레지스트리와 실제 경로 불일치 금지.

## Layer Index
| Layer | File | Role |
|---|---|---|
| 00.meta | `00.meta/manifest.yaml` | 검증 정책 메타 |
| 10.core | `10.core/core.md` | 공통 검증 기준 |
| 20.modules | `20.modules/modules_index.md` | scan/sync/frontmatter 모듈 |
| 30.references | `30.references/loading_policy.md` | 참조 로딩 |
| 40.orchestrator | `40.orchestrator/orchestrator.md` | 검증 라우팅 |

## Quick Start
```bash
python3 02_Swarm/context-orchestrated-filesystem/skills/04.skill-governance/scripts/sync_swarms_skill_manager.py \
  --swarm-root 02_Swarm --dry-run
```

## When Unsure
- 정책 판정이 애매하면 warning으로 기록하고 remediation 항목을 남긴다.
