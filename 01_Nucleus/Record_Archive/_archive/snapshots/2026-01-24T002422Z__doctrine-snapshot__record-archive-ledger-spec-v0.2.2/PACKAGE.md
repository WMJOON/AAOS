---
timestamp: "2026-01-24T00:24:22Z"
package_id: "2026-01-24T002422Z__doctrine-snapshot__record-archive-ledger-spec-v0.2.2"
type: "doctrine-snapshot"
status: "sealed"

source_refs:
  - "04_Agentic_AI_OS/01_AAOS-Record_Archive/DNA_BLUEPRINT.md"
  - "04_Agentic_AI_OS/01_AAOS-Record_Archive/scripts/ledger_keeper.py"
  - "04_Agentic_AI_OS/01_AAOS-Record_Archive/templates/ARCHIVE_PACKAGE_TEMPLATE.md"
  - "04_Agentic_AI_OS/01_AAOS-Record_Archive/README.md"

targets:
  - "04_Agentic_AI_OS/01_AAOS-Record_Archive"

audit_refs: []

related_packages:
  - "_archive/snapshots/2026-01-24T091500Z__doctrine-snapshot__record-archive-dna-v0.2.0/"

integrity:
  manifest: "MANIFEST.sha256"
  manifest_sha256: "b9f961e3be46b04baa086da8bbdfc366ae0c30bff2f3e8f6bba2c9bc0ccb7783"

created_by:
  actor: "codex"
  method: "manual"

change_summary:
  to_version: "0.2.2"
  changes:
    - "HASH_LEDGER의 `hash`를 MANIFEST.sha256 파일 sha256로 정의 고정"
    - "ledger_keeper.py가 동일 정의를 따르도록 수정"
    - "README/DNA_BLUEPRINT 문구 정합화 및 Hard Rules 번호 수정"
    - "snapshots 버킷 보존정책을 10년으로 조정(요약 패키지로 갱신)"
---
# Archive Package: Record Archive Ledger Spec v0.2.2

## Summary

- Purpose: Ledger 정의/스크립트/문서 불일치 해소 및 운영 규칙 정합화.
- Evidence: payload에 변경된 핵심 파일 스냅샷을 포함.
