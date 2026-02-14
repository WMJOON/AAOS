# Swarm Skill Registry: context-orchestrated-filesystem
- Generated at: `2026-02-14T08:58:33+00:00`
- Swarm root: `/Users/wmjoon/Library/Mobile Documents/iCloud~md~obsidian/Documents/wmjoon/04_Agentic_AI_OS/02_Swarm/context-orchestrated-filesystem`
- Skill count: `5`

## Skills
| Skill Folder | Name | Source | Context ID | Description | Trigger | Role | Scripts | Templates | References | Consumers |
|---|---|---|---|---|---|---|---|---|---|
| 00.cof-pointerical-tool-creator | cof-pointerical-tool-creator | cof-pointerical-tool-creator | - | Creates pointer-safe COF Skill/Rule/Workflow/Sub-Agent documents. Use when creat | - | - | Y | Y | Y | 00.cof-pointerical-tool-creator, renderer, validator, writer |
| 01.cof-glob-indexing | cof-glob-indexing | cof-glob-indexing | - | Resolves the nearest COF /[n].index/ from a target directory, scans within that  | - | - | Y | N | N | - |
| 02.cof-swarm-skill-manager | cof-swarm-skill-manager | cof-swarm-skill-manager | - | Manage skills across each Swarm by scanning skill directories, generating per-sw | - | - | Y | N | N | - |
| 03.cof-task-manager-node | cof-task-manager-node | cof-task-manager-node | - | Creates and manages `NN.agents-task-context/` nodes (tickets, verification, vali | - | - | Y | Y | N | 01.cof-task-manager, archiver, node-creator, ticket-manager, validator |
| 04.cof-task-solver-agent-group | solving-tickets | solving-tickets | - | Dispatch tickets to AI CLI agents based on tag heuristics. Use when automating t | - | - | Y | N | N | - |

## Agent Inheritance Overview
- `00.cof-pointerical-tool-creator`: 00.cof-pointerical-tool-creator, renderer, validator, writer
- `01.cof-glob-indexing`: -
- `02.cof-swarm-skill-manager`: -
- `03.cof-task-manager-node`: 01.cof-task-manager, archiver, node-creator, ticket-manager, validator
- `04.cof-task-solver-agent-group`: -
