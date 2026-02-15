# Loading Policy -- cortex-agora Skill Governance

## 항상 로딩

| File | Reason |
|------|--------|
| `10.core/core.md` | 거버넌스 원칙, 정의, CC map, when_unsure |
| `40.orchestrator/orchestrator.md` | 3-Phase 프로세스, 분기 규칙 |

## 온디맨드 로딩

| Trigger | Files |
|---------|-------|
| Phase 1 (Metadata) | `20.modules/module.metadata-validation.md` |
| Phase 2 (Archive) | `20.modules/module.archive-integrity.md` + change_archive JSONL 3종 + templates 3종 + bridge script |
| Phase 3 (Consumption) | `20.modules/module.consumption-contract.md` + `behavior/BEHAVIOR_FEED.jsonl` + COWI skill 참조 |
| Report 생성 | `30.references/governance_check_report.template.md` |

## 외부 참조 (cross-component)

| Component | Path | Used In |
|-----------|------|---------|
| COWI pull script | `02_Swarm/context-orchestrated-workflow-intelligence/skills/00.agora-consumption-bridge/scripts/pull_agora_feedback.py` | Phase 3 (CP-01, CP-02) |
| COWI skill | `02_Swarm/context-orchestrated-workflow-intelligence/skills/00.agora-consumption-bridge/SKILL.md` | Phase 3 (CP-07) |
| cortex-agora DNA | `02_Swarm/cortex-agora/DNA.md` | Phase 3 (XR-01~XR-06) |

## 로딩 순서

```
Core + Orchestrator (항상)
  └→ Phase 1: module.metadata-validation
       └→ Phase 2: module.archive-integrity
            + JSONL files, templates, bridge script
            └→ Phase 3: module.consumption-contract
                 + BEHAVIOR_FEED, COWI references
                 └→ Final: governance_check_report template
```
