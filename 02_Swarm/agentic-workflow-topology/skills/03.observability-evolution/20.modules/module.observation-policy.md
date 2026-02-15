# module.observation-policy

## Question Axis

**어떤 신호를 어떤 소스에서 언제 관찰할 것인가?**

---

## 신호 소스 레지스트리

| Source | Type | Access |
|--------|------|--------|
| SQLite SoT | `audit_logs` 테이블 | `sql_checks.sql` + 신호별 쿼리 |
| Behavior Feed | JSONL (export_behavior_feed.py 산출물) | 파일 파싱 |
| Workflow Spec | topology-design JSON 산출물 | 기대 동작 기준선 참조 |

### SQLite `audit_logs` 스키마

```
id              INTEGER PRIMARY KEY
date            TEXT (YYYY-MM-DD)
task_name       TEXT
mode            TEXT
action          TEXT
status          TEXT (success | fail)
notes           TEXT
continuation_hint TEXT
transition_repeated INTEGER (0=first, 1=retry)
created_at      TEXT (ISO 8601)
```

---

## 6종 이상 신호 (Anomaly Signal)

### AS-1: `performance_drift`
- **정의**: 실행 시간이 히스토리컬 평균에서 2σ 초과 이탈
- **감지**: OW 내 task_name별 실행 시간 분포 비교
- **기본 심각도**: notice (>2σ), warning (>3σ), critical (>4σ 또는 타임아웃)

### AS-2: `failure_cluster`
- **정의**: 동일 task_name에서 OW 내 3건 이상 연속 실패
- **감지**: `WHERE status='fail' GROUP BY task_name HAVING COUNT(*) >= 3`
- **기본 심각도**: warning (3-4건), critical (5건 이상)

### AS-3: `retry_spike`
- **정의**: OW 내 `transition_repeated=1` 비율이 전체 이벤트의 20% 초과
- **감지**: 재시도 비율 = `COUNT(transition_repeated=1) / COUNT(*)`
- **기본 심각도**: notice (20-30%), warning (30-50%), critical (50%+)

### AS-4: `bottleneck`
- **정의**: 단일 노드(task_name)가 전체 실행 시간의 60% 이상 소비
- **감지**: task_name별 실행 시간 비율 계산
- **기본 심각도**: warning (60-80%), critical (80%+)

### AS-5: `human_deferral_loop`
- **정의**: `human_intervention=true` 이벤트가 OW 내 전체의 40% 초과
- **감지**: behavior feed에서 `outcome.human_intervention` 비율
- **기본 심각도**: notice (40-50%), warning (50-70%), critical (70%+)

### AS-6: `rsv_inflation`
- **정의**: 실제 RSV 소비가 설계 RSV 타깃의 130% 초과
- **감지**: workflow_spec의 `rsv_target` 대비 실행 결과 비교
- **기본 심각도**: warning (130-150%), critical (150%+)

---

## 심각도 판정 매트릭스

최종 심각도 = max(빈도 심각도, 영향 심각도, 재발 심각도)

| 기준 | notice | warning | critical |
|------|--------|---------|----------|
| **빈도** | OW 내 1-2회 | 3-5회 | 6회+ |
| **영향 범위** | 단일 노드 | 2-3 노드 | 전체 워크플로우 |
| **재발** | 첫 발생 | 이전 OW에서도 발생 | 3+ OW 연속 |

---

## 관찰 일정

| 모드 | OW 길이 | 트리거 |
|------|---------|--------|
| weekly | 7일 | 매주 정기 (기본값) |
| biweekly | 14일 | 안정된 워크플로우 |
| event | 실시간 | critical AS 감지 시 즉시 |
| on_demand | 사용자 지정 | 사용자 명시 요청 |

---

## 관찰 절차

1. **데이터 수집**: OW 범위 내 SQLite 쿼리 실행 → raw event 목록
2. **behavior feed 보충**: JSONL에서 OW 범위 이벤트 파싱 (available한 경우)
3. **신호 스캔**: 6종 AS 각각에 대해 감지 규칙 적용
4. **심각도 판정**: 매트릭스 기반 최종 심각도 산출
5. **신호 인벤토리 구성**: `signal_inventory[]` 산출

### 산출물: Signal Inventory

```json
{
  "observation_window": { "start": "...", "end": "..." },
  "mode": "weekly | biweekly | event | on_demand",
  "total_events": 142,
  "signal_inventory": [
    {
      "signal_id": "AS-2026-02-15-001",
      "type": "failure_cluster",
      "severity": "warning",
      "affected_task": "T3-analysis",
      "count": 4,
      "evidence_refs": ["audit_id:45", "audit_id:47", "audit_id:48", "audit_id:51"]
    }
  ]
}
```
