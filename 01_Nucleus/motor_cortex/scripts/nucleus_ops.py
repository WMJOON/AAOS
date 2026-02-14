#!/usr/bin/env python3
"""
Nucleus operational entrypoint.

Commands:
- health: run Nucleus health checks (skills scan, audit integrity, archive ledger, governance checks)
- bootstrap: initialize local SQLite operational audit log DB
- log: append one operational audit log row
- supervision-check: run lower-layer (02_Swarm/03_Manifestation) supervision checks
- supervision-cycle: run supervision checks and seal an operations package in record_archive
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MINIMAL_SQLITE_SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS audit_logs (
    id TEXT PRIMARY KEY,
    date DATE NOT NULL,
    task_name TEXT NOT NULL,
    mode TEXT NOT NULL,
    action TEXT NOT NULL,
    status TEXT NOT NULL
       CHECK (status IN ('success', 'fail', 'in_progress')),
    notes TEXT,
    evidences TEXT,
    next_gate TEXT,
    model_families TEXT,
    context_for_next TEXT,
    continuation_hint TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS document_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    file_path TEXT NOT NULL,
    reference_type TEXT NOT NULL DEFAULT 'mention'
       CHECK (reference_type IN ('mention', 'read', 'edit', 'create')),
    context TEXT,
    related_task_id TEXT,
    referenced_by TEXT NOT NULL DEFAULT 'agent'
       CHECK (referenced_by IN ('user', 'agent')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (related_task_id) REFERENCES audit_logs(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_date ON audit_logs(date);
CREATE INDEX IF NOT EXISTS idx_audit_logs_status ON audit_logs(status);
CREATE INDEX IF NOT EXISTS idx_doc_refs_path ON document_references(file_path);
"""


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def detect_aaos_root(start: Path) -> Path:
    current = start.resolve()
    while current != current.parent:
        if (current / "00_METADoctrine" / "DNA.md").exists() and (current / "01_Nucleus").exists():
            return current
        current = current.parent
    raise RuntimeError("Failed to detect AAOS root. Run inside 04_Agentic_AI_OS or pass --aaos-root.")


def run_cmd(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _path_status(path: Path) -> dict[str, Any]:
    return {"path": str(path), "exists": path.exists(), "is_dir": path.is_dir()}


def _read_text_safe(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _check_governance_frontmatter(content: str, source_name: str) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    has_priority_stack = ("AAOS Canon > META Doctrine" in content) or (
        "Canon" in content and "META Doctrine" in content
    )
    has_termination_signal = any(
        token in content
        for token in ("natural_dissolution", "Natural Dissolution", "termination conditions", "종료 조건")
    )
    has_context_or_retention = any(
        token in content for token in ("max_days", "context_for_next", "retention", "해체")
    )
    checks.append(
        {
            "name": f"{source_name}:priority_stack",
            "ok": has_priority_stack,
            "detail": "상위 규범 우선순위 명시",
        }
    )
    checks.append(
        {
            "name": f"{source_name}:termination_or_context",
            "ok": has_termination_signal and has_context_or_retention,
            "detail": "종료/보존 또는 다음 컨텍스트 경로",
        }
    )
    checks.append(
        {
            "name": f"{source_name}:consensus_fields",
            "ok": ("model_id" in content and "model_family" in content)
            or "multi-agent-consensus" in content,
            "detail": "합의 메타데이터(최소 model_id/model_family 또는 multi-agent-consensus)",
        }
    )
    checks.append(
        {
            "name": f"{source_name}:archive_chain",
            "ok": "MANIFEST.sha256" in content and "HASH_LEDGER.md" in content,
            "detail": "증빙 체인(MANIFEST+HASH_LEDGER) 참조",
        }
    )
    checks.append(
        {
            "name": f"{source_name}:governance_voice",
            "ok": ("decree" in content or "homing_instinct" in content),
            "detail": "governance 용어(decree/homing_instinct) 일치",
        }
    )
    return checks


def _run_governance_checks(aaos_root: Path) -> list[dict[str, Any]]:
    targets = [
        aaos_root / "01_Nucleus" / "README.md",
        aaos_root / "01_Nucleus" / "immune_system" / "README.md",
        aaos_root / "01_Nucleus" / "immune_system" / "DNA.md",
        aaos_root / "01_Nucleus" / "record_archive" / "README.md",
        aaos_root / "01_Nucleus" / "record_archive" / "DNA.md",
        aaos_root / "01_Nucleus" / "deliberation_chamber" / "README.md",
        aaos_root / "01_Nucleus" / "deliberation_chamber" / "DNA.md",
        aaos_root / "01_Nucleus" / "motor_cortex" / "README.md",
        aaos_root / "01_Nucleus" / "motor_cortex" / "DNA.md",
    ]
    checks: list[dict[str, Any]] = []
    for p in targets:
        if not p.exists():
            checks.append({"name": f"{p}:exists", "ok": False, "detail": "필수 Nucleus 문서 누락"})
            continue
        try:
            content = _read_text_safe(p)
            checks.extend(_check_governance_frontmatter(content, str(p.relative_to(aaos_root))))
        except Exception as e:
            checks.append({"name": f"{p}:read", "ok": False, "detail": str(e)})
    return checks


SKILL_FRONTMATTER_ALLOWED_KEYS = {
    "name",
    "description",
    "argument-hint",
    "disable-model-invocation",
    "user-invocable",
    "allowed-tools",
    "model",
    "context",
    "agent",
    "hooks",
}

NUCLEUS_CANONICAL_FRONTMATTER_FILES = [
    "01_Nucleus/governance/AGENTS.md",
    "01_Nucleus/motor_cortex/governance/AGENTIC_WORKFLOW_ORCHESTRATION.md",
    "01_Nucleus/README.md",
    "01_Nucleus/immune_system/README.md",
    "01_Nucleus/record_archive/README.md",
    "01_Nucleus/deliberation_chamber/README.md",
    "01_Nucleus/motor_cortex/README.md",
]
NUCLEUS_CANONICAL_FRONTMATTER_ALLOWED_KEYS = {"name", "scope", "status", "version", "updated"}
NUCLEUS_CANONICAL_FRONTMATTER_MAX_KEYS = 5
SKILL_FRONTMATTER_MAX_KEYS = 4


def _iter_skill_files(aaos_root: Path) -> list[Path]:
    files: list[Path] = []
    for p in aaos_root.rglob("SKILL.md"):
        if "_archive" in p.parts:
            continue
        files.append(p)
    return files


def _extract_frontmatter_keys(text: str) -> list[str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return []
    keys: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^([A-Za-z0-9_-]+)\s*:", line)
        if m:
            keys.append(m.group(1))
    return keys


def _run_skills_policy_checks(aaos_root: Path) -> dict[str, Any]:
    violations: list[dict[str, Any]] = []
    total = 0
    for skill_path in _iter_skill_files(aaos_root):
        total += 1
        content = _read_text_safe(skill_path)
        keys = _extract_frontmatter_keys(content)
        missing_required = [k for k in ("name", "description") if k not in keys]
        nonstandard = [k for k in keys if k not in SKILL_FRONTMATTER_ALLOWED_KEYS]
        entropy_exceeded = len(keys) > SKILL_FRONTMATTER_MAX_KEYS
        if missing_required or nonstandard or entropy_exceeded:
            violations.append(
                {
                    "path": str(skill_path),
                    "missing_required": missing_required,
                    "nonstandard_keys": nonstandard,
                    "frontmatter_key_count": len(keys),
                    "max_allowed_keys": SKILL_FRONTMATTER_MAX_KEYS,
                }
            )
    return {
        "ok": len(violations) == 0,
        "total_skills": total,
        "violations": violations,
        "policy_source": "https://code.claude.com/docs/en/skills",
    }


def _run_frontmatter_hygiene_checks(aaos_root: Path) -> dict[str, Any]:
    violations: list[dict[str, Any]] = []
    for rel in NUCLEUS_CANONICAL_FRONTMATTER_FILES:
        p = aaos_root / rel
        if not p.exists():
            violations.append({"path": str(p), "error": "missing file"})
            continue
        keys = _extract_frontmatter_keys(_read_text_safe(p))
        if not keys:
            violations.append({"path": str(p), "error": "missing frontmatter"})
            continue
        missing_required = [k for k in ("name", "scope", "status", "updated") if k not in keys]
        non_minimal = [k for k in keys if k not in NUCLEUS_CANONICAL_FRONTMATTER_ALLOWED_KEYS]
        entropy_exceeded = len(keys) > NUCLEUS_CANONICAL_FRONTMATTER_MAX_KEYS
        if missing_required or non_minimal or entropy_exceeded:
            violations.append(
                {
                    "path": str(p),
                    "missing_required": missing_required,
                    "non_minimal_keys": non_minimal,
                    "frontmatter_key_count": len(keys),
                    "max_allowed_keys": NUCLEUS_CANONICAL_FRONTMATTER_MAX_KEYS,
                }
            )
    return {"ok": len(violations) == 0, "violations": violations}


def _run_nucleus_path_hygiene_checks(aaos_root: Path) -> dict[str, Any]:
    nucleus_root = aaos_root / "01_Nucleus"
    forbidden_dirs = {"legacy", "change_packets"}
    disallowed_dirs: list[str] = []
    disallowed_blueprint_files: list[str] = []
    for p in nucleus_root.rglob("*"):
        if "_archive" in p.parts:
            continue
        if p.is_dir() and p.name in forbidden_dirs:
            disallowed_dirs.append(str(p))
        if p.is_file() and p.suffix.lower() == ".md" and "BLUEPRINT" in p.name:
            disallowed_blueprint_files.append(str(p))
    return {
        "ok": len(disallowed_dirs) == 0 and len(disallowed_blueprint_files) == 0,
        "disallowed_dirs": sorted(disallowed_dirs),
        "disallowed_blueprint_files": sorted(disallowed_blueprint_files),
    }


def _run_immune_naming_checks(aaos_root: Path) -> dict[str, Any]:
    immune_root = aaos_root / "01_Nucleus" / "immune_system"
    skills_root = immune_root / "skills"
    required_dirs = [
        skills_root / "core",
        skills_root / "judgment-dna",
        skills_root / "judgment-permission",
        skills_root / "governance-skill",
        skills_root / "lineage-context",
        skills_root / "instruction-nucleus",
    ]
    missing_required = [str(p) for p in required_dirs if not p.exists()]
    forbidden_legacy = [
        immune_root / "SWARM_INQUISITOR_SKILL",
        immune_root / "inquisitor",
        skills_root / "_shared",
        skills_root / "blueprint-judgment",
        skills_root / "permission-judgment",
        skills_root / "skill-governance",
        skills_root / "context-lineage",
        skills_root / "inquisitor-instruction-nucleus",
    ]
    still_exists_legacy = [str(p) for p in forbidden_legacy if p.exists()]
    return {
        "ok": len(missing_required) == 0 and len(still_exists_legacy) == 0,
        "missing_required_dirs": missing_required,
        "legacy_dirs_present": still_exists_legacy,
    }


def _run_lowercase_subdir_checks(aaos_root: Path) -> dict[str, Any]:
    nucleus_root = aaos_root / "01_Nucleus"
    institution_roots = [
        nucleus_root / "immune_system",
        nucleus_root / "record_archive",
        nucleus_root / "deliberation_chamber",
        nucleus_root / "motor_cortex",
    ]
    violations: list[str] = []
    for root in institution_roots:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if not p.is_dir():
                continue
            if "_archive" in p.parts:
                continue
            name = p.name
            if any(ch.isupper() for ch in name):
                violations.append(str(p))
    return {"ok": len(violations) == 0, "violations": sorted(violations)}


def _run_institution_topfile_checks(aaos_root: Path) -> dict[str, Any]:
    institution_roots = [
        aaos_root / "00_METADoctrine",
        aaos_root / "01_Nucleus",
        aaos_root / "02_Swarm",
        aaos_root / "03_Manifestation",
        aaos_root / "01_Nucleus" / "immune_system",
        aaos_root / "01_Nucleus" / "record_archive",
        aaos_root / "01_Nucleus" / "deliberation_chamber",
        aaos_root / "01_Nucleus" / "motor_cortex",
    ]
    allowed_files = {"README.md", "DNA.md"}
    violations: list[dict[str, Any]] = []

    for root in institution_roots:
        if not root.exists():
            continue
        files = sorted([p.name for p in root.iterdir() if p.is_file()])
        extra_files = [name for name in files if name not in allowed_files]
        missing_required = [name for name in sorted(allowed_files) if name not in files]
        if extra_files or missing_required:
            violations.append(
                {
                    "root": str(root),
                    "extra_files": extra_files,
                    "missing_required": missing_required,
                }
            )

    return {"ok": len(violations) == 0, "violations": violations}


def _iter_layer_modules(layer_root: Path) -> list[Path]:
    modules: list[Path] = []
    if not layer_root.exists():
        return modules
    for p in sorted(layer_root.iterdir()):
        if not p.is_dir():
            continue
        if p.name.startswith("."):
            continue
        if p.name in {"_archive", "__pycache__"}:
            continue
        modules.append(p)
    return modules


OUTWARD_SUPERVISION_TARGETS = {
    "02_Swarm": [
        "context-orchestrated-filesystem",
        "context-orchestrated-ontology",
        "cortex-agora",
    ],
    "03_Manifestation": ["summon-agents"],
}


def _run_lower_layer_supervision_checks(aaos_root: Path) -> dict[str, Any]:
    swarm_root = aaos_root / "02_Swarm"
    manifestation_root = aaos_root / "03_Manifestation"
    required_issues: list[str] = []
    recommendations: list[str] = []
    module_reports: list[dict[str, Any]] = []
    supervision_scope: list[dict[str, Any]] = []
    scope_records: dict[str, dict[str, Any]] = {}

    target_index = {
        "02_Swarm": {p for p in OUTWARD_SUPERVISION_TARGETS["02_Swarm"]},
        "03_Manifestation": {p for p in OUTWARD_SUPERVISION_TARGETS["03_Manifestation"]},
    }

    def evaluate_module(module_path: Path, layer: str) -> dict[str, Any]:
        readme = module_path / "README.md"
        dna = module_path / "DNA.md"
        checks: list[dict[str, Any]] = []
        module_issues: list[str] = []
        module_reco: list[str] = []
        module_name = module_path.relative_to(aaos_root).as_posix()
        module_basename = module_path.name
        scope_enabled = module_basename in target_index[layer]

        def add_check(name: str, ok: bool, required: bool, note: str) -> None:
            checks.append(
                {
                    "name": name,
                    "required": required,
                    "ok": ok,
                    "value": bool(ok),
                    "note": note,
                }
            )
            if ok:
                return
            if required:
                module_issues.append(f"{name} missing")
            else:
                module_reco.append(f"{name} missing")

        add_check("readme_exists", readme.exists(), scope_enabled, "README.md exists")
        add_check("dna_exists", dna.exists(), scope_enabled, "DNA.md exists")

        behavior_score = False
        resource_limit_score = False
        execution_binding_score = False
        reference_valid_score = False
        natural_dissolution_score = False
        for item in module_path.rglob("*"):
            if not item.is_file():
                continue
            name = item.name.lower()
            if "behavior" in name or "feed" in name or "observation" in name:
                behavior_score = True
            if "resource" in name or "limit" in name or "constraint" in name:
                resource_limit_score = True
            if "binding" in name or "execution" in name:
                execution_binding_score = True
            try:
                content = item.read_text(encoding="utf-8", errors="ignore").lower()
            except Exception:
                continue
            if "natural_dissolution" in content or "termination" in content or "dissolve" in content:
                natural_dissolution_score = True
            if "reference" in content or "references" in content or "upstream" in content:
                reference_valid_score = True
            if "resource" in content or "limit" in content or "constraint" in content:
                resource_limit_score = True
            if "behavior" in content or "feed" in content or "observation" in content:
                behavior_score = True
            if "binding" in content or "execution" in content:
                execution_binding_score = True

        add_check("behavior_observability", behavior_score, False, "behavior/feed/observability evidence")
        add_check("natural_dissolution", natural_dissolution_score, False, "natural dissolution / termination policy")
        add_check("resource_limits", resource_limit_score, False, "resource/limit/constraint field")
        add_check("execution_binding", execution_binding_score, layer == "03_Manifestation", "execution/manifestation binding evidence")
        add_check("reference_fields", reference_valid_score, False, "DNA 참조/상위 의존성 표기")

        if module_issues:
            required_issues.append(f"{module_name}: {', '.join(module_issues)}")
        for reco in module_reco:
            recommendations.append(f"{module_name}: {reco}")

        scope_status = "needs-improvement" if module_issues else "ok"
        scope_record = {
            "layer": layer,
            "module": module_name,
            "scope_target": scope_enabled,
            "module_path": str(module_path),
            "status": scope_status,
            "checks": checks,
            "required_checks": [c for c in checks if c["required"]],
            "recommended_checks": [c for c in checks if not c["required"]],
        }
        if scope_enabled:
            scope_records[module_name] = scope_record
            supervision_scope.append(scope_record)

        return {
            "layer": layer,
            "module": module_name,
            "readme": readme.exists(),
            "dna": dna.exists(),
            "required_issues": module_issues,
            "recommendations": module_reco,
            "scope_target": scope_enabled,
            "scope_checks": checks,
        }

    for module in _iter_layer_modules(swarm_root):
        module_reports.append(evaluate_module(module, "02_Swarm"))

    for module in _iter_layer_modules(manifestation_root):
        module_reports.append(evaluate_module(module, "03_Manifestation"))

    watchlist: list[dict[str, Any]] = []
    for layer, modules in OUTWARD_SUPERVISION_TARGETS.items():
        root = swarm_root if layer == "02_Swarm" else manifestation_root
        for module_name in modules:
            module_path = root / module_name
            module_rel = f"{layer}/{module_name}"
            scope_match = scope_records.get(module_rel)
            if scope_match is None:
                watchlist.append(
                    {
                        "layer": layer,
                        "module": module_rel,
                        "scope_target": True,
                        "status": "missing",
                        "required_checks": [
                            {"name": "module_exists", "required": True, "ok": False, "value": False, "note": "target module path not found"}
                        ],
                        "recommended_checks": [],
                    }
                )
                required_issues.append(f"{module_rel}: target module missing")
                continue
            watchlist.append(
                {
                    "layer": layer,
                    "module": module_rel,
                    "scope_target": True,
                    "status": scope_match["status"],
                    "required_checks": scope_match["required_checks"],
                    "recommended_checks": scope_match["recommended_checks"],
                }
            )

    blueprint_files: list[str] = []
    for root in (swarm_root, manifestation_root):
        if not root.exists():
            continue
        for p in root.rglob("*.md"):
            if "_archive" in p.parts:
                continue
            if "BLUEPRINT" in p.name:
                blueprint_files.append(str(p))
    if blueprint_files:
        required_issues.append("legacy blueprint files detected outside _archive")

    if not (aaos_root / "01_Nucleus" / "governance" / "AGENTS.md").exists():
        recommendations.append(
            "01_Nucleus/governance/AGENTS.md check skipped: missing for cross-layer traceability context"
        )

    supervision_stage = "needs-improvement" if required_issues else "ok"

    return {
        "ok": len(required_issues) == 0,
        "roots": {
            "02_Swarm": str(swarm_root),
            "03_Manifestation": str(manifestation_root),
        },
        "watchlist": watchlist,
        "modules": module_reports,
        "supervision_scope": supervision_scope,
        "required_issues": required_issues,
        "recommendations": recommendations,
        "blueprint_files": sorted(blueprint_files),
        "supervision_stage": supervision_stage,
        "summary": {
            "modules_checked": len(module_reports),
            "required_issue_count": len(required_issues),
            "recommendation_count": len(recommendations),
            "watchlist_size": len(watchlist),
            "supervision_stage": supervision_stage,
        },
    }


def _format_supervision_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Lower Layer Supervision Report")
    lines.append("")
    lines.append(f"- timestamp: {report.get('timestamp')}")
    lines.append(f"- aaos_root: `{report.get('aaos_root')}`")
    lines.append(f"- supervision_ok: {report.get('ok')}")
    lines.append(f"- supervision_stage: {report.get('supervision_stage')}")
    lines.append("")
    summary = report.get("summary", {})
    lines.append("## Summary")
    lines.append(f"- modules_checked: {summary.get('modules_checked')}")
    lines.append(f"- required_issue_count: {summary.get('required_issue_count')}")
    lines.append(f"- recommendation_count: {summary.get('recommendation_count')}")
    lines.append(f"- watchlist_size: {summary.get('watchlist_size')}")
    lines.append(f"- supervision_stage: {summary.get('supervision_stage')}")
    lines.append("")
    watchlist = report.get("watchlist", [])
    lines.append("## Outward Supervision Watchlist")
    if watchlist:
        lines.append("| layer | module | status | required_ok/total | recommended_ok/total |")
        lines.append("|---|---|---|---|---|")
        for item in watchlist:
            checks_required = item.get("required_checks", [])
            checks_recommended = item.get("recommended_checks", [])
            req_ok = len([c for c in checks_required if c.get("ok")])
            req_total = len(checks_required)
            rec_ok = len([c for c in checks_recommended if c.get("ok")])
            rec_total = len(checks_recommended)
            lines.append(
                f"| {item.get('layer')} | {item.get('module')} | {item.get('status')} | "
                f"{req_ok}/{req_total} | {rec_ok}/{rec_total} |"
            )
    else:
        lines.append("- (none)")
    lines.append("")
    issues = report.get("required_issues", [])
    lines.append("## Required Issues")
    if issues:
        for issue in issues:
            lines.append(f"- {issue}")
    else:
        lines.append("- (none)")
    lines.append("")
    recos = report.get("recommendations", [])
    lines.append("## Recommendations")
    if recos:
        for reco in recos:
            lines.append(f"- {reco}")
    else:
        lines.append("- (none)")
    lines.append("")
    outputs = report.get("supervision_outputs", {})
    lines.append("## Supervision Outputs")
    if outputs:
        lines.append(f'- supervision_report_path: `{outputs.get("supervision_report_path")}`')
        lines.append(f'- improvement_queue_path: `{outputs.get("improvement_queue_path")}`')
        lines.append(f'- package_path: `{outputs.get("package_path")}`')
    else:
        lines.append("- (none)")
    lines.append("")
    blueprint_files = report.get("blueprint_files", [])
    lines.append("## Blueprint Files")
    if blueprint_files:
        for p in blueprint_files:
            lines.append(f"- `{p}`")
    else:
        lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)


def run_lower_layer_supervision(aaos_root: Path) -> dict[str, Any]:
    payload = _run_lower_layer_supervision_checks(aaos_root)
    payload["timestamp"] = utc_now_iso()
    payload["aaos_root"] = str(aaos_root)
    return payload


def run_supervision_cycle(aaos_root: Path, *, dry_run: bool = False) -> tuple[dict[str, Any], bool]:
    health_report = run_health(aaos_root)
    supervision_report = run_lower_layer_supervision(aaos_root)
    workflow_report, workflow_ok = workflow_audit_report(
        aaos_root / "01_Nucleus" / "motor_cortex" / "templates" / "WORKFLOW_TRACE_MANIFEST_TEMPLATE.md"
    )

    ts = utc_now_iso()
    stamp = ts.replace("-", "").replace(":", "")
    package_id = f"{stamp}__ops-supervision__swarm-manifestation"
    package_rel = Path("_archive") / "operations" / package_id
    package_dir = aaos_root / "01_Nucleus" / "record_archive" / package_rel
    payload_dir = package_dir / "payload"
    payload_dir.mkdir(parents=True, exist_ok=True)

    health_json = payload_dir / "HEALTH_REPORT.json"
    supervision_json = payload_dir / "LOWER_LAYER_SUPERVISION.json"
    workflow_json = payload_dir / "WORKFLOW_AUDIT.json"
    summary_md = payload_dir / "SUMMARY.md"
    improvement_md = payload_dir / "IMPROVEMENT_QUEUE.md"

    supervision_outputs = {
        "supervision_report_path": str(supervision_json),
        "improvement_queue_path": str(improvement_md),
        "package_path": str(package_dir),
    }
    supervision_report["supervision_outputs"] = supervision_outputs
    if "supervision_stage" not in supervision_report:
        supervision_report["supervision_stage"] = (
            "needs-improvement" if supervision_report.get("required_issues") else "ok"
        )

    health_json.write_text(json.dumps(health_report, indent=2, ensure_ascii=False), encoding="utf-8")
    supervision_json.write_text(json.dumps(supervision_report, indent=2, ensure_ascii=False), encoding="utf-8")
    workflow_json.write_text(json.dumps(workflow_report, indent=2, ensure_ascii=False), encoding="utf-8")

    required_issues = supervision_report.get("required_issues", [])
    recommendations = supervision_report.get("recommendations", [])
    supervision_stage = "needs-improvement" if required_issues else "ok"
    governance_warns = len([c for c in health_report.get("governance_checks", []) if not c.get("ok")])
    cycle_ok = bool(health_report.get("critical_ok")) and bool(supervision_report.get("ok")) and workflow_ok
    cycle_status = "ok" if cycle_ok else "needs-improvement"

    summary_md.write_text(
        "\n".join(
            [
                "# Supervision Summary",
                "",
                f"- timestamp: {ts}",
                f"- cycle_status: {cycle_status}",
                f"- supervision_stage: {supervision_stage}",
                f"- health_critical_ok: {health_report.get('critical_ok')}",
                f"- lower_layer_supervision_ok: {supervision_report.get('ok')}",
                f"- workflow_audit_ok: {workflow_ok}",
                f"- governance_warn_count: {governance_warns}",
                f"- required_issue_count: {len(required_issues)}",
                f"- recommendation_count: {len(recommendations)}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    lines = ["# Improvement Queue", ""]
    lines.append("## Required")
    if required_issues:
        for issue in required_issues:
            lines.append(f"- [ ] {issue}")
    else:
        lines.append("- [ ] none")
    lines.append("")
    lines.append("## Recommended")
    if recommendations:
        for reco in recommendations:
            lines.append(f"- [ ] {reco}")
    else:
        lines.append("- [ ] none")
    lines.append("")
    improvement_md.write_text("\n".join(lines), encoding="utf-8")

    manifest_path = package_dir / "MANIFEST.sha256"
    manifest_entries: list[str] = []
    for p in sorted(payload_dir.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(package_dir).as_posix()
        manifest_entries.append(f"{sha256_file(p)}  {rel}")
    manifest_path.write_text("\n".join(manifest_entries) + "\n", encoding="utf-8")
    manifest_sha = sha256_file(manifest_path)

    package_md = package_dir / "PACKAGE.md"
    package_md.write_text(
        "\n".join(
            [
                "---",
                f'timestamp: "{ts}"',
                f'package_id: "{package_id}"',
                'type: "other"',
                f'status: "{ "pending" if dry_run else "sealed" }"',
                "",
                "source_refs:",
                '  - "01_Nucleus/motor_cortex/scripts/nucleus_ops.py"',
                '  - "01_Nucleus/motor_cortex/governance/AGENTIC_WORKFLOW_ORCHESTRATION.md"',
                "",
                "targets:",
                '  - "02_Swarm/"',
                '  - "03_Manifestation/"',
                "",
                "audit_refs:",
                '  - "01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md"',
                '  - "01_Nucleus/record_archive/_archive/meta-audit-log/META_AUDIT_LOG.md"',
                "",
                "related_packages: []",
                "",
                "integrity:",
                '  manifest: "MANIFEST.sha256"',
                f'  manifest_sha256: "{manifest_sha}"',
                "",
                "created_by:",
                '  actor: "motor-cortex"',
                f'  method: "{ "dry-run" if dry_run else "tool" }"',
                "",
                f'notes: "supervision cycle status={cycle_status}; governance_warns={governance_warns}"',
                "---",
                "# Archive Package",
                "",
                "## Summary",
                "",
                "- Why this package exists:",
                "  - Nucleus가 하위 Swarm/Manifestation의 통제+개선 상태를 주기 점검하기 위해 생성.",
                "- What it proves:",
                f"  - health_critical_ok={health_report.get('critical_ok')}, lower_layer_supervision_ok={supervision_report.get('ok')}, workflow_audit_ok={workflow_ok}.",
                "- What can be reproduced from it:",
                "  - health/supervision/workflow 결과 및 개선 큐를 동일 경로에서 재현 가능.",
                "",
                "## Contents",
                "",
                "- `payload/HEALTH_REPORT.json`",
                "- `payload/LOWER_LAYER_SUPERVISION.json`",
                "- `payload/WORKFLOW_AUDIT.json`",
                "- `payload/SUMMARY.md`",
                "- `payload/IMPROVEMENT_QUEUE.md`",
                "- `MANIFEST.sha256`",
                "",
            ]
        ),
        encoding="utf-8",
    )

    seal_cp = None
    if not dry_run:
        ledger_keeper = aaos_root / "01_Nucleus" / "record_archive" / "scripts" / "ledger_keeper.py"
        summary = f"motor_cortex supervision cycle status={cycle_status}"
        notes = f"required_issues={len(required_issues)},recommendations={len(recommendations)},workflow_ok={workflow_ok}"
        seal_cp = run_cmd(
            [
                sys.executable,
                str(ledger_keeper),
                "seal",
                str(package_dir),
                "--summary",
                summary,
                "--targets",
                "02_Swarm/,03_Manifestation/",
                "--notes",
                notes,
            ]
        )
        if seal_cp.returncode != 0:
            return (
                {
                    "timestamp": ts,
                    "ok": False,
                    "error": "failed to seal package with ledger_keeper",
                    "package_path": str(package_dir),
                    "supervision_outputs": supervision_outputs,
                    "supervision_stage": supervision_stage,
                    "ledger_output": (seal_cp.stdout + "\n" + seal_cp.stderr).strip(),
                },
                False,
            )

    return (
        {
            "timestamp": ts,
            "ok": cycle_ok,
            "dry_run": dry_run,
            "cycle_status": cycle_status,
            "supervision_stage": supervision_stage,
            "package_path": str(package_dir),
            "package_rel_path": str(package_rel),
            "supervision_outputs": supervision_outputs,
            "health_critical_ok": health_report.get("critical_ok"),
            "lower_layer_supervision_ok": supervision_report.get("ok"),
            "workflow_audit_ok": workflow_ok,
            "required_issue_count": len(required_issues),
            "recommendation_count": len(recommendations),
            "ledger_output": (seal_cp.stdout.strip() if seal_cp else "dry-run; no ledger update"),
        },
        cycle_ok,
    )


def parse_workflow_manifest(path: Path) -> dict[str, str]:
    """
    Parse minimal key-value manifest style workflow artifacts.
    Expected fields:
      workflow_id
      issue_proposer
      issue_signature
      goal_statement
      dq_index
      rsv_total
      topology_type
      topology_rationale
      task_graph_signature
      record_path
      direction_signature
      plan_author
      plan_critic
      plan_critic_model_id
      plan_critic_provider
      plan_critic_model_family
      plan_critic_status
      criticality_separation_required
      criticality_model_family_separated
      decomposition_author
      decomposition_critic
      decomposition_critic_model_id
      decomposition_critic_provider
      decomposition_critic_model_family
      decomposition_critic_status
      model_consensus
      cross_ref_validation
      dissolution_monitor_status
    """
    if not path.exists():
        raise FileNotFoundError(f"Workflow manifest not found: {path}")

    parsed: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_]+):\s*(.+)$", line)
        if match:
            parsed[match.group(1)] = match.group(2).strip()
    return parsed


def _is_human_proposer(value: str) -> bool:
    lower = value.lower().strip()
    return lower.startswith("human:") or lower == "human" or lower.startswith("user:")


def _normalize_identity(value: str) -> str:
    normalized = re.sub(r"\s+", " ", value.strip().lower())
    if (len(normalized) >= 2) and (
        (normalized[0] == '"' and normalized[-1] == '"') or (normalized[0] == "'" and normalized[-1] == "'")
    ):
        normalized = normalized[1:-1].strip()
    return normalized


def verify_agentic_workflow_manifest(path: Path) -> tuple[bool, list[str]]:
    try:
        data = parse_workflow_manifest(path)
    except FileNotFoundError as e:
        return False, [str(e)]

    errors: list[str] = []
    required = [
        "workflow_id",
        "issue_proposer",
        "issue_signature",
        "goal_statement",
        "dq_index",
        "rsv_total",
        "topology_type",
        "topology_rationale",
        "task_graph_signature",
        "record_path",
        "model_consensus",
        "criticality_model_family_separated",
        "criticality_separation_required",
        "direction_signature",
        "plan_author",
        "plan_critic",
        "plan_critic_status",
        "plan_critic_model_family",
        "plan_critic_model_id",
        "plan_critic_provider",
        "decomposition_author",
        "decomposition_critic",
        "decomposition_critic_status",
        "decomposition_critic_model_id",
        "decomposition_critic_provider",
        "decomposition_critic_model_family",
    ]
    for key in required:
        if key not in data or not data[key]:
            errors.append(f"missing required field: {key}")

    if errors:
        return False, errors

    if not _is_human_proposer(data["issue_proposer"]):
        errors.append("issue_proposer must be human/user origin (for example, human:alice or user:requester)")

    topology_type = _normalize_identity(data["topology_type"])
    allowed_topologies = {
        "linear",
        "branching",
        "parallel",
        "fanout_fanin",
        "hierarchical",
        "synthesis_centric",
        "state_transition",
        "composite",
    }
    if topology_type not in allowed_topologies:
        errors.append(
            "topology_type must be one of: linear, branching, parallel, fanout_fanin, hierarchical, synthesis_centric, state_transition, composite"
        )
    if "dq" not in _normalize_identity(data["dq_index"]):
        errors.append("dq_index must include DQ identifiers (for example, DQ1|DQ2)")
    try:
        rsv_total = float(data["rsv_total"])
        if rsv_total <= 0:
            errors.append("rsv_total must be a positive number")
    except ValueError:
        errors.append("rsv_total must be numeric (for example, 3.0)")
    if "->" not in data["task_graph_signature"]:
        errors.append("task_graph_signature must describe at least one edge (for example, T1->T2)")

    plan_author = _normalize_identity(data["plan_author"])
    plan_critic = _normalize_identity(data["plan_critic"])
    if plan_author == plan_critic:
        errors.append("plan_critic must be an independent reviewer (plan_author != plan_critic)")
    if data["plan_critic_status"].lower().strip() not in {"pass", "passed", "ok", "no-critical-objection"}:
        errors.append("plan_critic_status must be one of: pass, passed, ok, no-critical-objection")

    decomposition_author = _normalize_identity(data["decomposition_author"])
    decomposition_critic = _normalize_identity(data["decomposition_critic"])
    if _normalize_identity(data["plan_critic_model_family"]) == _normalize_identity(data["decomposition_critic_model_family"]):
        errors.append(
            "plan_critic_model_family and decomposition_critic_model_family must be different model families"
        )
    if decomposition_author == decomposition_critic:
        errors.append(
            "decomposition_critic must be an independent reviewer (decomposition_author != decomposition_critic)"
        )
    if data["decomposition_critic_status"].lower().strip() not in {
        "pass",
        "passed",
        "ok",
        "no-critical-objection",
    }:
        errors.append(
            "decomposition_critic_status must be one of: pass, passed, ok, no-critical-objection"
        )
    if data["criticality_separation_required"].lower().strip() != "true":
        errors.append("criticality_separation_required must be true")
    if data["criticality_model_family_separated"].lower().strip() != "true":
        errors.append("criticality_model_family_separated must be true")

    return len(errors) == 0, errors


def workflow_audit_report(report_path: Path) -> tuple[dict[str, Any], bool]:
    ok, errors = verify_agentic_workflow_manifest(report_path)
    return {
        "timestamp": utc_now_iso(),
        "path": str(report_path),
        "ok": ok,
        "errors": errors,
    }, ok


def run_health(aaos_root: Path) -> dict[str, Any]:
    nucleus_root = aaos_root / "01_Nucleus"
    immune_root = nucleus_root / "immune_system"
    archive_root = nucleus_root / "record_archive"
    skills_scan_tool = immune_root / "skills" / "core" / "auto_inquisitor.py"
    audit_tool = immune_root / "skills" / "core" / "audit.py"
    audit_log = archive_root / "_archive" / "audit-log" / "AUDIT_LOG.md"
    meta_audit_log = archive_root / "_archive" / "meta-audit-log" / "META_AUDIT_LOG.md"
    hash_ledger = archive_root / "indexes" / "HASH_LEDGER.md"
    sqlite_db = aaos_root / "01_Nucleus" / "motor_cortex" / "context" / "agent_log.db"

    required_paths = [
        nucleus_root,
        immune_root,
        archive_root,
        nucleus_root / "deliberation_chamber",
        nucleus_root / "motor_cortex",
        nucleus_root / "motor_cortex" / "README.md",
        nucleus_root / "motor_cortex" / "DNA.md",
        skills_scan_tool,
        audit_tool,
        audit_log,
        meta_audit_log,
        hash_ledger,
    ]
    path_checks = [_path_status(p) for p in required_paths]
    missing_required = [c["path"] for c in path_checks if not c["exists"]]

    scan_summary: dict[str, Any] = {"ok": False, "error": "scan not run"}
    if skills_scan_tool.exists():
        scan_cp = run_cmd([sys.executable, str(skills_scan_tool), "--scan", str(aaos_root), "--format", "json"])
        if scan_cp.returncode == 0:
            try:
                scan_obj = json.loads(scan_cp.stdout)
                counts: dict[str, int] = {}

                def walk(node: dict[str, Any]) -> None:
                    r = str(node.get("result", "Unknown"))
                    counts[r] = counts.get(r, 0) + 1
                    for sub in node.get("sub_structures", []) or []:
                        if isinstance(sub, dict):
                            walk(sub)

                if isinstance(scan_obj, dict):
                    walk(scan_obj)
                scan_summary = {"ok": True, "counts": counts}
            except json.JSONDecodeError as e:
                scan_summary = {"ok": False, "error": f"invalid scan JSON: {e}"}
        else:
            scan_summary = {"ok": False, "error": scan_cp.stderr.strip() or scan_cp.stdout.strip()}

    audit_checks: list[dict[str, Any]] = []
    if audit_tool.exists():
        for p in (audit_log, meta_audit_log):
            cp = run_cmd([sys.executable, str(audit_tool), "verify", str(p)])
            audit_checks.append(
                {
                    "path": str(p),
                    "ok": cp.returncode == 0,
                    "output": (cp.stdout + cp.stderr).strip(),
                }
            )

    ledger_ok = False
    ledger_error = ""
    if hash_ledger.exists():
        text = hash_ledger.read_text(encoding="utf-8", errors="replace")
        ledger_ok = bool(re.search(r'^hash:\s*"[a-f0-9]{16,64}"\s*$', text, re.MULTILINE))
        if not ledger_ok:
            ledger_error = "No valid hash entry found in HASH_LEDGER.md"
    else:
        ledger_error = "HASH_LEDGER.md not found"

    sqlite_info: dict[str, Any] = {"path": str(sqlite_db), "exists": sqlite_db.exists()}
    if sqlite_db.exists():
        try:
            with sqlite3.connect(sqlite_db) as conn:
                row = conn.execute("SELECT COUNT(*) FROM audit_logs").fetchone()
                sqlite_info["audit_logs_count"] = int(row[0]) if row else 0
        except sqlite3.Error as e:
            sqlite_info["error"] = str(e)

    governance_checks = _run_governance_checks(aaos_root)
    legacy_agent_path = nucleus_root / "AGENT.md"
    agent_policy = {
        "ok": not legacy_agent_path.exists(),
        "path": str(legacy_agent_path),
        "detail": "AGENT.md is deprecated; AGENTS.md is canonical",
    }
    skills_policy = _run_skills_policy_checks(aaos_root)
    frontmatter_hygiene = _run_frontmatter_hygiene_checks(aaos_root)
    path_hygiene = _run_nucleus_path_hygiene_checks(aaos_root)
    immune_naming = _run_immune_naming_checks(aaos_root)
    lowercase_subdirs = _run_lowercase_subdir_checks(aaos_root)
    institution_topfiles = _run_institution_topfile_checks(aaos_root)
    lower_layer_supervision = run_lower_layer_supervision(aaos_root)
    critical_ok = (
        len(missing_required) == 0
        and scan_summary.get("ok") is True
        and all(c.get("ok") for c in audit_checks)
        and ledger_ok
        and agent_policy["ok"]
        and skills_policy["ok"]
        and frontmatter_hygiene["ok"]
        and path_hygiene["ok"]
        and immune_naming["ok"]
        and lowercase_subdirs["ok"]
        and institution_topfiles["ok"]
    )

    return {
        "timestamp": utc_now_iso(),
        "aaos_root": str(aaos_root),
        "critical_ok": critical_ok,
        "required_paths": path_checks,
        "missing_required": missing_required,
        "scan": scan_summary,
        "audit_checks": audit_checks,
        "ledger": {"ok": ledger_ok, "error": ledger_error},
        "sqlite": sqlite_info,
        "governance_checks": governance_checks,
        "agent_policy": agent_policy,
        "skills_policy": skills_policy,
        "frontmatter_hygiene": frontmatter_hygiene,
        "path_hygiene": path_hygiene,
        "immune_naming": immune_naming,
        "lowercase_subdirs": lowercase_subdirs,
        "institution_topfiles": institution_topfiles,
        "lower_layer_supervision": lower_layer_supervision,
    }


def format_health_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# Nucleus Health Report")
    lines.append("")
    lines.append(f"- timestamp: {report.get('timestamp')}")
    lines.append(f"- aaos_root: `{report.get('aaos_root')}`")
    lines.append(f"- critical_ok: {'YES' if report.get('critical_ok') else 'NO'}")
    lines.append("")

    lines.append("## Required Paths")
    for item in report.get("required_paths", []):
        status = "OK" if item.get("exists") else "MISSING"
        lines.append(f"- [{status}] `{item.get('path')}`")
    lines.append("")

    lines.append("## Skills Scan")
    scan = report.get("scan", {})
    if scan.get("ok"):
        for key in sorted(scan.get("counts", {})):
            lines.append(f"- {key}: {scan['counts'][key]}")
    else:
        lines.append(f"- error: {scan.get('error', 'unknown')}")
    lines.append("")

    lines.append("## Audit Integrity")
    for c in report.get("audit_checks", []):
        status = "OK" if c.get("ok") else "FAIL"
        lines.append(f"- [{status}] `{c.get('path')}`")
    lines.append("")

    lines.append("## Record Archive Ledger")
    ledger = report.get("ledger", {})
    lines.append(f"- ok: {ledger.get('ok')}")
    if ledger.get("error"):
        lines.append(f"- error: {ledger.get('error')}")
    lines.append("")

    sqlite_info = report.get("sqlite", {})
    lines.append("## SQLite Operational Log")
    lines.append(f"- path: `{sqlite_info.get('path')}`")
    lines.append(f"- exists: {sqlite_info.get('exists')}")
    if "audit_logs_count" in sqlite_info:
        lines.append(f"- audit_logs_count: {sqlite_info.get('audit_logs_count')}")
    if sqlite_info.get("error"):
        lines.append(f"- error: {sqlite_info.get('error')}")
    lines.append("")

    lines.append("## Canonical Policy")
    agent_policy = report.get("agent_policy", {})
    lines.append(f"- AGENT.md deprecated policy ok: {agent_policy.get('ok')}")
    if agent_policy.get("path"):
        lines.append(f"- path: `{agent_policy.get('path')}`")
    if agent_policy.get("detail"):
        lines.append(f"- detail: {agent_policy.get('detail')}")
    lines.append("")

    lines.append("## Skills Policy")
    skills_policy = report.get("skills_policy", {})
    lines.append(f"- ok: {skills_policy.get('ok')}")
    lines.append(f"- total_skills: {skills_policy.get('total_skills')}")
    lines.append(f"- policy_source: {skills_policy.get('policy_source')}")
    violations = skills_policy.get("violations", [])
    if violations:
        lines.append("- violations:")
        for v in violations[:50]:
            path = v.get("path")
            missing = ", ".join(v.get("missing_required", [])) or "-"
            nonstandard = ", ".join(v.get("nonstandard_keys", [])) or "-"
            key_count = v.get("frontmatter_key_count", "-")
            max_keys = v.get("max_allowed_keys", "-")
            lines.append(
                f"  - `{path}` | missing_required={missing} | nonstandard_keys={nonstandard} | keys={key_count}/{max_keys}"
            )
        if len(violations) > 50:
            lines.append(f"  - ... (+{len(violations) - 50} more)")
    lines.append("")

    lines.append("## Frontmatter Hygiene")
    fm = report.get("frontmatter_hygiene", {})
    lines.append(f"- ok: {fm.get('ok')}")
    fm_violations = fm.get("violations", [])
    if fm_violations:
        lines.append("- violations:")
        for v in fm_violations:
            if v.get("error"):
                lines.append(f"  - `{v.get('path')}` | error={v.get('error')}")
                continue
            missing = ", ".join(v.get("missing_required", [])) or "-"
            non_minimal = ", ".join(v.get("non_minimal_keys", [])) or "-"
            key_count = v.get("frontmatter_key_count", "-")
            max_keys = v.get("max_allowed_keys", "-")
            lines.append(
                f"  - `{v.get('path')}` | missing_required={missing} | non_minimal_keys={non_minimal} | keys={key_count}/{max_keys}"
            )
    lines.append("")

    lines.append("## Path Hygiene")
    path_hygiene = report.get("path_hygiene", {})
    lines.append(f"- ok: {path_hygiene.get('ok')}")
    bad_dirs = path_hygiene.get("disallowed_dirs", [])
    bad_blueprints = path_hygiene.get("disallowed_blueprint_files", [])
    if bad_dirs:
        lines.append("- disallowed_dirs:")
        for p in bad_dirs:
            lines.append(f"  - `{p}`")
    if bad_blueprints:
        lines.append("- disallowed_blueprint_files:")
        for p in bad_blueprints:
            lines.append(f"  - `{p}`")
    lines.append("")

    lines.append("## Immune Naming")
    immune_naming = report.get("immune_naming", {})
    lines.append(f"- ok: {immune_naming.get('ok')}")
    missing_required = immune_naming.get("missing_required_dirs", [])
    legacy_present = immune_naming.get("legacy_dirs_present", [])
    if missing_required:
        lines.append("- missing_required_dirs:")
        for p in missing_required:
            lines.append(f"  - `{p}`")
    if legacy_present:
        lines.append("- legacy_dirs_present:")
        for p in legacy_present:
            lines.append(f"  - `{p}`")
    lines.append("")

    lines.append("## Lowercase Subdirs")
    lowercase = report.get("lowercase_subdirs", {})
    lines.append(f"- ok: {lowercase.get('ok')}")
    violations = lowercase.get("violations", [])
    if violations:
        lines.append("- violations:")
        for p in violations:
            lines.append(f"  - `{p}`")
    lines.append("")

    lines.append("## Institution Top-Level Files")
    institution_topfiles = report.get("institution_topfiles", {})
    lines.append(f"- ok: {institution_topfiles.get('ok')}")
    violations = institution_topfiles.get("violations", [])
    if violations:
        lines.append("- violations:")
        for v in violations:
            root = v.get("root")
            extra = ", ".join(v.get("extra_files", [])) or "-"
            missing = ", ".join(v.get("missing_required", [])) or "-"
            lines.append(f"  - root=`{root}` | extra_files={extra} | missing_required={missing}")
    lines.append("")

    lines.append("## Lower Layer Supervision")
    lower_layer = report.get("lower_layer_supervision", {})
    lines.append(f"- ok: {lower_layer.get('ok')}")
    summary = lower_layer.get("summary", {})
    lines.append(f"- modules_checked: {summary.get('modules_checked')}")
    lines.append(f"- required_issue_count: {summary.get('required_issue_count')}")
    lines.append(f"- recommendation_count: {summary.get('recommendation_count')}")
    required_issues = lower_layer.get("required_issues", [])
    if required_issues:
        lines.append("- required_issues:")
        for issue in required_issues:
            lines.append(f"  - {issue}")
    recommendations = lower_layer.get("recommendations", [])
    if recommendations:
        lines.append("- recommendations:")
        for reco in recommendations:
            lines.append(f"  - {reco}")
    lines.append("")

    lines.append("## Governance Conformance Snapshot")
    for check in report.get("governance_checks", []):
        status = "OK" if check.get("ok") else "WARN"
        lines.append(f"- [{status}] {check.get('name')}: {check.get('detail', '')}")
    lines.append("")

    return "\n".join(lines)


def bootstrap_sqlite(aaos_root: Path) -> Path:
    db_path = aaos_root / "01_Nucleus" / "motor_cortex" / "context" / "agent_log.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.executescript(MINIMAL_SQLITE_SCHEMA)
        conn.commit()
    return db_path


def _ensure_sqlite_columns(conn: sqlite3.Connection) -> None:
    cols = {row[1] for row in conn.execute("PRAGMA table_info(audit_logs)").fetchall()}
    if "evidences" not in cols:
        conn.execute("ALTER TABLE audit_logs ADD COLUMN evidences TEXT")
    if "next_gate" not in cols:
        conn.execute("ALTER TABLE audit_logs ADD COLUMN next_gate TEXT")
    if "model_families" not in cols:
        conn.execute("ALTER TABLE audit_logs ADD COLUMN model_families TEXT")
    conn.commit()


def insert_log(
    aaos_root: Path,
    *,
    task_id: str,
    task_name: str,
    mode: str,
    action: str,
    status: str,
    notes: str,
    evidences: str | None,
    next_gate: str | None,
    model_families: str | None,
    context_for_next: str | None,
    continuation_hint: str | None,
) -> None:
    db_path = aaos_root / "01_Nucleus" / "motor_cortex" / "context" / "agent_log.db"
    if not db_path.exists():
        bootstrap_sqlite(aaos_root)

    today = datetime.now(timezone.utc).date().isoformat()
    with sqlite3.connect(db_path) as conn:
        _ensure_sqlite_columns(conn)
        conn.execute(
            """
            INSERT INTO audit_logs
            (id, date, task_name, mode, action, status, notes, evidences, next_gate, model_families, context_for_next, continuation_hint)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task_id,
                today,
                task_name,
                mode,
                action,
                status,
                notes,
                evidences,
                next_gate,
                model_families,
                context_for_next,
                continuation_hint,
            ),
        )
        conn.commit()


def main() -> int:
    parser = argparse.ArgumentParser(description="Nucleus operations helper")
    parser.add_argument("--aaos-root", type=Path, default=None, help="Path to 04_Agentic_AI_OS")
    sub = parser.add_subparsers(dest="command", required=True)

    p_health = sub.add_parser("health", help="Run Nucleus health checks")
    p_health.add_argument("--json", action="store_true", help="Print JSON output")
    p_health.add_argument("--write-report", type=Path, default=None, help="Write markdown report file")

    sub.add_parser("bootstrap", help="Initialize SQLite operational log DB")

    p_log = sub.add_parser("log", help="Insert one operational log row into SQLite DB")
    p_log.add_argument("--task-id", required=True)
    p_log.add_argument("--task-name", required=True)
    p_log.add_argument("--mode", default="ops")
    p_log.add_argument("--action", required=True)
    p_log.add_argument("--status", default="success", choices=["success", "fail", "in_progress"])
    p_log.add_argument("--notes", default="")
    p_log.add_argument("--evidences", default=None, help="Evidence refs for upper-gate traceability")
    p_log.add_argument("--next-gate", default=None, help="Upper-institution gate target")
    p_log.add_argument("--model-families", default=None, help="Comma-separated model families")
    p_log.add_argument("--context-for-next", default=None, help="Next-context handoff notes")
    p_log.add_argument("--continuation-hint", default=None)

    p_workflow_audit = sub.add_parser(
        "workflow-audit",
        help="Validate agentic workflow trace (issue→archive→plan→immune→revision→execute)",
    )
    p_workflow_audit.add_argument("workflow_path", type=Path, help="Path to workflow manifest file")

    p_supervision_check = sub.add_parser(
        "supervision-check",
        help="Check 02_Swarm/03_Manifestation supervision status",
    )
    p_supervision_check.add_argument("--json", action="store_true", help="Print JSON output")
    p_supervision_check.add_argument(
        "--write-report",
        type=Path,
        default=None,
        help="Write markdown supervision report file",
    )

    p_supervision_cycle = sub.add_parser(
        "supervision-cycle",
        help="Run supervision + create/seal operations package in record_archive",
    )
    p_supervision_cycle.add_argument("--dry-run", action="store_true", help="Create package without ledger seal")

    args = parser.parse_args()
    aaos_root = args.aaos_root.resolve() if args.aaos_root else detect_aaos_root(Path.cwd())

    if args.command == "bootstrap":
        db_path = bootstrap_sqlite(aaos_root)
        print(f"Bootstrapped SQLite operational log: {db_path}")
        return 0

    if args.command == "log":
        insert_log(
            aaos_root,
            task_id=args.task_id,
            task_name=args.task_name,
            mode=args.mode,
            action=args.action,
            status=args.status,
            notes=args.notes,
            evidences=args.evidences,
            next_gate=args.next_gate,
            model_families=args.model_families,
            context_for_next=args.context_for_next,
            continuation_hint=args.continuation_hint,
        )
        print(f"Inserted log row: {args.task_id}")
        return 0

    if args.command == "health":
        report = run_health(aaos_root)
        if args.write_report:
            target = args.write_report
            if not target.is_absolute():
                target = aaos_root / target
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(format_health_markdown(report), encoding="utf-8")
            print(f"Wrote report: {target}")
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print(format_health_markdown(report))
        return 0 if report.get("critical_ok") else 1

    if args.command == "workflow-audit":
        if not args.workflow_path:
            print("ERROR: workflow_path is required")
            return 1
        report, ok = workflow_audit_report(args.workflow_path)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if ok else 1

    if args.command == "supervision-check":
        report = run_lower_layer_supervision(aaos_root)
        if args.write_report:
            target = args.write_report
            if not target.is_absolute():
                target = aaos_root / target
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(_format_supervision_markdown(report), encoding="utf-8")
            print(f"Wrote report: {target}")
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print(_format_supervision_markdown(report))
        return 0 if report.get("ok") else 1

    if args.command == "supervision-cycle":
        cycle_report, ok = run_supervision_cycle(aaos_root, dry_run=bool(args.dry_run))
        print(json.dumps(cycle_report, indent=2, ensure_ascii=False))
        return 0 if ok else 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
