"""Shared frontmatter helpers for COF skill scripts."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


class FrontmatterParseError(ValueError):
    """Raised when frontmatter cannot be parsed into a mapping."""


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


def split_frontmatter_and_body(content: str) -> Tuple[Dict[str, Any], str]:
    """Split markdown into frontmatter and body.

    Returns ({}, body) when no frontmatter exists.
    """
    if not content.startswith("---"):
        return {}, content

    m = FRONTMATTER_RE.match(content)
    if not m:
        return {}, content

    fm = parse_frontmatter(m.group(1))
    return fm, content[m.end():].strip("\n")


def parse_frontmatter(frontmatter_text: str) -> Dict[str, Any]:
    """Parse YAML frontmatter text into a dictionary."""
    if not frontmatter_text.strip():
        return {}

    if yaml is not None:
        try:
            data = yaml.safe_load(frontmatter_text)
            if data is None:
                return {}
            if not isinstance(data, dict):
                raise FrontmatterParseError("Frontmatter must be a YAML mapping")
            return _coerce_scalar_map(data)
        except Exception as exc:  # pragma: no cover - dependency/runtime dependent
            raise FrontmatterParseError(str(exc)) from exc

    # Minimal fallback parser
    result: Dict[str, Any] = {}
    for raw in frontmatter_text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith("-"):
            # Minimal continuation for list items is unsupported in fallback parser.
            # Keep deterministic behavior by skipping malformed rows.
            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value == "":
            result[key] = []
            continue
        if value == "[]":
            result[key] = []
            continue
        if value == "{}":
            result[key] = {}
            continue

        # Parse inline YAML-like list
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            if inner:
                result[key] = [
                    _coerce_scalar(v.strip().strip("'").strip('"'))
                    for v in inner.split(",")
                    if v.strip()
                ]
            else:
                result[key] = []
            continue

        result[key] = _coerce_scalar(value)

    return result


def serialize_frontmatter(data: Dict[str, Any]) -> str:
    """Serialize frontmatter in a stable human-readable format."""
    if yaml is not None:
        # Keep stable, readable YAML in write path.
        dumped = yaml.safe_dump(_denormalize_scalar_map(data), sort_keys=False, default_flow_style=False, allow_unicode=True)
        dumped = dumped.strip("\n")
        return f"---\n{dumped}\n---"

    lines = ["---"]
    for key, value in data.items():
        lines.extend(_serialize_scalar(key, value, indent=""))
    lines.append("---")
    return "\n".join(lines)


def as_list(value: Any) -> List[str]:
    """Normalize value to a list of strings."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if str(v).strip()]
    if isinstance(value, tuple):
        return [str(v) for v in value if str(v).strip()]
    if isinstance(value, (int, float)):
        return [str(value)]
    if isinstance(value, bool):
        return ["true" if value else "false"]
    s = str(value).strip()
    return [s] if s else []


def _coerce_scalar(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip().strip('"').strip("'")
    return value


def _coerce_scalar_map(data: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(key, str):
            out[key.strip()] = value
        else:
            out[str(key)] = value
    return out


def _denormalize_scalar_map(data: Dict[str, Any]) -> Dict[str, Any]:
    # PyYAML handles rich types; this hook currently keeps structure stable.
    return {k: v for k, v in data.items()}


def _serialize_scalar(key: str, value: Any, *, indent: str) -> List[str]:
    prefix = indent + key
    if isinstance(value, dict):
        lines = [f"{prefix}:"]
        for k, v in value.items():
            lines.extend(_serialize_scalar(str(k), v, indent=indent + "  "))
        return lines
    if isinstance(value, list):
        if not value:
            return [f"{prefix}: []"]
        lines = [f"{prefix}:"]
        for item in value:
            lines.append(f"{indent}  - {item}")
        return lines
    return [f"{prefix}: {_format_scalar(value)}"]


def _format_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    s = str(value)
    if not s:
        return "''"
    if any(ch in s for ch in ":#\n[]{}(),"):
        return f'"{s.replace("\"", "\\\"")}"'
    return s


def safe_str(value: Any, fallback: str = "") -> str:
    if value is None:
        return fallback
    if isinstance(value, str):
        return value.strip()
    return str(value)
