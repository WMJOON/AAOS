---
status: frozen
frozen_at: "2026-02-15"
replaced_by:
  change_events: "02_Swarm/cortex-agora/records/change_events/"
  peer_feedback: "02_Swarm/cortex-agora/records/peer_feedback/"
  improvement_decisions: "02_Swarm/cortex-agora/records/improvement_decisions/"
migration_script: "02_Swarm/cortex-agora/scripts/migrate_jsonl_to_md.py"
---
# DEPRECATED

이 디렉토리의 JSONL 파일들은 동결(frozen) 상태입니다.

- `CHANGE_EVENTS.jsonl` → `records/change_events/*.md`
- `PEER_FEEDBACK.jsonl` → `records/peer_feedback/*.md`
- `IMPROVEMENT_DECISIONS.jsonl` → `records/improvement_decisions/*.md`

신규 레코드는 `records/` 하위에 개별 `.md` 파일로 기록합니다.
`change_archive_bridge.py`가 자동으로 `record_writer.py`를 사용합니다.
