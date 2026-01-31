"""Job utilities for detached/background execution.

This module implements a file-backed job registry so jobs can be polled even if
the MCP client disconnects. Jobs are executed via a detached `job_runner` child
process that updates the job JSON on completion.
"""

from __future__ import annotations

import json
import os
import tempfile
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .utils.paths import resolve_aaos_root


API_KEY_ENV_VARS = (
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "GEMINI_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "GOOGLE_APPLICATION_CREDENTIALS",
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_job_id() -> str:
    return uuid.uuid4().hex


def is_under_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except Exception:
        return False


def resolve_jobs_dir() -> Path:
    env_dir = os.environ.get("AAOS_JOBS_DIR")
    if env_dir:
        return Path(env_dir).expanduser().resolve()

    aaos_root = resolve_aaos_root()
    if aaos_root is None:
        return Path(tempfile.gettempdir()).resolve() / "aaos-jobs"

    return aaos_root / ".aaos" / "jobs"


def atomic_write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def strip_api_billing_env(env: dict[str, str]) -> tuple[dict[str, str], list[str]]:
    """Return a copy of env with known API-key env vars removed."""
    stripped: list[str] = []
    new_env = dict(env)
    for key in API_KEY_ENV_VARS:
        if key in new_env and str(new_env.get(key, "")).strip():
            stripped.append(key)
        new_env.pop(key, None)
    return new_env, stripped


@dataclass(frozen=True)
class JobPaths:
    job_dir: Path
    job_file: Path
    stdout_file: Path
    stderr_file: Path
    result_file: Path


def make_job_paths(job_id: str) -> JobPaths:
    job_dir = resolve_jobs_dir() / job_id
    return JobPaths(
        job_dir=job_dir,
        job_file=job_dir / "job.json",
        stdout_file=job_dir / "stdout.txt",
        stderr_file=job_dir / "stderr.txt",
        result_file=job_dir / "result.json",
    )


def tail_text(path: Path, *, max_bytes: int = 32_000) -> str:
    if not path.exists():
        return ""
    try:
        data = path.read_bytes()
    except Exception:
        return ""
    if len(data) > max_bytes:
        data = data[-max_bytes:]
    return data.decode("utf-8", errors="replace")


def validate_no_api_billing_requested(billing_mode: str, env: dict[str, str]) -> tuple[bool, list[str]]:
    """Return (ok, present_keys) for subscription_only mode."""
    if billing_mode != "subscription_only":
        return True, []
    present = [k for k in API_KEY_ENV_VARS if str(env.get(k, "")).strip()]
    return len(present) == 0, present


def redact_env_keys(env: dict[str, str], keys: Iterable[str]) -> dict[str, str]:
    redacted = dict(env)
    for k in keys:
        if k in redacted:
            redacted[k] = "***REDACTED***"
    return redacted

