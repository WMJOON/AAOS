#!/usr/bin/env python3
"""
Build and refresh skill registries for swarms under 02_Swarm.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
SHARED_DIR = SCRIPT_DIR.parent.parent / "_shared"
if str(SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_DIR))

from frontmatter import FrontmatterParseError, as_list, safe_str, split_frontmatter_and_body
from validate_skill_frontmatter import validate_skill_contracts


SWARM_SKILL_DIR_CANDIDATES = ("skills", "SKILLS")
DEFAULT_MAX_SKILLS = 8


def read_frontmatter(md_path: Path) -> Tuple[Dict[str, Any], List[str]]:
    errors: List[str] = []
    try:
        text = md_path.read_text(encoding="utf-8")
    except OSError as exc:
        return {}, [f"{md_path}: cannot read - {exc}"]

    try:
        fm, _ = split_frontmatter_and_body(text)
    except FrontmatterParseError as exc:
        return {}, [f"{md_path}: frontmatter parse error - {exc}"]

    data = fm

    if not data:
        errors.append(f"{md_path}: missing/invalid frontmatter")
    return data, errors


def read_sidecar_meta(meta_path: Path) -> Tuple[Dict[str, Any], List[str]]:
    errors: List[str] = []
    if not meta_path.exists():
        return {}, [f"{meta_path}: not found"]
    try:
        text = meta_path.read_text(encoding="utf-8").strip()
    except OSError as exc:
        return {}, [f"{meta_path}: cannot read - {exc}"]
    wrapped = f"---\n{text}\n---\n"
    try:
        fm, _ = split_frontmatter_and_body(wrapped)
    except FrontmatterParseError as exc:
        return {}, [f"{meta_path}: parse error - {exc}"]
    if not fm:
        errors.append(f"{meta_path}: missing/invalid metadata")
    return fm, errors


@dataclass
class SkillRecord:
    directory: Path
    name: str
    context_id: str
    description: str
    trigger: str
    role: str
    created: str
    has_scripts: bool
    has_templates: bool
    has_references: bool
    metadata_source: str
    consumers: List[str] = field(default_factory=list)


def discover_skills(swarm_root: Path) -> List[SkillRecord]:
    skills: List[SkillRecord] = []
    seen: set[str] = set()
    for candidate in SWARM_SKILL_DIR_CANDIDATES:
        container = swarm_root / candidate
        if not container.is_dir():
            continue

        for sub in sorted(p for p in container.iterdir() if p.is_dir()):
            key = str(sub.resolve()).casefold()
            if key in seen:
                continue
            seen.add(key)

            md_path = sub / "SKILL.md"
            if not md_path.exists():
                continue

            fm, _ = read_frontmatter(md_path)
            meta_path = sub / "SKILL.meta.yaml"
            metadata_source = "none"
            meta: Dict[str, Any] = {}
            legacy_keys = {"context_id", "role", "state", "scope", "lifetime", "trigger", "created"}
            legacy_present = any(key in fm for key in legacy_keys)
            if meta_path.exists():
                meta, meta_errors = read_sidecar_meta(meta_path)
                if meta_errors:
                    metadata_source = "broken_sidecar"
                    meta = {}
                else:
                    metadata_source = "skill_meta"
            elif legacy_present:
                metadata_source = "legacy_frontmatter"

            context_id = safe_str(meta.get("context_id"), safe_str(fm.get("context_id"), ""))
            trigger = safe_str(meta.get("trigger"), safe_str(fm.get("trigger"), ""))
            role = safe_str(meta.get("role"), safe_str(fm.get("role"), ""))
            created = safe_str(meta.get("created"), safe_str(fm.get("created"), ""))
            skills.append(
                SkillRecord(
                    directory=sub,
                    name=safe_str(fm.get("name"), sub.name),
                    context_id=context_id,
                    description=safe_str(fm.get("description"), "").replace("\n", " "),
                    trigger=trigger,
                    role=role,
                    created=created,
                    has_scripts=(sub / "scripts").is_dir(),
                    has_templates=(sub / "templates").is_dir(),
                    has_references=(sub / "references").is_dir(),
                    metadata_source=metadata_source,
                )
            )

    return skills


def scan_inheritance(swarm_root: Path) -> Dict[str, List[str]]:
    consumers: Dict[str, List[str]] = {}
    for md_path in swarm_root.rglob("AGENT.md"):
        fm, errors = read_frontmatter(md_path)
        if errors:
            continue

        for skill_name in as_list(fm.get("inherits_skill")) + as_list(fm.get("inherits_skills")):
            consumers.setdefault(skill_name, []).append(md_path.parent.name)
    return consumers


def enrich_consumers(skills: Iterable[SkillRecord], consumers: Dict[str, List[str]]) -> None:
    for skill in skills:
        identifiers = [identifier for identifier in [skill.context_id, skill.name] if identifier]
        if not identifiers:
            continue
        matched_agents = []
        for identifier in identifiers:
            matched_agents.extend(consumers.get(identifier, []))
        if not matched_agents:
            continue
        skill.consumers = sorted(set(matched_agents))


def validate(records: List[SkillRecord]) -> Tuple[List[str], List[str]]:
    warnings: List[str] = []
    errors: List[str] = []

    for skill in records:
        if not skill.name:
            warnings.append(f"{skill.directory}: missing name")
        if not skill.description:
            warnings.append(f"{skill.directory}: missing description")
        if not skill.context_id:
            warnings.append(f"{skill.directory}: missing context_id in SKILL.meta.yaml or legacy SKILL.md")
        if skill.metadata_source == "legacy_frontmatter":
            warnings.append(f"{skill.directory}: WARN(legacy_frontmatter) using inline SKILL.md metadata")
        if skill.metadata_source == "broken_sidecar":
            errors.append(f"{skill.directory}: invalid SKILL.meta.yaml sidecar")

    seen_contexts: Dict[str, List[str]] = {}
    for skill in records:
        if not skill.context_id:
            continue
        identity = skill.context_id
        seen_contexts.setdefault(identity, []).append(str(skill.directory))
    for context_id, paths in seen_contexts.items():
        if len(paths) > 1:
            warnings.append(f"duplicate context_id={context_id}: {', '.join(paths)}")

    return errors, warnings


def render_skill_table(records: List[SkillRecord]) -> str:
    if not records:
        return "- 등록된 스킬이 없습니다.\n"

    lines = [
        "| Skill Folder | Name | Source | Context ID | Description | Trigger | Role | Scripts | Templates | References | Consumers |",
        "|---|---|---|---|---|---|---|---|---|---|"
    ]
    for record in records:
        source = record.context_id or record.name
        lines.append(
            "| "
            f"{record.directory.name} | "
            f"{record.name or '-'} | "
            f"{source} | "
            f"{record.context_id or '-'} | "
            f"{record.description[:80] if record.description else '-'} | "
            f"{record.trigger or '-'} | "
            f"{record.role or '-'} | "
            f"{'Y' if record.has_scripts else 'N'} | "
            f"{'Y' if record.has_templates else 'N'} | "
            f"{'Y' if record.has_references else 'N'} | "
            f"{', '.join(record.consumers) or '-'} |"
        )
    return "\n".join(lines) + "\n"


def render_overload_section(label: str, count: int, max_skills: int) -> str:
    if count <= max_skills:
        return ""
    return f"- [경고] `{label}` has {count} skills (threshold: {max_skills})\n"


def write_swarm_registry(
    swarm_root: Path,
    records: List[SkillRecord],
    max_skills: int,
    warnings: List[str],
    dry_run: bool,
    out_name: str,
) -> List[str]:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    generated = [
        f"# Swarm Skill Registry: {swarm_root.name}\n",
        f"- Generated at: `{now}`\n",
        f"- Swarm root: `{swarm_root}`\n",
        f"- Skill count: `{len(records)}`\n",
    ]
    overload = render_overload_section(swarm_root.name, len(records), max_skills)
    if overload:
        generated.append(overload)

    if warnings:
        generated.append("\n## Warnings\n")
        for warning in warnings:
            generated.append(f"- {warning}\n")

    generated.append("\n## Skills\n")
    generated.append(render_skill_table(records))
    generated.append("\n## Agent Inheritance Overview\n")
    if any(record.consumers for record in records):
        for record in sorted(records, key=lambda item: item.directory.name):
            generated.append(f"- `{record.directory.name}`: {', '.join(record.consumers) if record.consumers else '-'}\n")
    else:
        generated.append("- 등록된 소비자 정보가 없습니다.\n")

    output = "".join(generated)
    if not dry_run:
        registry_root = swarm_root / "registry"
        registry_root.mkdir(exist_ok=True)
        output_path = registry_root / out_name
        output_path.write_text(output, encoding="utf-8")

        # Compatibility: if caller expects legacy location and it already exists, keep it synced.
        legacy_output = swarm_root / out_name
        if legacy_output.exists():
            legacy_output.write_text(output, encoding="utf-8")
    return [f"{swarm_root}: skill count={len(records)}"]


def build_swarm_report(
    swarm_root: Path,
    max_skills: int,
    skip_write: bool,
) -> Tuple[Dict[str, Any], List[str], List[str]]:
    records = discover_skills(swarm_root)
    consumers = scan_inheritance(swarm_root)
    enrich_consumers(records, consumers)
    records = sorted(records, key=lambda item: item.directory.name)

    errors, warnings = validate(records)
    swarm_summary = {
        "name": swarm_root.name,
        "path": str(swarm_root),
        "skill_count": len(records),
        "skills": [],
        "warnings": warnings,
        "errors": errors,
        "overloaded": len(records) > max_skills,
    }
    for record in records:
        swarm_summary["skills"].append(
            {
                "name": record.name,
                "context_id": record.context_id,
                "source": record.context_id or record.name,
                "description": record.description,
                "path": str(record.directory),
                "trigger": record.trigger,
                "role": record.role,
                "created": record.created,
                "has_scripts": record.has_scripts,
                "has_templates": record.has_templates,
                "has_references": record.has_references,
                "consumers": record.consumers,
            }
        )

    write_warnings: List[str] = []
    if errors:
        write_warnings.extend(errors)
    write_warnings.extend(warnings)

    write_swarm_registry(
        swarm_root=swarm_root,
        records=records,
        max_skills=max_skills,
        warnings=warnings,
        dry_run=skip_write,
        out_name="SKILL_REGISTRY.md",
    )

    return swarm_summary, write_warnings, errors


def discover_swarms(swarm_root: Path) -> List[Path]:
    known: List[Path] = []
    if not swarm_root.is_dir():
        return known
    for child in sorted(swarm_root.iterdir()):
        if child.is_dir() and not child.name.startswith("_") and not child.name.startswith("."):
            if any((child / marker).is_dir() for marker in SWARM_SKILL_DIR_CANDIDATES):
                known.append(child)
            elif (child / "README.md").is_file() or (child / "DNA.md").is_file():
                known.append(child)
    return known


def collect_global_context_conflicts(summaries: List[Dict[str, Any]]) -> List[str]:
    location_map: Dict[str, List[str]] = {}
    for summary in summaries:
        for skill in summary.get("skills", []):
            identity = safe_str(skill.get("context_id")) or safe_str(skill.get("name"))
            if not identity:
                continue
            location_map.setdefault(identity, []).append(f"{summary['name']}:{skill['path']}")

    return [
        f"duplicate context identifier '{context_id}' in {', '.join(paths)}"
        for context_id, paths in sorted(location_map.items())
        if len(paths) > 1
    ]


def render_root_registry(
    summaries: List[Dict[str, Any]],
    max_skills: int,
    global_warnings: List[str],
) -> str:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        "# Swarm Skill Registry Index\n",
        f"- Generated at: `{now}`\n",
        f"- Scanned swarms: `{len(summaries)}`\n\n",
        "| Swarm | Skill Count | Overloaded | Warnings | Errors |\n",
        "|---|---:|---:|---:|---:|\n",
    ]
    for summary in summaries:
        lines.append(
            "| "
            f"{summary['name']} | "
            f"{summary['skill_count']} | "
            f"{'Y' if summary['overloaded'] else 'N'} | "
            f"{len(summary['warnings'])} | "
            f"{len(summary['errors'])} |\n"
        )
    lines.append("\n## Thresholds\n")
    lines.append(f"- Overload threshold: `{max_skills}` skills per Swarm\n")
    if global_warnings:
        lines.append("\n## Global Warnings\n")
        for warning in global_warnings:
            lines.append(f"- {warning}\n")

    return "".join(lines)


def write_root_registry(
    swarm_root: Path,
    summaries: List[Dict[str, Any]],
    max_skills: int,
    output_json: Optional[Path],
    skip_write: bool,
    global_warnings: List[str],
) -> None:
    index_text = render_root_registry(summaries, max_skills, global_warnings)
    if skip_write:
        return

    registry_root = swarm_root / "registry"
    registry_root.mkdir(exist_ok=True)
    index_path = registry_root / "SWARM_SKILL_REGISTRY.md"
    index_path.write_text(index_text, encoding="utf-8")

    legacy_index = swarm_root / "SWARM_SKILL_REGISTRY.md"
    if legacy_index.exists():
        legacy_index.write_text(index_text, encoding="utf-8")

    if not output_json:
        return

    output_json_path = output_json if output_json.suffix.lower() == ".json" else output_json.with_suffix(".json")
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "swarms": summaries,
    }
    output_json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve()
    default_swarm_root = script_dir.parents[4]
    parser = argparse.ArgumentParser(description="Build COF swarm skill registries.")
    parser.add_argument(
        "--swarm-root",
        default=str(default_swarm_root),
        help="Path to 02_Swarm root (default: script parent 04 path).",
    )
    parser.add_argument(
        "--max-skills",
        type=int,
        default=DEFAULT_MAX_SKILLS,
        help="Warn if a swarm has more than this many skills.",
    )
    parser.add_argument(
        "--json",
        default=None,
        help="Optional output JSON path under or outside repo.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be written without changing files.",
    )
    parser.add_argument(
        "--skip-write",
        action="store_true",
        help="Skip writing registry files.",
    )
    parser.add_argument(
        "--allow-legacy-frontmatter",
        action="store_true",
        help="Allow legacy SKILL.md inline metadata during migration.",
    )
    parser.add_argument(
        "--strict-skill-frontmatter",
        action="store_true",
        default=False,
        help="Hard-fail when SKILL.md uses forbidden keys (recommended).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    swarm_root = Path(args.swarm_root).expanduser().resolve()
    skip_write = args.skip_write or args.dry_run
    json_path = Path(args.json).expanduser().resolve() if args.json else None

    if not swarm_root.is_dir():
        print(f"ERROR: swarm-root not found -> {swarm_root}")
        return 1

    strict_enabled = args.strict_skill_frontmatter or (not args.allow_legacy_frontmatter)
    fm_errors, fm_warnings = validate_skill_contracts(
        swarm_root,
        strict=strict_enabled,
        allow_legacy_frontmatter=args.allow_legacy_frontmatter,
    )
    if fm_warnings:
        print("FRONTMATTER WARNINGS:")
        for warning in fm_warnings:
            print(f"- {warning}")
    if fm_errors:
        print("FRONTMATTER ERRORS:")
        for error in fm_errors:
            print(f"- {error}")
        return 1

    swarms = discover_swarms(swarm_root)
    if not swarms:
        print(f"WARNING: no swarms found under {swarm_root}")

    summaries: List[Dict[str, Any]] = []
    total_warnings: List[str] = []
    total_errors: List[str] = []

    for swarm in swarms:
        summary, warnings, errors = build_swarm_report(
            swarm_root=swarm,
            max_skills=args.max_skills,
            skip_write=skip_write,
        )
        summaries.append(summary)
        total_warnings.extend([f"{swarm.name}: {w}" for w in warnings])
        total_errors.extend([f"{swarm.name}: {e}" for e in errors])
        status = "OK" if not summary["errors"] else "ERROR"
        print(f"{status} {swarm.name}: {summary['skill_count']} skills")

    global_warnings = collect_global_context_conflicts(summaries)

    write_root_registry(
        swarm_root=swarm_root,
        summaries=summaries,
        max_skills=args.max_skills,
        output_json=json_path,
        skip_write=skip_write,
        global_warnings=global_warnings,
    )
    total_warnings.extend(global_warnings)

    if total_errors:
        print("\nERRORS:")
        for warning in total_errors:
            print(f"- {warning}")
    if total_warnings:
        print("\nWARNINGS:")
        for warning in total_warnings:
            print(f"- {warning}")

    if skip_write:
        print("\n[DRY-RUN] registry files were not written.")

    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
