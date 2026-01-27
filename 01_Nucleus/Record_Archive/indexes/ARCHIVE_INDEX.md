---
description: Record Archive 패키지 인덱스(추가만). 패키지 경로/타입/대상/요약/무결성 참조를 제공한다.
---
# Record Archive Index

## Format (권장)

```yaml
---
timestamp: "YYYY-MM-DDTHH:MM:SSZ"
package_path: "_archive/<bucket>/<timestamp>__<type>__<slug>/"
type: "audit-snapshot | meta-audit-snapshot | deliberation-consensus | approval-signature | doctrine-snapshot | other"
targets:
  - "path/or/id"
summary: "1-2 lines"
manifest_sha256: "<sha256 of MANIFEST.sha256 content or file hash>"
notes: "optional"
---
```

---
timestamp: "GENESIS"
package_path: "_archive/"
type: "other"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/Record_Archive"
summary: "Record Archive filesystem scaffold created"
manifest_sha256: "GENESIS"
---

---
timestamp: "2026-01-24T00:05:27Z"
package_path: "_archive/snapshots/2026-01-24T000527Z__other__record-archive-critic/"
type: "other"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/Record_Archive"
summary: "Archive the initial Record Archive critique (root Critic removed; preserved as append-only package)"
manifest_sha256: "6162d75422b1255f2774a7ce91c606cc32b1e0f872c3f2176feab7dbf765cb6a"
notes: "payload/CRITIC.md"
---

---
timestamp: "2026-01-24T09:15:00Z"
package_path: "_archive/snapshots/2026-01-24T091500Z__doctrine-snapshot__record-archive-dna-v0.2.0/"
type: "doctrine-snapshot"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/Record_Archive/DNA_BLUEPRINT.md"
summary: "Record Archive DNA Blueprint v0.1.0 → v0.2.0 변경 증빙. 버킷별 보존 정책, 검증 도구, Deliberation 연계 절차 추가."
manifest_sha256: "d6f774526a3ac6c8d908b9719264bf37de090bf1842231da90192cd61c4d99ca"
notes: "첫 번째 정규 상위기관 변경 게이트 패키지"
---

---
timestamp: "2026-01-24T00:24:22Z"
package_path: "_archive/snapshots/2026-01-24T002422Z__doctrine-snapshot__record-archive-ledger-spec-v0.2.2/"
type: "doctrine-snapshot"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/Record_Archive/DNA_BLUEPRINT.md"
  - "04_Agentic_AI_OS/01_Nucleus/Record_Archive/scripts/ledger_keeper.py"
summary: "Record Archive v0.2.2: HASH_LEDGER hash 정의 고정 + 스크립트/문서 정합화 + snapshots 보존정책 조정."
manifest_sha256: "b9f961e3be46b04baa086da8bbdfc366ae0c30bff2f3e8f6bba2c9bc0ccb7783"
notes: "Ledger spec mismatch fix; includes DNA_BLUEPRINT, ledger_keeper, README, template snapshot"
---

---
timestamp: "2026-01-24T00:28:38Z"
package_path: "_archive/snapshots/2026-01-24T002838Z__doctrine-snapshot__record-archive-ledger-keeper-v0.2.3/"
type: "doctrine-snapshot"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/Record_Archive/scripts/ledger_keeper.py"
  - "04_Agentic_AI_OS/01_Nucleus/Record_Archive/templates/VERIFY_LEDGER_CHECKLIST.md"
  - "04_Agentic_AI_OS/01_Nucleus/Record_Archive/DNA_BLUEPRINT.md"
summary: "Record Archive v0.2.3: ledger_keeper 파서 강화 + --dry-run 추가 + timestamp 검증 완화."
manifest_sha256: "2ad17ef612f07453b38f9847bbe3cfb511c1ccb0a6c8e204804760f59c3026b1"
notes: "Follow-up hardening to prevent ledger pollution and wrong prev_hash."
---

---
timestamp: "2026-01-24T00:32:19Z"
package_path: "_archive/snapshots/2026-01-24T003219Z__doctrine-snapshot__record-archive-flagship-consensus-v0.2.4/"
type: "doctrine-snapshot"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/Record_Archive/DNA_BLUEPRINT.md"
  - "04_Agentic_AI_OS/01_Nucleus/Record_Archive/templates/DELIBERATION_PACKET_TEMPLATE.md"
summary: "Record Archive v0.2.4: DNA 승격/변경에 플래그십 Agent 2종 합의 규정 추가."
manifest_sha256: "23fa636b5923369591332d16259aa1e5ce8fe10e12c45ed084acb5511ec0c66e"
notes: "Adds Flagship Consensus gate aligned with Upper-Institution Change Gate."
---

---
timestamp: "2026-01-24T01:10:31Z"
package_path: "_archive/snapshots/2026-01-24T011031Z__promotion__record-archive-dna-v0.2.4/"
type: "doctrine-snapshot"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/Record_Archive/DNA.md"
  - "04_Agentic_AI_OS/01_Nucleus/Record_Archive/DNA_BLUEPRINT.md"
summary: "Record Archive DNA promotion: DNA_BLUEPRINT.md → DNA.md (v0.2.4)."
manifest_sha256: "f4fbfd452a1cfc31ef37e2e4ace49600e548b08e1eb7bd6ac8bbc60566b8225a"
notes: "Audit: 01_Nucleus/Immune_system/AUDIT_LOG.md#2a1c26cbdd0a87a3"
---

---
timestamp: "2026-01-24T02:39:44Z"
package_path: "_archive/audit-log/2026-01-24T023944Z__audit-snapshot__immune-audit-log/"
type: "audit-snapshot"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/Immune_system/AUDIT_LOG.md"
summary: "Immune System AUDIT_LOG.md snapshot archived to Record Archive."
manifest_sha256: "1ce6d756875a878b07fae99ee70ae9883ba14cca8a648bc13d28998e9d9c732c"
notes: "Periodic snapshot; append-only"
---

---
timestamp: "2026-01-24T02:41:45Z"
package_path: "_archive/meta-audit-log/2026-01-24T024145Z__meta-audit-snapshot__immune-meta-audit-log/"
type: "meta-audit-snapshot"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/Immune_system/META_AUDIT_LOG.md"
summary: "Immune System META_AUDIT_LOG.md snapshot archived to Record Archive."
manifest_sha256: "c95e0847727d41bc1c249693107ca3a245e230e110e4e81791776a4330b1bae7"
notes: "Periodic snapshot; append-only"
---

---
timestamp: "2026-01-24T01:37:37Z"
package_path: "_archive/deliberation/2026-01-24T012500Z__deliberation__record-archive-v0.2.5/"
type: "deliberation-packet"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/Record_Archive/DNA.md"
  - "04_Agentic_AI_OS/01_Nucleus/Record_Archive/scripts/ledger_keeper.py"
summary: "Approval of Record Archive v0.2.5"
manifest_sha256: "a03991ad87619b32eccedd2f2457af863b0795ba40e95be07e9feb26b1ab8b66"
---
