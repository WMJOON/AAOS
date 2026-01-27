---
timestamp: "YYYY-MM-DDTHH:MM:SSZ"
package_id: "YYYY-MM-DDTHHMMSSZ__<type>__<slug>"
type: "audit-snapshot | meta-audit-snapshot | deliberation-consensus | approval-signature | doctrine-snapshot | other"
status: "sealed" # sealed, pending, disputed

source_refs:
  - "absolute/or/vault-relative/path"

targets:
  - "path/or/id"

audit_refs:
  - "04_Agentic_AI_OS/01_Nucleus/Immune_system/AUDIT_LOG.md#<entry-hash-or-timestamp>"
  - "04_Agentic_AI_OS/01_Nucleus/Immune_system/META_AUDIT_LOG.md#<entry-id>"

related_packages:
  - "_archive/<bucket>/<timestamp>__<type>__<slug>/"

integrity:
  manifest: "MANIFEST.sha256"
  manifest_sha256: "<fill after generating>"

created_by:
  actor: "<agent-name-or-human>"
  method: "manual | tool"

notes: "optional"
---
# Archive Package

## Summary

- Why this package exists:
- What it proves:
- What can be reproduced from it:

## Contents

- `payload/` :
- `MANIFEST.sha256` :
