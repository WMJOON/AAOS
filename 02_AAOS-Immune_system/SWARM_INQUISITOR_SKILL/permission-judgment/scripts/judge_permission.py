#!/usr/bin/env python3
"""
Permission Request 검증 (Permission Principal Doctrine)

Usage:
  python3 judge_permission.py <permission_request.md> [--audit <audit_log_path>]

Minimal required frontmatter keys:
  - type, created, requester, action, target, risk_level, justification
  - time_bound.expires
  - natural_dissolution.termination_conditions
  - natural_dissolution.dissolution_steps
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from _shared.yaml_validator import validate_permission_request
from _shared.audit import safe_append_audit_entry, utc_now_iso, verify_audit_integrity


def default_audit_path() -> Path:
    immune_root = Path(__file__).resolve().parents[3]
    return (immune_root / "AUDIT_LOG.md").resolve()

def main() -> int:
    parser = argparse.ArgumentParser(description="Judge a permission request")
    parser.add_argument("request_md", help="Permission request markdown with YAML frontmatter")
    parser.add_argument("--audit", default=None, help="Audit log path (default: 02_AAOS-Immune_system/AUDIT_LOG.md)")
    parser.add_argument("--no-audit", action="store_true", help="Do not write audit log")
    parser.add_argument("--force-audit", action="store_true", help="Append audit log even if integrity verification fails")
    args = parser.parse_args()

    request_path = Path(args.request_md).expanduser().resolve()
    audit_path = Path(args.audit).expanduser().resolve() if args.audit else default_audit_path()

    result, reasons = validate_permission_request(request_path)

    print(f"Request: {request_path}")
    print(f"Result: {result}")
    if reasons:
        print("\nNotes:")
        for r in reasons:
            print(f"  - {r}")

    if not args.no_audit:
        if audit_path.exists() and not args.force_audit:
            ok, errors = verify_audit_integrity(audit_path)
            if not ok:
                print("ERROR: Audit log integrity violation detected; refusing to append.", file=sys.stderr)
                for e in errors:
                    print(f"  - {e}", file=sys.stderr)
                return 1

        safe_append_audit_entry(
            audit_path=audit_path,
            entry={
                "timestamp": utc_now_iso(),
                "type": "permission-judgment",
                "target": str(request_path),
                "result": result,
                "reasons": reasons or ["OK"],
                "notes": "",
            },
            require_integrity=not args.force_audit,
        )

    if result == "Canonical":
        return 0
    if result == "Canonical-Conditional":
        return 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
