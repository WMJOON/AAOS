# module.metadata-validation

## Purpose

AWT 4개 governed skill(00~03)의 메타데이터, 사이드카, 4-Layer 구조를 정책 기준으로 점검한다.

## Scope

- SKILL.md frontmatter 검증
- SKILL.meta.yaml sidecar 검증
- 4-Layer 필수 디렉토리 존재 여부
- 00.meta/manifest.yaml 내부 일관성

## Inputs

- 각 governed skill의 디렉토리 경로 (`00.meta/manifest.yaml`의 `governed_skills[].dir`)
- 정책 기준: `SKILL_4LAYER_CONTRACT.md`, `00.meta/manifest.yaml`

---

## Checklist: SKILL.md Frontmatter (per skill)

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| FM-01 | `name` 필드 존재 | required string | FAIL |
| FM-02 | `description` 필드 존재 | required string, "Use when..." 포함 권장 | WARN |
| FM-03 | `name` 값이 `awt-{role-slug}` 패턴 | prefix=awt- | WARN |
| FM-04 | SKILL.md 총 줄 수 | <= 120 | Phase A: WARN / Phase B: FAIL |
| FM-05 | 필수 섹션 존재 | Trigger, Non-Negotiable Invariants, Layer Index, Quick Start, When Unsure | WARN |

## Checklist: SKILL.meta.yaml Sidecar (per skill)

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| SC-01 | 파일 존재 | `SKILL.meta.yaml` 존재 | FAIL |
| SC-02 | `context_id` 존재 | required, immutable | FAIL |
| SC-03 | `context_id` == frontmatter `name` | 일치 | FAIL |
| SC-04 | `role` 필드 | `SKILL` | WARN |
| SC-05 | `state` 필드 | const / mutable / active / frozen / archived 중 하나 | WARN |
| SC-06 | `scope` 필드 | `swarm` | WARN |
| SC-07 | `lifetime` 필드 | persistent / ticket / archived 중 하나 | WARN |
| SC-08 | `version` 필드 존재 | semver 권장 | WARN |

## Checklist: 4-Layer Structure (per skill)

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| 4L-01 | `00.meta/manifest.yaml` 존재 | required | Phase A: WARN / Phase B: FAIL |
| 4L-02 | `10.core/core.md` 존재 | required | Phase A: WARN / Phase B: FAIL |
| 4L-03 | `20.modules/modules_index.md` 존재 | required | Phase A: WARN / Phase B: FAIL |
| 4L-04 | `30.references/loading_policy.md` 존재 | required | Phase A: WARN / Phase B: FAIL |
| 4L-05 | `40.orchestrator/orchestrator.md` 존재 | required | Phase A: WARN / Phase B: FAIL |
| 4L-06 | `40.orchestrator/routing_rules.md` 존재 | required | Phase A: WARN / Phase B: FAIL |
| 4L-07 | `90.tests/test_cases.yaml` 존재 | required | Phase A: WARN / Phase B: FAIL |
| 4L-08 | `90.tests/eval_rubric.md` 존재 | required | Phase A: WARN / Phase B: FAIL |

## Checklist: Manifest Consistency (per skill)

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| MN-01 | `manifest.yaml.id` == `SKILL.meta.yaml.context_id` | 일치 | FAIL |
| MN-02 | `manifest.yaml.layout_version` | `4layer-v1` | WARN |
| MN-03 | `manifest.yaml.modules[]` vs `20.modules/` 실제 파일 | 1:1 대응 | WARN |
| MN-04 | `manifest.yaml.required_layers[]` vs 실제 디렉토리 | 모두 존재 | WARN |

---

## Outputs

- Per-skill metadata check results (`governance_check_report.metadata_checks` 섹션)
- 위반 항목 목록 + severity + remediation 권고

## When Unsure

- 체크 항목의 severity 판단이 모호하면 WARN으로 기본 분류하고 사용자 검토 요청.
- Phase A/B 구분이 불명확한 새 항목은 Phase A(warn)로 시작.
