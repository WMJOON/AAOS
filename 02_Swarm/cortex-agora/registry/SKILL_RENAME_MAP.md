# Skill Rename Map (NN.role-slug Migration)

This document records the one-time migration from legacy skill directory/identifier names to the unified `NN.role-slug` convention.

Transition policy:
- Keep this map for at least one release cycle.
- Treat the **new** names and paths as canonical.

## agentic-workflow-topology (AWT)

| Old Dir | New Dir | Old Name/Context ID/Source | New Name/Context ID/Source |
|---|---|---|---|
| `00.workflow-skill-manager` | `04.skill-governance` | `workflow-skill-manager` | `awt-skill-governance` |
| `01.mental-model-loader` | `00.mental-model-design` | `mental-model-loader` | `awt-mental-model-design` |
| `02.workflow-topology-scaffolder` | `01.topology-design` | `workflow-topology-scaffolder` | `awt-topology-design` |
| `03.workflow-mental-model-execution-designer` | `02.execution-design` | `workflow-mental-model-execution-designer` | `awt-execution-design` |
| `04.workflow-observability-and-evolution` | `03.observability-evolution` | `workflow-observability-and-evolution` | `awt-observability-evolution` |

## context-orchestrated-filesystem (COF)

| Old Dir | New Dir | Old Name/Context ID/Source | New Name/Context ID/Source |
|---|---|---|---|
| `00.cof-pointerical-tool-creator` | `00.pointerical-tooling` | `cof-pointerical-tool-creator` | `cof-pointerical-tooling` |
| `01.cof-glob-indexing` | `01.glob-indexing` | `cof-glob-indexing` | `cof-glob-indexing` |
| `02.cof-swarm-skill-manager` | `04.skill-governance` | `cof-swarm-skill-manager` | `cof-skill-governance` |
| `03.cof-task-manager-node` | `02.task-context-management` | `cof-task-manager-node` | `cof-task-context-management` |
| `04.cof-task-solver-agent-group` | `03.ticket-solving` | `cof-task-solver-agent-group` / `solving-tickets` | `cof-ticket-solving` |

`_shared` remains unchanged and is intentionally excluded from skill renaming.

## context-orchestrated-workflow-intelligence (COWI)

| Old Dir | New Dir | Old Name/Context ID/Source | New Name/Context ID/Source |
|---|---|---|---|
| `00.cowi-agora-consumption-bridge` | `00.agora-consumption-bridge` | `cowi-agora-consumption-bridge` | `cowi-agora-consumption-bridge` |
