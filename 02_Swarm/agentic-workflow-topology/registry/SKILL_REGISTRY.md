# Swarm Skill Registry: agentic-workflow-topology
- Generated at: `2026-02-14T08:58:33+00:00`
- Swarm root: `02_Swarm/agentic-workflow-topology`
- Skill count: `5`

## Skills
| Skill Folder | Name | Description |
|---|---|---|
| 00.workflow-skill-manager | workflow-skill-manager | Manages active workflow skills, validates metadata/dependencies/contracts, and maintains local+swarm registry runbook with policy/checklist workflow. |
| 01.mental-model-loader | mental-model-loader | Designs domain mental models and local chart loading policy, producing the `mental_model_bundle` contract. |
| 02.workflow-topology-scaffolder | workflow-topology-scaffolder | Designs workflow topology and scaffold spec from Goal→DQ→RSV→theta_GT, integrating topology and termination strategy. |
| 03.workflow-mental-model-execution-designer | workflow-mental-model-execution-designer | Designs node-level execution mapping so each workflow task applies the right mental model/chart. |
| 04.workflow-observability-and-evolution | workflow-observability-and-evolution | Analyzes SQLite workflow logs (agent-audit-log v1.2.0 compatible) and proposes manual periodic improvements with rollback-aware reports. |

## Agent Inheritance Overview
- 등록된 소비자 정보가 없습니다.
