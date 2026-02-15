---
description: Record Archive 패키지 무결성 해시 원장(추가만). prev_hash → hash 체인으로 변조 감지를 강화한다.
---
# Record Archive Hash Ledger

## Format (권장)

```yaml
---
timestamp: "YYYY-MM-DDTHH:MM:SSZ"
package_path: "_archive/<bucket>/<timestamp>__<type>__<slug>/"
artifact: "MANIFEST.sha256"
prev_hash: "<previous ledger hash>"
hash: "<current ledger hash>"
notes: "optional"
---
```

---
timestamp: "GENESIS"
package_path: "_archive/"
artifact: "MANIFEST.sha256"
prev_hash: "GENESIS"
hash: "GENESIS"
---

---
timestamp: "2026-01-24T00:05:27Z"
package_path: "_archive/snapshots/2026-01-24T000527Z__other__record-archive-critic/"
artifact: "MANIFEST.sha256"
prev_hash: "GENESIS"
hash: "6162d75422b1255f2774a7ce91c606cc32b1e0f872c3f2176feab7dbf765cb6a"
notes: "Ledger hash uses MANIFEST.sha256 file sha256"
---

---
timestamp: "2026-01-24T09:15:00Z"
package_path: "_archive/snapshots/2026-01-24T091500Z__doctrine-snapshot__record-archive-dna-v0.2.0/"
artifact: "MANIFEST.sha256"
prev_hash: "6162d75422b1255f2774a7ce91c606cc32b1e0f872c3f2176feab7dbf765cb6a"
hash: "d6f774526a3ac6c8d908b9719264bf37de090bf1842231da90192cd61c4d99ca"
notes: "Record Archive DNA v0.2.0 doctrine snapshot"
---

---
timestamp: "2026-01-24T00:25:04Z"
package_path: "_archive/snapshots/2026-01-24T002422Z__doctrine-snapshot__record-archive-ledger-spec-v0.2.2/"
artifact: "MANIFEST.sha256"
prev_hash: "d6f774526a3ac6c8d908b9719264bf37de090bf1842231da90192cd61c4d99ca"
hash: "b9f961e3be46b04baa086da8bbdfc366ae0c30bff2f3e8f6bba2c9bc0ccb7783"
notes: "Record Archive ledger spec v0.2.2: align hash definition + docs"
---

---
timestamp: "2026-01-24T00:29:19Z"
package_path: "_archive/snapshots/2026-01-24T002838Z__doctrine-snapshot__record-archive-ledger-keeper-v0.2.3/"
artifact: "MANIFEST.sha256"
prev_hash: "b9f961e3be46b04baa086da8bbdfc366ae0c30bff2f3e8f6bba2c9bc0ccb7783"
hash: "2ad17ef612f07453b38f9847bbe3cfb511c1ccb0a6c8e204804760f59c3026b1"
notes: "Record Archive ledger keeper v0.2.3: parser hardening + dry-run"
---

---
timestamp: "2026-01-24T00:33:02Z"
package_path: "_archive/snapshots/2026-01-24T003219Z__doctrine-snapshot__record-archive-flagship-consensus-v0.2.4/"
artifact: "MANIFEST.sha256"
prev_hash: "2ad17ef612f07453b38f9847bbe3cfb511c1ccb0a6c8e204804760f59c3026b1"
hash: "23fa636b5923369591332d16259aa1e5ce8fe10e12c45ed084acb5511ec0c66e"
notes: "Record Archive v0.2.4: flagship consensus gate for DNA promotion"
---

---
timestamp: "2026-01-24T01:11:50Z"
package_path: "_archive/snapshots/2026-01-24T011031Z__promotion__record-archive-dna-v0.2.4/"
artifact: "MANIFEST.sha256"
prev_hash: "23fa636b5923369591332d16259aa1e5ce8fe10e12c45ed084acb5511ec0c66e"
hash: "f4fbfd452a1cfc31ef37e2e4ace49600e548b08e1eb7bd6ac8bbc60566b8225a"
notes: "Record Archive DNA promotion: DNA_BLUEPRINT → DNA.md (v0.2.4)"
---

---
timestamp: "2026-01-24T01:37:37Z"
package_path: "_archive/deliberation/2026-01-24T012500Z__deliberation__record-archive-v0.2.5/"
artifact: "MANIFEST.sha256"
prev_hash: "f4fbfd452a1cfc31ef37e2e4ace49600e548b08e1eb7bd6ac8bbc60566b8225a"
hash: "6c38315a087c17f61a14c8f04b4712ad6adf5b39e427ce8cbbcfcd8d1700ca04"
notes: "Approval of Record Archive v0.2.5"
---

---
timestamp: "2026-01-24T02:40:27Z"
package_path: "_archive/audit-log/2026-01-24T023944Z__audit-snapshot__immune-audit-log/"
artifact: "MANIFEST.sha256"
prev_hash: "6c38315a087c17f61a14c8f04b4712ad6adf5b39e427ce8cbbcfcd8d1700ca04"
hash: "b2c7d0430f2eae40cbaba9caaf94c75ada4022395b555246ff4bbd5e11003898"
notes: "Immune System AUDIT_LOG snapshot"
---

---
timestamp: "2026-01-24T02:42:19Z"
package_path: "_archive/meta-audit-log/2026-01-24T024145Z__meta-audit-snapshot__immune-meta-audit-log/"
artifact: "MANIFEST.sha256"
prev_hash: "b2c7d0430f2eae40cbaba9caaf94c75ada4022395b555246ff4bbd5e11003898"
hash: "8ca43b65a5caab37687e2f711acb09b8c4dc7c49a4aa46f3490aac80bc4cf787"
notes: "Immune System META_AUDIT_LOG snapshot"
---

---
timestamp: "2026-02-14T00:00:00Z"
package_path: "_archive/"
artifact: "CHAIN_MIGRATION.marker"
prev_hash: "8ca43b65a5caab37687e2f711acb09b8c4dc7c49a4aa46f3490aac80bc4cf787"
hash: "209a8f26daf7eb5fea2a6a3669494c1f0c4e2a5a9707599995c8e9ec215440bc"
notes: "CHAIN MIGRATION: legacy manifest-only hashes prior to this entry; chain hashes (prev_hash + manifest) apply from here."
---

---
timestamp: "2026-02-14T04:54:43Z"
package_path: "_archive/deliberation/2026-02-14T144100Z__governance__workflow-orchestration-promotion/"
artifact: "MANIFEST.sha256"
prev_hash: "209a8f26daf7eb5fea2a6a3669494c1f0c4e2a5a9707599995c8e9ec215440bc"
hash: "6b94ea889fc4f0ab5138c90809a0afdbd23a1aef6374744ab2be6e018e388fa3"
notes: "promote AGENTIC_WORKFLOW_ORCHESTRATION_BLUEPRINT.md to canonical AGENTIC_WORKFLOW_ORCHESTRATION.md"
---

---
timestamp: "2026-02-14T04:55:30Z"
package_path: "_archive/deliberation/2026-02-14T144100Z__governance__workflow-orchestration-promotion/"
artifact: "MANIFEST.sha256"
prev_hash: "6b94ea889fc4f0ab5138c90809a0afdbd23a1aef6374744ab2be6e018e388fa3"
hash: "0b741460168d5ebabd6a466b03e7598158ea241e2c54654319e42e0da458b02e"
notes: "repair manifest hash consistency after correction"
---

---
timestamp: "2026-02-14T05:16:17Z"
package_path: "_archive/deliberation/2026-02-14T160700Z__governance__nucleus-provider-agnostic-workflow-enforcement/"
artifact: "MANIFEST.sha256"
prev_hash: "0b741460168d5ebabd6a466b03e7598158ea241e2c54654319e42e0da458b02e"
hash: "ca16ecb5b233dc5edbb3df047de01212a3b06bbdba0442276a5cb96deada5aec"
notes: "seal issue governance package: ISSUE-NUC-20260214-0001"
---

---
timestamp: "2026-02-14T05:53:28Z"
package_path: "_archive/audit-log/2026-02-14T142200Z__audit-snapshot__immune-audit-log/"
artifact: "MANIFEST.sha256"
prev_hash: "ca16ecb5b233dc5edbb3df047de01212a3b06bbdba0442276a5cb96deada5aec"
hash: "524d7c05254352e6e977c4473763e0dd260814182f3518aa30ee182b81490397"
notes: "periodic snapshot after Nucleus path consolidation"
---

---
timestamp: "2026-02-14T07:13:42Z"
package_path: "_archive/operations/20260214T071342Z__ops-supervision__swarm-manifestation/"
artifact: "MANIFEST.sha256"
prev_hash: "524d7c05254352e6e977c4473763e0dd260814182f3518aa30ee182b81490397"
hash: "37c4669ea79de8c5c6dda68d8492e5ebe7ba22aae9a72db98bc573cd712c4712"
notes: "required_issues=1,recommendations=1,workflow_ok=True"
---

---
timestamp: "2026-02-14T07:29:24Z"
package_path: "_archive/deliberation/20260214T072907Z__governance__nucleus-outward-supervision-loop-deficit/"
artifact: "MANIFEST.sha256"
prev_hash: "37c4669ea79de8c5c6dda68d8492e5ebe7ba22aae9a72db98bc573cd712c4712"
hash: "a36592d0a6ed0932f15015cfd8d8e3423d62d7e898682b4718761c55a3a022ab"
notes: "seal issue-issue: ISSUE-NUC-20260214-0002"
---

---
timestamp: "2026-02-15T08:04:40Z"
package_path: "_archive/operations/20260215T080440Z__swarm-observability__cortex-agora-change-review/"
artifact: "MANIFEST.sha256"
prev_hash: "a36592d0a6ed0932f15015cfd8d8e3423d62d7e898682b4718761c55a3a022ab"
hash: "9bc497270aeeabd972d5979395e13012e7129b0e6031e902b1e9b1cbd28bd619"
notes: "Full governance 3-phase passed; proposal closed"
---
