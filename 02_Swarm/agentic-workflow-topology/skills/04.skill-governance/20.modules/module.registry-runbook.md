# module.registry-runbook

## Purpose

AWT 로컬 레지스트리(`registry/SKILL_REGISTRY.md`)와 Swarm 레지스트리(`02_Swarm/cortex-agora/registry/SWARM_SKILL_REGISTRY.md`)가
실제 디렉토리 상태와 일치하는지 점검하고, 불일치 시 재생성 절차를 안내한다.

## Scope

- AWT 로컬 레지스트리 vs 실제 스킬 디렉토리 일치
- Swarm-level 레지스트리 vs AWT 로컬 레지스트리 일치
- context_id 중복 검출 (AWT 내부 + cross-swarm)
- 레지스트리 재생성 runbook

## Inputs

- `02_Swarm/agentic-workflow-topology/registry/SKILL_REGISTRY.md`
- `02_Swarm/cortex-agora/registry/SWARM_SKILL_REGISTRY.md`
- `02_Swarm/cortex-agora/registry/GLOBAL_SKILL_REGISTRY.json`
- 실제 `skills/` 디렉토리 구조

---

## Checklist: Registry <-> Directory Consistency

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| RG-01 | 레지스트리의 각 skill 항목 vs `skills/` 디렉토리 존재 | 1:1 대응 | FAIL |
| RG-02 | `skills/`에 있지만 레지스트리에 없는 디렉토리 | 없어야 함 | WARN |
| RG-03 | 레지스트리에 있지만 `skills/`에 없는 항목 | 없어야 함 | FAIL |
| RG-04 | 레지스트리의 `Name` == 해당 skill의 `SKILL.md` frontmatter `name` | 일치 | WARN |
| RG-05 | 레지스트리의 `Context ID` == 해당 skill의 `SKILL.meta.yaml` `context_id` | 일치 | FAIL |
| RG-06 | 레지스트리의 `Layout` == `4layer-v1` | 모든 AWT 스킬 | WARN |
| RG-07 | 레지스트리의 Skill count == 실제 스킬 디렉토리 수 | 일치 | WARN |

## Checklist: Cross-Swarm Consistency

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| XS-01 | SWARM_SKILL_REGISTRY의 AWT 섹션 vs AWT 로컬 레지스트리 | 항목 수/이름 일치 | WARN |
| XS-02 | GLOBAL_SKILL_REGISTRY.json의 AWT 항목 vs AWT 로컬 | context_id 목록 일치 | WARN |
| XS-03 | context_id cross-swarm 중복 없음 | `awt-*` prefix는 AWT에만 | FAIL |

## Checklist: Deprecation/Lifecycle

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| DP-01 | deprecated 상태 스킬이 레지스트리에 표기 | `status: deprecated` 반영 | WARN |
| DP-02 | SKILL_RENAME_MAP.md와 현재 레지스트리 일치 | old name으로 참조하는 곳 없음 | WARN |

---

## 재생성 절차 (Registry Regeneration Runbook)

```
1. Dry-run으로 현재 불일치 확인:
   python3 02_Swarm/context-orchestrated-filesystem/skills/04.skill-governance/scripts/sync_swarms_skill_manager.py \
     --swarm-root 02_Swarm --dry-run

2. 불일치 항목 review (stdout 확인)

3. 사용자 승인 후 실제 재생성:
   python3 02_Swarm/context-orchestrated-filesystem/skills/04.skill-governance/scripts/sync_swarms_skill_manager.py \
     --swarm-root 02_Swarm

4. 생성된 레지스트리 diff 확인 (git diff)

5. governance_check_report의 registry_sync_status 갱신
```

---

## Outputs

- Per-registry check results (`governance_check_report.registry_sync_status` 섹션)
- 재생성 필요 여부 판정
- 재생성 후 diff summary

## When Unsure

- 디렉토리는 있지만 SKILL.md가 없는 경우: WIP 스킬로 분류, WARN 기록.
- 레지스트리 형식이 변경된 경우: 이전 형식과 현재 형식 양쪽 제시, 사용자 판단 요청.
