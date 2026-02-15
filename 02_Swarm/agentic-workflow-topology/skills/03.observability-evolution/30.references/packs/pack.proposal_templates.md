# pack.proposal_templates

> **로딩 조건**: ΔQ >= 2 (개선 제안 생성 시 템플릿 필요)

분류별 Improvement Proposal 작성 템플릿.

---

## 공통 구조

모든 IP는 다음 필수 필드를 포함한다:

```yaml
proposal_id: "IP-YYYY-MM-DD-NNN"
observation_window: { start: "", end: "" }
trigger_signals: []
classification: ""
target_skill: ""
observed_pattern: ""
root_cause_hypothesis: ""
proposed_change:
  action: ""
  detail: ""
  affected_artifacts: []
expected_effect: ""
rollback_rule: ""
confidence: ""
evidence_refs: []
```

---

## Template: Topology 제안

```yaml
classification: topology
target_skill: 01.topology-design

# 행동 유형별 작성 가이드
# action: split_node
proposed_change:
  action: split_node
  detail: "{원래 노드} → {새 노드 A} + {새 노드 B}. 분할 기준: {Explicit Output 단위}"
  affected_artifacts: ["workflow_topology_spec.task_graph.nodes"]

expected_effect: "병목 해소: {노드}의 실행 비중 {현재}% → 예상 {목표}%"
rollback_rule: "분할 후 2 OW 내 hand-off 비용이 분할 이전 bottleneck 비용을 초과하면 합병 복원"

# action: change_topology
proposed_change:
  action: change_topology
  detail: "{현재 topology} → {제안 topology}. 전환 근거: {signal summary}"
  affected_artifacts: ["workflow_topology_spec.workflow_topology"]

rollback_rule: "전환 후 2 OW 내 새로운 루프 위험 발생 시 원래 topology로 복원"
```

## Template: Execution 제안

```yaml
classification: execution
target_skill: 02.execution-design

# action: recalibrate_theta
proposed_change:
  action: recalibrate_theta
  detail: "{노드}의 θ_GT band {현재 min-max} → {제안 min-max}. 근거: {performance_drift 데이터}"
  affected_artifacts: ["workflow_topology_spec.task_graph.nodes[].theta_gt_band"]

expected_effect: "Continue/Reframe/Stop 판정 정확도 향상"
rollback_rule: "재보정 후 1 OW 내 retry_spike 증가 시 이전 band로 복원"

# action: add_fallback
proposed_change:
  action: add_fallback
  detail: "{노드}에 fallback path 추가: {조건} 시 {대체 경로}"
  affected_artifacts: ["execution_plan.fallback_rules"]

rollback_rule: "fallback 경로가 3 OW 내 1회도 활성화되지 않으면 제거"

# action: adjust_gate
proposed_change:
  action: adjust_gate
  detail: "{gate}에 auto-approve 조건 추가: {조건}. human_deferral_loop 감소 기대"
  affected_artifacts: ["execution_plan.node_mode_policy"]

rollback_rule: "auto-approve 적용 후 품질 저하(failure_cluster 발생) 시 수동 gate 복원"
```

## Template: Policy 제안

```yaml
classification: policy
target_skill: 04.skill-governance

proposed_change:
  action: update_policy
  detail: "{대상 정책}: {현재 규칙} → {제안 규칙}. 근거: {반복 패턴}"
  affected_artifacts: ["skill_governance_rules"]

rollback_rule: "정책 변경 후 2 OW 내 부작용 발생 시 이전 정책으로 복원"
```

## Template: Operational 제안

```yaml
classification: operational
target_skill: DNA.md / 스웜 설정

proposed_change:
  action: update_config
  detail: "{설정 항목}: {현재값} → {제안값}. 근거: {운영 데이터}"
  affected_artifacts: ["DNA.md", "swarm_config"]

rollback_rule: "설정 변경 후 1 OW 내 예상 효과 미달 시 원래 값으로 복원"
```
