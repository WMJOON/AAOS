---
name: workflow-observability-and-evolution
description: Analyze workflow execution logs from SQLite SoT, produce periodic manual review outputs, and propose workflow improvements based on repeated patterns with agent-audit-log v1.2.0 compatibility.
---

# Workflow Observability and Evolution

SQLite 로그를 기준으로 워크플로우 반복 패턴을 분석하고 개선안을 제시한다.

## Logging Policy

- SoT: SQLite (`00.context/agent_log.db`)
- Schema compatibility target: `agent-audit-log v1.2.0`
- 자동 스케줄링 없음
- 수동 정기 점검 템플릿 사용 (주간/격주)
- behavior feed는 기본 dual-write 금지, 수동 요약 export만 허용
- export canonical field는 `group_id`이며 `trace_id`는 하위 호환 필드로 병행 기록

## Bootstrap / Migration Runbook

신규 DB 초기화:

```bash
mkdir -p 00.context
sqlite3 00.context/agent_log.db < 03_AgentsTools/01_agent-audit-log/v0.0.1/agent-audit-log/schema/init.sql
```

기존 DB 업그레이드(v1.x -> v1.2.0):

```bash
sqlite3 00.context/agent_log.db < 03_AgentsTools/01_agent-audit-log/v0.0.1/agent-audit-log/schema/migrate_v1_to_v1_1.sql
```

호환성 확인(최소):

```sql
SELECT name, type
FROM sqlite_master
WHERE name IN ('audit_logs', 'v_open_followups', 'v_agent_document_frequency')
ORDER BY type, name;
```

## Output: `workflow_improvement_report`

필수 섹션:
- `observed_patterns`
- `risk_signals`
- `proposed_changes`
- `expected_effect`
- `rollback_rule`

템플릿: `references/workflow_improvement_report.template.md`
- 주간 점검 시트: `references/weekly_review.template.md`
- 격주 점검 시트: `references/biweekly_review.template.md`

## Standard Routine (Manual)

1. Bootstrap/Migration 상태를 점검하고 SQL 호환성 체크를 수행한다.
2. `references/sql_checks.sql`로 최근 실행 패턴을 조회한다.
3. 반복 실패/재시도/인간개입 신호를 분류한다.
4. 주간/격주 템플릿으로 `workflow_improvement_report`를 작성한다.
5. 개선 제안을 기록하고 기대효과 및 롤백 조건을 명시한다.

## Behavior Feed Export Runbook

```bash
python3 04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/skills/04.workflow-observability-and-evolution/scripts/export_behavior_feed.py \
  --db-path 04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/00.context/agent_log.db \
  --out-path 04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/behavior/BEHAVIOR_FEED.jsonl \
  --from-ts 2026-02-14T00:00:00Z \
  --limit 500
```

Dry-run:

```bash
python3 04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/skills/04.workflow-observability-and-evolution/scripts/export_behavior_feed.py \
  --db-path 04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/00.context/agent_log.db \
  --out-path 04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/behavior/BEHAVIOR_FEED.jsonl \
  --dry-run
```

## Guardrail

- 자동 개선 반영/자동 차단은 수행하지 않는다.
- 제안은 사람이 승인한 뒤에만 상위 workflow spec에 반영한다.
