#!/usr/bin/env python3
"""
Deliberation Chamber 계획 생명주기 관리.

Commands:
  create  --id WORKFLOW_ID --slug SLUG   새 계획 디렉토리 생성
  close   PLAN_DIR --archive-path PATH   계획 종료 → _closed/ 이동
  list    [--active | --closed]          계획 목록 출력
  sync                                   레지스트리를 파일시스템 기준으로 재생성

레지스트리(PLANS_REGISTRY.md)는 모든 명령 실행 시 자동 갱신된다.
에이전트는 레지스트리만 읽으면 활성 계획을 파악할 수 있다.

Usage:
  python3 01_Nucleus/motor_cortex/scripts/plan_manager.py create --id ISSUE-NUC-20260215-0001 --slug my-improvement
  python3 01_Nucleus/motor_cortex/scripts/plan_manager.py close 2026-02-15__my-improvement --archive-path "01_Nucleus/record_archive/_archive/deliberation/..."
  python3 01_Nucleus/motor_cortex/scripts/plan_manager.py list --active
  python3 01_Nucleus/motor_cortex/scripts/plan_manager.py sync
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

# -- paths (프로젝트 루트 기준) ------------------------------------

_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parents[2]  # 04_Agentic_AI_OS/

PLANS_DIR = _PROJECT_ROOT / "01_Nucleus" / "deliberation_chamber" / "plans"
CLOSED_DIR = PLANS_DIR / "_closed"
TASKS_DIR = _PROJECT_ROOT / "01_Nucleus" / "deliberation_chamber" / "tasks"
REGISTRY_FILE = PLANS_DIR / "PLANS_REGISTRY.md"


# -- helpers -------------------------------------------------------

_YAML_KV = re.compile(r"^(\w[\w_]*):\s*(.+)$")


def _read_plan_info(plan_dir: Path, *, location: str = "active") -> dict:
    """계획 README.md에서 메타정보를 추출한다."""
    info: dict = {
        "dir": plan_dir.name,
        "location": location,
        "status": "unknown",
        "workflow_id": "",
        "scope": "",
        "created": "",
        "closed": "",
        "archive_path": "",
    }
    readme = plan_dir / "README.md"
    if not readme.exists():
        return info

    in_frontmatter = False
    for line in readme.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "---":
            in_frontmatter = not in_frontmatter
            continue
        if not in_frontmatter:
            continue
        m = _YAML_KV.match(stripped)
        if m and m.group(1) in info:
            info[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    return info


def _scan_all() -> list[dict]:
    """파일시스템에서 모든 계획을 스캔한다."""
    plans: list[dict] = []
    if PLANS_DIR.exists():
        for d in sorted(PLANS_DIR.iterdir()):
            if d.is_dir() and not d.name.startswith("_"):
                plans.append(_read_plan_info(d, location="active"))
    if CLOSED_DIR.exists():
        for d in sorted(CLOSED_DIR.iterdir()):
            if d.is_dir():
                plans.append(_read_plan_info(d, location="closed"))
    return plans


def _write_registry(plans: list[dict]) -> None:
    """PLANS_REGISTRY.md를 생성한다."""
    active = [p for p in plans if p["location"] == "active"]
    closed = [p for p in plans if p["location"] == "closed"]

    lines = [
        "# Plans Registry",
        "",
        "> 이 파일은 `plan_manager.py`가 자동 생성합니다. 수동 편집 금지.",
        "",
        "## 활성 계획",
        "",
    ]
    if active:
        lines.append("| workflow_id | directory | status | created |")
        lines.append("|-------------|-----------|--------|---------|")
        for p in active:
            lines.append(
                f"| {p['workflow_id']} | `{p['dir']}` | {p['status']} | {p['created']} |"
            )
    else:
        lines.append("(없음)")
    lines += ["", "## 종료 계획", ""]
    if closed:
        lines.append("| workflow_id | directory | archive_path |")
        lines.append("|-------------|-----------|--------------|")
        for p in closed:
            lines.append(
                f"| {p['workflow_id']} | `_closed/{p['dir']}` | `{p['archive_path']}` |"
            )
    else:
        lines.append("(없음)")
    lines.append("")

    REGISTRY_FILE.write_text("\n".join(lines), encoding="utf-8")


def _sync() -> list[dict]:
    """파일시스템을 스캔하고 레지스트리를 갱신한다."""
    plans = _scan_all()
    _write_registry(plans)
    return plans


# -- commands ------------------------------------------------------

def cmd_create(args: argparse.Namespace) -> None:
    date_str = datetime.now().strftime("%Y-%m-%d")
    dir_name = f"{date_str}__{args.slug}"
    plan_path = PLANS_DIR / dir_name

    if plan_path.exists():
        print(f"ERROR: 이미 존재합니다: {plan_path.relative_to(_PROJECT_ROOT)}")
        sys.exit(1)

    plan_path.mkdir(parents=True, exist_ok=True)

    readme = f"""---
type: plan-index
workflow_id: {args.id}
status: active
created: "{date_str}"
scope: "{args.scope}"
---

# {args.slug.replace('-', ' ').replace('_', ' ').title()}

## 포함 산출물

- (작성 예정)

## 상태 요약

| Stage | 상태 |
|-------|------|
| 1. 문제제기 | 진행 중 |
| 2. record_archive 기록 | - |
| 3. Deliberation 계획 | - |
| 4. Immune 비판 | - |
| 5. Deliberation 개선 | - |
| 6. 실행/봉인 | - |
| 6-b. 계획 정리 | - |
"""
    (plan_path / "README.md").write_text(readme, encoding="utf-8")

    _sync()
    print(f"OK: {plan_path.relative_to(_PROJECT_ROOT)}")


def cmd_close(args: argparse.Namespace) -> None:
    source = PLANS_DIR / args.plan_dir

    if not source.exists():
        if (CLOSED_DIR / args.plan_dir).exists():
            print(f"SKIP: 이미 종료됨: _closed/{args.plan_dir}")
            return
        print(f"ERROR: 계획을 찾을 수 없습니다: {args.plan_dir}")
        sys.exit(1)

    # README 갱신
    readme_path = source / "README.md"
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
        date_str = datetime.now().strftime("%Y-%m-%d")
        for old_status in ("active", "draft", "in_progress"):
            content = content.replace(
                f"status: {old_status}",
                f'status: closed\nclosed: "{date_str}"\narchive_path: "{args.archive_path}"',
            )
        readme_path.write_text(content, encoding="utf-8")

    # task bundle 갱신
    task_file = TASKS_DIR / f"{args.plan_dir}.md"
    if task_file.exists():
        tc = task_file.read_text(encoding="utf-8")
        for old in ("sealed", "in_progress", "active"):
            tc = tc.replace(f"status: {old}", "status: done")
        task_file.write_text(tc, encoding="utf-8")

    # _closed/ 이동
    CLOSED_DIR.mkdir(exist_ok=True)
    dest = CLOSED_DIR / args.plan_dir
    shutil.move(str(source), str(dest))

    _sync()
    print(f"OK: _closed/{args.plan_dir}")
    print(f"    archive: {args.archive_path}")


def cmd_list(args: argparse.Namespace) -> None:
    plans = _sync()

    if args.active:
        plans = [p for p in plans if p["location"] == "active"]
    elif args.closed:
        plans = [p for p in plans if p["location"] == "closed"]

    if not plans:
        print("(없음)")
        return

    for p in plans:
        loc = "" if p["location"] == "active" else "_closed/"
        archive = f"  → {p['archive_path']}" if p["archive_path"] else ""
        print(f"  [{p['status']:>7}]  {loc}{p['dir']}{archive}")


def cmd_sync(_args: argparse.Namespace) -> None:
    plans = _sync()
    active = sum(1 for p in plans if p["location"] == "active")
    closed = sum(1 for p in plans if p["location"] == "closed")
    print(f"OK: Registry synced ({active} active, {closed} closed)")


# -- main ----------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deliberation Chamber 계획 생명주기 관리",
    )
    sub = parser.add_subparsers(dest="command")

    p_create = sub.add_parser("create", help="새 계획 생성")
    p_create.add_argument("--id", required=True, help="workflow_id")
    p_create.add_argument("--slug", required=True, help="계획 슬러그")
    p_create.add_argument("--scope", default="01_Nucleus", help="범위")

    p_close = sub.add_parser("close", help="계획 종료 → _closed/ 이동")
    p_close.add_argument("plan_dir", help="계획 디렉토리명")
    p_close.add_argument("--archive-path", required=True, help="봉인 아카이브 경로")

    p_list = sub.add_parser("list", help="계획 목록")
    p_list.add_argument("--active", action="store_true", help="활성만")
    p_list.add_argument("--closed", action="store_true", help="종료만")

    sub.add_parser("sync", help="레지스트리 재생성")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    {"create": cmd_create, "close": cmd_close, "list": cmd_list, "sync": cmd_sync}[
        args.command
    ](args)


if __name__ == "__main__":
    main()
