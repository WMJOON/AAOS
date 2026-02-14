---
name: nucleus-global-skills-playbook
status: draft
updated: 2026-02-14
---
# Nucleus Global Skills Playbook

Nucleus 개선 시 글로벌 스킬을 일관되게 적용하기 위한 운영 플레이북.

## Scope

- 대상: `01_Nucleus/immune_system/`, `01_Nucleus/deliberation_chamber/`, `01_Nucleus/motor_cortex/`, `01_Nucleus/record_archive/`
- 목적: 판단 가능성(Judgability), 종료 품질, 인수인계 품질 강화

## Skill Mapping

| Skill | Primary Use | Nucleus Touchpoint |
|---|---|---|
| `agent-audit-log` | 세션 간 운영 로그 표준화(SQLite) | Immune, record_archive |
| `02.workflow-topology-scaffolder` | Goal→DQ→RSV→Task Graph + termination 설계 | Deliberation |
| `03.workflow-mental-model-execution-designer` | Task node별 멘탈모델/모드 적용 설계 | Deliberation, Immune |
| `04.workflow-observability-and-evolution` | 실행 패턴 관찰/개선 제안 리포트 | record_archive, motor_cortex |
| `playwright` | 실행 플로우 자동화/검증 | motor_cortex |

## Standard Runbook

1. 문제제기: 이슈/문맥/성공기준을 기록한다.
2. record_archive 기록: 증적 추적 포인터를 남긴다.
3. Deliberation 계획: DoD, 위험도, context_for_next를 사전 선언하고 2개 이상 대안 비교 후 승인 후보를 정한다.
4. Immune 비판: 작성자 외 에이전트가 계획/리스크를 Critique하고 승/보류/보완 결정을 받는다.
5. Deliberation 개선: 비판 반영 후 실행 단위와 의존성, 검증 포인트를 구조화한다.
6. 실행/종결: motor_cortex가 실행/검증을 수행하고, 결과를 record_archive로 봉인한다.

보조 규칙(내제화):

- Deliberation은 단계 3의 분해 리스트/티켓을 직접 관리하고, 단계 5에서 개선안을 반영한다.
- Deliberation에서 추출한 분석 패턴 개선 제안은 다음 주기 계획의 입력으로만 취급한다.
- Immune는 승인/보류/조건부 승인 판단의 최종 승인 기관이다.
- Archive는 모든 승인 변경/감사 증빙 및 실행 결과를 HASH_LEDGER/ARCHIVE_INDEX로 봉인한다.
- 상위기관 변경은 제안→증빙→심판→서명→피드백 루프를 완료해야 한다.
- Open Agent Council 규약상 최소 2개 이상 `model_family`와 반론-합의 흔적이 남아야 한다.
- 상호검증 단계(`cross_ref_validator`, `dissolution_monitor`)를 종료 포인트에 포함한다.

## Output Contract (Minimum)

- `workflow_spec.json`
- `termination_declarations.json`
- `DELIBERATION_PACKET.md`
- `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md` 또는 `01_Nucleus/record_archive/_archive/meta-audit-log/META_AUDIT_LOG.md` 엔트리
- `_archive/*/PACKAGE.md` + `MANIFEST.sha256` + ledger update
- `context_for_next` + `multi-agent-consensus` 메타데이터(`model_id`, `model_family`, `verdict`, `rationale`)

## Guardrails

- SQLite 운영 로그는 canonical 판정 로그를 대체하지 않는다.
- 종료 조건 없는 변경안은 승격 대상이 아니다.
- 과설명/무한 탐색 징후가 보이면 `re-chart` 또는 `human gate`로 즉시 전환한다.
