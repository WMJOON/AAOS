---
name: workflow-skill-manager
description: Manage the 01~04 workflow skills in agentic-workflow-topology. Validates metadata/dependencies/contracts and maintains local+swarm registry runbook using policy and checklist (no auto enforcement).
---

# Workflow Skill Manager

`00.workflow-skill-manager`는 `agentic-workflow-topology` 내부 스킬 체계를 관리한다.

## Managed Skills

- `01.mental-model-loader`
- `02.workflow-topology-scaffolder`
- `03.workflow-mental-model-execution-designer`
- `04.workflow-observability-and-evolution`

## Responsibilities

1. 스킬 계약/버전/의존성/deprecation 정책 관리
2. 메타데이터 정합성 점검 (허용 frontmatter 키/개수, 필수 키 `name`/`description`)
3. 레지스트리 갱신 runbook 운영 (로컬 + swarm registry)
4. 변경 승인 체크리스트 운영 (수동 점검, 자동 집행 없음)

## Output Contracts

### `skill_system_manifest` (YAML)

필수 키:
- `skill_id`
- `version`
- `status`
- `depends_on`
- `contracts`
- `deprecation_policy`

스키마: `references/skill_system_manifest.schema.yaml`

### `governance_check_report` (Markdown/JSON)

필수 섹션:
- `metadata_checks`
- `dependency_checks`
- `compatibility_checks`
- `registry_sync_status`
- `action_items`

템플릿: `references/governance_check_report.template.md`

## Checklist (Policy + Manual)

- [ ] 01~04 `SKILL.md` frontmatter가 Claude Skills 허용 키 정책을 만족한다.
- [ ] 01~04 `SKILL.md`에 필수 키 `name`, `description`이 존재한다.
- [ ] legacy alias가 존재하는 경우, 라우팅/종료 조건이 문서화되어 있다.
- [ ] active skill contracts(`mental_model_bundle`, `workflow_topology_spec`, `workflow_mental_model_execution_plan`, `workflow_improvement_report`) 연결이 맞다.
- [ ] 레지스트리 파일이 최신이다.

## Registry Runbook

```bash
python3 04_Agentic_AI_OS/02_Swarm/context-orchestrated-filesystem/skills/02.cof-swarm-skill-manager/scripts/sync_swarms_skill_manager.py \
  --swarm-root 04_Agentic_AI_OS/02_Swarm \
  --dry-run
```

참고:
- 위 스크립트는 legacy `context_id` 검사 로직이 남아 있을 수 있다.
- Claude Skills 정책(`name`, `description`)과 충돌하면 레지스트리는 수동으로 업데이트하고, frontmatter를 확장하지 않는다.

이 스킬은 자동 수정/자동 차단을 수행하지 않는다.
