---
name: cof-pointerical-tool-creator
description: Creates pointer-safe COF Skill/Rule/Workflow/Sub-Agent documents. Use when creating or updating COF docs.
version: "0.2"
---

# COF Pointerical Tool Creator

COF 포인터 모델을 준수하는 **실제 문서**(Skill/Rule/Workflow/Sub-Agent)를 생성한다.

> **설계 스펙**: [SPEC.md](SPEC.md) 참조

---

## When to Use

- COF 문서를 새로 만들거나 갱신할 때
- 포인터 안전(pointer-safe) 구조를 강제한 템플릿/스켈레톤이 필요할 때
- 재귀적 스킬 생성 패턴(스킬로 스킬/룰/워크플로우 생성)을 적용할 때

---

## Quick Reference

### 필수 입력

| 파라미터 | 설명 |
|---------|------|
| `doc_type` | `skill` \| `rule` \| `workflow` \| `sub-agent` |
| `output_path` | 산출물 저장 경로 |
| `context_id` | 전역 유일 식별자 (패턴: `cof-[a-z0-9-]+`) |
| `title` | 문서 제목 |

### 선택 입력

| 파라미터 | 기본값 |
|---------|--------|
| `state` | `const` |
| `scope` | `swarm` |
| `lifetime` | `persistent` |
| `created` | 현재 날짜 |

> 전체 파라미터 명세: [SPEC.md § 3. Inputs](SPEC.md#3-inputs)

---

## Script Usage

```bash
python3 scripts/create_pointerical_doc.py \
  --type skill \
  --title "My Skill Title" \
  --out "/abs/path/to/SKILL.md" \
  --context-id cof-my-skill \
  --state const \
  --scope swarm \
  --lifetime persistent
```

---

## Manual Usage (Templates)

템플릿을 복사하여 수동 편집:

| 문서 타입 | 템플릿 |
|----------|--------|
| SKILL | [templates/SKILL_TEMPLATE.md](templates/SKILL_TEMPLATE.md) |
| RULE | [templates/RULE_TEMPLATE.md](templates/RULE_TEMPLATE.md) |
| WORKFLOW | [templates/WORKFLOW_TEMPLATE.md](templates/WORKFLOW_TEMPLATE.md) |
| SUB-AGENT | [templates/SUB_AGENT_TEMPLATE.md](templates/SUB_AGENT_TEMPLATE.md) |

---

## Generation Checklist

```
Doc Generation Progress:
- [ ] Step 1: Validate Inputs (context_id 형식/유일성, output_path 유효성)
- [ ] Step 2: Resolve Template (doc_type에 맞는 템플릿 선택)
- [ ] Step 3: Render Frontmatter (context_id/role/state/scope/lifetime/created)
- [ ] Step 4: Render Body (플레이스홀더 치환)
- [ ] Step 5: Validate Pointer Safety (Hard Constraints 검증)
- [ ] Step 6: Write Document (저장 및 반환 구조 생성)
```

> 전체 워크플로우: [SPEC.md § 5. Core Workflow](SPEC.md#5-core-workflow)

---

## Guardrails (Hard Constraints)

| # | 제약 | 위반 시 |
|---|-----|--------|
| 1 | `context_id` 없는 문서 금지 | `MISSING_CONTEXT_ID` → 중단 |
| 2 | `history` 컨텍스트를 `active`로 참조 금지 | `INVALID_HISTORY_REF` → 경고 |
| 3 | 디렉토리 ROLE과 state 불일치 금지 | `ROLE_DIR_MISMATCH` → 경고 |
| 4 | 수명 전이 누락된 Workflow 금지 | `MISSING_LIFETIME_TRANSITION` → 중단 |
| 5 | 숫자 인덱스(`NN`)에 의미 부여 금지 | `INDEX_SEMANTIC_VIOLATION` → 경고 |

> 전체 에러 코드: [SPEC.md § 7. Error Handling](SPEC.md#7-error-handling)

---

## References

| 문서 | 용도 |
|------|------|
| [SPEC.md](SPEC.md) | 전체 설계 스펙 |
| [references/](references/) | Normative 해석 문서들 |
| [templates/](templates/) | 문서 타입별 템플릿 |
| [../../rules/cof-environment-set.md](../../rules/cof-environment-set.md) | COF Rule Genome |
