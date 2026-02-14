---
name: aaos-deliberation-chamber
scope: "04_Agentic_AI_OS/01_Nucleus/deliberation_chamber"
version: "0.1.2"
status: canonical
updated: "2026-02-14"
---

# AAOS Deliberation Chamber

> AIVarium.Nucleus 구성 요소: 합의를 “어떻게 만들었는지”를 구조화한다.

본 기관은 집행/차단/판정을 직접 수행하지 않고, 결정의 증거 체인을 정리해 Immune System에 제공한다.

## 운영 정렬

- 상위 규범 우선순위를 준수한다.
- `homing_instinct` 운영을 사용한다. 충돌·불명확·권한 경계 시 작업을 멈추고 META/Immune로 귀속한다.
- 계획 단계는 `Goal → DQ → RSV → Topology → Task Graph` 순서를 기본 계약으로 사용한다.
- 최종 산출물은 Record Archive로 이관 가능한 형식이어야 한다.
- 분해 업무 리스트(체크리스트/티켓)는 Deliberation Chamber가 보유·관리합니다.
- record_archive 패턴 분석 결과를 **Stage-5 입력 항목**으로만 승인하고, Deliberation Chamber가 `DECOMPOSITION_TODO.md`로 1:1 분해한다.
- 외향 감시(`supervision-check`/`supervision-cycle`) 산출물은 1회성 제안이 아니라 Deliberation 정식 입력 경로이다.
- `plans/`와 `tasks/`는 작업 라우팅용 보관소이며, 승인 완료 후 산출물은 영구 보존체계(record_archive)로 이관되어야 한다.
- 봉인 완료 후 계획 README의 `status`를 `closed`로 전환하고 `archive_path`를 기록한 뒤, `plans/_closed/`로 이동한다.
- 에이전트는 `plans/` 직하 디렉토리만 활성 계획으로 스캔한다. `_closed/`는 스캔 대상에서 제외된다.

## 역할

- 변경 제안을 논점/리스크/판단 질문으로 구조화
- 다중 에이전트 합의 토픽(Claim, Counterclaim, Synthesis)을 정리
- 승인/거부/보류 판정 전용 evidence 패키지 작성
- `record_archive` 제출용 Deliberation Packet 표준 템플릿 준수
- 실행 증적/회고 산출물은 record_archive에 저장할 증빙 형태로 정리

## 비권한

- 집행, 차단, 최종 승인은 Immune System의 권한이다.
- 증빙 보존은 Record Archive의 권한이다.
- 승인 판단은 Immune가 최종 승인 기관입니다.

## 상호 작동 루프

```text
입력(변경 제안)
  -> Deliberation 구조화 (claim/counter/synthesis)
  -> 판정 패킷 작성 (합의 근거, 위험, 대안)
  -> Immune System 심판
  -> 승인/보류/거부 반영 + context_for_next 작성
  -> Record Archive 패키지 봉인
  -> IMPROVEMENT_QUEUE -> DECOMPOSITION_TODO 전달
```
 
## Plans/Tasks 산출물 책임

- `plans/<id>/`는 상위 변경 대응을 위한 계획 단위이고, `tasks/<id>/`는 합의와 실행 항목의 작업 단위이다.
- plan/task 종료 시점에서 `DELIBERATION_PACKET`/`EVIDENCE`/`SEAL_TO_ARCHIVE`는 `01_Nucleus/record_archive/_archive/`의 영구 패키지로 이관된다.
- `plans/`, `tasks/` 경로 자체는 작업 디렉토리이며, `record_archive` 봉인본이 존재하는 경우에만 규범상 최종 근거로 인정된다.

## 제출물 규격 (필수)

- `DELIBERATION_PACKET.md`
- 모델 메타데이터(`model_id`, `model_family`, `provider`, `verdict`, `rationale`)
- 근거 링크(`EVIDENCE` / `CHANGE` / `RISK` / `VERDICT` 경로)
- 합의 결론과 해소 조건(예: unresolved risk 보류, 수정요청)
- 다음 컨텍스트(`context_for_next`)

## Quick Start (권장)

1. 글로벌 스킬로 목표를 DQ/RSV 단계로 구조화  
   - `02.workflow-topology-scaffolder`
   - `03.workflow-mental-model-execution-designer`
2. plans/tasks 폴더에서 증빙·판단 근거를 정리
3. `templates/DELIBERATION_PACKET_TEMPLATE.md` 기반으로 패킷 구성
4. `SKILL` 체크리스트(termination declaration 포함) 충족
5. Immune 결과 반영 후 Archive 패키지로 이관

## 6단계 연계(표준)

1. 문제제기: 사용자 요청/이슈의 경로, 범위, KPI를 정리
2. record_archive 기록: 이슈 증적을 기록하고 추적 포인터 확보
3. Deliberation 계획: 대안 비교와 승인 후보를 제시
4. Immune 비판: 계획에 대한 독립 비판 및 보완 권고 수렴
5. Deliberation 개선: Deliberation Chamber가 TODO(체크리스트/티켓)를 최신화하고 record_archive 분석/패턴 제안을 반영
6. 실행/종결: 실행 결과와 검증 로그를 record_archive에 봉인하고 Immune 판단 결과를 반영

각 단계는 누락 여부를 체크해 미완성일 경우 `Request-Changes`로 되돌립니다.

## Skills 연동

- `deliberation-instruction-nucleus`: Nucleus 목적, 합의 규칙, 종료 조건을 사전 계약으로 고정
- `02.workflow-topology-scaffolder`: Goal→DQ→RSV 토폴로지 + 종료 전략 설계
- `03.workflow-mental-model-execution-designer`: 노드별 멘탈모델 적용 설계

## 버전 이력

- v0.1.0: 최초 DNA 제안 운영 분리
- v0.1.1: 모체/동급 기관 경계 정합성 업데이트
- v0.1.2: Canon/META 정렬 + 합의 산출물 메타데이터 강화
