# Change Summary (v0.2.2)

## Problem

- `HASH_LEDGER.md`의 `hash` 의미가 문서/체크리스트/스크립트 간에 불일치하여 검증 실패 및 운영 혼선 위험이 있었다.

## Decision

- `indexes/HASH_LEDGER.md`의 `hash`는 **`MANIFEST.sha256` 파일의 sha256** 로 고정한다.
- `prev_hash`는 직전 엔트리의 `hash`를 가리킨다.
- 체인 무결성은 “prev_hash 연결 + 각 MANIFEST 재해싱”으로 검증한다.

## Changes

- `scripts/ledger_keeper.py`: `hash=sha256(prev+manifest)` 방식을 제거하고, `hash=manifest_sha256`로 기록하도록 수정.
- `DNA_BLUEPRINT.md`: Hard Rules 번호 중복 수정, 디렉토리 컨벤션 명확화, snapshots 보존정책 10년으로 정합화.
- `README.md`: snapshots 보존 문구 정합화.
- `templates/ARCHIVE_PACKAGE_TEMPLATE.md`: `related_packages` 필드 추가(패키지 간 참조를 audit_refs와 분리).

