---
name: cof-ticket-solving
description: Dispatch tickets to AI CLI agents based on tag heuristics. Use when automating ticket-based agent workflows or coordinating multi-agent collaboration.
---

# Solving Tickets

Reads a ticket from `NN.agents-task-context/tickets/` and dispatches it to the appropriate agent group. **One agent group solves one ticket.**

## When to Use

- Processing tickets from `NN.agents-task-context/tickets/` (status: `todo` or `in-progress`)
- Automating ticket-based agent workflows with tag-driven selection
- Coordinating multi-agent collaboration (Council of Elders mode)
- Integrating AI CLI outputs back into ticket documentation

## Quick Start

```bash
# Auto-select agent by ticket tags
python3 scripts/solve_ticket.py \
  --ticket "/path/to/NN.agents-task-context/tickets/implement-feature.md"

# Explicit provider selection
python3 scripts/solve_ticket.py \
  --ticket "./01.agents-task-context/tickets/security-audit.md" \
  --provider claude

# Council of Elders (all agents)
python3 scripts/solve_ticket.py \
  --ticket "./01.agents-task-context/tickets/architecture-review.md" \
  --all

# With custom timeout and context depth
python3 scripts/solve_ticket.py \
  --ticket "./tickets/complex-task.md" \
  --timeout 600 \
  --context-depth 15
```

## Inputs

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--ticket` | Y | - | Absolute or relative path to ticket file |
| `--provider` | N | auto | Force specific provider: `claude`, `codex`, `gemini` |
| `--all` | N | false | Council mode: dispatch to all available providers |
| `--timeout` | N | 300 | Execution timeout in seconds per agent |
| `--context-depth` | N | 10 | Max depth for cof-glob-indexing |
| `--dry-run` | N | false | Parse and plan without execution |
| `--skip-indexing` | N | false | Skip context indexing (use existing) |
| `--require-indexing` | N | false | Fail if indexing produces no artifacts (no minimal-context fallback) |
| `--max-retries` | N | 1 | Max retries for timed-out agent runs |
| `--retry-timeout-delta` | N | 60 | Timeout increase per retry in seconds |
| `--format` | N | text | Output format: `text` or `json` |

## Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Execution Result | Ticket `## Execution Result` section | Agent output appended to ticket |
| Status Update | Ticket frontmatter `status` field | `todo` -> `in-progress` -> `done` or `blocked` |
| Agent Log | `NN.agents-task-context/AGENT_LOG.md` | Timestamped execution log |
| JSON Result | stdout (with `--format json`) | Structured execution result |

## Agent Selection Heuristics

| Tag(s) | Group Type | Agents | Rationale |
|--------|------------|--------|-----------|
| `security`, `audit` | single | claude | Security analysis, compliance review |
| `performance`, `optimization` | single | gemini | Performance engineering, benchmarking |
| `architecture`, `refactor` | single | codex | Code structure, design patterns |
| `review`, `critique`, `consensus` | council | all | Cross-verification, parallel review |
| `sequential`, `iterative`, `refinement` | sequential | all | Context accumulation, iterative refinement |
| (default) | single | claude | General-purpose fallback |

## Workflow Checklist

```
Ticket Progress:
- [ ] Step 1: Parse ticket frontmatter and body
- [ ] Step 2: Validate ticket status (skip if done)
- [ ] Step 3: Index context via cof-glob-indexing
- [ ] Step 4: Select agent by tag heuristics
- [ ] Step 5: Assemble context (NODE_INDEX + ROLE_EVIDENCE + ticket)
- [ ] Step 6: Dispatch via collaborate.py
- [ ] Step 7: Integrate result to ticket
- [ ] Step 8: Update status (done/blocked)
- [ ] Step 9: Append to AGENT_LOG.md
```

### Step Details

**Step 1-2**: Parse ticket YAML frontmatter. Extract `status`, `priority`, `tags`, `dependencies`. If `status: done`, exit immediately.

**Step 3**: Run context indexing:
```bash
python3 {COF}/skills/01.glob-indexing/scripts/cof_glob_indexing.py \
  --target-dir "{ticket_directory}" \
  --max-depth {context-depth}
```

**Step 4**: Apply tag heuristics (see table above). Explicit `--provider` or `--all` overrides auto-selection.

**Step 5**: Build context from:
- `NODE_INDEX.md` (structure overview)
- `ROLE_EVIDENCE.md` (role directory evidence)
- Ticket content (description + action items)

**Step 6**: Dispatch to collaborate.py:
```bash
python3 {SUMMON_AGENTS}/skill/sa-call-cli-agents/scripts/collaborate.py run \
  -p {provider} \
  --context {context_file} \
  -m "{action_items}" \
  --format json \
  --timeout {timeout}
```

**Step 7-9**: Parse JSON response, append `## Execution Result` section, update `status` field, log to `AGENT_LOG.md`.

## Constraints

1. **One Group, One Ticket**: A single agent group processes exactly one ticket at a time. No parallel ticket processing within one invocation.

2. **Context Boundary**: Context is limited to the cof-glob-indexing scope. Do not reference files outside the resolved node boundary.

3. **Result Recording**: All execution results MUST be written to the ticket file. Silent failures are forbidden.

4. **Status Integrity**: Status transitions follow strict order: `todo` -> `in-progress` -> `done` | `blocked`. No skipping or reversing.

5. **Idempotency**: Re-running on a `done` ticket is a no-op. Re-running on `in-progress` resumes from current state.

6. **YAML Frontmatter Limitations**: 내장 YAML 파서는 다음 제한사항이 있음:
   - nested dict는 1레벨까지만 지원
   - multiline string (|, >) 미지원
   - anchor/alias (&, *) 미지원
   - 복잡한 구조가 필요하면 PyYAML 의존성 추가 고려

## Error Handling

| Error | SEV | Detection | Recovery |
|-------|-----|-----------|----------|
| Ticket not found | SEV-1 | File access | Abort with error |
| Invalid ticket format | SEV-2 | YAML parse | Abort with error |
| Context indexing failure | SEV-2 | Script exit code | Fallback to minimal context |
| Agent not available | SEV-2 | CLI error | Mark blocked, log full error |
| Agent timeout | SEV-2 | Timeout exceeded | Retry up to `--max-retries` (default: 1) with `--retry-timeout-delta` (default: +60s), then mark blocked |
| Agent execution error | SEV-3 | Non-zero exit | Mark blocked, log full error |
| Result integration failure | SEV-2 | File write error | Retry once, then abort |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success: ticket processed and status updated |
| 1 | Partial: execution completed but with warnings |
| 2 | Error: ticket not found or invalid format |
| 3 | Error: context indexing failed (when `--require-indexing`) |
| 4 | Error: all agents unavailable |
| 5 | Error: agent execution failed, ticket marked blocked |

## References

- **Spec**: `@ref(cof-ticket-solving-spec)` → [SPEC.md](SPEC.md)
- **Dependencies**:
  - `@ref(cof-glob-indexing)` - 컨텍스트 인덱싱
  - `@ref(call-cli-agents)` - 에이전트 디스패치
  - `@ref(cof-task-context-management)` - 티켓 관리 (upstream)
- **Normative**: `@ref(skill-normative-interpretation)`
- **Rule Genome**: `@ref(cof-environment-set)`
