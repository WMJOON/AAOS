---
description: cortex-agora 변경/비판/개선 인덱스(append-only). proposal별 최신 상태와 record_archive 봉인 참조를 추적한다.
---
# Cortex Agora Change Index

## Format

```yaml
---
timestamp: "YYYY-MM-DDTHH:MM:SSZ"
proposal_id: "P-..."
latest_status: "open|improving|closed|sealed"
latest_change_event_id: "ce_..."
feedback_count: 0
last_decision: "accepted|partially_accepted|deferred|rejected|none"
record_archive_package_ref: "_archive/operations/... (optional)"
---
```

---
timestamp: "GENESIS"
proposal_id: "GENESIS"
latest_status: "open"
latest_change_event_id: "GENESIS"
feedback_count: 0
last_decision: "none"
record_archive_package_ref: ""
---

---
timestamp: "2026-02-14T12:00:00Z"
proposal_id: "P-SWARM-V014-BATCH"
latest_status: "open"
latest_change_event_id: "ce_20260214T120000Z_swarm-v014-batch_created"
feedback_count: 0
last_decision: "none"
record_archive_package_ref: ""
---

---
timestamp: "2026-02-14T12:01:00Z"
proposal_id: "P-SWARM-V014-BATCH"
latest_status: "open"
latest_change_event_id: "ce_20260214T120000Z_swarm-v014-batch_created"
feedback_count: 1
last_decision: "none"
record_archive_package_ref: ""
---

---
timestamp: "2026-02-14T12:02:00Z"
proposal_id: "P-SWARM-V014-BATCH"
latest_status: "open"
latest_change_event_id: "ce_20260214T120000Z_swarm-v014-batch_created"
feedback_count: 2
last_decision: "none"
record_archive_package_ref: ""
---

---
timestamp: "2026-02-14T12:03:00Z"
proposal_id: "P-SWARM-V014-BATCH"
latest_status: "open"
latest_change_event_id: "ce_20260214T120000Z_swarm-v014-batch_created"
feedback_count: 3
last_decision: "none"
record_archive_package_ref: ""
---

---
timestamp: "2026-02-14T12:04:00Z"
proposal_id: "P-SWARM-V014-BATCH"
latest_status: "open"
latest_change_event_id: "ce_20260214T120000Z_swarm-v014-batch_created"
feedback_count: 4
last_decision: "none"
record_archive_package_ref: ""
---

---
timestamp: "2026-02-14T12:05:00Z"
proposal_id: "P-SWARM-V014-BATCH"
latest_status: "open"
latest_change_event_id: "ce_20260214T120000Z_swarm-v014-batch_created"
feedback_count: 5
last_decision: "none"
record_archive_package_ref: ""
---

---
timestamp: "2026-02-14T12:06:00Z"
proposal_id: "P-SWARM-V014-BATCH"
latest_status: "open"
latest_change_event_id: "ce_20260214T120000Z_swarm-v014-batch_created"
feedback_count: 6
last_decision: "none"
record_archive_package_ref: ""
---

---
timestamp: "2026-02-14T12:07:00Z"
proposal_id: "P-SWARM-V014-BATCH"
latest_status: "open"
latest_change_event_id: "ce_20260214T120000Z_swarm-v014-batch_created"
feedback_count: 7
last_decision: "none"
record_archive_package_ref: ""
---

---
timestamp: "2026-02-14T12:08:00Z"
proposal_id: "P-SWARM-V014-BATCH"
latest_status: "improving"
latest_change_event_id: "ce_20260214T120800Z_swarm-v014-batch_updated"
feedback_count: 7
last_decision: "none"
record_archive_package_ref: ""
---

---
timestamp: "2026-02-14T12:09:00Z"
proposal_id: "P-SWARM-V014-BATCH"
latest_status: "improving"
latest_change_event_id: "ce_20260214T120800Z_swarm-v014-batch_updated"
feedback_count: 7
last_decision: "accepted"
record_archive_package_ref: ""
---
