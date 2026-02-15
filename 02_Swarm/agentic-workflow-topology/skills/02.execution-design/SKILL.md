---
name: awt-execution-design
description: Design how each workflow task node should apply mental models/charts at execution time. Produces `workflow_mental_model_execution_plan` with `bundle_ref` and `node_chart_map` from topology and mental model bundle.
---

# awt-execution-design

## Purpose
- `workflow_topology_spec` + `mental_model_bundle` → `workflow_mental_model_execution_plan` 매핑.
- `SKILL.md`는 로더이며 상세 규칙은 모듈 문서로 위임한다.

## Trigger
- 노드별 chart 적용 방식이 필요할 때
- θ_GT 기반 mode/model 배정이 필요할 때
- handoff 계약과 fallback 정책을 실행 단계로 연결해야 할 때

## Non-Negotiable Invariants
- 입력은 `workflow_topology_spec` + `mental_model_bundle`만 허용.
- 출력은 7개 required 키를 모두 포함: `bundle_ref`, `node_chart_map`, `task_to_chart_map`, `node_mode_policy`, `model_selection_policy`, `handoff_contract`, `fallback_rules`.
- checkpoint(`preflight`, `pre_h1`, `pre_h2`)와 node_chart_map 정합성 유지.
- chart_ids 빈 배열 금지, bundle에 없는 chart_id 참조 금지.
- optional 확장 필드가 없어도 기본 소비 계약은 깨지지 않아야 함.

## Module → Output Key Mapping
| Module | Output Keys |
|---|---|
| `module.node-mapping` | `bundle_ref`, `node_chart_map`, `task_to_chart_map` |
| `module.mode-policy` | `node_mode_policy`, `model_selection_policy` |
| `module.fallback-handoff` | `handoff_contract`, `fallback_rules` |

## Layer Index
| Layer | File | Role |
|---|---|---|
| 00.meta | `00.meta/manifest.yaml` | 계획 계약 메타 |
| 10.core | `10.core/core.md` | 공통 매핑 원칙 · 용어 · 스키마 키 소유권 |
| 20.modules | `20.modules/modules_index.md` | node-mapping · mode-policy · fallback-handoff |
| 30.references | `30.references/loading_policy.md` | reference 로딩 규칙 |
| 40.orchestrator | `40.orchestrator/orchestrator.md` | 실행 조합 라우팅 |

## Quick Start
- 입력 스키마: `references/workflow_mental_model_execution_plan.schema.json`
- chart 할당: `20.modules/module.node-mapping.md`
- θ_GT → mode: `20.modules/module.mode-policy.md` (참조: `reference/workflow-cone-analyzer/CONE_PROFILES.md`)

## When Unsure
- 모드 충돌은 `module.mode-policy.md` Override 규칙 우선.
- handoff 불확실성은 `module.fallback-handoff.md` 기준으로 보수 처리.
- θ_GT 추정 불확실 시 `reference/workflow-cone-analyzer/CONE_PROFILES.md` 로딩.
