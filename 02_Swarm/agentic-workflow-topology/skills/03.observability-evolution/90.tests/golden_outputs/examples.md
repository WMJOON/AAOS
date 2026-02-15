# Golden Output Examples

## Example 1: TC02 -- 주간 리뷰, retry_spike 감지

### Phase 1 산출물

```json
{
  "observation_window": { "start": "2026-02-08", "end": "2026-02-15" },
  "mode": "scheduled",
  "total_events": 87,
  "signal_inventory": [
    {
      "signal_id": "AS-2026-02-15-001",
      "type": "retry_spike",
      "severity": "warning",
      "affected_task": "T3-research",
      "count": 22,
      "evidence_refs": ["audit_id:34", "audit_id:36", "audit_id:38", "audit_id:41"]
    }
  ]
}
```

### Phase 2 산출물

```json
{
  "pattern_analysis": {
    "anomaly_signals": [
      { "signal_id": "AS-2026-02-15-001", "type": "retry_spike", "severity": "warning", "pattern_group": "PG-01" }
    ],
    "severity_distribution": { "notice": 0, "warning": 1, "critical": 0 },
    "top_patterns": [
      { "pattern_id": "PG-01", "type": "retry_spike", "severity": "warning", "affected_nodes": ["T3-research"], "signal_count": 22 }
    ]
  }
}
```

### Phase 3 제시 (Scheduled Checkpoint)

```markdown
## Observation Summary (OW: 2026-02-08 ~ 2026-02-15)

### 신호 요약
| Type | Count | Severity | Affected Nodes |
|------|-------|----------|----------------|
| retry_spike | 22 | warning | T3-research |

### Top 패턴 상세
1. **T3-research 재시도 급증**
   - 근거: OW 내 87 이벤트 중 22건(25.3%)이 재시도. 정상 수준(< 20%) 초과.
   - 영향: T3 노드 처리 시간 증가, 후속 노드 지연

### 개선 제안
1. [IP-2026-02-15-001] T3의 max_iterations를 3 → 5로 상향 (확신도: medium)

### 피드백 요청
a) 제안 승인/수정/거부
b) 추가 분석 요청
c) 이번 리뷰 건너뛰기
```

### Phase 4 산출물

```json
{
  "proposals": [
    {
      "proposal_id": "IP-2026-02-15-001",
      "observation_window": { "start": "2026-02-08", "end": "2026-02-15" },
      "trigger_signals": ["AS-2026-02-15-001"],
      "classification": "topology",
      "target_skill": "01.topology-design",
      "observed_pattern": "T3-research 노드에서 재시도율 25.3% (정상 < 20%)",
      "root_cause_hypothesis": "max_iterations=3이 해당 리서치 태스크의 convergence에 불충분",
      "proposed_change": {
        "action": "modify_node",
        "detail": "T3-research의 max_iterations를 3 → 5로 상향. 추가로 θ_GT band 하한을 0.1 낮춤",
        "affected_artifacts": ["workflow_topology_spec.task_graph.nodes[T3]"]
      },
      "expected_effect": "재시도율 25% → 15% 이하로 감소, convergence 달성률 향상",
      "rollback_rule": "변경 후 2 OW 내 재시도율이 여전히 20% 초과이면 원래 설정으로 복원",
      "confidence": "medium",
      "evidence_refs": ["sql_query:Q-AS3", "audit_id:34,36,38,41"],
      "user_feedback": { "checkpoint_id": "HC-2026-02-15-001", "decision": "approve" }
    }
  ]
}
```

### Phase 5 최종 산출물

```json
{
  "observation_window": { "start": "2026-02-08", "end": "2026-02-15" },
  "mode": "scheduled",
  "signal_summary": { "total": 87, "by_type": { "retry_spike": 22 }, "by_severity": { "warning": 1 } },
  "top_patterns": [{ "pattern_id": "PG-01", "type": "retry_spike", "affected_nodes": ["T3-research"] }],
  "checkpoint": { "id": "HC-2026-02-15-001", "user_feedback_collected": true },
  "proposals": [
    { "proposal_id": "IP-2026-02-15-001", "status": "submitted_to_agora", "target_skill": "01.topology-design" }
  ],
  "evolution_metrics": {
    "active_cycles": 1,
    "closure_rate_30d": 0.0,
    "avg_cycle_days": 0,
    "stale_proposals": 0
  }
}
```

---

## Example 2: TC03 -- Critical failure_cluster 이벤트 트리거

### Phase 3 제시 (Event Checkpoint)

```markdown
## ALERT: Critical Anomaly Detected

- **신호**: failure_cluster in T2-analysis
- **심각도**: CRITICAL
- **근거**: 최근 5건 연속 실행 실패 (audit_id: 71-75, status='fail')
- **감지 시점**: 2026-02-15T14:32:00Z

### 즉시 선택지
a) 근본 원인 분석 요청
b) 즉시 개선안 생성
c) 워크플로우 일시 중단 + 에스컬레이션
d) 확인 후 모니터링 유지
```

---

## Example 3: TC01 -- 이상 없음, 간략 리뷰

### Phase 3 제시 (간략 Scheduled Checkpoint)

```markdown
## Observation Summary (OW: 2026-02-08 ~ 2026-02-15)

- 총 이벤트: 65
- 감지된 이상 신호: 0
- 모든 지표가 정상 범위 내입니다.

이번 주기에는 개선 제안이 없습니다.
다음 리뷰: 2026-02-22
```
