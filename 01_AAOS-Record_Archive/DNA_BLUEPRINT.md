---
name: "AAOS-Record-Archive"
version: "0.1.0"
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

## Directory Convention (recommended)

- `_archive/<target>/<timestamp>/...`
- `indexes/` (선택): 아카이브 목록, 해시/메타데이터 인덱스

## Version Note

- v0.1.0 : Record Archive System DNA Blueprint 최초 성문화
