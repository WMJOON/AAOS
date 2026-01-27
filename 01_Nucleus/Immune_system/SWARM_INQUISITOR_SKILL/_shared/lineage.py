from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class LineageNode:
    level: str
    path: Path
    exists: bool
    note: str = ""


SEVERITY_ORDER = ["low", "medium", "high", "meta"]


def _find_aaos_root(start: Path) -> Optional[Path]:
    """
    Locate AAOS root folder (04_Agentic_AI_OS) by walking upward.
    """
    cur = start.resolve()
    if cur.is_file():
        cur = cur.parent

    for p in [cur, *cur.parents]:
        if p.name == "04_Agentic_AI_OS":
            return p
    return None


def _find_nearest_blueprint(start: Path) -> Optional[Path]:
    """
    Find nearest ancestor directory (including itself) containing DNA.md (official) or DNA_BLUEPRINT.md (proposal).
    """
    cur = start.resolve()
    if cur.is_file():
        cur = cur.parent

    for p in [cur, *cur.parents]:
        dna = p / "DNA.md"
        if dna.exists():
            return dna
        blueprint = p / "DNA_BLUEPRINT.md"
        if blueprint.exists():
            return blueprint
    return None


def _find_nearest_rule(start: Path, *, exclude: Optional[Path] = None) -> Optional[Path]:
    """
    Find nearest RULE.md in current/ancestor directories.
    (Not AAOS root METADoctrine.md; this is node-local rule if present.)
    """
    cur = start.resolve()
    if cur.is_file():
        cur = cur.parent

    exclude = exclude.resolve() if exclude else None

    for p in [cur, *cur.parents]:
        candidate = (p / "RULE.md").resolve()
        if exclude and candidate == exclude:
            continue
        if candidate.exists():
            return candidate
    return None


def resolve_lineage(
    target_path: Path,
    *,
    severity: str = "medium",
) -> Tuple[List[LineageNode], Dict[str, str]]:
    """
    Resolve normative reference chain for an action starting at target_path.

    The chain is ordered from local(node) -> (record archive) -> immune doctrine/tools (+ deliberation chamber) -> meta -> canon.
    Severity controls how far upward the caller should consult:
      - low: node DNA (+ node rule if present)
      - medium: + immune doctrine + inquisitor core
      - high: + meta doctrine + canon
      - meta: + META_AUDIT_LOG + multi-agent consensus expectations (human-gated)
    """
    severity = (severity or "medium").strip().lower()
    if severity not in SEVERITY_ORDER:
        raise ValueError(f"Unknown severity '{severity}'. Expected one of: {', '.join(SEVERITY_ORDER)}")

    aaos_root = _find_aaos_root(target_path)
    if aaos_root is None:
        aaos_root = Path()

    meta_doctrine_path = (aaos_root / "METADoctrine.md").resolve()

    nearest_blueprint = _find_nearest_blueprint(target_path)
    # Exclude AAOS root META Doctrine from "node.rule" to avoid duplication.
    nearest_rule = _find_nearest_rule(target_path, exclude=meta_doctrine_path if meta_doctrine_path.exists() else None)

    record_archive_root = aaos_root / "01_Nucleus" / "Record_Archive"
    immune_root = aaos_root / "01_Nucleus" / "Immune_system"
    deliberation_root = aaos_root / "01_Nucleus" / "Deliberation_Chamber"
    canon_path = aaos_root / "README.md"
    immune_doctrine_path = immune_root / "AAOS_DNA_DOCTRINE_RULE.md"
    inquisitor_root = immune_root / "SWARM_INQUISITOR_SKILL"
    audit_log_path = immune_root / "AUDIT_LOG.md"
    meta_audit_log_path = immune_root / "META_AUDIT_LOG.md"

    nodes: List[LineageNode] = []

    # Local node context
    if nearest_blueprint:
        nodes.append(LineageNode("node.dna_blueprint", nearest_blueprint, True))
    else:
        nodes.append(
            LineageNode(
                "node.dna_blueprint",
                (target_path if target_path.is_dir() else target_path.parent) / "DNA.md",
                False,
                note="Missing; structure is Non-Canonical until DNA.md (or DNA_BLUEPRINT.md) exists.",
            )
        )

    if nearest_rule:
        nodes.append(LineageNode("node.rule", nearest_rule, True))

    # Always include immune doctrine/tools for medium+
    if SEVERITY_ORDER.index(severity) >= SEVERITY_ORDER.index("medium"):
        nodes.extend(
            [
                LineageNode("record.archive", record_archive_root, record_archive_root.exists()),
                LineageNode("immune.doctrine", immune_doctrine_path, immune_doctrine_path.exists()),
                LineageNode("immune.inquisitor", inquisitor_root, inquisitor_root.exists()),
                LineageNode("immune.audit_log", audit_log_path, audit_log_path.exists()),
                LineageNode("deliberation.chamber", deliberation_root, deliberation_root.exists()),
            ]
        )

    # Meta + Canon for high+
    if SEVERITY_ORDER.index(severity) >= SEVERITY_ORDER.index("high"):
        nodes.extend(
            [
                LineageNode("meta.doctrine", meta_doctrine_path, meta_doctrine_path.exists()),
                LineageNode("canon", canon_path, canon_path.exists()),
            ]
        )

    # Meta change governance
    if severity == "meta":
        nodes.append(LineageNode("meta.audit_log", meta_audit_log_path, meta_audit_log_path.exists()))

    guidance: Dict[str, str] = {
        "severity": severity,
        "principle": "Read local DNA first; escalate to immune/meta/canon based on action severity.",
        "low": "Read node DNA (+ node RULE if present).",
        "medium": "Additionally read Immune Doctrine + ensure Inquisitor/Audit path is used.",
        "high": "Additionally read META Doctrine + Canon; treat as permission-gated if destructive.",
        "meta": "META-level change: requires META_AUDIT_LOG entry and multi-agent consensus + human approval.",
    }

    return nodes, guidance


def format_lineage_markdown(nodes: List[LineageNode], guidance: Dict[str, str]) -> str:
    lines: List[str] = []
    lines.append("# AAOS Lineage Resolution")
    lines.append("")
    lines.append("## Guidance")
    lines.append("")
    lines.append(f"- Severity: `{guidance.get('severity', '')}`")
    lines.append(f"- Principle: {guidance.get('principle', '')}")
    lines.append("")

    sev = guidance.get("severity", "medium")
    if sev in guidance:
        lines.append(f"- This level: {guidance[sev]}")
        lines.append("")

    lines.append("## References (local → global)")
    lines.append("")
    for n in nodes:
        status = "OK" if n.exists else "MISSING"
        note = f" — {n.note}" if n.note else ""
        lines.append(f"- `{n.level}`: `{n.path}` [{status}]{note}")
    lines.append("")
    return "\n".join(lines)


def format_lineage_text(nodes: List[LineageNode], guidance: Dict[str, str]) -> str:
    lines: List[str] = []
    lines.append("AAOS Lineage Resolution")
    lines.append(f"Severity: {guidance.get('severity', '')}")
    lines.append(f"Principle: {guidance.get('principle', '')}")
    sev = guidance.get("severity", "medium")
    if sev in guidance:
        lines.append(f"This level: {guidance[sev]}")
    lines.append("")
    lines.append("References (local → global):")
    for n in nodes:
        status = "OK" if n.exists else "MISSING"
        suffix = f" ({n.note})" if n.note else ""
        lines.append(f"- {n.level}: {n.path} [{status}]{suffix}")
    return "\n".join(lines).rstrip() + "\n"
