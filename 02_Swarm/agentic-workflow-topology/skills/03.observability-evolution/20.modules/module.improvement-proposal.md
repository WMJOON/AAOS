# module.improvement-proposal

## Question Axis

**어떤 구체적 개선안을 어떤 근거로 제안할 것인가?**

---

## 패턴 → 제안 매핑

각 Anomaly Signal 유형은 후보 개선 행동에 매핑된다.

| AS Type | 후보 Action | Target Skill |
|---------|-------------|--------------|
| `failure_cluster` | topology 재구성, 노드 재설계, fallback rule 추가 | topology-design, execution-design |
| `retry_spike` | max_iterations 조정, 루프 위험 mitigation 업데이트 | topology-design |
| `bottleneck` | 노드 분할, parallel topology 검토 | topology-design |
| `human_deferral_loop` | auto-approve 조건 제안, gate 기준 정교화 | execution-design |
| `rsv_inflation` | Goal reframe 권고, 워크플로우 분할 | topology-design |
| `performance_drift` | θ_GT band 재보정, mode/model 전환 | execution-design |

---

## Improvement Proposal 스키마

```json
{
  "proposal_id": "IP-YYYY-MM-DD-NNN",
  "observation_window": {
    "start": "ISO8601",
    "end": "ISO8601"
  },
  "trigger_signals": ["AS-2026-02-15-001"],
  "classification": "topology | execution | policy | operational",
  "target_skill": "01.topology-design | 02.execution-design | 04.skill-governance",
  "observed_pattern": "string: 관찰된 패턴 요약",
  "root_cause_hypothesis": "string: 근본 원인 가설",
  "proposed_change": {
    "action": "modify_node | split_node | add_edge | update_policy | recalibrate_theta | add_fallback | adjust_gate",
    "detail": "string: 구체적 변경 내용",
    "affected_artifacts": ["workflow_topology_spec", "mental_model_bundle"]
  },
  "expected_effect": "string: 예상 효과",
  "rollback_rule": "string: 제안이 역효과일 때 되돌리는 규칙",
  "confidence": "high | medium | low",
  "evidence_refs": ["sql_query:...", "behavior_feed:awt:123"],
  "user_feedback": {
    "checkpoint_id": "HC-...",
    "decision": "approve | modify | reject"
  }
}
```

---

## 제안 생성 절차

1. **패턴 수신**: Phase 2에서 검증된 `top_patterns[]` 수신
2. **매핑 룩업**: AS type → 후보 action 테이블 참조
3. **근본 원인 추론**: 패턴의 evidence_refs를 기반으로 가설 수립
4. **타깃 스킬 결정**: classification에 따라 라우팅
5. **제안 구조화**: IP 스키마에 맞춰 필드 채움
6. **확신도 산정**: 증거 강도 + 사용자 피드백 유무로 결정
7. **사용자 제시**: Phase 3 HITL 체크포인트에서 검증 요청

---

## 확신도 산정 규칙

| 조건 | 확신도 |
|------|--------|
| 정량적 증거 + 사용자 confirmed | `high` |
| 정량적 증거, 사용자 미검증 | `medium` |
| 정성적 추론만, 또는 사용자 disputed | `low` |

---

## 검증 규칙 (Validation)

1. 증거 없는 제안 **금지** (`evidence_refs` 비어있으면 생성 불가)
2. `rollback_rule` 없는 제안 **금지**
3. `confidence < medium`인 제안은 사용자 검증 후에만 agora 제출 가능
4. `target_skill`이 명시되지 않으면 `classification=operational`로 기본 분류
5. 동일 패턴에 대해 2개 이상 경합 제안 시, 두 제안의 트레이드오프를 명시하고 사용자 선택 요청

---

## 판단 출력 형식

Core의 4-tuple 준수:

```
{
  "판단": "T3 노드를 T3a(수집) + T3b(분석)으로 분할",
  "근거": "bottleneck AS: T3가 전체 실행시간의 72% 소비 (audit_id: 45-51)",
  "트레이드오프": "분할 시 hand-off 비용 발생 vs 현행 병목 지속",
  "확신도": "medium"
}
```
