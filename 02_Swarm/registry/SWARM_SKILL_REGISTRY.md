# Swarm Skill Registry Index
- Generated at: `2026-02-14T12:10:00+00:00`
- Scanned swarms: `4`

| Swarm | Status | Skill Count | Overloaded | Warnings | Errors |
|---|---|---:|---:|---:|---:|
| agentic-workflow-topology | active | 5 | N | 0 | 0 |
| context-orchestrated-filesystem | active | 5 | N | 0 | 0 |
| context-orchestrated-workflow-intelligence | active | 1 | N | 0 | 0 |
| cortex-agora | active | 1 | N | 0 | 0 |

## Thresholds
- Overload threshold: `8` skills per Swarm

## Migration Note

- legacy ontology swarm은 `context-orchestrated-workflow-intelligence`로 단일 배치(A+B) 전환 완료.
- Alias 경로는 유지하지 않으며, canonical 경로는 `02_Swarm/context-orchestrated-workflow-intelligence`이다.

## Operation Policy Note

- Behavior Feed는 Agora-First 관찰 경로를 따르며, 장기 immutable 보존은 `cortex-agora change_archive -> record_archive seal`로 수행한다.
- `01_Nucleus/record_archive` direct sink(직접 유입) 방식은 Swarm observability 정책에서 금지한다.
