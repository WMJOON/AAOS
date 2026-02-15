# Loading Policy

## 기본 규칙

항상 로딩:
- `10.core/core.md` -- 거버넌스 원칙, 점검 대상 목록, CC map, when_unsure
- `40.orchestrator/orchestrator.md` -- 3-Phase 프로세스, 라우팅 규칙

온디맨드 로딩:
- `20.modules/module.*.md` -- Phase별 필요 모듈만
- `references/skill_system_manifest.schema.yaml` -- manifest 검증 시
- `references/governance_check_report.template.md` -- 보고서 생성 시
- 각 governed skill의 schema 파일 -- contract-sync 시

## 거버넌스 전용 Reference 목록

| Reference | 파일 | 로딩 트리거 |
|-----------|------|------------|
| skill_system_manifest.schema | `references/skill_system_manifest.schema.yaml` | Phase 1에서 manifest 검증 시 |
| governance_check_report.template | `references/governance_check_report.template.md` | 최종 보고서 작성 시 |

## 외부 Schema Reference (Cross-Skill)

contract-sync 모듈 실행 시 아래 schema를 온디맨드 로딩:

| Schema | Path (relative to skills/) | 트리거 |
|--------|---------------------------|--------|
| mental_model_bundle | `00.mental-model-design/references/mental_model_bundle.schema.yaml` | CC-01 검증 시 |
| workflow_topology_spec | `01.topology-design/references/workflow_topology_spec.schema.json` | CC-02, CC-03 검증 시 |
| execution_plan | `02.execution-design/references/workflow_mental_model_execution_plan.schema.json` | CC-01, CC-04 검증 시 |

## 로딩 순서

```
Core + Orchestrator (항상)
  -> Phase 1: metadata-validation (모듈만, 필요 시 manifest schema)
  -> Phase 2: contract-sync (모듈 + cross-skill schema 파일들)
  -> Phase 3: registry-runbook (모듈만)
  -> 최종: governance_check_report template
```
