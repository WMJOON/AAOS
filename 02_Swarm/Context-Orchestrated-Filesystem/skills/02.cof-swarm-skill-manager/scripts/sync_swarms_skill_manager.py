#!/usr/bin/env python3
"""
Build and refresh skill registries for swarms under 02_Swarm.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:
    import yaml
except ImportError:
    yaml = None


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SWARM_SKILL_DIR_CANDIDATES = ("skills", "SKILLS")
DEFAULT_MAX_SKILLS = 8


def parse_frontmatter(text: str) -> Dict[str, Any]:
    fm_match = FRONTMATTER_RE.search(text)
    if not fm_match:
        return {}

    fm_text = fm_match.group(1)
    if yaml is not None:
        try:
            data = yaml.safe_load(fm_text)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    data: Dict[str, Any] = {}
    for raw in fm_text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data


def read_frontmatter(md_path: Path) -> Tuple[Dict[str, Any], List[str]]:
    errors: List[str] = []
    try:
        text = md_path.read_text(encoding="utf-8")
    except OSError as exc:
        return {}, [f"{md_path}: cannot read - {exc}"]

    data = parse_frontmatter(text)
    if not data:
        errors.append(f"{md_path}: missing/invalid frontmatter")
    return data, errors


def safe_text(value: Any, fallback: str = "") -> str:
    if value is None:
        return fallback
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)):
        return str(value)
    return str(value)


def as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [safe_text(v) for v in value if safe_text(v, "").strip()]
    return [safe_text(value)] if safe_text(value).strip() else []


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
            skills.append(
                SkillRecord(
                    directory=sub,
                    name=safe_text(fm.get("name"), sub.name),
                    context_id=safe_text(fm.get("context_id"), ""),
                    description=safe_text(fm.get("description"), "").replace("\n", " "),
                    trigger=safe_text(fm.get("trigger"), ""),
                    role=safe_text(fm.get("role"), ""),
                    created=safe_text(fm.get("created"), ""),
                    has_scripts=(sub / "scripts").is_dir(),
                    has_templates=(sub / "templates").is_dir(),
                    has_references=(sub / "references").is_dir(),
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

    seen_contexts: Dict[str, List[str]] = {}
    for skill in records:
        identity = skill.context_id if skill.context_id else skill.name
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
            identity = safe_text(skill.get("context_id")) or safe_text(skill.get("name"))
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
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    swarm_root = Path(args.swarm_root).expanduser().resolve()
    skip_write = args.skip_write or args.dry_run
    json_path = Path(args.json).expanduser().resolve() if args.json else None

    if not swarm_root.is_dir():
        print(f"ERROR: swarm-root not found -> {swarm_root}")
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
