---
workflow_id: ISSUE-NUC-20260214-0002
status: open
scope: 01_Nucleus
severity: high
issue_proposer: human:wmjoon
issue_signature: "Nucleus는 주기적 외향 감시(supervision-check/supervision-cycle) 산출물을 Deliberation Stage-5 개선 입력으로 자동 반영하지 못해 하위 레이어 개선 루프가 비활성 상태였다."
created: "2026-02-14"
---

# 문제제기: 외향적 감독/개선 루프 결손

## issue_scope

- 대상 영역: `01_Nucleus`
- 범위: Swarm/Manifestation 하위 모듈의 외향 감시(`supervision-check`, `supervision-cycle`)를 Deliberation 개선 루프로 연결
- 영향: `nucleus_ops`가 생성한 감시 결과를 사람이 수동 판독하는 구조로 인해 운영 피드백 소실, 반복 누락, 상향 제안 지연

## success_criteria (실행 규격)

### KPI-1: 감독 항목 규격화

- [ ] `SUPERVISION_SCOPE.md`에 Swarm 3개 모듈(`context-orchestrated-filesystem`, `context-orchestrated-ontology`, `cortex-agora`)과 Manifestation 1개 모듈(`summon-agents`)을 명시한다.
- [ ] 각 모듈별로 공통 점검항목을 명시한다.
  - [ ] `README.md` 존재
  - [ ] `DNA.md` 존재
  - [ ] 경계/자원/관측성 항목 점검 항목명 고정
  - [ ] 상향 제안(Deliberation 입력) 가능성 점검 항목명 고정

### KPI-2: 루프 입력-판단-기록 흐름 형식화

- [ ] `supervision-check --json` 출력에 `supervision_scope`, `required_issues`, `recommendations`가 항상 존재한다.
- [ ] `supervision-cycle --dry-run` 실행 시 아래 패키지가 모두 존재한다.
  - `payload/LOWER_LAYER_SUPERVISION.json`
  - `payload/IMPROVEMENT_QUEUE.md`
  - `payload/SUMMARY.md`
  - `payload/WORKFLOW_AUDIT.json`
  - `PACKAGE.md`
- [ ] `LOWER_LAYER_SUPERVISION.json` 내에 다음 메타 필드가 존재한다.
  - `supervision_scope`
  - `supervision_outputs` (`supervision_report_path`, `improvement_queue_path`, `package_path`)
  - `supervision_stage`

### KPI-3: 패턴 분석 → 개선안 경로 정합

- [ ] `IMPROVEMENT_QUEUE.md`의 각 항목이 `DECOMPOSITION_TODO.md`에 1:1 대응되는 TODO로 변환된다.
- [ ] `DECOMPOSITION_TODO.md`에는 `improvement_id`, `source`, `status`, `owner`, `evidence` 필드가 유지된다.
- [ ] Stage-5 종료 판단에서 `DECOMPOSITION_TODO.md`와 `task bundle` 일치도를 `evidence`로 기록한다.

### KPI-4: 상호 연동 및 상향 제어

- [ ] `01_Nucleus/deliberation_chamber/README.md`에 record_archive 패턴 개선 제안의 Stage-5 입력 경로를 명시한다.
- [ ] `01_Nucleus/motor_cortex/governance/AGENTIC_WORKFLOW_ORCHESTRATION.md`에 외향 감시 루프(2-b)와 Stage-5 규칙을 반영한다.
- [ ] `01_Nucleus/motor_cortex/README.md`에 주간 supervision cycle runbook을 추가한다.

## risk_level

- 현재 위험도: `high`
- W1: 하위 레이어 자율 확장 시 무감독 구간 확대
- W2: 개선 피드백 누락으로 반복 결함 악화
- W3: Stage-5 체크리스트와 감시 결과의 비일치로 Deliberation 증적 약화

## context_for_next

- 다음 액션:
  1. `supervision` 산출물 스키마를 `nucleus_ops.py`에서 고정하고 `LOWER_LAYER_SUPERVISION.json`에 경로/메타를 추가한다.
  2. 위원회 문서(AGENTIC_WORKFLOW_ORCHESTRATION, Deliberation/Motor Cortex README)에서 외향 루프 Stage-5 입력 규칙을 문서화한다.
  3. `SUPERVISION_SCOPE.md`와 task bundle를 기준으로 `DECOMPOSITION_TODO.md` 및 `EVIDENCE.md`를 완성한다.
  4. 패키지 산출물 일치성 확인 후 `SEAL_TO_ARCHIVE.md` 절차 실행한다.

