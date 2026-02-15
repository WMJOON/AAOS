---
name: your-skill-name
description: Describe when to use this skill in one sentence.
---

# [Skill Title]

## 0. Purpose

- 목적과 범위를 간결히 서술한다.

## 1. Capability Declaration

| Category | Value |
|----------|-------|
| allowed_contexts | `working`, `ticket`, ... |
| forbidden_contexts | `history` (read-only), ... |
| consumers | immune \| agora \| agent |

## 2. Inputs / Outputs

### Inputs

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `param1` | `string` | Y | 설명 |
| `param2` | `boolean` | N | 설명 |

### Outputs

| 산출물 | 타입 | 설명 |
|--------|------|------|
| `output1` | `file` | 설명 |

## 3. Constraints

- 금지된 포인터 접근 명시
- 실행 코드 포함 금지
- history는 read-only

## 4. References

- 관련 Rule/Workflow 링크
- Skill Normative: `../references/skill-normative-interpretation.md`
