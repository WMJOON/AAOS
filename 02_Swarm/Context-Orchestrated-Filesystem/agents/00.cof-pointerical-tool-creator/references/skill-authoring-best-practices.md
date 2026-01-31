---
context_id: cof-skill-authoring-best-practices
role: REFERENCE
state: const
scope: swarm
lifetime: persistent
created: "2026-01-31"
source: "Anthropic Skill Authoring Best Practices + COF Normative"
---

# Skill Authoring Best Practices

COF 포인터 모델과 Claude 공식 가이드라인을 통합한 스킬 작성 규범.

> **Source**: Anthropic Official Documentation + COF Normative Interpretation

---

## 1. Core Principles

### 1.1 Concise is Key

Context window는 공공재다. 모든 토큰이 비용을 발생시킨다.

**기본 가정**: Claude는 이미 똑똑하다.

```
Challenge each piece of information:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this paragraph justify its token cost?"
```

**Good** (~50 tokens):
```markdown
## Extract PDF text

Use pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

**Bad** (~150 tokens):
```markdown
PDF (Portable Document Format) files are a common file format...
(Claude already knows what PDFs are)
```

### 1.2 Degrees of Freedom

| Freedom | When | Example |
|---------|------|---------|
| **High** | Multiple approaches valid | Code review process |
| **Medium** | Preferred pattern exists | Report generation |
| **Low** | Operations fragile | Database migration |

**Analogy**:
- Narrow bridge with cliffs → Low freedom, exact instructions
- Open field → High freedom, general direction

---

## 2. YAML Frontmatter

### 2.1 Claude Required Fields

```yaml
---
name: solving-tickets          # gerund form, lowercase, hyphens
description: Does X. Use when Y.  # 3rd person, max 1024 chars
---
```

**Naming Rules:**
- Max 64 characters
- Lowercase letters, numbers, hyphens only
- No XML tags, no "anthropic", "claude"
- **Prefer gerund form**: `processing-pdfs`, `solving-tickets`

**Description Rules:**
- Non-empty, max 1024 characters
- **3rd person**: "Processes files" (not "I can help you")
- **Include trigger**: "Use when working with PDFs"

### 2.2 COF Additional Fields

```yaml
---
context_id: cof-xxxx           # Global unique, immutable
role: SKILL
state: const | mutable | active | frozen | archived
scope: immune | agora | nucleus | swarm
lifetime: ticket | persistent | archived
created: "YYYY-MM-DD"
---
```

### 2.3 Combined Example

```yaml
---
name: solving-tickets
description: Reads tickets and dispatches to AI agents. Use when automating ticket workflows.
context_id: cof-task-solver
role: SKILL
state: const
scope: swarm
lifetime: persistent
created: "2026-01-31"
---
```

---

## 3. Document Structure

### 3.1 Recommended Order

```markdown
# [Skill Title]

## Quick Start           ← First! Show usage immediately
## [Core Feature]        ← Main functionality
## Workflow              ← Checklist format
## Inputs / Outputs      ← Parameters
## Constraints           ← Hard/soft limits
## Error Handling        ← Recovery patterns
## References            ← Links to other docs
```

### 3.2 Size Limits

- **SKILL.md body**: Under 500 lines
- **Split when approaching limit**: Use progressive disclosure

### 3.3 Progressive Disclosure

```
skill/
├── SKILL.md              # Overview (loaded when triggered)
├── SPEC.md               # Detailed spec (loaded as needed)
├── reference/
│   ├── api.md            # API docs (loaded as needed)
│   └── examples.md       # Examples (loaded as needed)
└── scripts/
    └── main.py           # Executed, not loaded
```

**Keep references one level deep** from SKILL.md.

---

## 4. Workflow Pattern

### 4.1 Checklist Format

```markdown
## Workflow

Copy this checklist:

```
Task Progress:
- [ ] Step 1: Action
- [ ] Step 2: Action
- [ ] Step 3: Validate
- [ ] Step 4: Complete
```

**Step 1**: Description...
**Step 2**: Description...
```

### 4.2 Feedback Loop

```markdown
1. Make changes
2. **Validate immediately**: `python validate.py`
3. If fails → fix → validate again
4. **Only proceed when validation passes**
```

---

## 5. COF Capability Declaration

COF 규범에서 요구하는 추가 섹션:

```markdown
## Capability Declaration

| Category | Value |
|----------|-------|
| allowed_contexts | `working`, `ticket`, `reference` |
| forbidden_contexts | `history` (read-only), `runtime` |
| consumers | agent |
```

---

## 6. Anti-Patterns

### Avoid

- [ ] Windows paths (`\`) → Use forward slashes (`/`)
- [ ] Time-sensitive info → Use "old patterns" section
- [ ] Too many options → Provide default with escape hatch
- [ ] Vague names → `helper`, `utils`, `tools`
- [ ] Deep nesting → Keep references one level deep
- [ ] Verbose explanations → Claude already knows

### Prefer

- [x] Gerund naming: `processing-pdfs`
- [x] Quick Start first
- [x] Checklist workflows
- [x] Concrete examples
- [x] Consistent terminology

---

## 7. Validation Checklist

```
Skill Doc Validation:
- [ ] name: gerund form, lowercase, ≤64 chars
- [ ] description: 3rd person, "Use when...", ≤1024 chars
- [ ] context_id: unique, cof-[a-z0-9-]+ pattern
- [ ] role: SKILL
- [ ] Quick Start section exists and is near top
- [ ] Body under 500 lines
- [ ] References one level deep
- [ ] No time-sensitive information
- [ ] Consistent terminology
- [ ] Workflow has checklist format
- [ ] COF Capability Declaration present
```

---

## 8. References

- **Anthropic Official**: `03_AgentsTools/Skill-authoring-best-practices.md`
- **COF Skill Normative**: `../../skills/00.cof-pointerical-tool-creator/references/skill-normative-interpretation.md`
- **COF Rule Genome**: `../../rules/cof-environment-set.md`
