#!/usr/bin/env python3
"""
Natural Dissolution Monitor & Executor

AAOS에서 선언된 Natural Dissolution을 실제로 모니터링하고 실행하는 시스템.

기능:
1. 구조별 종료 조건 모니터링
2. 자원 상한 감시
3. 자동 해체 실행 (요약 → 아카이브 → 삭제)
4. 해체 기록 남기기

사용법:
  # 전체 스캔
  python dissolution_monitor.py --scan /path/to/aaos_root

  # 특정 구조 해체 실행
  python dissolution_monitor.py --dissolve /path/to/structure --reason "목적 완료"

  # 자원 상한 검사만
  python dissolution_monitor.py --check-limits /path/to/structure
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

from yaml_validator import YAMLValidator
from audit import safe_append_audit_entry, utc_now_iso


class ResourceLimitViolation:
    """자원 상한 위반 정보"""
    def __init__(self, limit_type: str, limit: int, actual: int, path: str):
        self.limit_type = limit_type
        self.limit = limit
        self.actual = actual
        self.path = path

    def __repr__(self) -> str:
        return f"{self.limit_type}: {self.actual}/{self.limit} at {self.path}"


class DissolutionMonitor:
    """Natural Dissolution 모니터링 및 실행"""

    def __init__(self, aaos_root: Path, audit_log_path: Optional[Path] = None):
        self.aaos_root = aaos_root.resolve()
        self.immune_root = self.aaos_root / "02_AAOS-Immune_system"
        self.audit_log_path = audit_log_path or (self.immune_root / "AUDIT_LOG.md")
        self.archive_root = self.aaos_root / "_archive"

    def _load_blueprint(self, structure_path: Path) -> Optional[YAMLValidator]:
        """구조의 DNA.md(정식) 또는 DNA_BLUEPRINT.md(제안) 로드"""
        dna_path = structure_path / "DNA.md"
        bp_path = structure_path / "DNA_BLUEPRINT.md"
        active = dna_path if dna_path.exists() else bp_path
        if not active.exists():
            return None
        text = active.read_text(encoding="utf-8")
        return YAMLValidator(text)

    def check_resource_limits(self, structure_path: Path) -> List[ResourceLimitViolation]:
        """
        구조의 자원 상한 검사

        Returns:
            위반 목록 (빈 리스트면 정상)
        """
        violations: List[ResourceLimitViolation] = []
        bp = self._load_blueprint(structure_path)

        if not bp or not bp.is_valid():
            return violations  # Blueprint 없으면 검사 불가

        # max_files 검사
        max_files = bp.get("resource_limits.max_files")
        if max_files and isinstance(max_files, int):
            actual_files = sum(1 for _ in structure_path.rglob("*") if _.is_file())
            if actual_files > max_files:
                violations.append(ResourceLimitViolation(
                    "max_files", max_files, actual_files, str(structure_path)
                ))

        # max_folders 검사
        max_folders = bp.get("resource_limits.max_folders")
        if max_folders and isinstance(max_folders, int):
            actual_folders = sum(1 for _ in structure_path.rglob("*") if _.is_dir())
            if actual_folders > max_folders:
                violations.append(ResourceLimitViolation(
                    "max_folders", max_folders, actual_folders, str(structure_path)
                ))

        # max_log_kb 검사 (로그 파일 크기)
        max_log_kb = bp.get("resource_limits.max_log_kb")
        if max_log_kb and isinstance(max_log_kb, int):
            log_files = list(structure_path.rglob("*.log")) + list(structure_path.rglob("*LOG*.md"))
            total_kb = sum(f.stat().st_size for f in log_files if f.is_file()) / 1024
            if total_kb > max_log_kb:
                violations.append(ResourceLimitViolation(
                    "max_log_kb", max_log_kb, int(total_kb), str(structure_path)
                ))

        return violations

    def check_termination_conditions(
        self,
        structure_path: Path,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, List[str]]:
        """
        종료 조건 충족 여부 검사

        Args:
            structure_path: 검사 대상 구조
            context: 외부 컨텍스트 (예: {"project_completed": True})

        Returns:
            (should_dissolve, matched_conditions)
        """
        bp = self._load_blueprint(structure_path)
        if not bp or not bp.is_valid():
            return False, []

        conditions = bp.get("natural_dissolution.termination_conditions", [])
        if not isinstance(conditions, list):
            return False, []

        matched: List[str] = []
        context = context or {}

        for condition in conditions:
            if not isinstance(condition, str):
                continue

            # 간단한 조건 매칭 (실제 구현에서는 더 복잡한 로직 필요)
            condition_lower = condition.lower()

            # 컨텍스트 기반 매칭
            if "project" in condition_lower and context.get("project_completed"):
                matched.append(condition)
            elif "목적" in condition and context.get("purpose_completed"):
                matched.append(condition)
            elif "완료" in condition and context.get("task_completed"):
                matched.append(condition)

            # 시간 기반 매칭
            if "days" in condition_lower or "일" in condition:
                # retention.max_days 확인
                max_days = bp.get("natural_dissolution.retention.max_days")
                if max_days and isinstance(max_days, int):
                    created = bp.get("created")
                    if created:
                        try:
                            created_date = datetime.strptime(created, "%Y-%m-%d")
                            days_elapsed = (datetime.now() - created_date).days
                            if days_elapsed > max_days:
                                matched.append(f"{condition} (elapsed: {days_elapsed} days)")
                        except ValueError:
                            pass

        return len(matched) > 0, matched

    def generate_summary(self, structure_path: Path) -> str:
        """
        구조의 요약 문서 생성

        Returns:
            마크다운 형식의 요약 문서
        """
        bp = self._load_blueprint(structure_path)
        name = bp.get("name", structure_path.name) if bp else structure_path.name
        purpose = bp.get("natural_dissolution.purpose", "Unknown") if bp else "Unknown"
        version = bp.get("version", "Unknown") if bp else "Unknown"
        created = bp.get("created", "Unknown") if bp else "Unknown"

        # 파일 목록 수집
        files = list(structure_path.rglob("*"))
        file_count = sum(1 for f in files if f.is_file())
        folder_count = sum(1 for f in files if f.is_dir())

        # 주요 파일 목록 (마크다운 파일 중심)
        md_files = [f.relative_to(structure_path) for f in structure_path.rglob("*.md") if f.is_file()]
        py_files = [f.relative_to(structure_path) for f in structure_path.rglob("*.py") if f.is_file()]

        summary = f"""---
type: dissolution-summary
source_structure: "{name}"
dissolved_at: "{utc_now_iso()}"
---

# Dissolution Summary: {name}

## Original Structure

- **Name**: {name}
- **Version**: {version}
- **Created**: {created}
- **Purpose**: {purpose}
- **Location**: {structure_path}

## Statistics at Dissolution

- Total Files: {file_count}
- Total Folders: {folder_count}

## Key Files

### Markdown Documents
{chr(10).join(f"- {f}" for f in md_files[:20])}
{f"... and {len(md_files) - 20} more" if len(md_files) > 20 else ""}

### Python Scripts
{chr(10).join(f"- {f}" for f in py_files[:10])}
{f"... and {len(py_files) - 10} more" if len(py_files) > 10 else ""}

## Dissolution Details

- Dissolved by: AAOS Dissolution Monitor
- Timestamp: {utc_now_iso()}
- Archive Location: {self.archive_root / name}

---
This summary was auto-generated during Natural Dissolution.
"""
        return summary

    def execute_dissolution(
        self,
        structure_path: Path,
        reason: str,
        archive: bool = True,
        delete_after_archive: bool = True,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        구조 해체 실행

        Args:
            structure_path: 해체할 구조 경로
            reason: 해체 사유
            archive: 아카이브 생성 여부
            delete_after_archive: 아카이브 후 원본 삭제 여부
            dry_run: True면 실제 실행 없이 계획만 반환

        Returns:
            실행 결과
        """
        result: Dict[str, Any] = {
            "structure": str(structure_path),
            "reason": reason,
            "timestamp": utc_now_iso(),
            "dry_run": dry_run,
            "steps": [],
            "success": False
        }

        bp = self._load_blueprint(structure_path)
        name = bp.get("name", structure_path.name) if bp else structure_path.name

        # Step 1: 요약 생성
        summary = self.generate_summary(structure_path)
        summary_path = structure_path / "DISSOLUTION_SUMMARY.md"
        result["steps"].append({
            "action": "generate_summary",
            "path": str(summary_path)
        })

        if not dry_run:
            summary_path.write_text(summary, encoding="utf-8")

        # Step 2: 아카이브
        if archive:
            archive_path = self.archive_root / name / utc_now_iso().replace(":", "-")
            result["steps"].append({
                "action": "archive",
                "source": str(structure_path),
                "destination": str(archive_path)
            })

            if not dry_run:
                archive_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(structure_path, archive_path)

        # Step 3: 삭제
        if delete_after_archive:
            result["steps"].append({
                "action": "delete",
                "path": str(structure_path)
            })

            if not dry_run:
                shutil.rmtree(structure_path)

        # Audit 기록
        result["steps"].append({
            "action": "audit_log",
            "path": str(self.audit_log_path)
        })

        if not dry_run:
            safe_append_audit_entry(
                audit_path=self.audit_log_path,
                entry={
                    "timestamp": utc_now_iso(),
                    "type": "dissolution-execution",
                    "target": str(structure_path),
                    "result": "Dissolved",
                    "reasons": [reason],
                    "notes": f"Archived: {archive}, Deleted: {delete_after_archive}",
                },
                require_integrity=True,
            )

        result["success"] = True
        return result

    def scan_all_structures(self) -> List[Dict[str, Any]]:
        """
        AAOS 전체를 스캔하여 해체가 필요한 구조 목록 반환
        """
        findings: List[Dict[str, Any]] = []

        for item in self.aaos_root.iterdir():
            if not item.is_dir() or item.name.startswith('.') or item.name == "_archive":
                continue

            dna_path = item / "DNA.md"
            bp_path = item / "DNA_BLUEPRINT.md"
            if not (dna_path.exists() or bp_path.exists()):
                # 하위 폴더 검색
                for subitem in item.iterdir():
                    if subitem.is_dir():
                        sub_dna = subitem / "DNA.md"
                        sub_bp = subitem / "DNA_BLUEPRINT.md"
                        if sub_dna.exists() or sub_bp.exists():
                            findings.extend(self._analyze_structure(subitem))
            else:
                findings.extend(self._analyze_structure(item))

        return findings

    def _analyze_structure(self, structure_path: Path) -> List[Dict[str, Any]]:
        """단일 구조 분석"""
        findings: List[Dict[str, Any]] = []

        # 자원 상한 검사
        violations = self.check_resource_limits(structure_path)
        if violations:
            findings.append({
                "path": str(structure_path),
                "type": "resource_limit_violation",
                "severity": "warning",
                "details": [repr(v) for v in violations],
                "action_required": "Consider cleanup or dissolution"
            })

        # 종료 조건 검사 (기본 컨텍스트)
        should_dissolve, matched = self.check_termination_conditions(structure_path)
        if should_dissolve:
            findings.append({
                "path": str(structure_path),
                "type": "termination_condition_met",
                "severity": "critical",
                "details": matched,
                "action_required": "Execute dissolution"
            })

        return findings


# CLI 인터페이스
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AAOS Natural Dissolution Monitor")
    parser.add_argument("--scan", type=str, help="Scan AAOS root for dissolution candidates")
    parser.add_argument("--check-limits", type=str, help="Check resource limits for a structure")
    parser.add_argument("--dissolve", type=str, help="Execute dissolution for a structure")
    parser.add_argument("--reason", type=str, default="Manual dissolution", help="Reason for dissolution")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without executing")
    parser.add_argument("--no-archive", action="store_true", help="Skip archiving before deletion")
    parser.add_argument("--audit", type=str, help="Custom audit log path")
    args = parser.parse_args()

    if args.scan:
        aaos_root = Path(args.scan).resolve()
        audit_path = Path(args.audit).resolve() if args.audit else None
        monitor = DissolutionMonitor(aaos_root, audit_path)

        print(f"🔍 Scanning AAOS structures in: {aaos_root}\n")
        findings = monitor.scan_all_structures()

        if not findings:
            print("✅ No dissolution candidates found.")
        else:
            print(f"⚠️  Found {len(findings)} issue(s):\n")
            for finding in findings:
                print(f"  [{finding['severity'].upper()}] {finding['path']}")
                print(f"    Type: {finding['type']}")
                print(f"    Details: {finding['details']}")
                print(f"    Action: {finding['action_required']}")
                print()

    elif args.check_limits:
        structure_path = Path(args.check_limits).resolve()
        # AAOS 루트 추정 (상위 폴더에서 찾기)
        aaos_root = structure_path.parent
        while aaos_root.name != "04_Agentic_AI_OS" and aaos_root.parent != aaos_root:
            aaos_root = aaos_root.parent

        monitor = DissolutionMonitor(aaos_root)
        violations = monitor.check_resource_limits(structure_path)

        if not violations:
            print(f"✅ {structure_path.name}: All resource limits OK")
        else:
            print(f"⚠️  {structure_path.name}: Resource limit violations:")
            for v in violations:
                print(f"  - {v}")

    elif args.dissolve:
        structure_path = Path(args.dissolve).resolve()
        aaos_root = structure_path.parent
        while aaos_root.name != "04_Agentic_AI_OS" and aaos_root.parent != aaos_root:
            aaos_root = aaos_root.parent

        audit_path = Path(args.audit).resolve() if args.audit else None
        monitor = DissolutionMonitor(aaos_root, audit_path)

        print(f"{'🧪 DRY RUN: ' if args.dry_run else ''}Dissolving: {structure_path}")
        print(f"Reason: {args.reason}")
        print()

        result = monitor.execute_dissolution(
            structure_path,
            reason=args.reason,
            archive=not args.no_archive,
            dry_run=args.dry_run
        )

        print("Steps:")
        for step in result["steps"]:
            print(f"  - {step['action']}: {step.get('path', step.get('destination', ''))}")

        if result["success"]:
            print(f"\n✅ Dissolution {'planned' if args.dry_run else 'completed'} successfully")
        else:
            print(f"\n❌ Dissolution failed")

    else:
        parser.print_help()
