from __future__ import annotations

import re
from typing import Optional


_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def extract_frontmatter(text: str) -> Optional[str]:
    """
    Extract YAML frontmatter block (as raw text) from a Markdown document.
    Returns None if missing.
    """
    match = _FRONTMATTER_RE.search(text)
    return match.group(1) if match else None


def has_key(frontmatter: str, key: str) -> bool:
    """
    Very small, dependency-free key presence check.
    This does NOT parse YAML; it only checks for a `key:` line anywhere.
    """
    pattern = re.compile(rf"(?m)^\s*{re.escape(key)}\s*:", re.UNICODE)
    return bool(pattern.search(frontmatter))

