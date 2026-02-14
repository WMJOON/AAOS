# Swarm Skill Registry: context-orchestrated-filesystem
- Generated at: `2026-02-14T16:00:00+00:00`
- Swarm root: `02_Swarm/context-orchestrated-filesystem`
- Skill count: `5`

## Skills
| Skill Folder | Name | Description |
|---|---|---|
| 00.cof-pointerical-tool-creator | cof-pointerical-tool-creator | Creates pointer-safe COF Skill/Rule/Workflow/Sub-Agent documents. Use when creating or updating COF docs. |
| 01.cof-glob-indexing | cof-glob-indexing | Resolves the nearest COF /[n].index/ from a target directory, scans within that node boundary, and writes NODE_INDEX.md and ROLE_EVIDENCE.md under the resolved index. Use when the user needs COF context boundary detection, role directory inference, or anchor discovery. |
| 02.cof-swarm-skill-manager | cof-swarm-skill-manager | Manage skills across each Swarm by scanning skill directories, generating per-swarm registries, detecting duplicate context IDs, and warning when a Swarm has overloaded skill sets. Use when you need to reduce skill sprawl and keep skill inventories reliable. |
| 03.cof-task-manager-node | cof-task-manager-node | Creates and manages `NN.agents-task-context/` nodes (tickets, verification, validation, archiving) for persistent agent context tracking in COF. |
| 04.cof-task-solver-agent-group | solving-tickets | Dispatch tickets to AI CLI agents based on tag heuristics. Use when automating ticket-based agent workflows or coordinating multi-agent collaboration. |

## Agent Inheritance Overview
- `00.cof-pointerical-tool-creator`: renderer, validator, writer
- `01.cof-glob-indexing`: -
- `02.cof-swarm-skill-manager`: -
- `03.cof-task-manager-node`: archiver, node-creator, ticket-manager, validator
- `04.cof-task-solver-agent-group`: -
