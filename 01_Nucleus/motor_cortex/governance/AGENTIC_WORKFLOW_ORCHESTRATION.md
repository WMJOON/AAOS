---
name: aaos-agentic-workflow-orchestration
scope: "04_Agentic_AI_OS/01_Nucleus"
status: canonical
version: "0.2.4"
updated: "2026-02-14"
---

# AAOS Agentic Workflow Orchestration

> Canonical Standard (승격: Blueprint 제도 폐지 후 운영 표준으로 편입)

## 목적

문제 제기부터 실행 종료까지 누락을 줄이고, 각 단계가 다음 단계의 입력(`context_for_next`)으로 이어지도록 강제합니다.

기본 경로:
1) 문제제기 → 2) record_archive 기록 → 3) Deliberation 계획 → 4) Immune 비판 → 5) Deliberation 개선 → 6) 실행/종결
1스텝 체인: 문제제기 산출물 -> `record_archive` 증적 등록 -> `01_Nucleus/deliberation_chamber/plans` 작성.

### 작업 디렉토리 책임 (Working Directory Ownership)

| 단계 | 작업 디렉토리 | 설명 |
|------|---------------|------|
| 1~5 (계획/심의) | `deliberation_chamber/plans/<plan-id>/` | 비평, 종합, 매니페스트 등 모든 작업 산출물 |
| 2 (증적 등록) | `record_archive` | 추적 포인터(임시 ID/경로)만 기록. 작업 파일 보관 금지 |
| 6 (실행) | `motor_cortex/` | 승인된 계획 실행, 검증 수행, 실패 시 귀속 처리 |
| 6-b (봉인) | `record_archive/_archive/<bucket>/` | 완료된 증빙 패키지만 append-only로 수용 |

> **금지**: `record_archive`에 `pending/`, `working/` 등 작업용 디렉토리를 생성하는 것은 append-only 원칙 위반이다. 모든 활성 작업 산출물은 `deliberation_chamber`에서 관리하고, 봉인 완료 후에만 `record_archive/_archive/`로 이관한다.

## 적용 주체 (Provider-Agnostic Rule)

이 표준은 Nucleus 작업을 수행하는 모든 에이전트에게 동일하게 적용됩니다.
`Claude`, `Gemini`, `Grok`를 포함한 모든 모델/에이전트 계열은 아래 규칙을 동일하게 준수합니다.
이 규칙은 `01_Nucleus/governance/AGENTS.md`에서 시행 규칙으로 고정됩니다.

## 필수 규칙 (MUST)

- 각 단계는 문서화된 산출물과 판별 가능한 완료 조건을 반드시 남겨야 합니다.
- Deliberation 단계(3,5)는 `Goal → Decision Questions(DQ) → RSV → Topology → Task Graph` 순서를 기본 설계 계약으로 사용해야 합니다.
- 1스텝 위반 금지:
  - 문제제기(1단계) 없이 2~3단계로 점프할 수 없다.
  - record_archive 기록(2단계) 없이 3단계(Deliberation 계획)로 점프할 수 없다.
- 동일 모델 인스턴스(Codex/Claude/Gemini/Grok 포함)는 동일 단계에서 전체 체인을 단독 수행할 수 없습니다.
  - 적어도 두 개 이상의 다른 모델군이 핵심 판단 단계(plan_critic / decomposition_critic)를 분리해 수행해야 합니다.
  - 위 규칙은 `plan_critic`와 `decomposition_critic`가 서로 다른 `model_family`에서 온 기록으로 남을 때만 통과합니다.
  - 감사 아티팩트에 `criticality_model_family_separated: true`가 남지 않으면 비승격 대상입니다.
- 문제제기(1단계)는 인간 사용자/책임자 발화 또는 승인된 운영 이슈로만 시작할 수 있습니다.
- record_archive 기록(2단계)이 선행되어야 Deliberation 계획(3단계)을 시작할 수 있습니다.
- 상위기관(메타/기관/군체 이상) 변경은 제안→증빙→심판→서명→피드백 루프(`Proposal → Evidence → Judgment → Signature → Feedback`)를 반드시 통과해야만 정식 정통성으로 인정됩니다.
- 상위기관 변경은 `DELIBERATION_PACKET`, `record_archive/_archive/audit-log/AUDIT_LOG.md`, `record_archive/_archive/meta-audit-log/META_AUDIT_LOG.md`, `record_archive/_archive`로의 교차 봉인을 요구합니다.
- Open Agent Council 다중 모델군 규약을 준수해야 합니다.
  - 최소 2개 이상의 서로 다른 `model_family` 반영을 남기고, 가능하면 4개 이상의 계열을 비교/반론/합의 대상으로 둡니다.
  - `multi-agent-consensus` 또는 동등 증빙이 Deliberation 산출물에 있어야 합니다.
- 분해 TODO(체크리스트, 티켓, 작업항목)는 Deliberation 개선(5단계)에서 Deliberation Chamber가 직접 관리해야 합니다.
- 실행 결과/증빙은 실행/종결(6단계)에서 record_archive에 봉인해야 합니다.
- Deliberation Chamber에서 추출한 분석 패턴 개선 제안만이 다음 주기 개선안으로 승인됩니다.
- Deliberation 계획(3단계)과 Deliberation 개선(5단계)은 `작성자와 다른 에이전트`의 독립 Critique를 통과해야 다음 단계로 진행할 수 있습니다.
- Critique는 동일 모델 패밀리 반복이 아닌 다른 에이전트/패밀리로 수행하는 것을 우선 원칙으로 둡니다.
- Critique는 `model_family` 다양성 규약을 위반하지 않아야 합니다.
- Immune System은 단계별 승인/거부/보류 판단의 최종 기관입니다.
- 상위기관 경계가 불명확하면 즉시 정지하고 META/Immune로 귀속합니다.
- `context_for_next`는 단계 종료마다 반드시 갱신합니다.
- 상위 변경(특히 DNA/규범/거버넌스 변경)은 반드시 Deliberation+Immune+Archive 루프를 통과합니다.
- 상위 변경의 종료 후 `cross_ref_validator`와 `dissolution_monitor` 정합성 검증이 필요합니다.

## 단계별 패턴

## 1) 문제제기 (Problem Framing)

- 입력: 이상 징후, 품질 이슈, 요구 변경, 사용자 요청
- 산출물:
  - `issue_scope`
  - 영향 범위(영향 bucket, 파일/모듈, 리스크 레벨)
  - 성공 기준(측정 가능 KPI 또는 판단 기준)
- 게이트:
  - 문제 정의가 재현 가능하고, 범위가 1단락으로 압축 가능한가
  - 책임기관(`record_archive/Immune/Deliberation`)이 명확한가
- 산출물 추가:
  - `issue_proposer`: 문제제기 발화 주체(사람/인간 승인자)
  - `issue_signature`: 증상·범위·성공 기준의 1문장 식별자

## 2) record_archive 기록 (Evidence Registration)

- 입력: 문제제기 산출물
- 산출물:
  - `WORKFLOW_TRACE_MANIFEST` 1건 → `deliberation_chamber/plans/<plan-id>/`에 저장
  - 이슈 KPI/범위 요약
  - 아카이브 추적 포인터(임시 ID 또는 패스)
- 게이트:
  - 증적이 쿼리 가능한 형태로 기록되었는가
  - 문제 책임기관과 승인 경로가 남아 있는가
- 산출물 추가:
  - `record_path`: 봉인 예정 경로 포인터 (`record_archive/_archive/<bucket>/`). 파일 자체는 `deliberation_chamber`에 보관한다.

### 2-b) 외향 감시 루프 (Outward Supervision)

- 입력: 하위 레이어 대상 모듈 상태 점검 요구
- 실행 순서:
  1. `python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py supervision-check --json`
  2. `python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py supervision-cycle`
  3. `payload/LOWER_LAYER_SUPERVISION.json` 정규 파싱(필수: `supervision_scope`, `supervision_outputs`, `supervision_stage` 확인)
  4. Deliberation Stage-5에서 IMPROVEMENT_QUEUE를 `DECOMPOSITION_TODO`로 전환
  5. 필요 시 `Immune`에서 위험성/적용범위 비판 후 조치 반영
- 게이트: `supervision_stage`가 `needs-improvement`인 경우 Stage-5 `required` TODO 미해결 전까지 상위 변경은 승인 불가

## 3) Deliberation 계획 (Deliberation Planning)

- 입력: record_archive 기록 산출물
- 산출물:
  - Topology 설계 계약(필수):
    - `goal_statement`
    - `decision_questions`(또는 manifest의 `dq_index`)
    - `rsv_total`
    - `topology_type` + 선택 근거(`topology_rationale`)
    - `task_graph_signature`(노드/엣지 요약)
  - 작업 범위(Scope)
  - 우선순위 및 비용 추정
  - 완료 정의(Definition of Done)
  - 위험 완화 항목
  - `context_for_next` 초안
  - 후보 대안/선택 사유
  - Open Agent Council 후보 비교(최소 2개 모델군)
- 게이트:
  - Topology 3-signal(Goal 성격 / Semantic Entropy 분포 / RSV 규모) 근거가 남아 있는가
  - 선택된 topology가 Task Graph와 모순되지 않는가
  - 대안 비교와 승인 후보가 문서화되었는가
  - `context_for_next`에 실패 시 회귀 포인트가 명시되는가
  - `model_id`, `model_family`, `verdict`, `rationale` 메타데이터가 상위기관 대상이라면 저장되었는가
- 산출물 추가:
  - `direction_signature`: 후보 비교 결과와 승인 방향(요약)
  - `plan_author`: 계획 작성자

## 4) Immune 비판 (Immune Critique)

- 입력: Deliberation 계획 산출물
- 산출물:
  - 승인/보류/조건부 승인 판정
  - 리스크 및 보완 권고
- 게이트:
  - 판단 결과가 명확한가 (`허용`, `보류`, `조건부 허용`)
  - 보완 권고가 실행 단계 입력으로 전달될 수 있는가
- 산출물 추가:
  - `plan_critic`: Immune 독립 에이전트의 계획 반영성 검토
  - `plan_critic_status`: `pass`/`passed`/`ok`/`no-critical-objection`
- 승인 조건:
  - 상위기관 변경의 경우 `record_archive/_archive/audit-log/AUDIT_LOG.md`와 `record_archive/_archive/meta-audit-log/META_AUDIT_LOG.md` 교차참조를 남기고 `plan_critic`/`plan_critic_status` 근거를 봉인해야 함

## 5) Deliberation 개선 (Deliberation Revision)

- 입력: Immune 비판 피드백
- 산출물:
  - Topology-Task Graph 정합성 보정(필수):
    - DQ 누락/중복 점검
    - `Σ(node.rsv_target) ≈ rsv_total` 점검(허용 오차 ±10%)
    - hand-off/loop risk 반영 후 `task_graph_signature` 갱신
  - 비판 반영 수정안
  - 분해 리스트/작업 티켓의 소유권: Deliberation Chamber
  - 단계별 TODO(파일/모듈 단위)
  - 작업 간 의존성
  - 검증 포인트(검증 명령/판독 기준)
  - 책임/에이전트 또는 모델 패밀리
- 외향 감시 산출물 전용 반영 규칙: Stage-5 TODO는 `IMPROVEMENT_QUEUE`에서 기원한 항목만 반영하고, unrelated 개선안은 별도 Stage-5 번들로 분리
- 게이트:
  - 누락/역전 이슈가 정정되었는가
  - TODO 단위와 검증 포인트가 실행 가능하게 정합되는가
- 산출물 추가:
  - `decomposition_author`: 개선안 반영 작성자
  - `decomposition_critic`: 다른 에이전트의 분해 품질 검토 및 누락 항목 지적
  - `decomposition_critic_status`: `pass`/`passed`/`ok`/`no-critical-objection`
- 승인 조건:
  - `decomposition_critic`가 완료되고 누락/역전 이슈가 정정된 뒤에만 실행 단계 진입
  - 상위기관 대상은 `DELIBERATION_PACKET`의 합의 메타데이터를 붙여야 함

## 6) 실행 및 종료 (Execution & Closure)

- 입력: 작업 분해 항목
- 산출물:
  - 변경 파일/패치
  - 검증 결과(`ledger_keeper --verify`, health check)
  - `ARCHIVE_INDEX` 및 `HASH_LEDGER` 반영
  - AUDIT 기록(필요 시 Immune 로그)
  - record_archive 봉인 경로 및 hash ledger 링크
  - 다음 사이클 진입 정보(`context_for_next`)
- 게이트:
  - 실행 로그와 산출물이 1:1로 추적되는가
  - record_archive 무결성 증명(HASH_LEDGER, ARCHIVE_INDEX) 반영 여부
  - 검증 실패 항목이 있다면 `on_conflict`로 중단 처리했는가
  - 상위기관의 경우 cross_ref/dissolution 후속 검증까지 완료했는가
  - 실행 책임 기관(`motor_cortex`)이 실행 계약(scope/rollback/termination)을 충족했는가

### 6-b) 계획 정리 (Plan Cleanup)

봉인 완료 후 `plan_manager.py`로 계획을 종료한다.

```bash
python3 01_Nucleus/motor_cortex/scripts/plan_manager.py close <plan-dir> \
  --archive-path "01_Nucleus/record_archive/_archive/deliberation/<sealed-package>/"
```

스크립트가 자동 수행하는 작업:
1. 계획 README `status` → `closed`, `archive_path` 기록
2. 관련 task bundle `status` → `done`
3. 계획 디렉토리를 `plans/_closed/`로 이동
4. `PLANS_REGISTRY.md` 재생성

- 게이트:
  - `plan_manager.py list --active`에서 해당 계획이 보이지 않는가
  - `PLANS_REGISTRY.md` 종료 계획에 봉인 경로가 기록되었는가

> **스캔 규칙**: 에이전트는 `PLANS_REGISTRY.md`만 읽으면 활성 계획을 파악할 수 있다. 디렉토리 스캔 불필요. `plans/_closed/`는 필요 시 명시적으로 참조한다.

## 누락 방지 체크리스트 (패턴 레벨)

1. 문제제기에서 KPI/성공 기준이 비어 있지 않은가?
2. record_archive 기록(2단계)에 추적 산출물이 남았는가?
3. 분해 리스트(체크리스트/티켓)가 Deliberation Chamber에서 관리되었는가?
4. Deliberation 계획(3단계)과 Immune 비판(4단계)이 모두 완료되었는가?
5. Deliberation 개선(5단계)에서 Immune 피드백이 반영되었고 누락이 정정되었는가?
6. 실행 결과가 record_archive(`ARCHIVE_INDEX`, `HASH_LEDGER`)에 봉인되었는가?
7. 실행 후 `--verify`와 아카이브 무결성 검증이 완료되었는가?
8. `context_for_next`가 새 시작점으로 정리되었는가?
9. 상위기관 변경이면 제안→증빙→심판→서명→피드백 루프가 완료되었는가?
10. Open Agent Council 다중 모델군 합의 기록이 남았는가?
11. `cross_ref_validator`와 `dissolution_monitor` 검증 단계가 존재하는가?
12. 봉인 후 `plan_manager.py close`로 계획이 종료되었는가?

## Nucleus 전개와 매핑

- Deliberation Chamber: 단계 1~5의 모든 작업 산출물 보관, 증거 형식화, 분해 리스트 관리, 패턴 개선 제안 생산
- Immune System: 단계 4의 승인·판정·충돌 처리(최종 승인 기관)
- Motor Cortex: 단계 6의 실행 오케스트레이션/검증/중단(on_conflict) 처리
- Record Archive: 단계 2(추적 포인터 등록), 6-b(종료 증적 봉인). 작업 파일 보관 금지, 봉인된 패키지만 수용

## 실행 절차 (권장)

```bash
# 1) 현재 상태를 기록
python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py health

# 2) 아카이브 체인 검증
python3 01_Nucleus/record_archive/scripts/ledger_keeper.py --verify

# 3) 정합성/해체 모니터링 검증
python3 01_Nucleus/immune_system/skills/core/cross_ref_validator.py \
  --root 04_Agentic_AI_OS \
  --check-inline-paths
python3 01_Nucleus/immune_system/skills/core/dissolution_monitor.py \
  --scan 04_Agentic_AI_OS --dry-run

# 4) 구현/문서 반영 후 상태 반영
python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py log \
  --task-id TASK-NUC-WORKFLOW \
  --task-name "agentic workflow refinement" \
  --action "apply 6-stage orchestration pattern" \
  --status success \
  --context-for-next "next: verify cross-module docs parity"

# 5) 계획 정리 (Stage 6-b)
python3 01_Nucleus/motor_cortex/scripts/plan_manager.py close <plan-dir> \
  --archive-path "01_Nucleus/record_archive/_archive/deliberation/<sealed-package>/"

# 6) 활성 계획 확인
python3 01_Nucleus/motor_cortex/scripts/plan_manager.py list --active
```

## 템플릿 체크 규칙

- 한 단계라도 미완성이면 다음 단계로 진행하지 않습니다.
- 미완성 항목은 `Request-Changes`로 Immune 귀속 또는 재작업으로 되돌립니다.
- 모든 핵심 단계(1~6)는 최소 1회 로그 또는 문서 라인으로 남겨야 합니다.
- 상위기관 변경 산출물은 단계별 로그와 함께 `multi-agent-consensus` 교차참조를 남겨야 합니다.

## 감사 아티팩트 형식

```text
workflow_id: TASK-NUC-....
issue_proposer: human:requester
issue_signature: "<문제 정의, 범위, KPI 요약>"
goal_statement: "<최종 목표 1문장>"
dq_index: "DQ1|DQ2|DQ3"
rsv_total: 3.0
topology_type: "linear|branching|parallel|fanout_fanin|hierarchical|synthesis_centric|state_transition|composite"
topology_rationale: "<Goal/SE/RSV 기반 선택 근거>"
task_graph_signature: "T1->T2->T3"
record_path: "_archive/deliberation/<timestamp>__<type>__<slug>/"
model_consensus: "multi-agent-consensus"
plan_critic_model_id: "claude-opus-4-6"
plan_critic_provider: "Anthropic"
plan_critic_model_family: "anthropic-claude"
direction_signature: "<개선방향 요약: 후보 비교 결과 + 승인 방향>"
plan_author: "agent-A"
plan_critic: "agent-B"
plan_critic_status: no-critical-objection
decomposition_author: "agent-B"
decomposition_critic: "agent-C"
decomposition_critic_status: no-critical-objection
decomposition_critic_model_id: "gemini-1.5-pro"
decomposition_critic_provider: "Google"
decomposition_critic_model_family: "google-gemini"
criticality_separation_required: "true"
criticality_model_family_separated: "true"
cross_ref_validation: "pending"
dissolution_monitor_status: "not-applicable"
```

검증:

```bash
python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py workflow-audit 01_Nucleus/workflow_manifest.md
```
