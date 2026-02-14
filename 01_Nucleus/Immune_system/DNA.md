---
name: aaos-immune-system-dna
scope: "04_Agentic_AI_OS/01_Nucleus/immune_system"
status: canonical
version: "0.3.4"
updated: "2026-02-14"
---

# AAOS Immune System DNA

## Supremacy Clause

본 문서와 하위 규범은 Canon / META / Immune Doctrine에 종속된다.
우선순위 충돌 시 `Canon > META Doctrine > Immune Doctrine > This document`를 따른다.
정합성 판단이 불투명하면 즉시 판정/변경을 중단하고 승인·감사 절차를 선행한다.

## 운영 원리

- 정통성 판정의 대상: 구조 생성, 확장, 장기 보존, 권한 변경
- 기본 원칙: 정식 DNA + Natural Dissolution + resource limits + audit trace 필수
- 집행: Inquisitor + AUDIT_LOG 체인으로 수행

## 대전제 (Doctrine Premises)

- 대전제는 본 문서(`DNA.md`)에서 관리한다.
- 고복잡도 규칙은 `01_Nucleus/immune_system/rules/` 모듈로 분할한다.
- 규칙 정본 인덱스: `01_Nucleus/immune_system/rules/README.md`

## 핵심 룰

1. **정식 DNA 선행**
   - `DNA.md`가 없으면 구조 생성/확장은 허용되지 않는다.
2. **Natural Dissolution**
   - 존재 목적과 종료 조건/해체 절차, 보존 요건이 명시되어야 한다.
3. **권한 심판**
   - Tool/API 접근, 장기 유지, 구조 이동/복제, 조직 확장은 Permission 심판 전제이다.
4. **감사 무결성**
   - `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md`는 해시체인 형식으로 기록되며 삭제·변조를 금지한다.
5. **상위 변경 게이트 준수**
   - Canon/META/기관 DNA 변경은 상향 심사 절차를 완료해야 한다.
6. **최종 승인권**
   - 실행/승인/거부/보류 판단의 최종 기관은 Immune System이다.
   - Deliberation이나 Record Archive의 산출물은 판정 입력으로만 취급되며, 최종 의사결정은 Immune의 로그/감사 체인에 반영되어야 한다.

## 상위 변경 게이트(요약)

요건:

1. 다중 합의(`multi-agent-consensus`, 최소 2 모델 family)
2. `01_Nucleus/record_archive/_archive/meta-audit-log/META_AUDIT_LOG.md`에 변경 사유/리스크 등록
3. `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md` 판정 엔트리 생성
4. Canon Guardian 승인
5. `context_for_next` 업데이트

예외(긴급):
- 보안 패치: 단일 Agent + 인간 승인 후 사후 합의

## 기록·판정 체계

- META 수준 승인: `01_Nucleus/record_archive/_archive/meta-audit-log/META_AUDIT_LOG.md`
- 일반 판정: `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md`
- 판정 타입: `judgment-dna`(DNA 정통성 판정), `judgment-permission`, `auto-enforcement`, `dissolution-execution`

## Self-Validation 메커니즘

Immune System은 자가 완전 검증을 수행하지 않으며,
Canon 정렬/구조 해시/자원 한계 점검으로만 자기 무결성을 모니터링한다.

## Growth and Change Rules

- 허용 확장:
  - Inquisitor/검증 템플릿 추가 또는 정교화
  - 자동 enforcement 능력 보강
  - 기존 정책과 충돌하지 않는 검사 루틴 강화
- 변경 전 체크:
  - [ ] Canon/META 충돌 없음
  - [ ] META_AUDIT_LOG 사유 등록
  - [ ] 기존 Audit 형식과 호환

## Version Note

- v0.3.0: 다중 합의 규정 반영
- v0.3.1: 텍스트·메타데이터 정합성 보강
- v0.3.2: 문서-운영 규칙 정렬(upper gate / rollback / context_for_next 강조)
