# pack.sql_queries

> **로딩 조건**: 항상 (Phase 1 신호 수집 시)

SQLite SoT `audit_logs` 테이블에 대한 신호별 쿼리 템플릿.

---

## 기본 쿼리

### Q-BASE-01: 상태 분포

```sql
SELECT status, COUNT(*) AS cnt
FROM audit_logs
WHERE date BETWEEN '{ow_start}' AND '{ow_end}'
GROUP BY status
ORDER BY cnt DESC;
```

### Q-BASE-02: 재시도 신호

```sql
SELECT id, date, task_name, mode, status, transition_repeated, notes
FROM audit_logs
WHERE transition_repeated = 1
  AND date BETWEEN '{ow_start}' AND '{ow_end}'
ORDER BY date DESC;
```

### Q-BASE-03: 미결 후속 작업

```sql
SELECT id, date, task_name, mode, continuation_hint
FROM audit_logs
WHERE continuation_hint IS NOT NULL
  AND continuation_hint != ''
  AND date BETWEEN '{ow_start}' AND '{ow_end}'
ORDER BY date DESC;
```

---

## 신호별 쿼리

### Q-AS1: performance_drift

```sql
SELECT task_name,
       COUNT(*) AS exec_count,
       AVG(JULIANDAY(created_at) - JULIANDAY(date)) AS avg_duration_days
FROM audit_logs
WHERE date BETWEEN '{ow_start}' AND '{ow_end}'
GROUP BY task_name
ORDER BY avg_duration_days DESC;
```

### Q-AS2: failure_cluster

```sql
SELECT task_name, COUNT(*) AS fail_count,
       GROUP_CONCAT(id) AS audit_ids
FROM audit_logs
WHERE status = 'fail'
  AND date BETWEEN '{ow_start}' AND '{ow_end}'
GROUP BY task_name
HAVING fail_count >= 3
ORDER BY fail_count DESC;
```

### Q-AS3: retry_spike

```sql
SELECT
  ROUND(100.0 * SUM(CASE WHEN transition_repeated = 1 THEN 1 ELSE 0 END) / COUNT(*), 1) AS retry_pct,
  COUNT(*) AS total,
  SUM(CASE WHEN transition_repeated = 1 THEN 1 ELSE 0 END) AS retries
FROM audit_logs
WHERE date BETWEEN '{ow_start}' AND '{ow_end}';
```

### Q-AS4: bottleneck

```sql
SELECT task_name,
       COUNT(*) AS event_count,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM audit_logs WHERE date BETWEEN '{ow_start}' AND '{ow_end}'), 1) AS pct
FROM audit_logs
WHERE date BETWEEN '{ow_start}' AND '{ow_end}'
GROUP BY task_name
ORDER BY event_count DESC
LIMIT 5;
```

### Q-AS5: human_deferral_loop

```sql
SELECT COUNT(*) AS total_events,
       SUM(CASE WHEN notes LIKE '%human%' OR notes LIKE '%manual%' OR continuation_hint LIKE '%human%' THEN 1 ELSE 0 END) AS human_events
FROM audit_logs
WHERE date BETWEEN '{ow_start}' AND '{ow_end}';
```

### Q-AS6: rsv_inflation

> RSV 비교는 workflow_spec의 `rsv_target`과 실행 결과를 대조해야 하므로, 이 쿼리는 실행 완료 노드 수/DQ 닫힘 여부를 근사 지표로 사용한다.

```sql
SELECT task_name, mode,
       SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) AS success_count,
       SUM(CASE WHEN status = 'fail' THEN 1 ELSE 0 END) AS fail_count,
       COUNT(*) AS total
FROM audit_logs
WHERE date BETWEEN '{ow_start}' AND '{ow_end}'
GROUP BY task_name, mode;
```

---

## 문서 참조 빈도 (보조)

```sql
SELECT file_path, reference_count, last_referenced
FROM v_agent_document_frequency
ORDER BY reference_count DESC
LIMIT 20;
```
