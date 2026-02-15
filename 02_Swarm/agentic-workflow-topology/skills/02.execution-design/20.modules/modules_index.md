# Modules Index

## Module → Schema Key Mapping

| Module | Role | File | Output Keys |
|---|---|---|---|
| module.node-mapping | chart 할당 · bundle 추적 | `20.modules/module.node-mapping.md` | `bundle_ref`, `node_chart_map`, `task_to_chart_map` |
| module.mode-policy | θ_GT → mode · model 배정 | `20.modules/module.mode-policy.md` | `node_mode_policy`, `model_selection_policy` |
| module.fallback-handoff | 노드 간 계약 · 실패 대응 | `20.modules/module.fallback-handoff.md` | `handoff_contract`, `fallback_rules` |

## Execution Order
```
1. module.node-mapping   (chart 할당 확정)
       ↓
2. module.mode-policy    (할당된 chart의 θ_GT 기반 mode 결정)
       ↓
3. module.fallback-handoff (확정된 mode/chart 기반 handoff·fallback 설계)
```

> **의존성**: mode-policy는 node-mapping 결과에 의존한다. fallback-handoff는 둘 다에 의존한다.
