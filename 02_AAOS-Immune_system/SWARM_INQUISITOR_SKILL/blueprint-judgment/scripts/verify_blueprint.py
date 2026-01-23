#!/usr/bin/env python3
"""
DNA Blueprint 검증 (Canonicality 판정)

Usage:
  python3 verify_blueprint.py <target_path> [--blueprint AUTO|DNA.md|DNA_BLUEPRINT.md] [--audit <audit_log_path>]

Rules (minimal):
  - Blueprint file must exist
  - 실제 YAML 파싱 및 빈 값 검증 (yaml_validator)
  - Audit log는 해시체인 무결성 검증 후 append
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from _shared.yaml_validator import validate_blueprint
from _shared.audit import safe_append_audit_entry, utc_now_iso, verify_audit_integrity


def resolve_blueprint_path(target_path: str, blueprint_filename: str) -> Path:
    path = Path(target_path).expanduser().resolve()
    if path.is_file():
        return path
    # AUTO: prefer official DNA.md, otherwise fallback to DNA_BLUEPRINT.md (proposal)
    if blueprint_filename.strip().upper() == "AUTO":
        dna = (path / "DNA.md").resolve()
        if dna.exists():
            return dna
        return (path / "DNA_BLUEPRINT.md").resolve()
    return (path / blueprint_filename).resolve()


def default_audit_path() -> Path:
    # .../02_AAOS-Immune_system/SWARM_INQUISITOR_SKILL/blueprint-judgment/scripts/verify_blueprint.py
    immune_root = Path(__file__).resolve().parents[3]
    return (immune_root / "AUDIT_LOG.md").resolve()

def main() -> int:
    parser = argparse.ArgumentParser(description="Verify AAOS DNA Blueprint")
    parser.add_argument("target_path", help="Folder containing DNA.md or DNA_BLUEPRINT.md, or a DNA file path")
    parser.add_argument(
        "--blueprint",
        default="AUTO",
        help="Blueprint filename, or AUTO to prefer DNA.md then DNA_BLUEPRINT.md (default: AUTO)",
    )
    parser.add_argument("--audit", default=None, help="Audit log path (default: 02_AAOS-Immune_system/AUDIT_LOG.md)")
    parser.add_argument("--no-audit", action="store_true", help="Do not write audit log")
    parser.add_argument("--force-audit", action="store_true", help="Append audit log even if integrity verification fails")
    args = parser.parse_args()

    blueprint_path = resolve_blueprint_path(args.target_path, args.blueprint)
    audit_path = Path(args.audit).expanduser().resolve() if args.audit else default_audit_path()

    result, reasons = validate_blueprint(blueprint_path)

    print(f"Blueprint: {blueprint_path}")
    print(f"Result: {result}")
    if reasons:
        print("\nReasons:")
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
                "type": "blueprint-judgment",
                "target": str(blueprint_path),
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
