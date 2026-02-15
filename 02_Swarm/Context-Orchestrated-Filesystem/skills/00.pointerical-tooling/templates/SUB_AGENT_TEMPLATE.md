---
name: "[sub-agent-name]"
description: "[3rd person description. Use when...]"
---
<!-- COF 식별 메타는 SKILL.meta.yaml 또는 상위 manifest에 저장 -->

# [Sub-Agent Title]

## 0. Mission

- 담당 역할과 범위를 명시

## 1. Capability Declaration

| Category | Value |
|----------|-------|
| allowed_contexts | `working`, `ticket`, ... |
| forbidden_contexts | `history` (read-only), ... |
| parent_agent | `[상위 에이전트 context_id 또는 역할]` |

## 2. Inputs / Outputs

### Inputs

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `param1` | `string` | Y | 설명 |

### Outputs

| 산출물 | 타입 | 설명 |
|--------|------|------|
| `output1` | `file` | 설명 |

## 3. Escalation & Handoff

### Escalation Conditions

| Condition | Action |
|-----------|--------|
| 권한 부족 | 상위 에이전트에 위임 |
| 실패 3회 초과 | 중단 및 보고 |
| ... | ... |

### Handoff Protocol

- 보고 대상: `[상위 에이전트]`
- 보고 형식: `[구조화된 반환값 또는 로그]`

## 4. Constraints

- 금지된 포인터 접근 명시
- 위임 범위 제한 명시

## 5. References

- 관련 Rule/Workflow/Skill 링크
- Sub-Agent Normative: `../references/subagent-normative-interpretation.md`
