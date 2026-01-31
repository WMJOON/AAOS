"""MCP Tool wrapper for cof-task-solver-agent-group skill."""

import asyncio
import os
import subprocess
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
import sys

from ..utils.paths import get_script_path
from ..utils.frontmatter import parse_frontmatter
from ..jobs import (
    JobPaths,
    atomic_write_json,
    make_job_paths,
    new_job_id,
    read_json,
    strip_api_billing_env,
    tail_text,
    utc_now_iso,
)

_JOB_ID_RE = re.compile(r"^[0-9a-f]{32}$")


@dataclass
class SolveTicketResult:
    """Result of solving a ticket."""

    success: bool
    ticket_path: str
    original_status: str
    final_status: str
    agent_group: dict
    execution_time: float | None
    output: str
    error: str | None = None


@dataclass
class StartSolveJobResult:
    success: bool
    job_id: str
    job_paths: JobPaths
    message: str
    stripped_env_vars: list[str]


class TaskSolverTool:
    """MCP Tool for solving tickets via AI CLI agents.

    Wraps the cof-task-solver-agent-group skill to:
    - Dispatch tickets to appropriate AI CLI agents
    - Support single, council, and sequential agent groups
    - Record execution results back to tickets
    """

    TOOL_NAME = "cof_solve_ticket"
    TOOL_DESCRIPTION = """Solve a ticket by dispatching it to an AI CLI agent.

Use this tool when you need to:
- Automatically process a ticket from NN.agents-task-context/tickets/
- Dispatch to claude, codex, or gemini based on ticket tags
- Run council mode for cross-verification (all agents in parallel)
- Run sequential mode for iterative refinement

The tool will:
1. Parse the ticket
2. Index context via cof-glob-indexing
3. Select agent(s) based on tags
4. Execute and record results to the ticket"""

    def __init__(self):
        self._script_path = get_script_path(
            'cof-task-solver-agent-group',
            'solve_ticket.py'
        )

    @property
    def input_schema(self) -> dict:
        """JSON Schema for tool input."""
        return {
            "type": "object",
            "properties": {
                "ticket_path": {
                    "type": "string",
                    "description": "Path to the ticket file to solve"
                },
                "provider": {
                    "type": "string",
                    "enum": ["claude", "codex", "gemini"],
                    "description": "Force specific provider (overrides auto-selection)"
                },
                "council_mode": {
                    "type": "boolean",
                    "description": "Run all providers in parallel for cross-verification",
                    "default": False
                },
                "timeout": {
                    "type": "integer",
                    "description": "Execution timeout in seconds (default: 300)",
                    "default": 300
                },
                "context_depth": {
                    "type": "integer",
                    "description": "Max depth for context indexing (default: 10)",
                    "default": 10
                },
                "dry_run": {
                    "type": "boolean",
                    "description": "Parse and plan without execution",
                    "default": False
                },
                "allow_minimal_context": {
                    "type": "boolean",
                    "description": "Allow execution when indexing produces no artifacts (fallback to minimal context)",
                    "default": False
                },
                "billing_mode": {
                    "type": "string",
                    "enum": ["subscription_only", "allow_api"],
                    "description": "subscription_only strips API key env vars for the job to avoid pay-per-token billing",
                    "default": "subscription_only"
                }
            },
            "required": ["ticket_path"]
        }

    async def execute(
        self,
        ticket_path: str,
        provider: str | None = None,
        council_mode: bool = False,
        timeout: int = 300,
        context_depth: int = 10,
        dry_run: bool = False,
        allow_minimal_context: bool = False,
        billing_mode: str = "subscription_only",
    ) -> SolveTicketResult:
        """Execute ticket solving."""
        if self._script_path is None:
            return SolveTicketResult(
                success=False,
                ticket_path=ticket_path,
                original_status="unknown",
                final_status="unknown",
                agent_group={},
                execution_time=None,
                output="",
                error="solve_ticket.py script not found"
            )

        ticket_file = Path(ticket_path).resolve()
        if not ticket_file.exists():
            return SolveTicketResult(
                success=False,
                ticket_path=ticket_path,
                original_status="unknown",
                final_status="unknown",
                agent_group={},
                execution_time=None,
                output="",
                error=f"Ticket file not found: {ticket_path}"
            )

        working_dir = ticket_file.parent.parent if ticket_file.parent.name == "tickets" else ticket_file.parent

        # Parse original status
        try:
            content = ticket_file.read_text()
            fm, _ = parse_frontmatter(content)
            original_status = fm.get("status", "todo")
        except Exception:
            original_status = "unknown"

        # Build command
        args: list[str] = [
            sys.executable, str(self._script_path),
            "--ticket", str(ticket_file),
            "--timeout", str(timeout),
            "--context-depth", str(context_depth),
            "--format", "json"
        ]

        if provider:
            args.extend(["--provider", provider])
        if council_mode:
            args.append("--all")
        if dry_run:
            args.append("--dry-run")
        if allow_minimal_context:
            args.append("--allow-minimal-context")

        try:
            env = dict(os.environ)
            if billing_mode == "subscription_only":
                env, _ = strip_api_billing_env(env)

            result = await asyncio.to_thread(
                subprocess.run,
                args,
                capture_output=True,
                text=True,
                timeout=timeout + 60,  # Extra buffer for overhead
                env=env,
                cwd=str(working_dir),
            )

            if result.returncode == 0:
                try:
                    output_data = json.loads(result.stdout)
                    agent_results = output_data.get("agent_results") or []
                    output_text = ""
                    error_text = ""

                    if isinstance(agent_results, list) and agent_results:
                        parts: list[str] = []
                        for r in agent_results:
                            if not isinstance(r, dict):
                                continue
                            provider = r.get("provider", "unknown")
                            ok = bool(r.get("success"))
                            out = (r.get("output") or "").strip()
                            err = (r.get("error") or "").strip()
                            if out:
                                parts.append(f"[{provider}] {'OK' if ok else 'FAIL'}\n{out}")
                            if (not ok) and err and not error_text:
                                error_text = err
                        output_text = "\n\n".join(parts).strip()

                    return SolveTicketResult(
                        success=output_data.get("status") == "success",
                        ticket_path=ticket_path,
                        original_status=original_status,
                        final_status=output_data.get("ticket", {}).get("final_status", "unknown"),
                        agent_group=output_data.get("execution", {}).get("agent_group", {}),
                        execution_time=output_data.get("execution", {}).get("execution_time"),
                        output=output_text,
                        error=error_text or output_data.get("error_message")
                    )
                except json.JSONDecodeError:
                    return SolveTicketResult(
                        success=True,
                        ticket_path=ticket_path,
                        original_status=original_status,
                        final_status="done",
                        agent_group={},
                        execution_time=None,
                        output=result.stdout,
                        error=None
                    )
            else:
                return SolveTicketResult(
                    success=False,
                    ticket_path=ticket_path,
                    original_status=original_status,
                    final_status="blocked",
                    agent_group={},
                    execution_time=None,
                    output=result.stdout,
                    error=result.stderr
                )

        except subprocess.TimeoutExpired:
            return SolveTicketResult(
                success=False,
                ticket_path=ticket_path,
                original_status=original_status,
                final_status="blocked",
                agent_group={},
                execution_time=None,
                output="",
                error=f"Execution timed out after {timeout + 60} seconds"
            )
        except Exception as e:
            return SolveTicketResult(
                success=False,
                ticket_path=ticket_path,
                original_status=original_status,
                final_status="blocked",
                agent_group={},
                execution_time=None,
                output="",
                error=f"Unexpected error: {str(e)}"
            )

    async def start_solve_job(
        self,
        ticket_path: str,
        provider: str | None = None,
        council_mode: bool = False,
        timeout: int = 300,
        context_depth: int = 10,
        dry_run: bool = False,
        allow_minimal_context: bool = False,
        billing_mode: str = "subscription_only",
    ) -> StartSolveJobResult:
        if self._script_path is None:
            return StartSolveJobResult(
                success=False,
                job_id="",
                job_paths=make_job_paths("invalid"),
                message="solve_ticket.py script not found",
                stripped_env_vars=[],
            )

        ticket_file = Path(ticket_path).resolve()
        if not ticket_file.exists():
            return StartSolveJobResult(
                success=False,
                job_id="",
                job_paths=make_job_paths("invalid"),
                message=f"Ticket file not found: {ticket_path}",
                stripped_env_vars=[],
            )

        working_dir = ticket_file.parent.parent if ticket_file.parent.name == "tickets" else ticket_file.parent

        job_id = new_job_id()
        paths = make_job_paths(job_id)
        paths.job_dir.mkdir(parents=True, exist_ok=True)

        # Command to execute (solve_ticket.py)
        solver_cmd: list[str] = [
            sys.executable, str(self._script_path),
            "--ticket", str(ticket_file),
            "--timeout", str(timeout),
            "--context-depth", str(context_depth),
            "--format", "json",
        ]
        if provider:
            solver_cmd.extend(["--provider", provider])
        if council_mode:
            solver_cmd.append("--all")
        if dry_run:
            solver_cmd.append("--dry-run")
        if allow_minimal_context:
            solver_cmd.append("--allow-minimal-context")

        env = dict(os.environ)
        stripped: list[str] = []
        if billing_mode == "subscription_only":
            env, stripped = strip_api_billing_env(env)

        job_record = {
            "id": job_id,
            "kind": "cof_solve_ticket",
            "status": "queued",
            "created_at": utc_now_iso(),
            "ticket_path": str(ticket_file),
            "cwd": str(working_dir),
            "provider": provider,
            "council_mode": council_mode,
            "timeout": timeout,
            "context_depth": context_depth,
            "dry_run": dry_run,
            "billing_mode": billing_mode,
            "paths": {
                "job_file": str(paths.job_file),
                "stdout_file": str(paths.stdout_file),
                "stderr_file": str(paths.stderr_file),
                "result_file": str(paths.result_file),
            },
            "stripped_env_vars": stripped,
        }
        atomic_write_json(paths.job_file, job_record)

        runner_cmd: list[str] = [
            sys.executable,
            "-m",
            "aaos_mcp.job_runner",
            "--job-file",
            str(paths.job_file),
            "--stdout-file",
            str(paths.stdout_file),
            "--stderr-file",
            str(paths.stderr_file),
            "--result-file",
            str(paths.result_file),
            "--",
            *solver_cmd,
        ]

        try:
            subprocess.Popen(
                runner_cmd,
                cwd=str(working_dir),
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
                close_fds=True,
            )
        except Exception as e:
            job_record["status"] = "failed"
            job_record["finished_at"] = utc_now_iso()
            job_record["error"] = f"Failed to start job_runner: {e}"
            atomic_write_json(paths.job_file, job_record)
            return StartSolveJobResult(
                success=False,
                job_id=job_id,
                job_paths=paths,
                message=job_record["error"],
                stripped_env_vars=stripped,
            )

        return StartSolveJobResult(
            success=True,
            job_id=job_id,
            job_paths=paths,
            message="Job started",
            stripped_env_vars=stripped,
        )

    async def get_job_status(self, job_id: str) -> dict:
        if not _JOB_ID_RE.fullmatch(job_id):
            return {"error": "Invalid job_id format"}
        paths = make_job_paths(job_id)
        if not paths.job_file.exists():
            return {"error": f"Job not found: {job_id}"}
        try:
            return read_json(paths.job_file)
        except Exception as e:
            return {"error": str(e), "job_id": job_id}

    async def get_job_logs(self, job_id: str, max_bytes: int = 32_000) -> dict:
        if not _JOB_ID_RE.fullmatch(job_id):
            return {"error": "Invalid job_id format"}
        paths = make_job_paths(job_id)
        if not paths.job_file.exists():
            return {"error": f"Job not found: {job_id}"}
        return {
            "job_id": job_id,
            "stdout": tail_text(paths.stdout_file, max_bytes=max_bytes),
            "stderr": tail_text(paths.stderr_file, max_bytes=max_bytes),
        }

    async def cancel_job(self, job_id: str) -> dict:
        if not _JOB_ID_RE.fullmatch(job_id):
            return {"error": "Invalid job_id format"}
        paths = make_job_paths(job_id)
        if not paths.job_file.exists():
            return {"error": f"Job not found: {job_id}"}

        job = read_json(paths.job_file)
        pgid = job.get("runner_pgid") or job.get("runner_pid")
        if not pgid:
            return {"job_id": job_id, "cancelled": False, "message": "No runner pid/pgid recorded yet"}

        try:
            os.killpg(int(pgid), 15)  # SIGTERM
            return {"job_id": job_id, "cancelled": True, "signal": "SIGTERM", "pgid": int(pgid)}
        except Exception as e:
            return {"job_id": job_id, "cancelled": False, "error": str(e)}

    async def get_ticket_status(self, ticket_path: str) -> dict:
        """Get current status of a ticket without solving it."""
        ticket_file = Path(ticket_path).resolve()
        if not ticket_file.exists():
            return {"error": f"Ticket not found: {ticket_path}"}

        try:
            content = ticket_file.read_text()
            fm, body = parse_frontmatter(content)

            return {
                "path": str(ticket_file),
                "title": fm.get("title", ticket_file.stem),
                "status": fm.get("status", "todo"),
                "priority": fm.get("priority", "P2"),
                "tags": fm.get("tags", []),
                "execution": fm.get("execution"),
                "has_result": "## Execution Result" in body
            }
        except Exception as e:
            return {"error": str(e)}
