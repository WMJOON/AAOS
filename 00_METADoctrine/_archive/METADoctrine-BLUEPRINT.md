---
type: meta-doctrine-archive
status: archived
version: v0.1.19
archived_reason: "Blueprint 제도 폐지 (비동기 감사 로그 기반 순환점검 체계로 전환)"
archived_at: 2026-02-14
---

# METADoctrine Blueprint (Archive)

## 용도

이 문서는 현재 시행 문서가 아니라 과거 `METADoctrine` Blueprint 설계의 정합성 보존용 아카이브입니다.
실행 규범이 아니라, 제도 변경 이력 및 이전 의사결정의 참고용 기록으로만 사용합니다.

## 정리 배경

- 기존 Blueprint 제도(사람 중심 2차 점검 절차)는 병목 구간이 되어 에이전트 성능/속도 개선에 제약이 됨.
- `agent-audit-log` 기반의 `Record_Archive`, `Immune_system`, `Deliberation_Chamber` 중심 비동기 검증 구조로 전환하면서
  Blueprint는 정규 제도에서 제외되고 기록 보존 항목으로만 전환.

## 상태

- 현재 적용 제도: 아님(archived)
- 참조 제도: `00_METADoctrine/METADoctrine_BLUEPRINT.md`(정리 및 폐지 후 정합성 반영본)
- 본 문서 처리 원칙: 기능 추가/변경의 기준 문서로 사용하지 않음.

## 과거 핵심 사항 보존 요약

- 핵심 개념은 `Metadoc-First`, 모듈형 제어, Approval/TTL/Change Packet/비상 종료 조건 등
  당시 설계의 일부였으며, 이후 `Immune_system`의 승인/점검 책임과 `Record_Archive`의 감사 이력 축적으로 이동됨.
- 재가동/재적용이 필요한 과거 기준이 있을 경우, 새로 정립된 `Deliberation_Chamber` 운영 패턴을 통해 반영해야 함.
