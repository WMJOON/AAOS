# Output Contract (Full JSON Schema)

## 최종 산출물 구조

```json
{
  "workflow_topology": {
    "type": "linear | branching | parallel | fanout_fanin | hierarchical | synthesis_centric | state_transition | composite",
    "rationale": ["선택 근거 문자열 배열"]
  },

  "decision_questions": [
    {
      "id": "DQ1",
      "question": "이 Workflow가 답해야 하는 핵심 질문",
      "weight": 1.5
    }
  ],

  "rsv": {
    "rsv_total": 6.5,
    "estimation_method": "decision_questions_weighted_sum"
  },

  "task_graph": {
    "nodes": [
      {
        "node_id": "T1",
        "name": "노드 이름",
        "explicit_output": {
          "type": "memo | table | checklist | spec | risk_register | policy | decision | summary | state",
          "schema": "선택적 스키마 이름",
          "required_sections": ["선택적 필수 섹션"],
          "acceptance_criteria": ["수용 기준"]
        },
        "inputs": ["입력 설명"],
        "dependencies": ["의존 node_id"],
        "semantic_entropy_expected": 0.7,
        "theta_gt_band": {"min": 0.4, "max": 0.8},
        "rsv_target": 1.5,
        "assigned_dqs": ["DQ1", "DQ3"],
        "stop_condition": "종료 조건 서술"
      }
    ],
    "edges": [
      {
        "from": "T1",
        "to": "T2",
        "condition": "선택적 조건 (branching/conditional 시)"
      }
    ]
  },

  "loop_risk_assessment": [
    {
      "loop_type": "convergence | redundancy_accumulation | semantic_dependency_cycle | rsv_inflation | human_deferral | exploration_spiral",
      "where": "node_id 또는 edge 식별자",
      "risk": "low | med | high",
      "mitigation": ["대응 전략"]
    }
  ],

  "handoff_strategy": {
    "handoff_points": ["node_id"],
    "minimize_context_loss_rules": ["규칙 서술"]
  },

  "execution_policy": {
    "continue_reframe_stop_rules": [
      "Continue: theta_gt_actual ∈ [band.min, band.max] AND rsv_accumulated < rsv_target",
      "Continue: theta_gt_actual > band.max (아직 수렴 안 됨, 반복 계속)",
      "Reframe: theta_gt_actual < band.min (과도 수렴, DQ 재정의 검토)",
      "Reframe: RSV_total 대비 진행률 < 30%이면서 절반 이상 노드 완료",
      "Stop: redundancy == true (중복 증산 루프 감지)",
      "Stop: rsv_accumulated >= rsv_target (노드 목표 달성)",
      "Stop: 모든 DQ closed 또는 token_budget 소진"
    ],
    "estimator_integration": {
      "script": "scripts/estimator.py",
      "invoke_per": "node iteration",
      "normalized_output_schema": "references/ESTIMATOR_GUIDE.md#normalized_output-스키마"
    },
    "human_gate_nodes": ["선택적 node_id"]
  }
}
```

---

## 필드 상세

### workflow_topology.type
8종 중 택1. composite일 경우 rationale에 서브그래프별 topology 명시.

### decision_questions[].weight
DQ가 Goal 달성에 기여하는 상대적 중요도.
합산이 RSV_total이 됨.

### task_graph.nodes[].explicit_output.type
노드의 산출물 형태. 노드 경계를 정의하는 핵심 필드.

### task_graph.nodes[].theta_gt_band
Semantic Entropy에 따른 허용 범위.
- min: 이 이하면 과도하게 좁은 해석 (정보 손실 가능)
- max: 이 이상이면 발산 (수렴 필요)

### task_graph.nodes[].assigned_dqs
이 노드가 닫을 DQ ID 목록.
RSV 검증에 사용: Σ(assigned DQ weights) ≈ rsv_target

### loop_risk_assessment[].loop_type
6종 루프 유형. 상세는 LOOP_RISK_PATTERNS.md 참조.

### execution_policy.estimator_integration
Runtime에서 estimator.py를 호출하기 위한 메타데이터.
- `script`: estimator 스크립트 경로
- `invoke_per`: 호출 주기 ("node iteration" = 노드 반복마다)
- `normalized_output_schema`: 정규화 스키마 참조 위치

### execution_policy.continue_reframe_stop_rules
Workflow 실행 중 의사결정 규칙. estimator 출력과 연동:
- **Continue**: theta_gt_actual이 band 내이고 rsv 미달
- **Reframe**: 과도 수렴 또는 RSV 진행 부진
- **Stop**: 목표 달성, 중복 감지, 또는 예산 소진
