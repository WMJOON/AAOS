# Module: Metadata Validation (Phase 1)

## 목적

cortex-agora governed skill(instruction-nucleus)의 SKILL.md frontmatter,
SKILL.meta.yaml sidecar, 4-Layer 구조(조건부)를 점검한다.

## 입력

- `skills/cortex-agora-instruction-nucleus/SKILL.md`
- `skills/cortex-agora-instruction-nucleus/SKILL.meta.yaml`

---

## Checklist: SKILL.md Frontmatter

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| FM-01 | `name` 필드 존재 | required string | FAIL |
| FM-02 | `description` 필드 존재 | required string, "Use when..." 권장 | WARN |
| FM-03 | `name` 값이 cortex-agora 네이밍 패턴 준수 | `cortex-agora-*` 형식 | WARN |
| FM-04 | SKILL.md 총 줄 수 | 4-Layer 스킬이면 <= 120줄. legacy면 제한 없음. | Phase A: WARN |
| FM-05 | Required sections 존재 | Purpose/Quick Start/Constraints 등 | WARN |
| FM-06 | frontmatter에 `context_id` 존재 | 존재 또는 sidecar에 위임 | WARN |
| FM-07 | `execution_mode` 명시 시 `:reference_only` | cortex-agora hard prohibition | FAIL |

---

## Checklist: SKILL.meta.yaml Sidecar

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| SC-01 | 파일 존재 | `SKILL.meta.yaml` present | FAIL |
| SC-02 | `context_id` 필드 존재 | required, immutable | FAIL |
| SC-03 | `context_id` == frontmatter `name` | 값 일치 | FAIL |
| SC-04 | `role` 필드 | `SKILL` | WARN |
| SC-05 | `state` 필드 | const / mutable / active / frozen / archived 중 하나 | WARN |
| SC-06 | `scope` 필드 | `swarm` | WARN |
| SC-07 | `lifetime` 필드 | persistent / ticket / archived 중 하나 | WARN |
| SC-08 | `consumers` 필드 존재 | downstream consumer 목록 | WARN |

---

## Checklist: 4-Layer 구조 (조건부)

> **Note**: instruction-nucleus는 현재 flat 구조(SKILL.md + SKILL.meta.yaml만 존재).
> 아래 체크는 **해당 스킬이 4-Layer로 업그레이드된 경우에만** 적용한다.
> 현재 상태에서는 모두 SKIP 처리.

| ID | Check | Expected | Severity |
|----|-------|----------|----------|
| 4L-01 | `00.meta/` 디렉토리 존재 | present | Phase A: WARN |
| 4L-02 | `00.meta/manifest.yaml` 존재 | present | Phase A: WARN |
| 4L-03 | `10.core/` 디렉토리 존재 | present | Phase A: WARN |
| 4L-04 | `10.core/core.md` 존재 | present | Phase A: WARN |
| 4L-05 | `20.modules/` 디렉토리 존재 | present | Phase A: WARN |
| 4L-06 | `30.references/` 디렉토리 존재 | present | Phase A: WARN |
| 4L-07 | `40.orchestrator/` 디렉토리 존재 | present | Phase A: WARN |
| 4L-08 | `90.tests/` 디렉토리 존재 | present | Phase B: WARN |

---

## 산출물

`governance_check_report.metadata_checks` 섹션에 기록.

## When Unsure

- frontmatter에 `context_id`가 없고 sidecar에만 있으면: PASS (sidecar가 SoT).
- legacy flat 구조에서 4L 체크 → SKIP, 보고서에 "flat structure, 4L not applicable" 기록.
