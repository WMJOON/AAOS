---
type: procedure
status: draft
created: "2026-01-24T01:16:37Z"
---
# Seal → Archive Procedure (Flagship Consensus)

## Goal

플래그십 Agent 2종 verdict/rationale가 채워진 `DELIBERATION_PACKET.md`를 Record Archive의 `_archive/deliberation/` 버킷에 **sealed 패키지**로 고정한다.

## Steps

1. `DELIBERATION_PACKET.md`의 `status`를 `submitted`로 변경한다.
2. 아래 패키지 폴더를 생성한다.

`04_Agentic_AI_OS/01_Nucleus/record_archive/_archive/deliberation/<timestamp>__deliberation-consensus__record-archive-dna-v0.2.4-flagship/`

3. `payload/DELIBERATION_PACKET.md`로 복사하고, `payload/EVIDENCE.md`도 함께 포함한다.
4. `templates/ARCHIVE_PACKAGE_TEMPLATE.md`로 `PACKAGE.md`를 생성해 `audit_refs`에 `AUDIT_LOG.md#2a1c26cbdd0a87a3`를 포함한다.
5. `MANIFEST.sha256`를 만들고, `scripts/ledger_keeper.py <package_path> "<notes>"`로 `HASH_LEDGER.md`에 체인을 연결한다.
6. `indexes/ARCHIVE_INDEX.md`에 엔트리를 추가한다.
7. Inquisitor에 “조건부 해제(Canonical)” 심판을 요청하고, 결과를 `AUDIT_LOG.md`에 남긴다.

