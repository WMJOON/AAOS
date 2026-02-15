---
name: "[workflow-name]"
description: "[3rd person description. Use when...]"
---
<!-- COF 식별 메타는 사이드카 파일 또는 상위 manifest에 저장 -->

# [Workflow Title]

## 0. Purpose

- 이 워크플로우가 해결하는 문제

## 1. Entry Context

| Field | Value |
|-------|-------|
| entry_pointer | `[입력 포인터 타입]` |
| preconditions | `[선행 조건]` |

## 2. Transition Steps

| Step | Action | State Before | State After |
|------|--------|--------------|-------------|
| 1 | 작업 설명 | mutable | active |
| 2 | 작업 설명 | active | frozen |
| 3 | ... | ... | ... |

## 3. Exit Rule

| Field | Value |
|-------|-------|
| exit_state | frozen \| archived |
| postconditions | `[후행 조건]` |

## 4. Lifetime Transition

> **필수**: 수명 전이 경로를 반드시 명시해야 한다.

```
[lifetime 전이 다이어그램 또는 설명]
ticket -> persistent -> archived
```

## 5. References

- 관련 Rule/Skill 링크
- Workflow Normative: `../references/workflow-normative-interpretation.md`
