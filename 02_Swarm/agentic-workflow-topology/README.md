---
name: aaos-agentic-workflow-topology
description: 워크플로우 구조/토폴로지 설계를 담당하는 Swarm. 실행 바인딩이나 티켓 런타임 관리는 수행하지 않는다.
---
# agentic-workflow-topology

`02_Swarm/agentic-workflow-topology/`는 "어떤 워크플로우를 설계할 것인가"를 다루는 설계 전용 Swarm이다.

## 책임 경계

- `context-orchestrated-filesystem`: 업무 티켓을 로컬 파일로 생성/관리/추적하는 실행 운영 계층
- `agentic-workflow-topology`: Goal/DQ/RSV/theta_GT 기반으로 workflow graph를 설계하는 전략/설계 계층
- `context-orchestrated-workflow-intelligence`: AWT 설계 출력과 COF 운영 맥락을 중재하는 관계/적응 계층
- AWT는 설계 결과를 제공하지만 직접 실행/자동반영은 수행하지 않는다.

## Skill System v2

### Active Skills (5)

1. `00.workflow-skill-manager`
2. `01.mental-model-loader`
3. `02.workflow-topology-scaffolder`
4. `03.workflow-mental-model-execution-designer`
5. `04.workflow-observability-and-evolution`

## 포함 범위

- 멘탈모델 정의/로딩 정책
- workflow topology 및 scaffold spec 설계
- task-node별 멘탈모델 적용 방법 설계
- SQLite SoT(`agent-audit-log v1.2.0`) 기반 실행 관찰/개선 제안
- SQLite SoT -> Behavior Feed(JSONL) 수동 요약 export
- 주간/격주 수동 점검 템플릿 운영
- 스킬 체계 메타관리(정책+체크리스트)

## 제외 범위

- 실제 업무 티켓 생성/상태 전이/아카이빙
- 툴 실행 오케스트레이션
- 자동 반영/자동 차단 집행

## Canonical Reference

- DNA: `04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/DNA.md`
- Swarm Root: `04_Agentic_AI_OS/02_Swarm/README.md`

## Behavior Feed Export

- export mode: manual summary export only (no always-on dual-write)
- canonical field: `group_id`
- backward compatibility: `trace_id` 병행 기록

```bash
python3 04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/skills/04.workflow-observability-and-evolution/scripts/export_behavior_feed.py \
  --db-path 04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/00.context/agent_log.db \
  --out-path 04_Agentic_AI_OS/02_Swarm/agentic-workflow-topology/behavior/BEHAVIOR_FEED.jsonl
```
