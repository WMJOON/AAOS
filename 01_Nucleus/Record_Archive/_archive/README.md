# _archive/

이 폴더는 Record Archive의 “실제 패키지 저장소”이다.

- 규칙: append-only (수정 금지, 추가만 허용)
- 패키지: `_archive/<bucket>/<timestamp>__<type>__<slug>/`
- 최소 구성: `PACKAGE.md` + `MANIFEST.sha256` + `payload/`

버킷별 목적:

- `audit-log/` : `AUDIT_LOG.md` 스냅샷
- `meta-audit-log/` : `META_AUDIT_LOG.md` 스냅샷
- `deliberation/` : Multi-Agent 합의/숙의 패킷
- `approvals/` : Canon Guardian 서명(정식 승격) 증빙
- `snapshots/` : Canon/META/기관 DNA 등 상위 변경 스냅샷

