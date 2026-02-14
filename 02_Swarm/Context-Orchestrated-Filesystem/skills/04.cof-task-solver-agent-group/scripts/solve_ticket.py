#!/usr/bin/env python3
"""
solve_ticket.py - COF Task Solver Agent Group

Reads a ticket from NN.agents-task-context/tickets/ and dispatches it to the
appropriate AI CLI agent(s) based on tag heuristics.

Core Principle: One agent group solves one ticket.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

AVAILABLE_PROVIDERS = ["claude", "codex", "gemini"]

# Single provider tag mapping
SINGLE_PROVIDER_TAG_MAP: Dict[str, str] = {
    # Security domain
    "security": "claude",
    "audit": "claude",
    "compliance": "claude",
    "vulnerability": "claude",
    # Performance domain
    "performance": "gemini",
    "optimization": "gemini",
    "benchmark": "gemini",
    "profiling": "gemini",
    # Architecture domain
    "architecture": "codex",
    "refactor": "codex",
    "design": "codex",
    "structure": "codex",
}

# Group execution tags
COUNCIL_TAGS = {"review", "critique", "consensus"}
SEQUENTIAL_TAGS = {"sequential", "iterative", "refinement"}

DEFAULT_AGENT = "claude"
VALID_PROVIDERS = {"claude", "codex", "gemini", "all"}
VALID_STATUSES = {"todo", "in-progress", "done", "blocked"}
VALID_GROUP_TYPES = {"single", "council", "sequential"}
VALID_CONTEXT_PASSING = {"full", "summary", "delta"}

# Default timeout retry behavior (aligns with SKILL.md)
DEFAULT_MAX_RETRIES = 1
DEFAULT_RETRY_TIMEOUT_DELTA_SECONDS = 60

# Exit codes
EXIT_SUCCESS = 0
EXIT_PARTIAL = 1
EXIT_TICKET_ERROR = 2
EXIT_CONTEXT_ERROR = 3
EXIT_NO_AGENTS = 4
EXIT_AGENT_FAILED = 5


# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _detect_cof_root(start_path: str) -> Optional[str]:
    """Detect COF root by looking for characteristic files/directories."""
    current = os.path.abspath(start_path)
    while True:
        # Check for COF markers
        if os.path.isfile(os.path.join(current, "core-docs", "COF_DOCTRINE.md")):
            return current
        if os.path.isfile(os.path.join(current, "COF_DOCTRINE.md")):
            return current
        if os.path.isdir(os.path.join(current, "skills")):
            parent = os.path.dirname(current)
            if os.path.basename(current) == "context-orchestrated-filesystem":
                return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def _detect_summon_agents_root(cof_root: Optional[str]) -> Optional[str]:
    """Detect summon-agents root relative to COF root."""
    if cof_root:
        # Try relative path from COF
        candidate = os.path.normpath(os.path.join(cof_root, "..", "..", "03_Manifestation", "summon-agents"))
        if os.path.isdir(candidate):
            return candidate
    # Fallback to environment variable
    return os.environ.get("SUMMON_AGENTS_ROOT")


# ---------------------------------------------------------------------------
# YAML Frontmatter Parser (Minimal / No Dependencies)
# ---------------------------------------------------------------------------

def _strip_yaml_inline_comment(value: str) -> str:
    """
    Strip YAML inline comments for unquoted scalars.
    Example: 'status: todo # comment' -> 'todo'
    """
    in_single = False
    in_double = False
    escaped = False

    for i, ch in enumerate(value):
        if escaped:
            escaped = False
            continue
        if ch == "\\" and in_double:
            escaped = True
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            continue
        if ch == "#" and not in_single and not in_double:
            if i == 0 or value[i - 1].isspace():
                return value[:i].rstrip()
    return value


def _unquote_yaml_scalar(value: str) -> str:
    if len(value) >= 2 and ((value[0] == value[-1] == '"') or (value[0] == value[-1] == "'")):
        return value[1:-1]
    return value


def _parse_inline_yaml_list(value: str) -> List[str]:
    inner = value[1:-1].strip()
    if not inner:
        return []
    parts = [p.strip() for p in inner.split(",")]
    return [_unquote_yaml_scalar(p) for p in parts if p]


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, content

    lines = content.split("\n")
    end_index = -1
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = i
            break

    if end_index == -1:
        return {}, content

    frontmatter_lines = lines[1:end_index]
    body = "\n".join(lines[end_index + 1:]).strip()

    # Minimal YAML parsing (supports scalars, inline lists, multiline lists, 1-level nested dict)
    frontmatter: Dict[str, Any] = {}
    current_key: Optional[str] = None
    current_kind: Optional[str] = None  # "list" | "dict"

    for line in frontmatter_lines:
        raw = line.rstrip("\n")
        if not raw.strip():
            continue

        # List item
        if raw.lstrip().startswith("- "):
            if current_key and current_kind == "list" and isinstance(frontmatter.get(current_key), list):
                frontmatter[current_key].append(raw.lstrip()[2:].strip())
            continue

        # Nested object (e.g. execution:)
        if raw.strip().endswith(":") and not raw.lstrip().startswith("-"):
            key = raw.strip()[:-1].strip()
            frontmatter[key] = {}
            current_key = key
            current_kind = "dict"
            continue

        if ":" in raw:
            parts = raw.strip().split(":", 1)
            key = parts[0].strip()
            value_raw = _strip_yaml_inline_comment(parts[1].strip())
            value_raw = _unquote_yaml_scalar(value_raw)

            if value_raw.startswith("[") and value_raw.endswith("]"):
                parsed: Any = _parse_inline_yaml_list(value_raw)
            elif value_raw == "":
                frontmatter[key] = []
                current_key = key
                current_kind = "list"
                continue
            elif value_raw == "{}":
                parsed = {}
            else:
                parsed = value_raw

            # Detect leading spaces for nested objects
            leading_spaces = len(line) - len(line.lstrip())
            if leading_spaces > 0 and current_key and current_kind == "dict" and isinstance(frontmatter.get(current_key), dict):
                frontmatter[current_key][key] = parsed
            else:
                frontmatter[key] = parsed
                current_key = None
                current_kind = None

    return frontmatter, body


def serialize_frontmatter(frontmatter: Dict[str, Any]) -> str:
    """Serialize frontmatter dict back to YAML string."""
    lines = ["---"]
    for key, value in frontmatter.items():
        if isinstance(value, dict):
            lines.append(f"{key}:")
            for k, v in value.items():
                if isinstance(v, list):
                    if not v:
                        lines.append(f"  {k}: []")
                    else:
                        lines.append(f"  {k}:")
                        for item in v:
                            lines.append(f"    - {str(item)}")
                elif isinstance(v, (int, float)):
                    lines.append(f"  {k}: {v}")
                else:
                    lines.append(f'  {k}: "{str(v)}"')
        elif isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {str(item)}")
        elif isinstance(value, (int, float)):
            lines.append(f"{key}: {value}")
        else:
            lines.append(f'{key}: "{str(value)}"')
    lines.append("---")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class TicketData:
    path: str
    frontmatter: Dict[str, Any]
    body: str
    title: str = ""
    description: str = ""
    action_items: List[str] = field(default_factory=list)
    definition_of_done: List[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        return str(self.frontmatter.get("status", "todo")).lower()

    @property
    def priority(self) -> str:
        return str(self.frontmatter.get("priority", "P2"))

    @property
    def tags(self) -> List[str]:
        tags = self.frontmatter.get("tags", [])
        if isinstance(tags, str):
            return [tags]
        return list(tags)

    @property
    def dependencies(self) -> List[str]:
        deps = self.frontmatter.get("dependencies", [])
        if isinstance(deps, str):
            return [deps]
        return list(deps)

    @property
    def target_path(self) -> Optional[str]:
        return self.frontmatter.get("target_path")


@dataclass
class AgentResult:
    id: str
    provider: str
    success: bool
    returncode: Optional[int]
    timed_out: bool
    output: str
    error: str
    execution_time: float
    timestamp: str


@dataclass
class AgentGroupPlan:
    """Plan for agent group execution (aligns with SPEC.md Section 2.2)."""
    type: str  # single | council | sequential
    agents: List[str]
    context_passing: str = "summary"  # full | summary | delta (sequential only)
    max_iterations: int = 1  # iterative refinement only

    def __post_init__(self) -> None:
        if self.type not in VALID_GROUP_TYPES:
            raise ValueError(f"Invalid group type: {self.type}")
        if self.context_passing not in VALID_CONTEXT_PASSING:
            raise ValueError(f"Invalid context_passing: {self.context_passing}")


@dataclass
class ExecutionResult:
    status: str  # success, partial, error
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    ticket_path: str = ""
    original_status: str = ""
    final_status: str = ""
    agent_group: Optional[AgentGroupPlan] = None
    started_at: str = ""
    completed_at: str = ""
    execution_time: float = 0.0
    context_file: Optional[str] = None
    agent_results: List[AgentResult] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Ticket Parsing
# ---------------------------------------------------------------------------

def parse_ticket(ticket_path: str) -> TicketData:
    """Parse a ticket file and extract structured data."""
    path = Path(ticket_path)
    if not path.exists():
        raise FileNotFoundError(f"Ticket not found: {ticket_path}")

    content = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(content)

    # Extract title (first # heading)
    title = ""
    title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    elif frontmatter.get("title"):
        title = str(frontmatter["title"])

    # Extract description (## Description section; aligns with COF ticket template)
    description = ""
    desc_match = re.search(r"##\s*Description\s*\n+([\s\S]*?)(?=\n##|\Z)", body, re.IGNORECASE)
    if desc_match:
        description = desc_match.group(1).strip()

    # Extract action items (## Action Items section)
    action_items: List[str] = []
    action_match = re.search(r"##\s*Action\s*Items?\s*\n+([\s\S]*?)(?=\n##|\Z)", body, re.IGNORECASE)
    if action_match:
        for line in action_match.group(1).split("\n"):
            line = line.strip()
            if line.startswith("- ") or line.startswith("* "):
                item = line[2:].strip()
                item = re.sub(r"^\[[ xX]\]\s*", "", item)  # markdown checkbox
                if item:
                    action_items.append(item)
            elif re.match(r"^\d+\.", line):
                item = re.sub(r"^\d+\.\s*", "", line).strip()
                item = re.sub(r"^\[[ xX]\]\s*", "", item)
                if item:
                    action_items.append(item)

    # Extract Definition of Done
    dod: List[str] = []
    dod_match = re.search(r"##\s*Definition\s*of\s*Done\s*\n+([\s\S]*?)(?=\n##|\Z)", body, re.IGNORECASE)
    if dod_match:
        for line in dod_match.group(1).split("\n"):
            line = line.strip()
            if line.startswith("- ") or line.startswith("* "):
                item = line[2:].strip()
                item = re.sub(r"^\[[ xX]\]\s*", "", item)
                if item:
                    dod.append(item)
            elif re.match(r"^\d+\.", line):
                item = re.sub(r"^\d+\.\s*", "", line).strip()
                item = re.sub(r"^\[[ xX]\]\s*", "", item)
                if item:
                    dod.append(item)

    return TicketData(
        path=str(path.absolute()),
        frontmatter=frontmatter,
        body=body,
        title=title,
        description=description,
        action_items=action_items,
        definition_of_done=dod,
    )


# ---------------------------------------------------------------------------
# Agent Group Selection
# ---------------------------------------------------------------------------

def select_group_plan(ticket: TicketData, args: argparse.Namespace) -> AgentGroupPlan:
    """Select the appropriate agent group based on ticket tags and CLI arguments.

    Selection priority:
    1. Explicit CLI override (--all or --provider)
    2. Group execution tags (council/sequential)
    3. Single provider tag mapping
    4. Default fallback (claude)
    """
    # Explicit override
    if getattr(args, "all", False):
        return AgentGroupPlan(type="council", agents=AVAILABLE_PROVIDERS)
    if getattr(args, "provider", None):
        return AgentGroupPlan(type="single", agents=[args.provider])

    tags = {t.lower() for t in ticket.tags}

    # Group execution selection
    if tags & COUNCIL_TAGS:
        return AgentGroupPlan(type="council", agents=AVAILABLE_PROVIDERS)
    if tags & SEQUENTIAL_TAGS:
        return AgentGroupPlan(
            type="sequential",
            agents=AVAILABLE_PROVIDERS,
            context_passing="summary",
        )

    # Single provider selection by tag
    for tag in ticket.tags:
        tag_lower = tag.lower()
        if tag_lower in SINGLE_PROVIDER_TAG_MAP:
            return AgentGroupPlan(
                type="single",
                agents=[SINGLE_PROVIDER_TAG_MAP[tag_lower]],
            )

    # Default fallback
    return AgentGroupPlan(type="single", agents=[DEFAULT_AGENT])


# ---------------------------------------------------------------------------
# Context Indexing
# ---------------------------------------------------------------------------

def run_context_indexing(
    target_dir: str,
    max_depth: int,
    cof_root: str,
) -> Tuple[Optional[str], Optional[str], List[str], Optional[str], Optional[Dict[str, Any]]]:
    """
    Run cof-glob-indexing and return paths to NODE_INDEX.md and ROLE_EVIDENCE.md.
    Returns (node_index_path, role_evidence_path, warnings, error_code, raw_json).
    """
    warnings: List[str] = []

    script_path = os.path.join(cof_root, "skills", "01.cof-glob-indexing", "scripts", "cof_glob_indexing.py")
    if not os.path.isfile(script_path):
        warnings.append(f"cof-glob-indexing script not found: {script_path}")
        return None, None, warnings, "SCRIPT_NOT_FOUND", None

    cmd = [
        sys.executable,
        script_path,
        "--target-dir", target_dir,
        "--max-depth", str(max_depth),
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = result.stdout.strip()

        if result.returncode != 0:
            stdout = (result.stdout or "").strip()
            stderr = (result.stderr or "").strip()

            # cof-glob-indexing prints JSON even on error; prefer its structured error_code when possible.
            try:
                data = json.loads(stdout) if stdout else None
            except Exception:
                data = None

            if isinstance(data, dict) and data.get("status") == "error":
                warnings.append(f"cof-glob-indexing failed: {json.dumps(data, ensure_ascii=False, indent=2)}")
                return None, None, warnings, str(data.get("error_code") or "UNKNOWN_ERROR"), data

            msg = stderr or stdout
            warnings.append(f"cof-glob-indexing failed: {msg}")
            return None, None, warnings, "SUBPROCESS_FAILED", None

        # Parse JSON output
        data = json.loads(output)
        if data.get("status") == "error":
            warnings.append(f"cof-glob-indexing error: {data.get('error_code')}")
            return None, None, warnings, str(data.get("error_code") or "UNKNOWN_ERROR"), data

        artifacts = data.get("artifacts", {})
        node_index = artifacts.get("node_index")
        role_evidence = artifacts.get("role_evidence")

        if data.get("warnings"):
            for w in data["warnings"]:
                warnings.append(f"indexing warning: {w.get('path', '')} - {w.get('reason', '')}")

        return node_index, role_evidence, warnings, None, data

    except subprocess.TimeoutExpired:
        warnings.append("cof-glob-indexing timed out")
        return None, None, warnings, "TIMEOUT", None
    except json.JSONDecodeError as e:
        warnings.append(f"Failed to parse indexing output: {e}")
        return None, None, warnings, "INVALID_JSON", None
    except Exception as e:
        warnings.append(f"Indexing error: {e}")
        return None, None, warnings, "UNKNOWN_EXCEPTION", None


def _safe_filename(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9._-]+", "_", s).strip("_")
    return s or "unknown"


def _write_indexing_failure_artifact(
    *,
    ticket: TicketData,
    agents_task_context_dir: str,
    target_dir: str,
    cof_root: str,
    error_code: str,
    error_message: str,
    raw_json: Optional[Dict[str, Any]],
    warnings: List[str],
) -> str:
    timestamp = _utc_now_iso().replace(":", "").replace("-", "")
    ticket_stem = _safe_filename(Path(ticket.path).stem)
    artifact_name = f"INDEXING_FAILURE_{ticket_stem}_{timestamp}.json"
    artifact_path = os.path.join(agents_task_context_dir, artifact_name)

    payload = {
        "type": "cof-indexing-failure",
        "timestamp": _utc_now_iso(),
        "ticket_path": ticket.path,
        "target_dir": target_dir,
        "cof_root": cof_root,
        "error_code": error_code,
        "error_message": error_message,
        "warnings": warnings,
        "raw": raw_json,
        "recommended_action": (
            "A directory admin should create a COF index anchor (e.g., '00.index/' or '01.index/') "
            "at the appropriate node boundary above target_dir, then re-run solve_ticket."
        ),
    }

    Path(artifact_path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return artifact_path


def append_indexing_failure_evidence(
    ticket: TicketData,
    *,
    error_code: str,
    error_message: str,
    target_dir: str,
    cof_root: str,
    artifact_path: str,
    raw_json: Optional[Dict[str, Any]],
    warnings: List[str],
) -> None:
    """Append indexing failure evidence section to ticket body."""
    content = Path(ticket.path).read_text(encoding="utf-8")

    content = re.sub(
        r"\n## Indexing Failure Evidence\n[\s\S]*?(?=\n## |\Z)",
        "",
        content,
        flags=re.MULTILINE,
    )

    lines: List[str] = []
    lines.append("\n## Indexing Failure Evidence\n")
    lines.append("\n**ADMIN ACTION REQUIRED**: COF index anchor not found or indexing failed.\n\n")
    lines.append(f"- **Timestamp (UTC)**: {_utc_now_iso()}\n")
    lines.append(f"- **Error Code**: `{error_code}`\n")
    lines.append(f"- **Error Message**: {error_message}\n")
    lines.append(f"- **Target Dir**: `{target_dir}`\n")
    lines.append(f"- **COF Root**: `{cof_root}`\n")
    lines.append(f"- **Artifact**: `{artifact_path}`\n")
    lines.append("\n### Recommended Remediation\n")
    lines.append(
        "- Create a COF index anchor directory (e.g., `00.index/`) at the intended node boundary above the target.\n"
    )
    lines.append("- Re-run ticket solving after the node boundary is established.\n")

    if raw_json is not None:
        lines.append("\n### Indexer Output (JSON)\n\n```json\n")
        lines.append(json.dumps(raw_json, ensure_ascii=False, indent=2)[:8000])
        lines.append("\n```\n")

    if warnings:
        lines.append("\n### Warnings\n")
        for w in warnings[:20]:
            lines.append(f"- {w}\n")

    content = content.rstrip() + "\n" + "".join(lines)
    Path(ticket.path).write_text(content, encoding="utf-8")


def append_indexing_failure_log(
    *,
    ticket: TicketData,
    agents_task_context_dir: str,
    artifact_path: str,
    error_code: str,
    error_message: str,
) -> None:
    """Append a lightweight entry to AGENT_LOG.md for directory admins."""
    log_path = os.path.join(agents_task_context_dir, "AGENT_LOG.md")
    if not os.path.isfile(log_path):
        Path(log_path).write_text("# Agent Execution Log\n\n", encoding="utf-8")

    timestamp = _utc_now_iso()
    ticket_filename = os.path.basename(ticket.path)
    relative_ticket = os.path.relpath(ticket.path, agents_task_context_dir)
    relative_artifact = os.path.relpath(artifact_path, agents_task_context_dir)

    lines = [f"\n## [{timestamp}] {ticket_filename} (INDEXING FAILED)\n\n"]
    lines.append(f"- **Error Code**: `{error_code}`\n")
    lines.append(f"- **Error Message**: {error_message}\n")
    lines.append(f"- **Ticket Path**: {relative_ticket}\n")
    lines.append(f"- **Evidence Artifact**: {relative_artifact}\n")
    lines.append("\n---\n")

    with open(log_path, "a", encoding="utf-8") as f:
        f.writelines(lines)


# ---------------------------------------------------------------------------
# Context Assembly
# ---------------------------------------------------------------------------

def assemble_context(
    ticket: TicketData,
    node_index_path: Optional[str],
    role_evidence_path: Optional[str],
) -> str:
    """Assemble the context for the agent prompt."""
    sections: List[str] = ["# Task Context\n"]

    # Node Structure
    if node_index_path and os.path.isfile(node_index_path):
        sections.append("## Node Structure\n")
        sections.append(Path(node_index_path).read_text(encoding="utf-8"))
        sections.append("\n")

    # Role Evidence
    if role_evidence_path and os.path.isfile(role_evidence_path):
        sections.append("## Role Evidence\n")
        sections.append(Path(role_evidence_path).read_text(encoding="utf-8"))
        sections.append("\n")

    # Ticket Content
    sections.append("## Ticket\n")
    sections.append(f"**Title**: {ticket.title}\n")
    sections.append(f"**Priority**: {ticket.priority}\n")
    sections.append(f"**Tags**: {', '.join(ticket.tags)}\n\n")

    if ticket.description:
        sections.append("### Description\n")
        sections.append(ticket.description)
        sections.append("\n\n")

    if ticket.action_items:
        sections.append("### Action Items\n")
        for i, item in enumerate(ticket.action_items, 1):
            sections.append(f"{i}. {item}\n")
        sections.append("\n")

    if ticket.definition_of_done:
        sections.append("### Definition of Done\n")
        for item in ticket.definition_of_done:
            sections.append(f"- {item}\n")
        sections.append("\n")

    sections.append("---\n\n")
    sections.append("Please complete all action items above. Ensure all Definition of Done criteria are met.\n")

    return "".join(sections)


def create_minimal_context(ticket: TicketData) -> str:
    """Create minimal context when indexing fails."""
    sections: List[str] = [
        "# Minimal Context\n\n",
        "Unable to perform full context indexing. Working with ticket content only.\n\n",
        "## Ticket\n\n",
        f"**Title**: {ticket.title}\n",
        f"**Priority**: {ticket.priority}\n",
        f"**Tags**: {', '.join(ticket.tags)}\n\n",
    ]

    if ticket.description:
        sections.append("### Description\n")
        sections.append(ticket.description)
        sections.append("\n\n")

    if ticket.action_items:
        sections.append("### Action Items\n")
        for i, item in enumerate(ticket.action_items, 1):
            sections.append(f"{i}. {item}\n")
        sections.append("\n")

    if ticket.definition_of_done:
        sections.append("### Definition of Done\n")
        for item in ticket.definition_of_done:
            sections.append(f"- {item}\n")

    return "".join(sections)


# ---------------------------------------------------------------------------
# Agent Dispatch
# ---------------------------------------------------------------------------

def dispatch_agent(
    agent: str,
    context_file: str,
    prompt: str,
    timeout: int,
    summon_agents_root: str,
) -> List[AgentResult]:
    """Dispatch to collaborate.py and return results."""
    script_path = os.path.join(
        summon_agents_root, "skill", "sa-call-cli-agents", "scripts", "collaborate.py"
    )

    if not os.path.isfile(script_path):
        return [AgentResult(
            id=f"{agent}_0",
            provider=agent,
            success=False,
            returncode=None,
            timed_out=False,
            output="",
            error=f"collaborate.py not found: {script_path}",
            execution_time=0.0,
            timestamp=_utc_now_iso(),
        )]

    cmd = [
        sys.executable,
        script_path,
        "run",
        "--context", context_file,
        "-m", prompt,
        "--format", "json",
        "--timeout", str(timeout),
    ]

    if agent == "all":
        cmd.append("--all")
    else:
        cmd.extend(["-p", agent])

    start_time = datetime.now(timezone.utc)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout + 30,  # Extra buffer for subprocess overhead
        )

        execution_time = (datetime.now(timezone.utc) - start_time).total_seconds()

        # Try to parse JSON output
        try:
            # Find JSON array in output (may have other text before it)
            output = result.stdout
            json_start = output.find("[")
            json_end = output.rfind("]") + 1
            if json_start >= 0 and json_end > json_start:
                json_str = output[json_start:json_end]
                results_data = json.loads(json_str)
                return [
                    AgentResult(
                        id=r.get("id", f"{agent}_0"),
                        provider=r.get("provider", agent),
                        success=r.get("success", False),
                        returncode=r.get("returncode"),
                        timed_out=r.get("timed_out", False),
                        output=r.get("output", ""),
                        error=r.get("error", ""),
                        execution_time=r.get("execution_time", execution_time),
                        timestamp=r.get("timestamp", _utc_now_iso()),
                    )
                    for r in results_data
                ]
        except json.JSONDecodeError:
            pass

        # Fallback: return raw output as single result
        return [AgentResult(
            id=f"{agent}_0",
            provider=agent,
            success=result.returncode == 0,
            returncode=result.returncode,
            timed_out=False,
            output=result.stdout,
            error=result.stderr,
            execution_time=execution_time,
            timestamp=_utc_now_iso(),
        )]

    except subprocess.TimeoutExpired:
        execution_time = (datetime.now(timezone.utc) - start_time).total_seconds()
        return [AgentResult(
            id=f"{agent}_0",
            provider=agent,
            success=False,
            returncode=None,
            timed_out=True,
            output="",
            error=f"Command timed out after {timeout} seconds",
            execution_time=execution_time,
            timestamp=_utc_now_iso(),
        )]
    except Exception as e:
        return [AgentResult(
            id=f"{agent}_0",
            provider=agent,
            success=False,
            returncode=None,
            timed_out=False,
            output="",
            error=str(e),
            execution_time=0.0,
            timestamp=_utc_now_iso(),
        )]


def _summarize_output(output: str, max_length: int = 2000) -> str:
    """Summarize agent output for context passing in sequential mode."""
    if len(output) <= max_length:
        return output
    # Keep first and last portions
    half = max_length // 2
    return output[:half] + "\n\n... [truncated] ...\n\n" + output[-half:]


def _build_sequential_context(
    base_context: str,
    previous_results: List[AgentResult],
    context_passing: str,
) -> str:
    """Build rolling context for sequential group execution."""
    sections = [base_context]

    if not previous_results:
        return base_context

    sections.append("\n\n---\n\n## Previous Agent Results\n")

    for i, result in enumerate(previous_results, 1):
        sections.append(f"\n### Step {i}: {result.provider.upper()}\n")
        sections.append(f"- Status: {'SUCCESS' if result.success else 'FAILED'}\n")

        if context_passing == "full":
            sections.append(f"\n#### Output\n\n{result.output}\n")
        elif context_passing == "summary":
            sections.append(f"\n#### Output (summarized)\n\n{_summarize_output(result.output)}\n")
        elif context_passing == "delta":
            # For delta, only include the last result
            if i == len(previous_results):
                sections.append(f"\n#### Output\n\n{result.output}\n")

    sections.append("\n---\n\nContinue from the previous results. Build upon what was done.\n")

    return "".join(sections)


def dispatch_group(
    group_plan: AgentGroupPlan,
    context_file: str,
    prompt: str,
    timeout: int,
    summon_agents_root: str,
) -> List[AgentResult]:
    """Dispatch agent group based on plan type (single, council, sequential)."""

    if group_plan.type == "single":
        # Single agent execution
        return dispatch_agent(
            group_plan.agents[0],
            context_file,
            prompt,
            timeout,
            summon_agents_root,
        )

    elif group_plan.type == "council":
        # Council mode: dispatch to all agents in parallel
        return dispatch_agent(
            "all",
            context_file,
            prompt,
            timeout,
            summon_agents_root,
        )

    elif group_plan.type == "sequential":
        # Sequential mode: execute agents in order, passing context
        all_results: List[AgentResult] = []
        base_context = Path(context_file).read_text(encoding="utf-8")

        for i, agent in enumerate(group_plan.agents):
            # Build rolling context with previous results
            rolling_context = _build_sequential_context(
                base_context,
                all_results,
                group_plan.context_passing,
            )

            # Write rolling context to temp file
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", delete=False, encoding="utf-8"
            ) as f:
                f.write(rolling_context)
                rolling_context_file = f.name

            try:
                # Dispatch to current agent
                results = dispatch_agent(
                    agent,
                    rolling_context_file,
                    prompt,
                    timeout,
                    summon_agents_root,
                )

                # Update result IDs to reflect sequence
                for j, result in enumerate(results):
                    result.id = f"seq_{i}_{agent}_{j}"

                all_results.extend(results)

                # Check if agent failed - stop sequence on failure
                if not all(r.success for r in results):
                    break

            finally:
                # Cleanup temp file
                try:
                    os.unlink(rolling_context_file)
                except Exception:
                    pass

        return all_results

    else:
        # Unknown type - should not happen due to validation
        return [AgentResult(
            id="error_0",
            provider="unknown",
            success=False,
            returncode=None,
            timed_out=False,
            output="",
            error=f"Unknown group type: {group_plan.type}",
            execution_time=0.0,
            timestamp=_utc_now_iso(),
        )]


# ---------------------------------------------------------------------------
# Ticket Update
# ---------------------------------------------------------------------------

def update_ticket_status(ticket: TicketData, new_status: str, execution_meta: Dict[str, Any]) -> None:
    """Update ticket frontmatter with new status and execution metadata (preserves body)."""
    ticket.frontmatter["status"] = new_status
    ticket.frontmatter.setdefault("execution", {})
    if isinstance(ticket.frontmatter["execution"], dict):
        ticket.frontmatter["execution"].update(execution_meta)
    else:
        ticket.frontmatter["execution"] = execution_meta

    current = Path(ticket.path).read_text(encoding="utf-8")
    current_frontmatter, current_body = parse_frontmatter(current)
    if not current_frontmatter:
        current_body = current.strip()

    current_frontmatter.update(ticket.frontmatter)
    new_frontmatter = serialize_frontmatter(current_frontmatter)
    Path(ticket.path).write_text(f"{new_frontmatter}\n\n{current_body}\n", encoding="utf-8")


def _retry_timed_out(
    results: List[AgentResult],
    context_file: str,
    prompt: str,
    timeout: int,
    summon_agents_root: str,
    max_retries: int,
    timeout_delta: int,
) -> Tuple[List[AgentResult], List[str]]:
    warnings: List[str] = []
    updated = list(results)

    for attempt in range(max_retries):
        timed_out_providers = sorted({r.provider for r in updated if r.timed_out})
        if not timed_out_providers:
            break

        retry_timeout = timeout + (attempt + 1) * timeout_delta
        warnings.append(
            f"Retrying timed-out agent(s) (attempt {attempt + 1}/{max_retries}, timeout={retry_timeout}s): "
            + ", ".join(timed_out_providers)
        )

        for provider in timed_out_providers:
            retry_results = dispatch_agent(
                provider,
                context_file,
                prompt,
                retry_timeout,
                summon_agents_root,
            )
            replacement = retry_results[0] if retry_results else None
            if replacement is None:
                continue

            updated = [replacement if r.provider == provider and r.timed_out else r for r in updated]

    return updated, warnings


def append_execution_result(
    ticket: TicketData,
    results: List[AgentResult],
    group_plan: Optional[AgentGroupPlan] = None,
) -> None:
    """Append execution result section to ticket body."""
    content = Path(ticket.path).read_text(encoding="utf-8")

    # Remove existing Execution Result section if present
    content = re.sub(
        r"\n## Execution Result\n[\s\S]*?(?=\n## |\Z)",
        "",
        content,
        flags=re.MULTILINE,
    )

    # Build new section
    section_lines = ["\n## Execution Result\n"]

    # Add group plan info if available
    if group_plan:
        section_lines.append(f"- **Group Type**: {group_plan.type}\n")
        section_lines.append(f"- **Agents**: {', '.join(group_plan.agents)}\n")
        if group_plan.type == "sequential":
            section_lines.append(f"- **Context Passing**: {group_plan.context_passing}\n")
        section_lines.append("\n")

    for result in results:
        section_lines.append(f"### {result.provider.upper()}\n")
        section_lines.append(f"- **Timestamp**: {result.timestamp}\n")
        section_lines.append(f"- **Execution Time**: {result.execution_time:.2f}s\n")

        if result.timed_out:
            section_lines.append("- **Status**: TIMED OUT\n")
        elif result.success:
            section_lines.append("- **Status**: SUCCESS\n")
        else:
            section_lines.append("- **Status**: FAILED\n")

        if result.output:
            section_lines.append("\n#### Output\n\n")
            section_lines.append("```\n")
            section_lines.append(result.output[:10000])  # Limit output size
            if len(result.output) > 10000:
                section_lines.append("\n... (truncated)")
            section_lines.append("\n```\n")

        if result.error:
            section_lines.append("\n#### Errors\n\n")
            section_lines.append("```\n")
            section_lines.append(result.error[:2000])
            section_lines.append("\n```\n")

        section_lines.append("\n")

    content = content.rstrip() + "\n" + "".join(section_lines)
    Path(ticket.path).write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Agent Log
# ---------------------------------------------------------------------------

def append_agent_log(
    ticket: TicketData,
    results: List[AgentResult],
    agents_task_context_dir: str,
) -> None:
    """Append entry to AGENT_LOG.md."""
    log_path = os.path.join(agents_task_context_dir, "AGENT_LOG.md")

    # Ensure file exists with header
    if not os.path.isfile(log_path):
        Path(log_path).write_text("# Agent Execution Log\n\n", encoding="utf-8")

    timestamp = _utc_now_iso()
    ticket_filename = os.path.basename(ticket.path)
    relative_path = os.path.relpath(ticket.path, agents_task_context_dir)

    lines = [f"\n## [{timestamp}] {ticket_filename}\n\n"]

    for result in results:
        result_status = "success" if result.success else ("timed_out" if result.timed_out else "failed")
        lines.append(f"- **Agent**: {result.provider}\n")
        lines.append(f"- **Execution Time**: {result.execution_time:.2f}s\n")
        lines.append(f"- **Result**: {result_status}\n")
        lines.append(f"- **Exit Code**: {result.returncode}\n")

    lines.append(f"- **Ticket Path**: {relative_path}\n")
    lines.append("\n---\n")

    with open(log_path, "a", encoding="utf-8") as f:
        f.writelines(lines)


# ---------------------------------------------------------------------------
# Main Workflow
# ---------------------------------------------------------------------------

def solve_ticket(args: argparse.Namespace) -> ExecutionResult:
    """Main workflow: parse -> index -> select -> dispatch -> integrate."""
    result = ExecutionResult(status="error")
    started_at = _utc_now_iso()
    result.started_at = started_at

    # Step 1: Parse ticket
    try:
        ticket = parse_ticket(args.ticket)
        result.ticket_path = ticket.path
        result.original_status = ticket.status
    except FileNotFoundError as e:
        result.error_code = "TICKET_NOT_FOUND"
        result.error_message = str(e)
        return result
    except Exception as e:
        result.error_code = "TICKET_PARSE_ERROR"
        result.error_message = str(e)
        return result

    if ticket.status not in VALID_STATUSES:
        result.error_code = "TICKET_INVALID_STATUS"
        result.error_message = f"Invalid ticket status: {ticket.frontmatter.get('status')!r}"
        return result

    # Check if already done
    if ticket.status == "done":
        result.status = "success"
        result.final_status = "done"
        result.warnings.append("Ticket already done, no action taken")
        return result

    # Detect paths
    ticket_dir = os.path.dirname(ticket.path)
    cof_root = _detect_cof_root(ticket_dir) or os.environ.get("COF_ROOT", "")
    summon_agents_root = _detect_summon_agents_root(cof_root)

    if not summon_agents_root:
        result.error_code = "SUMMON_AGENTS_NOT_FOUND"
        result.error_message = "Could not locate summon-agents directory"
        return result

    # Find agents-task-context directory (parent of tickets/)
    agents_task_context_dir = os.path.dirname(ticket_dir)
    if not os.path.basename(ticket_dir) == "tickets":
        # Ticket might not be in standard location
        agents_task_context_dir = ticket_dir

    # Step 2: Update status to in-progress (unless dry-run)
    if not args.dry_run:
        try:
            update_ticket_status(ticket, "in-progress", {
                "started_at": started_at,
                "agent_group": "pending",
            })
        except Exception as e:
            result.warnings.append(f"Failed to update status: {e}")

    # Step 3: Index context
    node_index_path: Optional[str] = None
    role_evidence_path: Optional[str] = None

    if not args.skip_indexing and cof_root:
        target_dir = ticket.target_path or ticket_dir
        node_index_path, role_evidence_path, index_warnings, index_error_code, index_raw = run_context_indexing(
            target_dir,
            args.context_depth,
            cof_root,
        )
        result.warnings.extend(index_warnings)
    else:
        target_dir = ticket.target_path or ticket_dir
        index_error_code = "COF_ROOT_NOT_DETECTED"
        index_raw = None

    # If indexing failed / no artifacts, hedge by stopping and recording evidence unless explicitly allowed.
    if not args.dry_run and not args.skip_indexing and not (node_index_path or role_evidence_path):
        allow_minimal = bool(getattr(args, "allow_minimal_context", False))
        if not allow_minimal:
            result.error_code = "CONTEXT_INDEXING_FAILED"
            result.error_message = (
                f"Context indexing produced no artifacts (index_error_code={index_error_code}). "
                "Admin must establish COF node boundary/index anchors."
            )
            result.final_status = "blocked"
            completed_at = _utc_now_iso()
            result.completed_at = completed_at
            result.execution_time = (datetime.now(timezone.utc) - datetime.fromisoformat(started_at)).total_seconds()

            try:
                artifact_path = _write_indexing_failure_artifact(
                    ticket=ticket,
                    agents_task_context_dir=agents_task_context_dir,
                    target_dir=target_dir,
                    cof_root=cof_root,
                    error_code=str(index_error_code or "UNKNOWN"),
                    error_message=result.error_message,
                    raw_json=index_raw,
                    warnings=result.warnings,
                )
            except Exception as e:
                artifact_path = ""
                result.warnings.append(f"Failed to write indexing failure artifact: {e}")

            # Update ticket to blocked + include metadata and evidence section
            try:
                execution_meta = {
                    "started_at": started_at,
                    "completed_at": completed_at,
                    "indexing_status": "failed",
                    "indexing_error_code": str(index_error_code or "UNKNOWN"),
                    "indexing_target_dir": target_dir,
                    "indexing_cof_root": cof_root,
                    "indexing_artifact": artifact_path,
                    "result": "indexing_failed",
                }
                update_ticket_status(ticket, "blocked", execution_meta)
            except Exception as e:
                result.warnings.append(f"Failed to update ticket status to blocked: {e}")

            try:
                append_indexing_failure_evidence(
                    ticket,
                    error_code=str(index_error_code or "UNKNOWN"),
                    error_message=result.error_message,
                    target_dir=target_dir,
                    cof_root=cof_root,
                    artifact_path=artifact_path,
                    raw_json=index_raw,
                    warnings=result.warnings,
                )
            except Exception as e:
                result.warnings.append(f"Failed to append indexing failure evidence: {e}")

            try:
                if artifact_path:
                    append_indexing_failure_log(
                        ticket=ticket,
                        agents_task_context_dir=agents_task_context_dir,
                        artifact_path=artifact_path,
                        error_code=str(index_error_code or "UNKNOWN"),
                        error_message=result.error_message,
                    )
            except Exception as e:
                result.warnings.append(f"Failed to append indexing failure log: {e}")

            return result

    if getattr(args, "require_indexing", False) and not (node_index_path or role_evidence_path):
        result.error_code = "CONTEXT_INDEXING_FAILED"
        result.error_message = "Indexing did not produce artifacts and --require-indexing was set"
        if not args.dry_run:
            try:
                update_ticket_status(ticket, "blocked", {"result": "indexing_failed"})
            except Exception as e:
                result.warnings.append(f"Failed to update ticket after indexing failure: {e}")
        return result

    # Step 4: Select agent group
    group_plan = select_group_plan(ticket, args)
    result.agent_group = group_plan

    # Update ticket with selected agent group
    if not args.dry_run:
        try:
            ticket.frontmatter.setdefault("execution", {})
            if not isinstance(ticket.frontmatter["execution"], dict):
                ticket.frontmatter["execution"] = {}
            ticket.frontmatter["execution"]["agent_group"] = {
                "type": group_plan.type,
                "agents": group_plan.agents,
                "context_passing": group_plan.context_passing,
            }
            update_ticket_status(ticket, "in-progress", ticket.frontmatter["execution"])
        except Exception as e:
            result.warnings.append(f"Failed to update agent group: {e}")

    # Step 5: Assemble context
    if node_index_path or role_evidence_path:
        context_content = assemble_context(ticket, node_index_path, role_evidence_path)
    else:
        context_content = create_minimal_context(ticket)
        result.warnings.append("Using minimal context (indexing unavailable)")

    # Write context to temp file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
        f.write(context_content)
        context_file = f.name
    result.context_file = context_file

    # Build prompt
    prompt_parts = []
    if ticket.action_items:
        prompt_parts.append("Complete the following action items:\n")
        for i, item in enumerate(ticket.action_items, 1):
            prompt_parts.append(f"{i}. {item}\n")

    if ticket.definition_of_done:
        prompt_parts.append("\nEnsure these criteria are met:\n")
        for item in ticket.definition_of_done:
            prompt_parts.append(f"- {item}\n")

    prompt = "".join(prompt_parts) if prompt_parts else f"Complete the task: {ticket.title}"

    # Dry run - stop here
    if args.dry_run:
        result.status = "success"
        result.final_status = ticket.status
        result.warnings.append("Dry run - no execution performed")
        print(f"[DRY RUN] Would dispatch to: {group_plan.type} group with {group_plan.agents}")
        print(f"[DRY RUN] Context file: {context_file}")
        print(f"[DRY RUN] Prompt:\n{prompt}")
        return result

    # Step 6: Dispatch based on group type
    agent_results = dispatch_group(
        group_plan,
        context_file,
        prompt,
        args.timeout,
        summon_agents_root,
    )

    agent_results, retry_warnings = _retry_timed_out(
        agent_results,
        context_file,
        prompt,
        args.timeout,
        summon_agents_root,
        args.max_retries,
        args.retry_timeout_delta,
    )
    result.warnings.extend(retry_warnings)
    result.agent_results = agent_results

    # Step 7: Determine final status
    all_success = all(r.success for r in agent_results)
    any_timeout = any(r.timed_out for r in agent_results)

    completed_at = _utc_now_iso()
    result.completed_at = completed_at
    total_time = sum(r.execution_time for r in agent_results)
    result.execution_time = total_time

    if all_success:
        final_status = "done"
        result.status = "success"
    elif any_timeout:
        final_status = "blocked"
        result.status = "partial"
        result.warnings.append("Agent(s) timed out (after retries)")
    else:
        final_status = "blocked"
        result.status = "error"
        result.error_code = "AGENT_FAILED"
        result.error_message = "; ".join(r.error for r in agent_results if r.error)

    result.final_status = final_status

    # Step 8: Update ticket
    try:
        execution_meta = {
            "started_at": started_at,
            "completed_at": completed_at,
            "agent_group": {
                "type": group_plan.type,
                "agents": group_plan.agents,
                "context_passing": group_plan.context_passing,
            },
            "execution_time": total_time,
            "result": "success" if all_success else ("timed_out" if any_timeout else "failed"),
        }
        update_ticket_status(ticket, final_status, execution_meta)
        append_execution_result(ticket, agent_results, group_plan)
    except Exception as e:
        result.warnings.append(f"Failed to update ticket: {e}")

    # Step 9: Log
    try:
        append_agent_log(ticket, agent_results, agents_task_context_dir)
    except Exception as e:
        result.warnings.append(f"Failed to write agent log: {e}")

    # Cleanup temp file
    try:
        os.unlink(context_file)
    except Exception:
        pass

    return result


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="COF Task Solver - Dispatch tickets to AI CLI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-select agent by tags
  python3 solve_ticket.py --ticket ./tickets/my-task.md

  # Force specific provider
  python3 solve_ticket.py --ticket ./tickets/security-audit.md --provider claude

  # Council of Elders (all agents)
  python3 solve_ticket.py --ticket ./tickets/architecture-review.md --all

  # Dry run
  python3 solve_ticket.py --ticket ./tickets/test.md --dry-run
        """,
    )

    parser.add_argument(
        "--ticket", "-t",
        required=True,
        help="Path to the ticket file",
    )
    parser.add_argument(
        "--provider", "-p",
        choices=["claude", "codex", "gemini"],
        help="Force specific provider",
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Council mode: dispatch to all available providers",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=int(os.environ.get("DEFAULT_TIMEOUT", "300")),
        help="Execution timeout in seconds (default: 300)",
    )
    parser.add_argument(
        "--context-depth",
        type=int,
        default=int(os.environ.get("DEFAULT_CONTEXT_DEPTH", "10")),
        help="Max depth for cof-glob-indexing (default: 10)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and plan without execution",
    )
    parser.add_argument(
        "--skip-indexing",
        action="store_true",
        help="Skip context indexing",
    )
    parser.add_argument(
        "--require-indexing",
        action="store_true",
        help="Fail if indexing produces no artifacts (no minimal-context fallback)",
    )
    parser.add_argument(
        "--allow-minimal-context",
        action="store_true",
        help="Allow execution when indexing produces no artifacts (fallback to minimal context).",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=int(os.environ.get("COF_SOLVING_TICKETS_MAX_RETRIES", str(DEFAULT_MAX_RETRIES))),
        help=f"Max retries for timed-out agent runs (default: {DEFAULT_MAX_RETRIES})",
    )
    parser.add_argument(
        "--retry-timeout-delta",
        type=int,
        default=int(os.environ.get("COF_SOLVING_TICKETS_RETRY_TIMEOUT_DELTA", str(DEFAULT_RETRY_TIMEOUT_DELTA_SECONDS))),
        help=f"Timeout increase per retry in seconds (default: {DEFAULT_RETRY_TIMEOUT_DELTA_SECONDS})",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    # Run the workflow
    result = solve_ticket(args)

    # Output
    if args.format == "json":
        agent_group_dict = None
        if result.agent_group:
            agent_group_dict = {
                "type": result.agent_group.type,
                "agents": result.agent_group.agents,
                "context_passing": result.agent_group.context_passing,
                "max_iterations": result.agent_group.max_iterations,
            }

        output = {
            "status": result.status,
            "error_code": result.error_code,
            "error_message": result.error_message,
            "ticket": {
                "path": result.ticket_path,
                "original_status": result.original_status,
                "final_status": result.final_status,
            },
            "execution": {
                "agent_group": agent_group_dict,
                "started_at": result.started_at,
                "completed_at": result.completed_at,
                "execution_time": result.execution_time,
                "context_file": result.context_file,
            },
            "agent_results": [asdict(r) for r in result.agent_results],
            "warnings": result.warnings,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'=' * 60}")
        print("COF TASK SOLVER RESULT")
        print(f"{'=' * 60}\n")
        print(f"Status: {result.status.upper()}")
        print(f"Ticket: {result.ticket_path}")
        if result.agent_group:
            print(f"Agent Group: {result.agent_group.type} / {result.agent_group.agents}")
        print(f"Status Change: {result.original_status} -> {result.final_status}")
        print(f"Execution Time: {result.execution_time:.2f}s")

        if result.error_message:
            print(f"\nError: {result.error_code}")
            print(f"  {result.error_message}")

        if result.warnings:
            print(f"\nWarnings:")
            for w in result.warnings:
                print(f"  - {w}")

        if result.agent_results:
            print(f"\nAgent Results:")
            for r in result.agent_results:
                status = "SUCCESS" if r.success else ("TIMEOUT" if r.timed_out else "FAILED")
                print(f"  [{r.provider}] {status} ({r.execution_time:.2f}s)")
                if r.output:
                    preview = r.output[:200].replace("\n", " ")
                    if len(r.output) > 200:
                        preview += "..."
                    print(f"    Output: {preview}")

        print(f"\n{'=' * 60}\n")

    # Exit code
    if result.status == "success":
        return EXIT_SUCCESS
    elif result.status == "partial":
        return EXIT_PARTIAL
    elif result.error_code == "TICKET_NOT_FOUND":
        return EXIT_TICKET_ERROR
    elif result.error_code == "TICKET_PARSE_ERROR":
        return EXIT_TICKET_ERROR
    elif result.error_code == "TICKET_INVALID_STATUS":
        return EXIT_TICKET_ERROR
    elif result.error_code == "CONTEXT_INDEXING_FAILED":
        return EXIT_CONTEXT_ERROR
    elif result.error_code == "SUMMON_AGENTS_NOT_FOUND":
        return EXIT_NO_AGENTS
    elif result.error_code == "AGENT_FAILED":
        return EXIT_AGENT_FAILED
    else:
        return EXIT_PARTIAL


if __name__ == "__main__":
    sys.exit(main())
