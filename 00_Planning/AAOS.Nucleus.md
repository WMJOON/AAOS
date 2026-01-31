# AAOS Nucleus (Planning)

AAOS의 **Nucleus(핵심 기관 레이어)** 를 AIVarium 전체 구조 안에서 조망하기 위한 *planning 문서*.

- Canonical source of truth: `04_Agentic_AI_OS/`
- 이 문서의 역할: 구조/관계/경계 정의를 초안으로 잡고, 필요 시 Deliberation/Immune Gate를 거쳐 Canonical 문서로 승격

## System Map (Draft)
```mermaid
flowchart TB

AIV[AAOS_AIVarium]

%% ===== NUCLEUS =====
subgraph NUC[AAOS_Nucleus]
    RA[Record_Archive]
    IS[Immune_System]
    DCN[Deliberation_Chamber]
end

%% ===== SWARMS =====
subgraph SW[AAOS_Swarms]

    subgraph SDC[Cortex_Agora]
        ARG[Ideation_and_Argument]
    end

    subgraph SCOF[Context_Orchestrated_Filesystem]
        TKT[tickets_md_yaml]
        CDB[Context_DB_SQLite]
        AGG[Agent_Group]
        AGENTS[Human_and_AI_Agents]
        AGG --> AGENTS
    end

    subgraph SOTHER[Other_Swarms]
        OSW[Future_Swarms]
    end

end

%% ===== STRUCTURE =====
AIV --> NUC
AIV --> SW

%% ===== NUCLEUS INTERNAL =====
RA --> IS
IS --> DCN
DCN --> RA

%% ===== EXECUTION FLOW =====
TKT --> AGG
CDB --> AGG
AGENTS -->|Execution_Events| CDB
AGENTS -->|Execution_Events| RA

%% ===== SWARM DC IMPROVEMENT FLOW =====
CDB -->|Context_Analysis| ARG
RA -->|History_Analysis| ARG
ARG -->|Improve_Swarm_Rules| SCOF
ARG -->|Improve_Swarm_Rules| SOTHER

%% ===== NUCLEUS PROMOTION FLOW =====
ARG -->|Promote_to_Nucleus| RA
RA --> IS
IS -->|Pass| DCN
DCN -->|DNA_Blueprint| SW
IS -->|Reject| ARG
```

## Canonical References

- Canon: [README.md](../README.md)
- META Doctrine: [METADoctrine.md](../METADoctrine.md)
- Deliberation Chamber DNA: [DNA_BLUEPRINT](../01_Nucleus/Deliberation_Chamber/DNA_BLUEPRINT.md)
- COF (Context Orchestrated Filesystem): [COF v0.1.3 DNA](../02_Swarm/Context-Orchestrated-Filesystem/DNA.md)
