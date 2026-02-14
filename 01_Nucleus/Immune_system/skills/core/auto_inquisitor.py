#!/usr/bin/env python3
"""
Auto Inquisitor - 자동 검증 시스템

Agent가 수동으로 검증을 호출하지 않아도 자동으로 개입하는 메커니즘.

사용 시나리오:
1. 폴더 생성 감시 (watchdog)
2. Git pre-commit hook
3. Agent 실행 전 wrapper
4. 주기적 스캔 (cron)

Dependencies:
  pip install watchdog (optional, for filesystem monitoring)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# 상대 경로로 다른 모듈 import
sys.path.insert(0, str(Path(__file__).resolve().parent))

from yaml_validator import validate_blueprint, validate_permission_request
from audit import safe_append_audit_entry, utc_now_iso
from lineage import format_lineage_markdown, format_lineage_text, resolve_lineage


class AutoInquisitor:
    """자동 검증 시스템"""

    def __init__(
        self,
        aaos_root: Path,
        audit_log_path: Optional[Path] = None,
        strict_mode: bool = False
    ):
        """
        Args:
            aaos_root: AAOS 루트 디렉토리 (04_Agentic_AI_OS)
            audit_log_path: Audit Log 경로 (None이면 기본 경로)
            strict_mode: True면 Canonical-Conditional도 차단
        """
        self.aaos_root = aaos_root.resolve()
        self.immune_root = self.aaos_root / "01_Nucleus" / "immune_system"
        self.audit_log_path = audit_log_path or (
            self.aaos_root / "01_Nucleus" / "record_archive" / "_archive" / "audit-log" / "AUDIT_LOG.md"
        )
        self.strict_mode = strict_mode

    def scan_structure(self, target_path: Path) -> Dict[str, Any]:
        """
        대상 경로의 AAOS 구조를 스캔하고 검증

        Returns:
            {
                "path": str,
                "has_blueprint": bool,
                "result": str,
                "reasons": list,
                "sub_structures": [...]
            }
        """
        target = target_path.resolve()
        result: Dict[str, Any] = {
            "path": str(target),
            "has_blueprint": False,
            "result": "Unknown",
            "reasons": [],
            "sub_structures": []
        }

        if not target.is_dir():
            result["result"] = "Non-Canonical"
            result["reasons"] = ["Not a directory"]
            return result

        # DNA 찾기: DNA.md(정식) 단일 기준
        dna_path = target / "DNA.md"
        active_dna = dna_path

        if not active_dna.exists():
            # AAOS 구조가 아닐 수 있음 - 하위 검색
            for subdir in target.iterdir():
                if subdir.is_dir() and not subdir.name.startswith('.'):
                    sub_dna = subdir / "DNA.md"
                    if sub_dna.exists():
                        result["sub_structures"].append(self.scan_structure(subdir))

            if not result["sub_structures"]:
                result["result"] = "Non-Canonical"
                result["reasons"] = ["No DNA.md found"]
            else:
                result["result"] = "Container"
                result["reasons"] = ["Contains sub-structures"]
            return result

        result["has_blueprint"] = True
        judgment_result, reasons = validate_blueprint(active_dna)
        result["result"] = judgment_result
        result["reasons"] = reasons

        # 하위 구조도 재귀적으로 검사
        for subdir in target.iterdir():
            if subdir.is_dir() and not subdir.name.startswith('.'):
                sub_dna = subdir / "DNA.md"
                if sub_dna.exists():
                    result["sub_structures"].append(self.scan_structure(subdir))

        return result

    def enforce_on_creation(
        self,
        target_path: Path,
        block_non_canonical: bool = True
    ) -> Tuple[bool, str]:
        """
        구조 생성 시점에 강제 검증

        Args:
            target_path: 생성하려는 구조 경로
            block_non_canonical: True면 Non-Canonical 시 생성 차단

        Returns:
            (allowed, message)
        """
        scan_result = self.scan_structure(target_path)

        # Audit 기록
        try:
            safe_append_audit_entry(
                audit_path=self.audit_log_path,
                entry={
                    "timestamp": utc_now_iso(),
                    "type": "auto-enforcement",
                    "target": str(target_path),
                    "result": scan_result["result"],
                    "reasons": scan_result["reasons"],
                    "notes": "Auto-Inquisitor enforcement on creation",
                },
                require_integrity=True,
            )
        except RuntimeError as e:
            return False, f"BLOCKED: Audit log integrity violation. {e}"

        if scan_result["result"] == "Non-Canonical":
            if block_non_canonical:
                return False, f"BLOCKED: Non-Canonical structure. Reasons: {scan_result['reasons']}"
            else:
                return True, f"WARNING: Non-Canonical structure allowed. Reasons: {scan_result['reasons']}"

        if scan_result["result"] == "Canonical-Conditional":
            if self.strict_mode:
                return False, f"BLOCKED (strict mode): Conditional structure. Reasons: {scan_result['reasons']}"
            else:
                return True, f"WARNING: Conditional approval. Fix: {scan_result['reasons']}"

        return True, "APPROVED: Canonical structure"

    def generate_preflight_check(self) -> str:
        """
        Agent Preflight Checklist를 자동 생성
        """
        checklist = """
## Agent Preflight Checklist (Auto-Generated)

이 체크리스트는 Auto-Inquisitor에 의해 생성되었습니다.
행동 전에 다음을 확인하세요:

### 1. 구조 생성/확장 시
- [ ] DNA.md가 준비되어 있는가?
- [ ] natural_dissolution 섹션이 완전한가?
  - [ ] purpose가 명시되어 있는가?
  - [ ] termination_conditions가 하나 이상인가?
  - [ ] dissolution_steps가 하나 이상인가?
- [ ] resource_limits가 설정되어 있는가?
- [ ] inquisitor.audit_log 경로가 올바른가?

### 2. 권한 요청 시
- [ ] PERMISSION-REQUEST-TEMPLATE.md를 사용했는가?
- [ ] time_bound.expires가 설정되어 있는가?
- [ ] justification이 충분한가?
- [ ] risk_level이 적절한가?

### 3. 실행 후
- [ ] 01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md에 기록이 남았는가?
- [ ] 오류 발생 시 롤백 계획이 있는가?

---
위 체크리스트를 통과하지 못하면 Auto-Inquisitor가 작업을 차단할 수 있습니다.
"""
        return checklist


def _flatten_scan(scan_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []

    def walk(node: Dict[str, Any]) -> None:
        items.append(node)
        for child in node.get("sub_structures", []) or []:
            if isinstance(child, dict):
                walk(child)

    walk(scan_result)
    return items


def _format_scan_report_markdown(scan_result: Dict[str, Any]) -> str:
    items = _flatten_scan(scan_result)

    canonical = [i for i in items if i.get("result") == "Canonical"]
    conditional = [i for i in items if i.get("result") == "Canonical-Conditional"]
    non_canonical = [i for i in items if i.get("result") == "Non-Canonical"]
    containers = [i for i in items if i.get("result") == "Container"]

    def section(title: str, rows: List[Dict[str, Any]]) -> str:
        if not rows:
            return f"## {title}\n\n- (none)\n"

        lines: List[str] = [f"## {title}", ""]
        for r in rows:
            path = r.get("path", "")
            reasons = r.get("reasons", []) or []
            lines.append(f"- `{path}`")
            if reasons:
                for reason in reasons[:8]:
                    lines.append(f"  - {reason}")
                if len(reasons) > 8:
                    lines.append(f"  - ... (+{len(reasons) - 8} more)")
        lines.append("")
        return "\n".join(lines)

    header = [
        "# AAOS Auto-Inquisitor Scan Report",
        "",
        "## Summary",
        "",
        f"- Total nodes scanned: {len(items)}",
        f"- Canonical: {len(canonical)}",
        f"- Canonical-Conditional: {len(conditional)}",
        f"- Non-Canonical: {len(non_canonical)}",
        f"- Containers (no blueprint at this level): {len(containers)}",
        "",
        "## Action Priority",
        "",
        "1. Fix `Non-Canonical` (blocked by default).",
        "2. Fix `Canonical-Conditional` (allowed unless strict mode).",
        "3. Keep `Canonical` as-is.",
        "",
    ]

    return "\n".join(header) + "\n" + (
        section("Non-Canonical", non_canonical)
        + section("Canonical-Conditional", conditional)
        + section("Canonical", canonical)
        + section("Containers", containers)
    )


def _format_scan_report_text(scan_result: Dict[str, Any]) -> str:
    items = _flatten_scan(scan_result)
    counts: Dict[str, int] = {}
    for i in items:
        k = i.get("result", "Unknown")
        counts[k] = counts.get(k, 0) + 1

    lines: List[str] = []
    lines.append("AAOS Auto-Inquisitor Scan Report")
    lines.append(f"Total nodes scanned: {len(items)}")
    lines.append("Counts:")
    for k in sorted(counts.keys()):
        lines.append(f"  - {k}: {counts[k]}")
    lines.append("")

    for i in items:
        if i.get("result") in ("Non-Canonical", "Canonical-Conditional"):
            lines.append(f"[{i.get('result')}] {i.get('path')}")
            for reason in (i.get("reasons", []) or [])[:8]:
                lines.append(f"  - {reason}")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def create_git_pre_commit_hook(aaos_root: Path) -> str:
    """
    Git pre-commit hook 스크립트 생성

    사용법:
      1. 이 함수의 출력을 .git/hooks/pre-commit에 저장
      2. chmod +x .git/hooks/pre-commit
    """
    hook_script = f'''#!/bin/bash
# AAOS Auto-Inquisitor Pre-Commit Hook
# Generated by auto_inquisitor.py

AAOS_ROOT="{aaos_root}"
IMMUNE_ROOT="${{AAOS_ROOT}}/01_Nucleus/immune_system"
VALIDATOR="${{IMMUNE_ROOT}}/skills/core/yaml_validator.py"

echo "🔍 AAOS Auto-Inquisitor: Validating changes..."

# 변경된 DNA 파일 검사
CHANGED_BLUEPRINTS=$(git diff --cached --name-only | grep -E "DNA\\.md$")

if [ -n "$CHANGED_BLUEPRINTS" ]; then
    echo "📋 Validating modified DNA docs..."
    while IFS= read -r bp; do
        echo "  - $bp"
        python3 "$VALIDATOR" "$bp" --type blueprint
        RESULT=$?
        if [ $RESULT -eq 1 ]; then
            echo "❌ BLOCKED: $bp is Non-Canonical"
            echo "Fix the issues above before committing."
            exit 1
        elif [ $RESULT -eq 2 ]; then
            echo "⚠️  WARNING: $bp is Canonical-Conditional"
            # Conditional은 경고만 표시 (차단 안 함)
        fi
    done <<< "$CHANGED_BLUEPRINTS"
fi

# 변경된 Permission Request 검사
CHANGED_PERMISSIONS=$(git diff --cached --name-only | grep -E "PERMISSION.*\\.md$")

if [ -n "$CHANGED_PERMISSIONS" ]; then
    echo "📋 Validating Permission Requests..."
    while IFS= read -r pr; do
        echo "  - $pr"
        python3 "$VALIDATOR" "$pr" --type permission
        RESULT=$?
        if [ $RESULT -eq 1 ]; then
            echo "❌ BLOCKED: $pr is Non-Canonical"
            exit 1
        elif [ $RESULT -eq 2 ]; then
            echo "⚠️  WARNING: $pr is Canonical-Conditional"
        fi
    done <<< "$CHANGED_PERMISSIONS"
fi

echo "✅ AAOS Auto-Inquisitor: All checks passed"
exit 0
'''
    return hook_script


def create_wrapper_script() -> str:
    """
    Agent 실행 전 wrapper 스크립트 생성

    사용법:
      agent_wrapper.sh your_agent_command
    """
    wrapper = '''#!/bin/bash
# AAOS Agent Wrapper - Auto-Inquisitor 통합

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AAOS_ROOT="$(cd "$SCRIPT_DIR/../../../../" && pwd)"
AUTO_INQUISITOR="${AAOS_ROOT}/01_Nucleus/immune_system/skills/core/auto_inquisitor.py"
if [ ! -f "$AUTO_INQUISITOR" ]; then
    echo "❌ AAOS auto-inquisitor not found: $AUTO_INQUISITOR"
    exit 1
fi

# Agent 실행 전 Preflight Check
echo "🛡️ AAOS Auto-Inquisitor: Running preflight check..."
python3 "$AUTO_INQUISITOR" --preflight "$AAOS_ROOT"

if [ $? -ne 0 ]; then
    echo "❌ Preflight check failed. Agent execution blocked."
    exit 1
fi

echo "✅ Preflight check passed. Executing agent..."

# 원래 명령 실행
exec "$@"
'''
    return wrapper


# CLI 인터페이스
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AAOS Auto-Inquisitor")
    parser.add_argument("--scan", type=str, help="Scan a directory for AAOS structures")
    parser.add_argument("--context", type=str, help="Resolve lineage for a file/dir path")
    parser.add_argument("--preflight", type=str, help="Generate preflight checklist for AAOS root")
    parser.add_argument("--gen-hook", type=str, help="Generate git pre-commit hook for AAOS root")
    parser.add_argument("--gen-wrapper", action="store_true", help="Generate agent wrapper script")
    parser.add_argument("--strict", action="store_true", help="Strict mode (block Conditional)")
    parser.add_argument(
        "--severity",
        choices=["low", "medium", "high", "meta"],
        default="medium",
        help="Action severity for --context (default: medium)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "md", "text"],
        default="json",
        help="Output format for --scan (default: json)",
    )
    args = parser.parse_args()

    if args.scan:
        aaos_root = Path(args.scan).resolve()
        inquisitor = AutoInquisitor(aaos_root, strict_mode=args.strict)
        result = inquisitor.scan_structure(aaos_root)
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif args.format == "md":
            print(_format_scan_report_markdown(result))
        else:
            print(_format_scan_report_text(result))

    elif args.context:
        target = Path(args.context).expanduser().resolve()
        nodes, guidance = resolve_lineage(target, severity=args.severity)
        if args.format == "md":
            print(format_lineage_markdown(nodes, guidance))
        elif args.format == "text":
            print(format_lineage_text(nodes, guidance))
        else:
            # json
            print(
                json.dumps(
                    {
                        "guidance": guidance,
                        "references": [
                            {"level": n.level, "path": str(n.path), "exists": n.exists, "note": n.note}
                            for n in nodes
                        ],
                    },
                    indent=2,
                    ensure_ascii=False,
                )
            )

    elif args.preflight:
        aaos_root = Path(args.preflight).resolve()
        inquisitor = AutoInquisitor(aaos_root)
        print(inquisitor.generate_preflight_check())

    elif args.gen_hook:
        aaos_root = Path(args.gen_hook).resolve()
        print(create_git_pre_commit_hook(aaos_root))

    elif args.gen_wrapper:
        print(create_wrapper_script())

    else:
        parser.print_help()
