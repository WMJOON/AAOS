import json
import subprocess
import sys
from pathlib import Path


def test_job_runner_updates_job_file(tmp_path: Path):
    job_dir = tmp_path / "job"
    job_dir.mkdir()

    job_file = job_dir / "job.json"
    stdout_file = job_dir / "stdout.txt"
    stderr_file = job_dir / "stderr.txt"
    result_file = job_dir / "result.json"

    job_file.write_text(json.dumps({"id": "job1", "status": "queued"}), encoding="utf-8")

    cmd = [
        sys.executable,
        "-m",
        "aaos_mcp.job_runner",
        "--job-file",
        str(job_file),
        "--stdout-file",
        str(stdout_file),
        "--stderr-file",
        str(stderr_file),
        "--result-file",
        str(result_file),
        "--",
        sys.executable,
        "-c",
        "import json; print('LOG LINE'); print(json.dumps({'status':'success','ticket':{'final_status':'done'}}))",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0

    job = json.loads(job_file.read_text(encoding="utf-8"))
    assert job["status"] == "succeeded"
    assert job["exit_code"] == 0
    assert job["result_status"] == "success"
    assert job["ticket"]["final_status"] == "done"


def test_job_runner_writes_parse_error_when_stdout_has_no_json(tmp_path: Path):
    job_dir = tmp_path / "job_no_json"
    job_dir.mkdir()

    job_file = job_dir / "job.json"
    stdout_file = job_dir / "stdout.txt"
    stderr_file = job_dir / "stderr.txt"
    result_file = job_dir / "result.json"

    job_file.write_text(json.dumps({"id": "job2", "status": "queued"}), encoding="utf-8")

    cmd = [
        sys.executable,
        "-m",
        "aaos_mcp.job_runner",
        "--job-file",
        str(job_file),
        "--stdout-file",
        str(stdout_file),
        "--stderr-file",
        str(stderr_file),
        "--result-file",
        str(result_file),
        "--",
        sys.executable,
        "-c",
        "print('plain text only')",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0

    job = json.loads(job_file.read_text(encoding="utf-8"))
    assert job["status"] == "succeeded"
    assert job["parse_error"] == "No JSON payload found in stdout tail"

    result_data = json.loads(result_file.read_text(encoding="utf-8"))
    assert result_data["parse_error"] == "No JSON payload found in stdout tail"
