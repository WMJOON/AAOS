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
  - "04_Agentic_AI_OS/01_Nucleus/record_archive"
summary: "Record Archive filesystem scaffold created"
manifest_sha256: "GENESIS"
---

---
timestamp: "2026-01-24T00:05:27Z"
package_path: "_archive/snapshots/2026-01-24T000527Z__other__record-archive-critic/"
type: "other"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/record_archive"
summary: "Archive the initial Record Archive critique (root Critic removed; preserved as append-only package)"
manifest_sha256: "6162d75422b1255f2774a7ce91c606cc32b1e0f872c3f2176feab7dbf765cb6a"
notes: "payload/CRITIC.md"
---

---
timestamp: "2026-01-24T09:15:00Z"
package_path: "_archive/snapshots/2026-01-24T091500Z__doctrine-snapshot__record-archive-dna-v0.2.0/"
type: "doctrine-snapshot"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/record_archive/DNA_BLUEPRINT.md"
summary: "Record Archive DNA Blueprint v0.1.0 → v0.2.0 변경 증빙. 버킷별 보존 정책, 검증 도구, Deliberation 연계 절차 추가."
manifest_sha256: "d6f774526a3ac6c8d908b9719264bf37de090bf1842231da90192cd61c4d99ca"
notes: "첫 번째 정규 상위기관 변경 게이트 패키지"
---

---
timestamp: "2026-01-24T00:24:22Z"
package_path: "_archive/snapshots/2026-01-24T002422Z__doctrine-snapshot__record-archive-ledger-spec-v0.2.2/"
type: "doctrine-snapshot"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/record_archive/DNA_BLUEPRINT.md"
  - "04_Agentic_AI_OS/01_Nucleus/record_archive/scripts/ledger_keeper.py"
summary: "Record Archive v0.2.2: HASH_LEDGER hash 정의 고정 + 스크립트/문서 정합화 + snapshots 보존정책 조정."
manifest_sha256: "b9f961e3be46b04baa086da8bbdfc366ae0c30bff2f3e8f6bba2c9bc0ccb7783"
notes: "Ledger spec mismatch fix; includes DNA_BLUEPRINT, ledger_keeper, README, template snapshot"
---

---
timestamp: "2026-01-24T00:28:38Z"
package_path: "_archive/snapshots/2026-01-24T002838Z__doctrine-snapshot__record-archive-ledger-keeper-v0.2.3/"
type: "doctrine-snapshot"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/record_archive/scripts/ledger_keeper.py"
  - "04_Agentic_AI_OS/01_Nucleus/record_archive/templates/VERIFY_LEDGER_CHECKLIST.md"
  - "04_Agentic_AI_OS/01_Nucleus/record_archive/DNA_BLUEPRINT.md"
summary: "Record Archive v0.2.3: ledger_keeper 파서 강화 + --dry-run 추가 + timestamp 검증 완화."
manifest_sha256: "2ad17ef612f07453b38f9847bbe3cfb511c1ccb0a6c8e204804760f59c3026b1"
notes: "Follow-up hardening to prevent ledger pollution and wrong prev_hash."
---

---
timestamp: "2026-01-24T00:32:19Z"
package_path: "_archive/snapshots/2026-01-24T003219Z__doctrine-snapshot__record-archive-flagship-consensus-v0.2.4/"
type: "doctrine-snapshot"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/record_archive/DNA_BLUEPRINT.md"
  - "04_Agentic_AI_OS/01_Nucleus/record_archive/templates/DELIBERATION_PACKET_TEMPLATE.md"
summary: "Record Archive v0.2.4: DNA 승격/변경에 플래그십 Agent 2종 합의 규정 추가."
manifest_sha256: "23fa636b5923369591332d16259aa1e5ce8fe10e12c45ed084acb5511ec0c66e"
notes: "Adds Flagship Consensus gate aligned with Upper-Institution Change Gate."
---

---
timestamp: "2026-01-24T01:10:31Z"
package_path: "_archive/snapshots/2026-01-24T011031Z__promotion__record-archive-dna-v0.2.4/"
type: "doctrine-snapshot"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/record_archive/DNA.md"
  - "04_Agentic_AI_OS/01_Nucleus/record_archive/DNA_BLUEPRINT.md"
summary: "Record Archive DNA promotion: DNA_BLUEPRINT.md → DNA.md (v0.2.4)."
manifest_sha256: "f4fbfd452a1cfc31ef37e2e4ace49600e548b08e1eb7bd6ac8bbc60566b8225a"
notes: "Audit: 01_Nucleus/immune_system/AUDIT_LOG.md#2a1c26cbdd0a87a3"
---

---
timestamp: "2026-01-24T01:37:37Z"
package_path: "_archive/deliberation/2026-01-24T012500Z__deliberation__record-archive-v0.2.5/"
type: "deliberation-packet"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/record_archive/DNA.md"
  - "04_Agentic_AI_OS/01_Nucleus/record_archive/scripts/ledger_keeper.py"
summary: "Approval of Record Archive v0.2.5"
manifest_sha256: "a03991ad87619b32eccedd2f2457af863b0795ba40e95be07e9feb26b1ab8b66"
---

---
timestamp: "2026-01-24T02:39:44Z"
package_path: "_archive/audit-log/2026-01-24T023944Z__audit-snapshot__immune-audit-log/"
type: "audit-snapshot"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/immune_system/AUDIT_LOG.md"
summary: "Immune System AUDIT_LOG.md snapshot archived to Record Archive."
manifest_sha256: "1ce6d756875a878b07fae99ee70ae9883ba14cca8a648bc13d28998e9d9c732c"
notes: "Periodic snapshot; append-only"
---

---
timestamp: "2026-01-24T02:41:45Z"
package_path: "_archive/meta-audit-log/2026-01-24T024145Z__meta-audit-snapshot__immune-meta-audit-log/"
type: "meta-audit-snapshot"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/record_archive/_archive/meta-audit-log/META_AUDIT_LOG.md"
summary: "Immune System META_AUDIT_LOG.md snapshot archived to Record Archive."
manifest_sha256: "c95e0847727d41bc1c249693107ca3a245e230e110e4e81791776a4330b1bae7"
notes: "Periodic snapshot; append-only"
---

---
timestamp: "2026-02-14T04:54:43Z"
package_path: "_archive/deliberation/2026-02-14T144100Z__governance__workflow-orchestration-promotion/"
type: "governance"
targets:
  - "_archive/deliberation/2026-02-14T144100Z__governance__workflow-orchestration-promotion"
summary: "promote AGENTIC_WORKFLOW_ORCHESTRATION_BLUEPRINT.md to canonical AGENTIC_WORKFLOW_ORCHESTRATION.md"
manifest_sha256: "0fd414b6f207f17ad962e94ddd8e82e6d1633b91c0217d47583f6b12eb7c5d85"
notes: "ledger hash: 6b94ea889fc4f0ab5138c90809a0afdbd23a1aef6374744ab2be6e018e388fa3"
---

---
timestamp: "2026-02-14T04:55:30Z"
package_path: "_archive/deliberation/2026-02-14T144100Z__governance__workflow-orchestration-promotion/"
type: "governance"
targets:
  - "_archive/deliberation/2026-02-14T144100Z__governance__workflow-orchestration-promotion"
summary: "repair manifest hash consistency after correction"
manifest_sha256: "303f0baa297432f0184f4f9165f621cd091239650184162782da5863a506306f"
notes: "ledger hash: 0b741460168d5ebabd6a466b03e7598158ea241e2c54654319e42e0da458b02e"
---

---
timestamp: "2026-02-14T05:16:17Z"
package_path: "_archive/deliberation/2026-02-14T160700Z__governance__nucleus-provider-agnostic-workflow-enforcement/"
type: "governance"
targets:
  - "_archive/deliberation/2026-02-14T160700Z__governance__nucleus-provider-agnostic-workflow-enforcement"
summary: "seal issue governance package: ISSUE-NUC-20260214-0001"
manifest_sha256: "a5666a967084041eb771ac20797cebb0b8d0c5fe7ab0ddea948777ea549ccb4d"
notes: "ledger hash: ca16ecb5b233dc5edbb3df047de01212a3b06bbdba0442276a5cb96deada5aec"
---

---
timestamp: "2026-02-14T05:53:28Z"
package_path: "_archive/audit-log/2026-02-14T142200Z__audit-snapshot__immune-audit-log/"
type: "audit-snapshot"
targets:
  - "04_Agentic_AI_OS/01_Nucleus/immune_system/AUDIT_LOG.md"
summary: "Immune System AUDIT_LOG.md snapshot (01_Nucleus path)"
manifest_sha256: "e272ce83320056dd456c9e457c08114185440c5a6a137ad2805a76063fecbd81"
notes: "periodic snapshot after Nucleus path consolidation; ledger hash: 524d7c05254352e6e977c4473763e0dd260814182f3518aa30ee182b81490397"
---

---
timestamp: "2026-02-14T07:13:42Z"
package_path: "_archive/operations/20260214T071342Z__ops-supervision__swarm-manifestation/"
type: "ops-supervision"
targets:
  - "02_Swarm/"
  - "03_Manifestation/"
summary: "motor_cortex supervision cycle status=needs-improvement"
manifest_sha256: "f2e6541ae11410a17c0f303fcf1448bf8482ca3c076b24dc3f975e291149b3bd"
notes: "required_issues=1,recommendations=1,workflow_ok=True; ledger hash: 37c4669ea79de8c5c6dda68d8492e5ebe7ba22aae9a72db98bc573cd712c4712"
---

---
timestamp: "2026-02-14T07:29:24Z"
package_path: "_archive/deliberation/20260214T072907Z__governance__nucleus-outward-supervision-loop-deficit/"
type: "governance"
targets:
  - "01_Nucleus/deliberation_chamber/plans/2026-02-14__nucleus-outward-supervision-loop-deficit/"
summary: "outward supervision loop deficit seal"
manifest_sha256: "4749ef4cdae439392f81c307bf46717c1964fa372addebb20bbdc90ee169f955"
notes: "seal issue-issue: ISSUE-NUC-20260214-0002; ledger hash: a36592d0a6ed0932f15015cfd8d8e3423d62d7e898682b4718761c55a3a022ab"
---
