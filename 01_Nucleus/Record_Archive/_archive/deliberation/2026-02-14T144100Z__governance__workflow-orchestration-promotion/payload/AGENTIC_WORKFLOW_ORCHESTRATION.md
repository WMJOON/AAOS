---
name: aaos-agentic-workflow-orchestration
scope: "04_Agentic_AI_OS/01_Nucleus"
owner: "AAOS Canon"
status: canonical
version: "0.2.1"
created: "2026-02-14"
archive_path: "04_Agentic_AI_OS/01_Nucleus/Record_Archive/_archive/deliberation/2026-02-14T144100Z__governance__workflow-orchestration-promotion/"
---

# AAOS Agentic Workflow Orchestration

> Canonical Standard (승격: Blueprint 제도 폐지 후 운영 표준으로 편입)

## 목적

문제 제기부터 실행 종료까지 누락을 줄이고, 각 단계가 다음 단계의 입력(`context_for_next`)으로 이어지도록 강제합니다.

기본 경로:
1) 문제제기 → 2) Record_Archive 기록 → 3) Deliberation 계획 → 4) Immune 비판 → 5) Deliberation 개선 → 6) 실행/종결

## 필수 규칙 (MUST)

- 각 단계는 문서화된 산출물과 판별 가능한 완료 조건을 반드시 남겨야 합니다.
- 문제제기(1단계)는 인간 사용자/책임자 발화 또는 승인된 운영 이슈로만 시작할 수 있습니다.
- Record_Archive 기록(2단계)이 선행되어야 Deliberation 계획(3단계)을 시작할 수 있습니다.
- 분해 TODO(체크리스트, 티켓, 작업항목)는 Deliberation 개선(5단계)에서 Deliberation Chamber가 직접 관리해야 합니다.
- 실행 결과/증빙은 실행/종결(6단계)에서 Record_Archive에 봉인해야 합니다.
- Deliberation Chamber에서 추출한 분석 패턴 개선 제안만이 다음 주기 개선안으로 승인됩니다.
- Deliberation 계획(3단계)과 Deliberation 개선(5단계)은 `작성자와 다른 에이전트`의 독립 Critique를 통과해야 다음 단계로 진행할 수 있습니다.
- Critique는 동일 모델 패밀리 반복이 아닌 다른 에이전트/패밀리로 수행하는 것을 우선 원칙으로 둡니다.
- Immune System은 단계별 승인/거부/보류 판단의 최종 기관입니다.
- 상위기관 경계가 불명확하면 즉시 정지하고 META/Immune로 귀속합니다.
- `context_for_next`는 단계 종료마다 반드시 갱신합니다.
- 상위 변경(특히 DNA/규범/거버넌스 변경)은 반드시 Deliberation+Immune+Archive 루프를 통과합니다.

## 단계별 패턴

## 1) 문제제기 (Problem Framing)

- 입력: 이상 징후, 품질 이슈, 요구 변경, 사용자 요청
- 산출물:
  - `issue_scope`
  - 영향 범위(영향 bucket, 파일/모듈, 리스크 레벨)
  - 성공 기준(측정 가능 KPI 또는 판단 기준)
- 게이트:
  - 문제 정의가 재현 가능하고, 범위가 1단락으로 압축 가능한가
  - 책임기관(`Record_Archive/Immune/Deliberation`)이 명확한가
- 산출물 추가:
  - `issue_proposer`: 문제제기 발화 주체(사람/인간 승인자)
  - `issue_signature`: 증상·범위·성공 기준의 1문장 식별자

## 2) Record_Archive 기록 (Evidence Registration)

- 입력: 문제제기 산출물
- 산출물:
  - `WORKFLOW_TRACE_MANIFEST` 1건
  - 이슈 KPI/범위 요약
  - 아카이브 추적 포인터(임시 ID 또는 패스)
- 게이트:
  - 증적이 쿼리 가능한 형태로 기록되었는가
  - 문제 책임기관과 승인 경로가 남아 있는가
- 산출물 추가:
  - `record_path`: Record_Archive 추적 대상 경로(또는 임시 패스)

## 3) Deliberation 계획 (Deliberation Planning)

- 입력: Record_Archive 기록 산출물
- 산출물:
  - 작업 범위(Scope)
  - 우선순위 및 비용 추정
  - 완료 정의(Definition of Done)
  - 위험 완화 항목
  - `context_for_next` 초안
  - 후보 대안/선택 사유
- 게이트:
  - 대안 비교와 승인 후보가 문서화되었는가
  - `context_for_next`에 실패 시 회귀 포인트가 명시되는가
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

## 5) Deliberation 개선 (Deliberation Revision)

- 입력: Immune 비판 피드백
- 산출물:
  - 비판 반영 수정안
  - 분해 리스트/작업 티켓의 소유권: Deliberation Chamber
  - 단계별 TODO(파일/모듈 단위)
  - 작업 간 의존성
  - 검증 포인트(검증 명령/판독 기준)
  - 책임/에이전트 또는 모델 패밀리
- 게이트:
  - 누락/역전 이슈가 정정되었는가
  - TODO 단위와 검증 포인트가 실행 가능하게 정합되는가
- 산출물 추가:
  - `decomposition_author`: 개선안 반영 작성자
  - `decomposition_critic`: 다른 에이전트의 분해 품질 검토 및 누락 항목 지적
  - `decomposition_critic_status`: `pass`/`passed`/`ok`/`no-critical-objection`
- 승인 조건:
  - `decomposition_critic`가 완료되고 누락/역전 이슈가 정정된 뒤에만 실행 단계 진입

## 6) 실행 및 종료 (Execution & Closure)

- 입력: 작업 분해 항목
- 산출물:
  - 변경 파일/패치
  - 검증 결과(`ledger_keeper --verify`, health check)
  - `ARCHIVE_INDEX` 및 `HASH_LEDGER` 반영
  - AUDIT 기록(필요 시 Immune 로그)
  - Record_Archive 봉인 경로 및 hash ledger 링크
  - 다음 사이클 진입 정보(`context_for_next`)
- 게이트:
  - 실행 로그와 산출물이 1:1로 추적되는가
  - Record_Archive 무결성 증명(HASH_LEDGER, ARCHIVE_INDEX) 반영 여부
  - 검증 실패 항목이 있다면 `on_conflict`로 중단 처리했는가

## 누락 방지 체크리스트 (패턴 레벨)

1. 문제제기에서 KPI/성공 기준이 비어 있지 않은가?
2. Record_Archive 기록(2단계)에 추적 산출물이 남았는가?
3. 분해 리스트(체크리스트/티켓)가 Deliberation Chamber에서 관리되었는가?
4. Deliberation 계획(3단계)과 Immune 비판(4단계)이 모두 완료되었는가?
5. Deliberation 개선(5단계)에서 Immune 피드백이 반영되었고 누락이 정정되었는가?
6. 실행 결과가 Record_Archive(`ARCHIVE_INDEX`, `HASH_LEDGER`)에 봉인되었는가?
7. 실행 후 `--verify`와 아카이브 무결성 검증이 완료되었는가?
8. `context_for_next`가 새 시작점으로 정리되었는가?

## Nucleus 전개와 매핑

- Deliberation Chamber: 단계 3/5의 증거 형식화, 분해 리스트 관리, 패턴 개선 제안 생산
- Immune System: 단계 4의 승인·판정·충돌 처리(최종 승인 기관)
- Record Archive: 단계 2(기록), 6(종료 증적) 및 실행 결과 봉인

## 실행 절차 (권장)

```bash
# 1) 현재 상태를 기록
python3 01_Nucleus/scripts/nucleus_ops.py health

# 2) 아카이브 체인 검증
python3 01_Nucleus/Record_Archive/scripts/ledger_keeper.py --verify

# 3) 구현/문서 반영 후 상태 반영
python3 01_Nucleus/scripts/nucleus_ops.py log \
  --task-id TASK-NUC-WORKFLOW \
  --task-name "agentic workflow refinement" \
  --action "apply 6-stage orchestration pattern" \
  --status success \
  --context-for-next "next: verify cross-module docs parity"
```

## 템플릿 체크 규칙

- 한 단계라도 미완성이면 다음 단계로 진행하지 않습니다.
- 미완성 항목은 `Request-Changes`로 Immune 귀속 또는 재작업으로 되돌립니다.
- 모든 핵심 단계(1~6)는 최소 1회 로그 또는 문서 라인으로 남겨야 합니다.

## 감사 아티팩트 형식

```text
workflow_id: TASK-NUC-....
issue_proposer: human:requester
issue_signature: "<문제 정의, 범위, KPI 요약>"
record_path: "_archive/workflow/<id>"
direction_signature: "<개선방향 요약: 후보 비교 결과 + 승인 방향>"
plan_author: "<agent-A>"
plan_critic: "<agent-B>"
plan_critic_status: no-critical-objection
decomposition_author: "<agent-B>"
decomposition_critic: "<agent-C>"
decomposition_critic_status: no-critical-objection
```

검증:

```bash
python3 01_Nucleus/scripts/nucleus_ops.py workflow-audit 01_Nucleus/workflow_manifest.md
```
