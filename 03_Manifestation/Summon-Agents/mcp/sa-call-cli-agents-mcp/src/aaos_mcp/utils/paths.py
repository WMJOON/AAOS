"""Path resolution utilities for AAOS/COF."""

import os
from pathlib import Path


def resolve_cof_root(start_path: str | None = None) -> Path | None:
    """Resolve the COF root directory.

    Priority:
    1. COF_ROOT environment variable (for Docker)
    2. Search upward for markers
    """
    # Priority 1: Environment variable (Docker-friendly)
    env_root = os.environ.get('COF_ROOT')
    if env_root:
        env_path = Path(env_root)
        if env_path.exists():
            return env_path

    # Priority 2: Search upward for markers
    if start_path:
        current = Path(start_path).resolve()
    else:
        current = Path.cwd()

    markers = ['COF_DOCTRINE.md', '.cof-root', 'DNA_BLUEPRINT.md']

    while current != current.parent:
        for marker in markers:
            if (current / marker).exists():
                return current

        # Check for skills directory pattern
        skills_dir = current / 'skills'
        if skills_dir.exists():
            subdirs = list(skills_dir.iterdir())
            cof_pattern = any(
                d.is_dir() and '.' in d.name and d.name.split('.')[0].isdigit()
                for d in subdirs
            )
            if cof_pattern:
                return current

        current = current.parent

    return None


def resolve_skills_path(cof_root: Path | None = None) -> Path | None:
    """Resolve the skills directory path."""
    if cof_root is None:
        cof_root = resolve_cof_root()

    if cof_root is None:
        return None

    skills_path = cof_root / 'skills'
    if skills_path.exists():
        return skills_path

    return None


def resolve_aaos_root(start_path: str | None = None) -> Path | None:
    """Resolve the AAOS root directory.

    Priority:
    1. AAOS_ROOT environment variable (for Docker)
    2. Search upward for markers
    """
    # Priority 1: Environment variable (Docker-friendly)
    env_root = os.environ.get('AAOS_ROOT')
    if env_root:
        env_path = Path(env_root)
        if env_path.exists():
            return env_path

    # Priority 2: Search upward
    if start_path:
        current = Path(start_path).resolve()
    else:
        current = Path.cwd()

    while current != current.parent:
        if current.name == '04_Agentic_AI_OS':
            return current
        if (current / 'METADoctrine.md').exists():
            return current
        current = current.parent

    return None


def get_script_path(skill_name: str, script_name: str) -> Path | None:
    """Get the path to a skill's script.

    Args:
        skill_name: e.g., 'cof-glob-indexing' or '01.cof-glob-indexing'
        script_name: e.g., 'cof_glob_indexing.py'
    """
    skills_path = resolve_skills_path()
    if skills_path is None:
        return None

    # Try direct match
    for skill_dir in skills_path.iterdir():
        if not skill_dir.is_dir():
            continue

        # Match by full name or stripped name
        dir_name = skill_dir.name
        stripped_name = dir_name.split('.', 1)[-1] if '.' in dir_name else dir_name

        if skill_name in (dir_name, stripped_name):
            script_path = skill_dir / 'scripts' / script_name
            if script_path.exists():
                return script_path

    return None
