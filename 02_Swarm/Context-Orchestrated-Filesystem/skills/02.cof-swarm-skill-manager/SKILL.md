---
name: cof-swarm-skill-manager
description: Manage skills across each Swarm by scanning skill directories, generating per-swarm registries, detecting duplicate context IDs, and warning when a Swarm has overloaded skill sets. Use when you need to reduce skill sprawl and keep skill inventories reliable.
---

# COF Swarm Skill Manager

각 Swarm의 `SKILL.md`를 스캔해 **스킬 레지스트리**를 생성하고, 과도한 스킬 증가를 감지하여 오퍼레이터가 스킬 구조를 정리하기 쉽도록 지원한다.

## When to Use

- 여러 Swarm의 Skill 목록을 한 번에 갱신할 때
- `SKILL.md` 누락/메타데이터 결손을 점검할 때
- Swarm별/전체 스킬 수 과다 경고가 필요한 경우
- 에이전트가 어떤 스킬을 상속했는지 빠르게 추적할 때

## Quick Start

```bash
python3 scripts/sync_swarms_skill_manager.py \
  --swarm-root "/path/to/04_Agentic_AI_OS/02_Swarm" \
  --max-skills 8
```

실행 결과:
- 각 Swarm 루트에 `SKILL_REGISTRY.md` 생성
- 전체 요약 파일 `02_Swarm/registry/SWARM_SKILL_REGISTRY.md` 생성
- 경고(중복 context_id, 과다 skill 보유, 누락 필드)를 콘솔에 출력

## Inputs

- `--swarm-root` (required): Swarm 루트 디렉토리 경로. 기본값: 스크립트 기준 상위 `02_Swarm`.
- `--max-skills` (default: 8): Swarm별 경고 임계치.
- `--json` (optional): 전역 JSON 레지스트리 경로. 지정 시 `SWARM_SKILL_REGISTRY.json` 생성.
- `--skip-write`: 파일 생성/갱신 없이 진단만 수행.
- `--dry-run`: `--skip-write`와 동일하게 동작.

## Outputs

- `SKILL_REGISTRY.md`: 각 Swarm 루트에 생성되는 스킬 레지스트리
- `02_Swarm/registry/SWARM_SKILL_REGISTRY.md`: 전체 스웜 요약
- 콘솔 보고서: 과다 스킬, 누락 `SKILL.md`, 중복 `context_id` 등

## Workflow

1. 지정한 Swarm 루트 하위에서 `skills/` 또는 `SKILLS/` 폴더를 탐색.
2. 하위 디렉토리의 `SKILL.md` frontmatter를 파싱.
3. 해당 Swarm의 AGENT 문서를 읽어 `inherits_skill` 정보를 집계.
4. 누락 필드, 중복 `context_id`, 과다 스킬 수(임계치 초과) 경고를 계산.
5. Swarm 및 전체 요약 레지스트리를 생성.

## Notes

- 이 스킬은 생성/수정/삭제 의사결정을 직접 수행하지 않고, 판단 근거를 제공한다.
- 스킬이 과도하게 늘어나는 것은 경고이며, 실제 분할/상속 정리 결정은 설계 토의로 처리한다.

## References

- Governance: `../00.cof-pointerical-tool-creator/references/cof-environment-set.md`
- Parent Skill: `00.cof-pointerical-tool-creator`
- Neighbor Skills: `cof-glob-indexing`, `cof-task-manager-node`, `cof-task-solver-agent-group`
