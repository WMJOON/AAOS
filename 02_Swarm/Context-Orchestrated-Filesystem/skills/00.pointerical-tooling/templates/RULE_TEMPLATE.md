---
name: "[rule-name]"
description: "[3rd person description. Use when...]"
---
<!-- COF 식별 메타는 사이드카 파일 또는 상위 manifest에 저장 -->

# [Rule Title]

## 0. Purpose

- 이 규칙이 보호하는 대상과 목적

## 1. Access Control

| Subject | Target Pointer Type | Condition | Permission |
|---------|---------------------|-----------|------------|
| agent | history | always | read-only |
| immune | working | on-violation | read-write |
| ... | ... | ... | ... |

## 2. Violation Handling

| Violation | SEV | Action |
|-----------|-----|--------|
| history write attempt | SEV-2 | reject + log |
| unauthorized access | SEV-1 | reject + alert |
| ... | ... | ... |

## 3. References

- 관련 Skill/Workflow 링크
- Rule Normative: `../references/rule-normative-interpretation.md`
