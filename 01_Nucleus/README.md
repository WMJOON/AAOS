---
name: aaos-nucleus
scope: "04_Agentic_AI_OS/01_Nucleus"
version: "0.2.1"
status: canonical
updated: "2026-02-14"
---

# AAOS Nucleus

Nucleus는 AAOS의 **기관 레이어(Validation Engine)** 이다.  
실행 책임은 `motor_cortex`로 분리하고, 나머지 기관은 판정·합의·증빙 루프를 담당한다.
기본 루프는 `문제제기` → `record_archive 기록` → `Deliberation` → `Immune 비판` → `Deliberation 개선` → `motor_cortex 실행` → `Archive 봉인`이다.

## 정렬 우선순위

`01_Nucleus`는 상위규범 계층을 따르며, 충돌 시 다음 순위로 판정한다.

1. Canon (`README.md`)
2. META Doctrine (`00_METADoctrine/DNA.md`)
3. Immune Doctrine (`01_Nucleus/immune_system/rules/README.md`)
4. 본 문서와 하위 운영 문서

## 구성

- `immune_system/`: 규범 판정, 권한 심판, 자원/해체 모니터링
- `deliberation_chamber/`: 다중 에이전트 합의 구조화, 근거 정리
- `motor_cortex/`: 실행 오케스트레이션, 검증 실행, 실패 시 귀속 처리
- `record_archive/`: 증빙 패키지/해시 체인/보존 인덱스

## 운영 원칙

- Nucleus 작업의 실행 규칙은 `01_Nucleus/governance/AGENTS.md`(Provider-agnostic MUST)로 고정한다.
- 새 구조/확장은 `DNA.md` 기반이어야 하며, 종료 조건과 자원 한계를 포함해야 한다.
- Canonical 판정이 모호하면 즉시 중단하고 상위기관으로 귀속한다.
- 상위기관 변경은 제안→증빙→심판→서명→피드백(6단계 운영 루프)으로 정식 전개해야 한다.
- 본 문서는 Nucleus 작업 수행자(Claude/Gemini/Grok 등 모든 에이전트)에 동일 적용됩니다.
- 동일 단계의 핵심 판단은 동일 모델군 단독 종료가 아니라 상호검증 분산 수행이어야 합니다.
- 패키지·증빙·판정은 모두 추적 가능해야 하며, Record Archive에 append-only로 보존한다.
- Nucleus 내부에서 발생하는 영구 기록은 모두 `01_Nucleus/record_archive/`로 일원화하며, 다른 폴더의 로그/증적은 작업 산출로만 취급한다.
- Swarm 행동 관찰 입력은 `02_Swarm/cortex-agora` 경유를 원칙으로 하며, `record_archive`는 봉인(seal) 단계의 장기 immutable SoT로 취급한다.
- Nucleus 산출물은 항상 종료 조건(`termination conditions`)과 다음 단계 입력(`context_for_next`)을 남긴다.
- `legacy`/`change_packets` 계열 경로는 운영 루트에서 금지하며, 반드시 `_archive/` 하위에만 둔다.
- `*_BLUEPRINT.md` 파일은 운영 루트에서 금지하며, 필요 시 `_archive/legacy/`로 격리 보관한다.
- 기관 하위 디렉토리명은 소문자(`lowercase` 또는 `lower_snake_case`)만 사용한다.
- 각 기관의 최상위 파일은 `README.md`, `DNA.md` 두 개만 허용한다(그 외는 하위 디렉토리로 분리).

## Nucleus 상위 변경 게이트 (필수)

다음은 상위기관 변경으로 분류되며, 해당 루틴을 반드시 통과해야 한다.

- `01_Nucleus/record_archive/`
- `01_Nucleus/immune_system/`
- `01_Nucleus/deliberation_chamber/`
- `01_Nucleus/motor_cortex/`

요건:

1. `multi-agent-consensus`(권장 4종, 최소 2개 model family)
2. Deliberation 산출물(합의/리스크/근거 요약)
3. `record_archive` 패키지 봉인(`PACKAGE.md`, `MANIFEST.sha256`, `HASH_LEDGER.md` 연계)
4. `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md` 판정 기록
5. `01_Nucleus/record_archive/_archive/meta-audit-log/META_AUDIT_LOG.md` 및 Canon Guardian 서명 근거
6. 상호검증: `cross_ref_validator` 및 `dissolution_monitor` 합격

## 표준 운영 흐름

1. Deliberation에서 변경 이슈를 토폴로지화하고 evidence를 구조화한다.
2. Immune가 판정/권한/종료 조건 적합성을 심사한다.
3. 승인/거부/수정요청 결과와 함께 Record Archive 패키지를 생성해 체인에 연결한다.
4. Motor Cortex가 실행/검증을 수행하고 결과를 반환한다.
5. 결과를 다음 작업 주기 context로 반영한다.

원칙:
- 분해 업무 리스트(체크리스트, 티켓)는 deliberation_chamber가 관리합니다.
- 실행/검증 수행은 motor_cortex가 담당합니다.
- 실행 결과와 검증 증거는 record_archive에 봉인합니다.
- record_archive로부터 나온 패턴/개선 인사이트는 다음 주기 Deliberation 개선안으로 제안합니다.
- immune_system은 최종 점검 승인 기관(승인/보류/조건부 승인)으로 판단합니다.

## Nucleus Agentic Workflow Pattern (반드시 적용)

`01_Nucleus/motor_cortex/governance/AGENTIC_WORKFLOW_ORCHESTRATION.md`에 정의된 6단계를 운영 표준으로 사용합니다.

적용 단계:

1. 문제제기: 인간이 이슈/목표를 증거 기반으로 정의
2. record_archive 기록: 이슈 증거를 추적 가능하게 먼저 봉인
3. Deliberation 계획: 대안 비교 후 실행 가능한 계획을 작성
4. Immune 비판: 계획에 대한 독립 비판/보완 권고를 받음
5. Deliberation 개선: 비판 반영으로 분해/의존성/검증 포인트 정합
6. 실행: 변경 반영 후 검증, 아카이브 연계, Immune/보류 처리를 완료

모든 단계는 누락 방지 체크리스트로 종료하고, 미완성 항목은 `Request-Changes` 또는 `on_conflict`로 되돌립니다.

상위기관 대상 변경은 `AGENTIC_WORKFLOW_ORCHESTRATION.md`의 상위기관 게이트(증빙 교차참조 + 다중 모델군 합의 + 교차검증/해체 모니터)까지 추가 적용됩니다.

## 빠른 정합성 체크리스트

- [ ] 상위 규범 우선순위가 문서에 명시되었는가?
- [ ] 하위 기관별 역할(`decree` / `homing_instinct`)이 구분되어 있는가?
- [ ] Natural Dissolution 목적/조건/해체 절차가 포함되었는가?
- [ ] Multi-agent 합의 항목에 model_id/model_family/provider가 남아 있는가?
- [ ] 변경 근거가 Record Archive 패키지로 append-only 보존되었는가?
- [ ] `context_for_next`를 통해 다음 주기 입력이 이어지는가?
- [ ] 상위기관 전환에서 `cross_ref_validator` + `dissolution_monitor` 결과가 남아 있는가?

## 스킬/스크립트 연동

- 핵심 운영 스킬
  - `agent-audit-log`: 운영 로그 표준화(SQLite)와 인수인계 추적 보조
  - `02.workflow-topology-scaffolder`: Deliberation 구조/종료 전략 설계
  - `03.workflow-mental-model-execution-designer`: 노드별 실행 시 멘탈모델 적용 설계
  - `04.workflow-observability-and-evolution`: 실행 로그 관찰 기반 개선 제안
- 핵심 실행 스크립트
  - `motor_cortex/scripts/nucleus_ops.py`

## Nucleus Ops 예시

```bash
python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py bootstrap
python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py health \
  --write-report 01_Nucleus/reports/HEALTH_REPORT.md
python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py supervision-check --json
python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py supervision-cycle
python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py workflow-audit 01_Nucleus/motor_cortex/templates/WORKFLOW_TRACE_MANIFEST_TEMPLATE.md
python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py log \
  --task-id TASK-NUC-001 \
  --task-name "Nucleus health cycle" \
  --action "health check + report" \
  --status success \
  --context-for-next "Review non-canonical nodes if any"
```
