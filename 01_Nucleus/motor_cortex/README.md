---
name: aaos-motor-cortex
scope: "04_Agentic_AI_OS/01_Nucleus/motor_cortex"
status: canonical
version: "0.1.0"
updated: "2026-02-14"
---

# AAOS Motor Cortex

Nucleus의 실행 전담 기관.
Deliberation/Immune/Record Archive의 판정·증빙 결과를 받아, 제한된 실행 계약 안에서 변경을 수행하고 결과를 다시 archive 체인으로 반환한다.

## 정렬 우선순위

1. Canon (`README.md`)
2. META Doctrine (`00_METADoctrine/DNA.md`)
3. Nucleus Rule (`01_Nucleus/README.md` + `01_Nucleus/motor_cortex/governance/AGENTIC_WORKFLOW_ORCHESTRATION.md`)
4. 본 문서와 `DNA.md`

## 역할

- 실행 플랜을 작업 가능한 실행 단위로 변환
- 실행 전/중/후 검증 게이트 수행
- 실패 시 `on_conflict` 중단 및 Deliberation/Immune로 즉시 귀속
- 실행 결과를 Record Archive 봉인 대상(`PACKAGE.md`/`MANIFEST.sha256`)으로 반환

## 경계

- 수행함: 실행 오케스트레이션, 검증 명령 실행, 종료 조건 확인
- 수행하지 않음: 규범 최종 판정(Immune 소유), 영구 증빙 보존(Record Archive 소유), 합의 산출물 작성(Deliberation 소유)

## 운영 루프

1. 입력 수신: Deliberation 개선안 + Immune 승인 상태
2. 실행 계약 확인: scope/limit/rollback/termination 조건 검증
3. 실행 수행: 변경 반영 + 검증 명령 실행
4. 결과 반환: `context_for_next` + archive 봉인 입력 전달

## 운영 명령

- `python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py health --json`
- `python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py supervision-check --json`
- `python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py supervision-cycle`

## Supervision Runbook

- `supervision-check --json` / `supervision-cycle`는 주간 정기 실행을 기본으로 운영한다.
- 권장 실행: 매주 1회(월~금 중 1회), 이벤트 대응 시에는 즉시 추가 실행한다.
- 실행 순서:
  1) `python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py supervision-check --json`
  2) `python3 01_Nucleus/motor_cortex/scripts/nucleus_ops.py supervision-cycle --dry-run`
  3) `LOWER_LAYER_SUPERVISION.json` + `IMPROVEMENT_QUEUE.md`를 Deliberation Stage-5 TODO 입력으로 전달
  4) 필요 시 실행 모드 `supervision-cycle`로 봉인 패키지를 생성

## 상위기관 변경 게이트

`motor_cortex`의 DNA/운영 규칙 변경은 상위기관 변경으로 취급한다.
필수 요건은 Nucleus 게이트(합의/감사/서명/증빙 체인)와 동일하다.

## 핵심 원칙

- decree: 실행은 승인된 계약 범위 안에서만 수행한다.
- homing_instinct: 경계가 모호하면 즉시 Immune로 귀속한다.
- 실행 종료 시 `context_for_next`와 검증 결과를 남기지 않으면 완료로 간주하지 않는다.
