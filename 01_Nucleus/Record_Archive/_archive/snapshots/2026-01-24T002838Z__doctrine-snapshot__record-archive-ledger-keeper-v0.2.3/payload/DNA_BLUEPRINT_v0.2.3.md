---
name: "AAOS-Record-Archive"
version: "0.2.3"
scope: "04_Agentic_AI_OS/01_AAOS-Record_Archive"
owner: "AAOS Canon"
created: "2026-01-22"
status: canonical

# Governance (homing instinct)
governance:
  voice: homing_instinct
  mother_ref: "04_Agentic_AI_OS/METADoctrine.md"
  sibling_ref: "04_Agentic_AI_OS/02_AAOS-Immune_system/"
  precedence:
    - "AAOS Canon"
    - "Record Archive"
    - "META Doctrine"
    - "Immune Doctrine"
    - "This document"
  on_conflict: "halt_then_home_to_meta_doctrine"

# Normative References (inherit Immune System)
canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/METADoctrine.md"
immune_doctrine_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/AAOS_DNA_DOCTRINE_RULE.md"
inquisitor_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/AUDIT_LOG.md"
meta_audit_log_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/META_AUDIT_LOG.md"

natural_dissolution:
  purpose: "AAOS의 감사/합의/승인/해체 기록을 장기 보존 가능한 형태로 아카이빙하고, 정통성 분쟁 시 근거를 재현 가능하게 제공한다"
  termination_conditions:
    - "상위 META Doctrine이 Record Archive의 역할을 다른 기관으로 이관할 때"
    - "AAOS Canon이 폐기되거나 대체될 때"
  dissolution_steps:
    - "archive index를 요약본으로 고정하고, 아카이브 무결성 해시를 기록한다"
    - "활성 인덱스를 읽기 전용 스냅샷으로 변환한다"
    - "후속 Archive 기관으로 경로/권한을 이관한다"
  retention:
    summary_required: true
    max_days: 3650

resource_limits:
  max_files: 5000
  max_folders: 500
  max_log_kb: 4096

# Bucket-specific Retention Policies
bucket_policies:
  audit-log:
    description: "Immune System AUDIT_LOG.md 스냅샷"
    retention_days: 1825  # 5년
    max_packages: 500
    compression_trigger_kb: 256
    priority: critical
  meta-audit-log:
    description: "META_AUDIT_LOG.md 스냅샷 (상위기관 변경)"
    retention_days: 3650  # 10년
    max_packages: 200
    compression_trigger_kb: 256
    priority: critical
  deliberation:
    description: "Deliberation Chamber 합의 산출물"
    retention_days: 1095  # 3년
    max_packages: 1000
    compression_trigger_kb: 128
    priority: high
  approvals:
    description: "인간 승인(서명) 기록"
    retention_days: 3650  # 10년 (법적 증빙 가능성)
    max_packages: 500
    compression_trigger_kb: 64
    priority: critical
  snapshots:
    description: "Canon/META/DNA 스냅샷"
    retention_days: 3650  # 10년 (필요 시 요약 패키지로 갱신)
    max_packages: 200
    compression_trigger_kb: 512
    priority: critical
  disputed:
    description: "분쟁/격리 패키지 (검증 실패 시)"
    retention_days: 365   # 분쟁 해결 후 재분류
    max_packages: 50
    compression_trigger_kb: 128
    priority: high

inquisitor:
  required: true
  audit_log: "../02_AAOS-Immune_system/AUDIT_LOG.md"
---

# AAOS Record Archive System (DNA Blueprint)

## Overview

Record Archive System은 AAOS의 “기억(기록)”을 보존하는 기관이다.
면역체계가 판정과 집행을 담당한다면, Archive는 그 판정의 근거와 계보를 장기 보존 가능한 형태로 남긴다.

## What it stores

- `AUDIT_LOG.md` / `META_AUDIT_LOG.md`의 장기 보존 스냅샷(필요 시 분할/압축)
- Multi-Agent 합의 증빙(스키마 엔트리, 근거 요약)
- Natural Dissolution 실행의 요약본(해체 사유, 결과, 아카이브 경로)

## Operating Principles

- Append-only: 원본 기록을 “수정”하지 않고, 추가 기록으로만 보존한다.
- Reproducibility: 정통성 판정의 근거가 재현 가능해야 한다.
- Homing Instinct: 충돌/불명확/권한 경계 감지 시 META Doctrine(METADoctrine.md)으로 귀속하고, 심판/집행은 Immune System(Inquisitor)로 요청한다.
- Anchor Safety: Audit Log의 앵커(초기 신뢰점) 분쟁을 줄이기 위해, 주기적 스냅샷/해시/인덱스를 남겨 “외부 고정(미러링)”을 가능하게 한다.

## Hard Rules (MUST)

1. **Tool-Mediated Ledger (v0.2.2+)**
   - `HASH_LEDGER.md` 업데이트는 반드시 `scripts/ledger_keeper.py`를 통해 수행되어야 한다.
   - 수동 문자열 편집은 비정상 조작으로 간주한다.
2. **Append-only**
   - 패키지/인덱스/원장은 “수정 금지, 추가만 허용”이 기본값이다.
3. **패키지 단위 보존**
   - 모든 증빙은 `_archive/` 아래 “패키지 폴더 1개”로 고정한다.
4. **무결성 파일 필수**
   - 모든 패키지는 `MANIFEST.sha256`를 포함해야 한다(패키지 내 파일의 sha256 목록).
5. **참조 관계 명시**
   - 모든 패키지는 `PACKAGE.md`에 `source_refs`(원본 경로)와 `audit_refs`(AUDIT_LOG/META_AUDIT_LOG 엔트리 참조)를 포함한다.
6. **충돌 시 중단 + 귀속**
   - 작성/검증 단계에서 불명확/권한 경계/충돌이 감지되면, 즉시 중단하고 Immune System(Inquisitor)로 귀속한다.

## Directory Convention (standard)

- `_archive/<bucket>/<timestamp>__<type>__<slug>/...`
- `indexes/` : 아카이브 목록/해시 원장 (append-only)
- `templates/` : 패키지/매니페스트/합의 패킷 템플릿

권장 버킷(고정):

- `_archive/audit-log/` : Immune System 감사 로그 스냅샷 (5년 보존)
- `_archive/meta-audit-log/` : META 감사 로그 스냅샷 (10년 보존)
- `_archive/deliberation/` : Deliberation Chamber 합의 산출물 (3년 보존)
- `_archive/approvals/` : 인간 승인/서명 기록 (10년 보존)
- `_archive/snapshots/` : Canon/META/기관 DNA 스냅샷 (10년 보존; 필요 시 요약 패키지로 갱신)
- `_archive/disputed/` : 분쟁/격리 패키지 (해결 시까지)

## Archive Package Spec (minimum)

패키지 폴더명:

- `<YYYY-MM-DDTHHMMSSZ>__<type>__<slug>/`

패키지 최소 구성:

- `PACKAGE.md` (메타데이터; `templates/ARCHIVE_PACKAGE_TEMPLATE.md` 기반)
- `MANIFEST.sha256` (sha256 목록; `templates/MANIFEST_SHA256_TEMPLATE.txt` 참고)
- `payload/` (증빙 파일들)

## Index & Hash Ledger (append-only)

- `indexes/ARCHIVE_INDEX.md`
  - 사람이 찾는 목록(패키지 경로, 타입, 대상, 요약, 매니페스트 해시)
- `indexes/HASH_LEDGER.md`
  - `prev_hash` → `hash` 체인으로 패키지 무결성 해시를 연결
  - `hash`는 `MANIFEST.sha256` 파일의 sha256 이다.

## Upper-Institution Change Gate (Record Archive duties)

다음 변경은 “상위기관 변경 게이트”로 취급하며, Record Archive는 최소 1개 이상의 패키지를 생성해 증빙을 고정해야 한다.

- Canon: `04_Agentic_AI_OS/README.md`
- META Doctrine: `04_Agentic_AI_OS/METADoctrine.md`
- 기관 DNA(Record Archive/Immune/Deliberation), Swarm 루트 DNA

패키지에 포함해야 하는 최소 증빙:

- 변경 전/후 스냅샷(대상 파일)
- Deliberation 합의 요약 + 근거 링크
- Immune System 판정/승인 참조(감사 로그 엔트리 또는 해시)
- `MANIFEST.sha256` 및 해시 원장 엔트리

## Version Note

- v0.1.0 : Record Archive System DNA Blueprint 최초 성문화
- v0.2.0 : 버킷별 보존 정책(retention policy) 추가, disputed 버킷 신설, 검증 체크리스트 추가, Deliberation 연계 워크플로우 명시
- v0.2.1 : `ledger_keeper.py` 기반 HASH_LEDGER 자동화 강제, 수동 편집 금지 조항 추가
- v0.2.2 : HASH_LEDGER `hash` 정의를 `MANIFEST.sha256` 파일 sha256로 고정하고, 스크립트/문서 정합화. snapshots 보존 정책을 10년으로 조정.
- v0.2.3 : ledger_keeper가 코드펜스 예시를 무시하도록 파서 강화, `--dry-run` 추가, timestamp 검증을 분쟁 처리로 완화.
