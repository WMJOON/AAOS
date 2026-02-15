# SKILL 4-Layer Contract (v1)

## Purpose
- 3개 Swarm(AWT/COF/COWI)의 active skills를 동일한 4-Layer 구조로 운영하기 위한 SoT.
- `SKILL.md`를 최소 로더로 유지하고 상세 실행 규칙을 레이어 문서로 분리한다.

## Scope
- 포함: `02_Swarm/agentic-workflow-topology/skills/*`, `02_Swarm/context-orchestrated-filesystem/skills/*`, `02_Swarm/context-orchestrated-workflow-intelligence/skills/*`
- 제외: `reference/`, `cortex-agora`, `_shared`

## Required Structure
각 스킬 디렉토리는 아래를 가져야 한다.
- `00.meta/manifest.yaml`
- `10.core/core.md`
- `20.modules/modules_index.md`
- `30.references/loading_policy.md`
- `40.orchestrator/orchestrator.md`
- `40.orchestrator/routing_rules.md`
- `90.tests/test_cases.yaml`
- `90.tests/eval_rubric.md`

## SKILL.md Loader Rule
- 최대 120줄
- 필수 섹션
  - Trigger
  - Non-Negotiable Invariants
  - Layer Index
  - Quick Start
  - When Unsure
- 금지
  - 장문 runbook 인라인
  - 긴 JSON 예시 인라인
  - self-contained 단독 실행 정책

## Naming
- 스킬 디렉토리: `NN.role-slug`
- 레이어 디렉토리: 점 표기(`00.meta`, `10.core`, ...)

## Compatibility
- `SKILL.md` frontmatter `name/description` 유지
- `SKILL.meta.yaml`의 `context_id` 계약 유지
- 기존 `references/`, `scripts/`, `templates/` 경로는 호환 유지

## Enforcement Policy
- Phase A (current): 4-Layer 누락/로더 초과는 warning
- Phase B (next release): 동일 위반을 error로 승격

## Validation Checklist
- [ ] 대상 11개 스킬에 필수 레이어 디렉토리 존재
- [ ] 각 `SKILL.md` 라인수 <= 120
- [ ] self-contained 정책 문구 제거
- [ ] 레지스트리의 `layout_version=4layer-v1` 상태 반영
