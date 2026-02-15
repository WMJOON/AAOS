# module.contract-sync

## Purpose

AWT 스킬 파이프라인의 5개 스킬 간 계약 결합점(CC-01~CC-05)이 정합적인지 점검한다.
이 모듈은 AWT 거버넌스의 핵심 차별화 요소이다.

## Scope

- Schema key 생산-소비 정합성
- Required key 누락 검출
- Optional extension 하위호환 검증
- Feedback loop closure 검증

## Inputs

- 각 skill의 schema 파일:
  - `00.mental-model-design/references/mental_model_bundle.schema.yaml`
  - `01.topology-design/references/workflow_topology_spec.schema.json`
  - `02.execution-design/references/workflow_mental_model_execution_plan.schema.json`
- 각 skill의 `10.core/core.md` (Input/Output Contract 섹션)
- `03.observability-evolution/40.orchestrator/orchestrator.md` (Phase 4 target_skill routing)

---

## CC-01: local_charts -> node_chart_map

Skill 00의 `mental_model_bundle.local_charts[].id`가 Skill 02의 `node_chart_map[].chart_ids`에서 참조될 때 정합성.

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| CC01-01 | `mental_model_bundle.local_charts[].id` 정의 존재 | schema에 required로 명시 | FAIL |
| CC01-02 | `execution_plan.node_chart_map[].chart_ids` 정의 존재 | schema에 required, minItems:1 | FAIL |
| CC01-03 | Skill 02 core.md가 "chart_ids의 모든 ID는 bundle.local_charts에 존재" 명시 | Global Invariant에 명시 | WARN |
| CC01-04 | `local_charts[].id` type == string, `chart_ids` items type == string | 타입 일치 | FAIL |

## CC-02: theta_gt_band -> mode-policy

Skill 01의 `task_graph.nodes[].theta_gt_band`가 Skill 02의 mode 배정 입력으로 사용될 때 정합성.

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| CC02-01 | Skill 01 schema에 `nodes[].theta_gt_band` 또는 `nodes[].theta_gt` 경로 존재 | 정의됨 | WARN |
| CC02-02 | Skill 02 `module.mode-policy.md`에 theta_GT 입력 참조 명시 | mode 배정 테이블에서 theta_GT 사용 | WARN |
| CC02-03 | Skill 02 core.md의 Input Contract에 `workflow_topology_spec` 의존 명시 | required로 선언 | FAIL |
| CC02-04 | theta_GT 값 범위 기대 (0~1 또는 L0~L4) 양쪽에서 일관적 | 동일 scale 사용 | WARN |

## CC-03: explicit_output.type -> mode selection

Skill 01의 `task_graph.nodes[].explicit_output.type`이 Skill 02의 mode selection에 영향을 줄 때 정합성.

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| CC03-01 | Skill 01 node 스키마에 `explicit_output` 필드 정의 | type 속성 포함 | WARN |
| CC03-02 | Skill 02 mode selection이 explicit_output.type 참조 | mode-policy 모듈에서 참조 존재 | WARN |

## CC-04: node_chart_map -> observability baseline

Skill 02의 `node_chart_map`이 Skill 03의 관찰 기준선으로 사용될 때 정합성.

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| CC04-01 | Skill 02 출력 schema에 `node_chart_map` required | required 목록에 포함 | FAIL |
| CC04-02 | Skill 03의 입력 인터페이스에 `workflow_spec_ref` 경로 | optional이지만 관찰 기준선 역할 명시 | WARN |
| CC04-03 | Skill 03 core.md에서 "execution plan 참조" 언급 | 기대 동작 기준선으로 사용 명시 | WARN |

## CC-05: improvement_proposal -> feedback loop

Skill 03의 `improvement_proposal`이 Skill 01/02로 환류될 때 정합성.

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| CC05-01 | Skill 03 `module.improvement-proposal`에서 `target_skill` 분류 규칙 존재 | topology/execution/operational 분류 | WARN |
| CC05-02 | Skill 03 `module.evolution-tracking`에서 lifecycle 추적 | `draft -> user_reviewed -> submitted -> accepted/rejected` | WARN |
| CC05-03 | cortex-agora 또는 COWI를 통한 환류 경로 명시 | agora 제출 경로 기술 | WARN |
| CC05-04 | Skill 01/02가 improvement_proposal을 수신하는 인터페이스 명시 | core.md 또는 manifest.yaml에 관련 참조 존재 | WARN |

---

## Schema Version Drift Check

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| SV-01 | 각 governed skill의 `manifest.yaml.version` 기록 | semver 존재 | WARN |
| SV-02 | schema 파일 변경 시 version bump 여부 | major/minor/patch 적절성 | WARN |
| SV-03 | 하위호환 위반 시 major bump | breaking change = major | WARN |

---

## Outputs

- Per-coupling-point check results (`governance_check_report.dependency_checks` 섹션)
- FAIL 항목: 즉시 수정 필요 목록
- WARN 항목: 다음 거버넌스 점검 시까지 추적 목록

## When Unsure

- 결합 관계가 명시적이지 않을 때: 양쪽 schema + core.md를 나란히 비교하여 제시, 사용자 판단 요청.
- schema 변경이 양쪽에서 동시에 진행 중일 때: 양쪽 변경 내역을 나란히 보여주고 어느 쪽이 선행해야 하는지 제안.
- optional extension의 결합 여부: optional이라도 실제 사용 중이면 WARN으로 추적.
