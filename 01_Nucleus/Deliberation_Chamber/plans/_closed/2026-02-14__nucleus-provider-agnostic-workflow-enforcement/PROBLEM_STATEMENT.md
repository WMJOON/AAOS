---
workflow_id: ISSUE-NUC-20260214-0001
status: open
scope: 01_Nucleus
severity: high
issue_proposer: human:requester
issue_signature: "Nucleus multi-provider workflow skips issue-framing -> plan/decomp separation checks causing critical governance bypass"
created: "2026-02-14"
---

# 문제제기: Nucleus 내 다중 프로바이더 에이전트의 워크플로우 미준수

## issue_scope

- 대상 영역: `01_Nucleus/` 하위 전체 운영
- 범위: `AGENTIC_WORKFLOW_ORCHESTRATION.md` 기반 6단계 워크플로우 미준수
- 영향: 상위기관 변경 규범 무시, 판단-근거 미기록, 모델 패밀리 분리 실패 가능성

## success_criteria

- KPI-1: Nucleus 신규 작업 생성 시 단계 1 산출물(`PROBLEM_STATEMENT.md`)이 1회 이상 존재해야 하며, `issue_id`/`issue_proposer`/`issue_signature`/`issue_scope`/`success_criteria`/`risk_level`/`context_for_next`가 모두 채워져야 한다.
- KPI-2: 단계 2 기록(`deliberation_chamber/plans/<plan-id>/WORKFLOW_MANIFEST`)은 단계 1 `workflow_id`를 `record_path`/`issue_signature` 참조와 함께 남겨야 한다.
- KPI-3: 단계 3 계획(`deliberation_chamber/plans/*`)에는 단계 1/2 결과의 참조가 포함되고, `context_for_next`가 누락되지 않아야 한다.
- KPI-4: `plan_critic_model_family`와 `decomposition_critic_model_family`가 서로 다르고, manifest `criticality_separation_required`/`criticality_model_family_separated`가 모두 `true`여야 한다.
- KPI-5: Deliberation 진입 전 `01_Nucleus/governance/AGENTS.md`의 1스텝 규칙 검증이 완료되어야 하며, 위반 항목이 있으면 `Request-Changes`로 즉시 중단되어야 한다.

검증 주기:
- 각 Nucleus 워크플로우 종료 시 `python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py workflow-audit <manifest>` 실행으로 KPI-4~KPI-5를 기본 검증한다.
- 최근 30건 종료 건 중 위반 건이 0건이어야 다음 단계 승인을 허용한다.

## risk_level

- 현재 위험도: `high`
- W1: 상위기관 변경 게이트 누락
  - 완화: `record_archive` 기록 단계에서 `record_path`와 `requested_action`를 의무화하고, `context_for_next` 점검을 강제한다.
- W2: 정통성 약화(모델군 편향/에코 챔버)
  - 완화: `plan_critic`/`decomposition_critic`의 model_family를 분리하고, `multi_agent_consensus`에 최소 2개 이상 명시한다.
- W3: 증빙 체인 붕괴
  - 완화: 이슈마다 위반 근거(문서 경로, 증적 링크, 위반 조건)를 `evidence_links`에 첨부하고 교차 검증한다.

## context_for_next

- 다음 액션: 
  1) 기존 준수 위반 후보를 `01_Nucleus/record_archive/`에서 검색한다.
     - 검색 기준: `workflow_id`, `issue_scope`, `problem_id`, `model_family`, `context_for_next`
     - 후보 산출물:
       - `01_Nucleus/record_archive/_archive/`
       - `01_Nucleus/deliberation_chamber/plans/`
       - 최근 Stage-2 `WORKFLOW_MANIFEST` 10건
  2) 미준수 항목별로 위반 증거 링크(파일/라인/판정 이유)를 수집해 01단계 문제제기 증거부록으로 정리한다.
  3) 정리본을 반영해 Step-2 manifest `record_path`와 Step-3 `DELIBERATION_PACKET`를 보강한다.
  4) 보강된 산출물을 바탕으로 `cross_ref_validator` 대상 2차 심사를 실행한다.

  선행 증거(예시 1건):
  - `01_Nucleus/deliberation_chamber/plans/_closed/2026-01-24__record-archive-dna-v0.2.4-flagship-consensus/` 내 일부 계획이 plan/decomposition 분리 기록 없이 진행된 사례(문서 경로/시기 확인 필요)
