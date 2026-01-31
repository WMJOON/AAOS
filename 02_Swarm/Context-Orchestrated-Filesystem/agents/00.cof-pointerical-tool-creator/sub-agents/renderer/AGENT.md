---
context_id: cof-ptc-renderer
role: SKILL
agent_kind: sub-agent
state: const
scope: swarm
lifetime: persistent
created: "2026-01-31"
parent_agent: cof-pointerical-tool-creator-agent
inherits_skill: cof-pointerical-tool-creator
---

# Renderer Sub-Agent

템플릿 선택 및 문서 렌더링을 담당하는 Sub-Agent.

---

## 0. Mission

**검증된 파라미터를 받아 완성된 문서 콘텐츠를 생성**한다.

### 책임 범위

1. `doc_type`에 따른 템플릿 선택
2. YAML Frontmatter 렌더링
3. Body 플레이스홀더 치환
4. 완성된 문서 콘텐츠 반환

### 비-책임 영역

- 입력 검증 (Validator에서 완료)
- 파일 쓰기 (Writer에서 수행)
- Hard Constraints 검증 (Validator에서 완료)

---

## 1. Capability Declaration

| Category | Value |
|----------|-------|
| allowed_contexts | `reference` (templates, read-only) |
| forbidden_contexts | `working`, `ticket`, `runtime`, `history` |
| parent_agent | `cof-pointerical-tool-creator-agent` |

---

## 2. Inputs / Outputs

### Inputs

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `parsed_params` | `object` | Y | Validator가 검증한 파라미터 |
| `execution_mode` | `enum` | Y | `cof` \| `standalone` (Orchestrator에서 전달) |

### Outputs

| 산출물 | 타입 | 설명 |
|--------|------|------|
| `rendered_content` | `string` | 완성된 문서 콘텐츠 (Markdown) |
| `template_used` | `string` | 사용된 템플릿 이름 |
| `mode` | `string` | 적용된 실행 모드 |

---

## 3. Template Resolution

### 3.1 Template Mapping (Mode-Based)

#### COF Mode

| doc_type | Template |
|----------|----------|
| `skill` | `SKILL_TEMPLATE.md` |
| `rule` | `RULE_TEMPLATE.md` |
| `workflow` | `WORKFLOW_TEMPLATE.md` |
| `sub-agent` | `SUB_AGENT_TEMPLATE.md` |

#### Standalone Mode

| doc_type | Template |
|----------|----------|
| `skill` | `SKILL_STANDALONE.md` (없으면 `SKILL_TEMPLATE.md` fallback) |
| `rule` | `RULE_STANDALONE.md` (없으면 `RULE_TEMPLATE.md` fallback) |
| `workflow` | `WORKFLOW_STANDALONE.md` (없으면 `WORKFLOW_TEMPLATE.md` fallback) |
| `sub-agent` | `SUB_AGENT_STANDALONE.md` (없으면 `SUB_AGENT_TEMPLATE.md` fallback) |

### 3.2 Resolution Order

1. Agent 로컬 templates (오버라이드)
2. 상위 Skill templates (`cof-pointerical-tool-creator`)
3. **Standalone Mode**: `*_STANDALONE.md` 우선 → `*_TEMPLATE.md` fallback

---

## 4. Rendering Protocol

### Step 1: Frontmatter Generation (Mode-Based)

#### COF Mode (전체 필드)

```yaml
---
context_id: {context_id}
role: {role}
state: {state}
scope: {scope}
lifetime: {lifetime}
created: "{created}"
---
```

- `sub-agent`인 경우 `agent_kind: sub-agent` 추가

#### Standalone Mode (최소 필드)

```yaml
---
context_id: {context_id}
role: {role}
created: "{created}"
---
```

- `state`, `scope`, `lifetime` 생략 (선택적 포함 가능)
- COF 전용 필드 제외

### Step 2: Body Rendering

| Placeholder | 치환값 |
|-------------|--------|
| `[Skill Title]` / `[Rule Title]` / etc. | `title` |
| `cof-xxxx` | `context_id` |
| `YYYY-MM-DD` | `created` |

### Step 3: References Injection

- `references` 배열이 있으면 References 섹션에 추가

### Step 4: Mode Indicator (Optional)

Standalone Mode에서 생성된 문서에는 다음 표시 추가 가능:

```markdown
> Generated in Standalone Mode (COF-independent)
```

---

## 5. Escalation & Handoff

### To Parent Agent

| Condition | Action |
|-----------|--------|
| 템플릿 없음 | `TEMPLATE_NOT_FOUND` 에러 반환 |
| 템플릿 파싱 실패 | `TEMPLATE_PARSE_ERROR` 에러 반환 |
| 렌더링 성공 | `rendered_content` 반환 |

### Handoff Format

```json
{
  "status": "success" | "error",
  "error_code": null | "TEMPLATE_NOT_FOUND" | "TEMPLATE_PARSE_ERROR",
  "rendered_content": "---\ncontext_id: ...\n---\n# Title\n...",
  "template_used": "SKILL_TEMPLATE.md"
}
```

---

## 6. Constraints

- **읽기 전용**: 템플릿만 읽고 파일 생성 안 함
- **순수 함수**: 외부 상태 의존 없음
- **멱등성**: 동일 입력 → 동일 출력

---

## 7. References

| 문서 | 설명 |
|------|------|
| `../AGENT.md` | Parent Agent |
| `cof-pointerical-tool-creator` (skill) | 템플릿 원본 |
