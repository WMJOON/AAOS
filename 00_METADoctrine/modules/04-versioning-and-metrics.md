---
name: aaos-meta-versioning-and-metrics
scope: "04_Agentic_AI_OS/00_METADoctrine/modules"
status: canonical
version: "0.2.0"
updated: "2026-02-14"
---

# Versioning and Metrics

## 버전 정책

- Core Doctrine 변경은 minor 이상으로 올린다.
- 게이트 규칙 변경은 반드시 Deliberation + Immune 승인 후 반영한다.

## 헬스 메트릭

필수:
1. `motor_cortex/scripts/nucleus_ops.py health`가 `critical_ok: YES`
2. `cross_ref_validator` broken links 0
3. Skills frontmatter 규범 위반 0
4. Canonical frontmatter hygiene 위반 0

## 운영 보고

- 변경 후 `record_archive`에 증빙 패키지 봉인
- `record_archive/_archive/audit-log/AUDIT_LOG.md`, `record_archive/_archive/meta-audit-log/META_AUDIT_LOG.md` 교차참조 기록
