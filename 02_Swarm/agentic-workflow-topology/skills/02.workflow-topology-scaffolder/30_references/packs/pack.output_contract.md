# Output Contract (Full JSON Schema + Strategy Gate)

## 최종 산출물 구조

```json
{
  "goal": "새로운 금융 규제 대응 전략 수립",
  "preflight": {
    "questions": [
      {"id": "PF1", "question": "멘탈모델 먼저 세팅할까요?", "required": true}
    ]
  },
  "workflow_profile": {
    "class": "strategy",
    "risk_tolerance": "high",
    "is_strategy_or_high_risk": true
  },
  "workflow_topology": {
    "type": "composite",
    "rationale": ["parallel + synthesis_centric 조합"]
  },
  "decision_questions": [
    {"id": "DQ1", "question": "규제 적용 대상은?", "weight": 1.5}
  ],
  "rsv": {
    "rsv_total": 6.5,
    "estimation_method": "decision_questions_weighted_sum"
  },
  "task_graph": {
    "nodes": [
      {"node_id": "T1", "name": "법/정책 제약 리스트"},
      {"node_id": "T2", "name": "운영 영향 분석"},
      {"node_id": "T3", "name": "고객 커뮤니케이션 리스크"},
      {"node_id": "T4", "name": "경쟁 사례 비교"},
      {"node_id": "C1", "name": "consumption bridge checkpoint"},
      {"node_id": "H1", "name": "human gate #1"},
      {"node_id": "H2", "name": "human gate #2"}
    ],
    "edges": [
      {"from": "T1", "to": "T4"},
      {"from": "T4", "to": "C1"},
      {"from": "C1", "to": "H1"},
      {"from": "H1", "to": "H2"}
    ]
  },
  "strategy_gate": {
    "enabled": true,
    "required_nodes": ["H1", "H2"],
    "required_edges": [
      {"from": "T4", "to": "C1"},
      {"from": "C1", "to": "H1"}
    ],
    "h1_requirements": {
      "web_evidence": {
        "required": true,
        "path_pattern": "02_Swarm/agentic-workflow-topology/agents/<agent-family>/<version>/artifacts/web_evidence/web_evidence_YYYY-MM-DD.md"
      },
      "cowi_artifacts": {
        "relation_context_map": true,
        "skill_usage_adaptation_report": true
      }
    },
    "finalization_guardrails": [
      "web evidence file missing -> H1 reject",
      "relation_context_map missing -> H1 reject",
      "skill_usage_adaptation_report missing -> H1 reject"
    ]
  },
  "execution_policy": {
    "human_gate_nodes": ["H1", "H2"]
  }
}
```

## Strategy/High-Risk Mandatory Rules

- `workflow_profile.class in {strategy, high_risk}`이면 `strategy_gate.enabled=true`.
- 첫 preflight 질문은 PF1 고정: `멘탈모델 먼저 세팅할까요?`.
- `H1`, `H2`는 선택이 아니라 기본 강제 노드다.
- `T4 -> C1 -> H1` 엣지는 필수다.

## H1 Gate Validation

전략/고위험 워크플로우는 아래가 모두 충족되어야 H1 finalization이 가능하다.

1. `web_evidence_YYYY-MM-DD.md` 파일 존재
2. COWI 산출물 존재
3. validator 결과 PASS

검증 CLI:

```bash
python3 02_Swarm/agentic-workflow-topology/skills/02.workflow-topology-scaffolder/scripts/validate_strategy_h1_gate.py \
  --workflow-spec /path/to/workflow_topology_spec.json \
  --agent-family claude \
  --agent-version 4.0 \
  --proposal-id P-SWARM-V014-BATCH \
  --evidence-date 2026-02-14
```
