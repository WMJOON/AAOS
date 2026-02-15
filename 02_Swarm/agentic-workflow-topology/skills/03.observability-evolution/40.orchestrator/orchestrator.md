# Orchestrator -- Observe → Interact → Evolve

## 5-Phase 프로세스

```
Phase 1: Signal Collection
Phase 2: Pattern Analysis
Phase 3: HITL Checkpoint
Phase 4: Improvement Proposal
Phase 5: Evolution Handoff
```

---

## Phase 1: Signal Collection

**모듈 로딩**: `observation-policy`
**참조팩 로딩**: `pack.sql_queries` (항상)

1. 관찰 모드 결정: `scheduled` / `event` / `on_demand`
2. Observation Window(OW) 설정
3. SQLite SoT에 대해 신호별 SQL 쿼리 실행 (Q-BASE + Q-AS1~6)
4. Behavior feed JSONL에서 OW 범위 이벤트 파싱 (가용 시)
5. Raw signal inventory 수집

**산출물**:
```json
{
  "observation_window": { "start": "...", "end": "..." },
  "mode": "scheduled | event | on_demand",
  "total_events": 142,
  "signal_inventory": [
    { "signal_id": "AS-...", "type": "...", "severity": "...", "count": 0, "evidence_refs": [] }
  ]
}
```

---

## Phase 2: Pattern Analysis

**모듈 로딩**: `observation-policy` (분류 규칙)
**참조팩 로딩**: `pack.anomaly_profiles` (ΔQ >= 2, 이상 감지 시)

1. 각 신호를 6종 AS 유형으로 분류
2. 심각도 판정 (빈도 × 영향 × 재발 매트릭스)
3. 관련 신호를 패턴으로 그룹화
4. 심각도 × 빈도 × 영향 기준 패턴 랭킹
5. Top-N 패턴 선정 (기본 N=3)

**산출물**:
```json
{
  "pattern_analysis": {
    "anomaly_signals": [
      { "signal_id": "AS-...", "type": "failure_cluster", "severity": "warning", "pattern_group": "PG-01" }
    ],
    "severity_distribution": { "notice": 2, "warning": 1, "critical": 0 },
    "top_patterns": [
      { "pattern_id": "PG-01", "type": "failure_cluster", "severity": "warning", "affected_nodes": ["T3"], "signal_count": 4 }
    ]
  }
}
```

**분기 규칙**:
- 이상 신호 없음 → Phase 3 (간략 SC) → Phase 5 (요약만)
- `critical` 존재 → 즉시 Phase 3 Event Checkpoint

---

## Phase 3: HITL Checkpoint

**모듈 로딩**: `hitl-interaction`

1. 체크포인트 모드 결정:
   - `critical` 신호 존재 → `event_checkpoint` (즉시)
   - 그 외 → `scheduled_checkpoint` (OW 종료 시)
2. 관찰 요약 포맷팅 (hitl-interaction 제시 프로토콜 사용)
3. Top 패턴 + 증거 발췌 제시
4. `auto_propose=true` → Phase 4 사전 실행 후 초안 제안 함께 제시
5. 구조화된 사용자 피드백 수집
6. 피드백 기록 (SQLite + behavior feed)

**산출물**:
```json
{
  "checkpoint": {
    "checkpoint_id": "HC-2026-02-15-001",
    "mode": "scheduled",
    "signals_presented": 3,
    "user_feedback_collected": true,
    "validated_patterns": ["PG-01"],
    "dismissed_patterns": []
  }
}
```

**에스컬레이션**: event_checkpoint + 48h 무응답 → `halt_and_escalate_to_audit`

---

## Phase 4: Improvement Proposal

**모듈 로딩**: `improvement-proposal`
**참조팩 로딩**: `pack.proposal_templates` (ΔQ >= 2)

1. 검증된 패턴마다 후보 개선 행동 생성 (매핑 테이블 참조)
2. 근본 원인 가설 수립 (evidence_refs 기반)
3. 타깃 스킬 결정 (classification → routing)
4. 확신도 산정 (증거 강도 + 사용자 피드백)
5. IP 스키마에 맞춰 제안 구조화
6. 사용자에게 제안 제시 → approve / modify / reject 수집

**산출물**:
```json
{
  "proposals": [
    {
      "proposal_id": "IP-2026-02-15-001",
      "classification": "topology",
      "target_skill": "01.topology-design",
      "action": "split_node",
      "confidence": "medium",
      "user_decision": "approve"
    }
  ]
}
```

---

## Phase 5: Evolution Handoff

**모듈 로딩**: `evolution-tracking`
**참조팩 로딩**: `pack.agora_format` (ΔQ >= 3, 제출 필요 시)

1. 승인된 제안 → cortex-agora change event 포맷 변환
2. 제출 조건 체크리스트 검증
3. Agora CHANGE_INDEX에 제출 (또는 수동 제출용 스테이징)
4. Evolution Cycle 상태 업데이트 (`draft → user_reviewed → submitted`)
5. 거부된 제안 → 거부 사유와 함께 아카이브
6. 폐루프 메트릭 산출 (closure_rate, avg_cycle_days, stale_proposals)
7. 주기적 리뷰 → 리뷰 템플릿 기반 보고서 생성

**최종 산출물**:
```json
{
  "observation_window": { "start": "...", "end": "..." },
  "mode": "scheduled",
  "signal_summary": { "total": 142, "by_type": {}, "by_severity": {} },
  "top_patterns": [],
  "checkpoint": { "id": "HC-...", "user_feedback_collected": true },
  "proposals": [
    { "proposal_id": "IP-...", "status": "submitted_to_agora", "target_skill": "01.topology-design" }
  ],
  "evolution_metrics": {
    "active_cycles": 3,
    "closure_rate_30d": 0.67,
    "avg_cycle_days": 12,
    "stale_proposals": 0
  }
}
```

---

## 모드별 Phase 실행 경로

| 모드 | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 |
|------|---------|---------|---------|---------|---------|
| `scheduled` | 전체 OW 수집 | 전체 분석 | SC | 전체 | 전체 |
| `event` | 이벤트 중심 수집 | 이벤트 분석 | EC (즉시) | 긴급 제안 | 스테이징 |
| `on_demand` | 사용자 지정 OW | 전체 분석 | SC | 전체 | 전체 |
| 이상 없음 | 수집 | 분석 (결과 0) | 간략 SC | 건너뜀 | 요약만 |
