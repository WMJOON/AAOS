---
name: solving-tickets
description: Reads tickets from task-manager and dispatches them to appropriate AI CLI agents (Claude, Codex, Gemini) via Summon-Agents. One agent group solves one ticket. Use when processing task-manager tickets, automating ticket-based workflows, or coordinating multi-agent collaboration.
context_id: cof-task-solver-agent-group
role: SKILL
state: const
scope: swarm
lifetime: persistent
created: "2026-01-31"
---

# Solving Tickets

Reads a ticket and dispatches it to the right agent. **One agent group solves one ticket.**

## Quick Start

```bash
# Single agent
python3 scripts/solve_ticket.py \
  --ticket "./task-manager/tickets/implement-feature.md" \
  --provider claude

# Auto-select by tags
python3 scripts/solve_ticket.py \
  --ticket "./task-manager/tickets/security-audit.md" \
  --auto

# Council of Elders (all agents)
python3 scripts/solve_ticket.py \
  --ticket "./task-manager/tickets/architecture-review.md" \
  --all
```

## Agent Selection

| Tag | Agent | Rationale |
|-----|-------|-----------|
| `security`, `audit` | claude | Security analysis |
| `performance`, `optimization` | gemini | Performance engineering |
| `architecture`, `refactor` | codex | Code structure |
| `review`, `critique` | all | Cross-verification |
| (default) | claude | Fallback |

## Workflow

Copy this checklist:

```
Ticket Progress:
- [ ] Step 1: Read ticket from task-manager/tickets/
- [ ] Step 2: Index context (cof-glob-indexing)
- [ ] Step 3: Select agent by tags
- [ ] Step 4: Dispatch via collaborate.py
- [ ] Step 5: Integrate result to ticket
- [ ] Step 6: Update status (done/blocked)
```

**Step 1**: Parse ticket frontmatter (status, priority, tags). Exit if `done`.

**Step 2**: Run indexing:
```bash
python3 scripts/cof_glob_indexing.py --target-dir "{ticket_path}" --max-depth 10
```

**Step 3**: Select agent using tag heuristics above.

**Step 4**: Dispatch:
```bash
python3 {SUMMON_AGENTS}/skill/call-cli-agents/scripts/collaborate.py run \
  -p {agent} --context {NODE_INDEX.md} -m "{action_items}" --format json
```

**Step 5-6**: Append `## Execution Result` to ticket, update `status: done` or `blocked`.

## Inputs / Outputs

**Inputs:**

| Param | Required | Default | Description |
|-------|----------|---------|-------------|
| `--ticket` | Y | - | Ticket file path |
| `--provider` | N | auto | `claude`\|`codex`\|`gemini` |
| `--all` | N | false | Council mode |
| `--timeout` | N | 300 | Seconds |

**Outputs:**

| Output | Location |
|--------|----------|
| Execution result | Ticket `## Execution Result` section |
| Status update | Ticket frontmatter `status` |
| Log | `task-manager/AGENT_LOG.md` |

## Constraints

- **One group, one ticket**: No parallel ticket processing
- **Context boundary**: Stay within cof-glob-indexing scope
- **Result recording**: All results must be written to ticket
- **Status integrity**: Only `todo→in-progress→done|blocked`

## Error Handling

| Error | SEV | Recovery |
|-------|-----|----------|
| Ticket not found | SEV-1 | Abort |
| Context failure | SEV-2 | Minimal context fallback |
| Agent timeout | SEV-2 | Retry with smaller context |
| Agent error | SEV-3 | Mark blocked |

## References

- **Spec**: [SPEC.md](SPEC.md)
- **Dependencies**:
  - cof-glob-indexing: `../01.cof-glob-indexing/SKILL.md`
  - call-cli-agents: `../../../03_Manifestation/Summon-Agents/skill/call-cli-agents/SKILL.md`
  - cof-task-manager-node: `../02.cof-task-manager-node/SKILL.md`
- **Normative**: `../00.cof-pointerical-tool-creator/references/skill-normative-interpretation.md`
