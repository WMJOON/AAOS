"""Detached job runner for file-backed AAOS MCP jobs.

This module is launched as a separate process (new session/process group) so it
can keep running even if the MCP server/client terminates.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from .jobs import atomic_write_json, read_json, utc_now_iso


class _Cancelled(Exception):
    pass


_cancel_requested = False
_CANCEL_GRACE_SECONDS = 5.0
_JSON_PARSE_MAX_BYTES = 1_000_000


def _handle_signal(_signum: int, _frame: Any) -> None:
    global _cancel_requested
    _cancel_requested = True


def _update_job(job_file: Path, updates: dict[str, Any]) -> dict[str, Any]:
    job = read_json(job_file)
    job.update(updates)
    atomic_write_json(job_file, job)
    return job


def _extract_last_json(text: str) -> Any | None:
    """
    Extract the last JSON value from a mixed stdout stream.

    `solve_ticket.py` may print human-readable lines before emitting JSON, so we
    scan the output and keep the last successfully decoded JSON value.
    """
    s = text.strip()
    if not s:
        return None

    decoder = json.JSONDecoder()
    last: Any | None = None

    for i, ch in enumerate(s):
        if ch not in "[{":
            continue
        try:
            value, end = decoder.raw_decode(s[i:])
        except Exception:
            continue
        # Accept values even if trailing whitespace exists.
        trailing = s[i + end :].strip()
        if trailing == "":
            return value
        last = value

    return last


def _read_tail_utf8(path: Path, *, max_bytes: int) -> str:
    data = path.read_bytes()
    if len(data) > max_bytes:
        data = data[-max_bytes:]
    return data.decode("utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AAOS MCP detached job runner")
    parser.add_argument("--job-file", required=True, help="Path to job.json to update")
    parser.add_argument("--stdout-file", required=True, help="Path to write captured stdout")
    parser.add_argument("--stderr-file", required=True, help="Path to write captured stderr")
    parser.add_argument("--result-file", required=True, help="Path to write parsed JSON result (best-effort)")
    parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Command after --")
    args = parser.parse_args(argv)

    job_file = Path(args.job_file).resolve()
    stdout_file = Path(args.stdout_file).resolve()
    stderr_file = Path(args.stderr_file).resolve()
    result_file = Path(args.result_file).resolve()

    if args.cmd[:1] == ["--"]:
        cmd = args.cmd[1:]
    else:
        cmd = list(args.cmd)

    if not cmd:
        _update_job(job_file, {
            "status": "failed",
            "finished_at": utc_now_iso(),
            "error": "No command provided to job_runner",
        })
        return 2

    # Ensure job dir exists
    job_file.parent.mkdir(parents=True, exist_ok=True)
    stdout_file.parent.mkdir(parents=True, exist_ok=True)
    stderr_file.parent.mkdir(parents=True, exist_ok=True)
    result_file.parent.mkdir(parents=True, exist_ok=True)

    for sig in (signal.SIGTERM, signal.SIGINT):
        try:
            signal.signal(sig, _handle_signal)
        except Exception:
            pass

    _update_job(job_file, {
        "status": "running",
        "started_at": utc_now_iso(),
        "runner_pid": os.getpid(),
        "runner_pgid": os.getpgrp(),
        "command": cmd,
    })

    try:
        if _cancel_requested:
            raise _Cancelled()

        with stdout_file.open("wb") as out_f, stderr_file.open("wb") as err_f:
            proc = subprocess.Popen(
                cmd,
                stdout=out_f,
                stderr=err_f,
                stdin=subprocess.DEVNULL,
                close_fds=True,
            )

            _update_job(job_file, {"child_pid": proc.pid})

            cancel_sent_at: float | None = None
            while True:
                rc = proc.poll()
                if rc is not None:
                    break
                if _cancel_requested:
                    if cancel_sent_at is None:
                        try:
                            proc.terminate()
                        except Exception:
                            pass
                        cancel_sent_at = time.monotonic()
                    elif time.monotonic() - cancel_sent_at >= _CANCEL_GRACE_SECONDS:
                        try:
                            proc.kill()
                        except Exception:
                            pass
                try:
                    proc.wait(timeout=0.25)
                except subprocess.TimeoutExpired:
                    continue

            returncode = proc.wait()

        parsed: dict[str, Any] | None = None
        parse_error: str | None = None
        stdout_text = ""
        try:
            stdout_text = _read_tail_utf8(stdout_file, max_bytes=_JSON_PARSE_MAX_BYTES)
            extracted = _extract_last_json(stdout_text)
            if isinstance(extracted, dict):
                parsed = extracted
            else:
                parsed = {"result": extracted} if extracted is not None else None
            if parsed is not None:
                result_file.write_text(json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8")
            else:
                parse_error = "No JSON payload found in stdout tail"
                result_file.write_text(
                    json.dumps(
                        {"parse_error": parse_error, "raw_stdout_tail": stdout_text[-32_000:]},
                        indent=2,
                        ensure_ascii=False,
                    ),
                    encoding="utf-8",
                )
        except Exception:
            parsed = None
            parse_error = "Failed to parse JSON from stdout"
            if stdout_text:
                result_file.write_text(
                    json.dumps(
                        {"parse_error": parse_error, "raw_stdout_tail": stdout_text[-32_000:]},
                        indent=2,
                        ensure_ascii=False,
                    ),
                    encoding="utf-8",
                )

        status = "succeeded" if returncode == 0 else "failed"
        if _cancel_requested:
            status = "cancelled"

        _update_job(job_file, {
            "status": status,
            "finished_at": utc_now_iso(),
            "exit_code": returncode,
            "result_status": parsed.get("status") if isinstance(parsed, dict) else None,
            "ticket": parsed.get("ticket") if isinstance(parsed, dict) else None,
            "warnings": parsed.get("warnings") if isinstance(parsed, dict) else None,
            "parse_error": parse_error,
        })

        return 0 if status == "succeeded" else 1

    except _Cancelled:
        _update_job(job_file, {
            "status": "cancelled",
            "finished_at": utc_now_iso(),
            "exit_code": None,
        })
        return 1
    except Exception as e:
        _update_job(job_file, {
            "status": "failed",
            "finished_at": utc_now_iso(),
            "exit_code": None,
            "error": str(e),
        })
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
