#!/usr/bin/env python3
"""
01.agents-task-context/ 노드 생성 스크립트 (legacy: task-manager/)

Usage:
    python create_node.py <target_path> --agent-family claude --agent-version 4.0
    python create_node.py <target_path> --agent-family claude --agent-version 4.0 --all
"""

import argparse
import re
import sys
from pathlib import Path

NODE_DIRNAME = "01.agents-task-context"
LEGACY_NODE_DIRNAME = "task-manager"
NAMESPACE_ANCHORS = (NODE_DIRNAME, LEGACY_NODE_DIRNAME, "agents")


def sanitize_namespace_token(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip()).strip("-")


def parse_namespace_from_path(path: Path) -> tuple[str, str] | None:
    parts = path.parts
    for idx, part in enumerate(parts):
        if part in NAMESPACE_ANCHORS and idx + 2 < len(parts):
            family = sanitize_namespace_token(parts[idx + 1])
            version = sanitize_namespace_token(parts[idx + 2])
            if family and version:
                return family, version
    return None


def resolve_agent_namespace(target: Path, agent_family: str, agent_version: str) -> tuple[str, str]:
    from_args = None
    if agent_family or agent_version:
        if not (agent_family and agent_version):
            raise ValueError("both --agent-family and --agent-version are required together")
        family = sanitize_namespace_token(agent_family)
        version = sanitize_namespace_token(agent_version)
        if not family or not version:
            raise ValueError("invalid --agent-family/--agent-version")
        from_args = (family, version)

    from_path = parse_namespace_from_path(target)
    if from_args and from_path and from_args != from_path:
        raise ValueError(
            "agent namespace mismatch between args and target path "
            f"(args={from_args[0]}/{from_args[1]}, path={from_path[0]}/{from_path[1]})"
        )

    if from_args:
        return from_args
    if from_path:
        return from_path
    raise ValueError("cannot resolve agent namespace from path or args")


def read_template(template_name: str) -> str:
    script_dir = Path(__file__).parent
    template_path = script_dir.parent / "templates" / template_name
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text(encoding="utf-8")


def create_rule_md(namespace_path: Path) -> None:
    content = read_template("NODE_RULE.md")
    (namespace_path / "RULE.md").write_text(content, encoding="utf-8")


def create_troubleshooting_md(namespace_path: Path) -> None:
    content = read_template("TROUBLESHOOTING-TEMPLATE.md")
    (namespace_path / "troubleshooting.md").write_text(content, encoding="utf-8")


def create_issue_notes(namespace_path: Path) -> None:
    issue_path = namespace_path / "issue_notes"
    issue_path.mkdir(exist_ok=True)
    content = read_template("ISSUE_NOTE_RULE.md")
    (issue_path / "RULE.md").write_text(content, encoding="utf-8")


def create_release_notes(namespace_path: Path) -> None:
    release_path = namespace_path / "release_notes"
    release_path.mkdir(exist_ok=True)
    content = read_template("RELEASE_NOTE_RULE.md")
    (release_path / "RULE.md").write_text(content, encoding="utf-8")


def create_task_context_node(
    target_path: str,
    agent_family: str,
    agent_version: str,
    with_issue_notes: bool = False,
    with_release_notes: bool = False,
) -> dict:
    result = {
        "success": False,
        "path": "",
        "namespace": "",
        "created": [],
        "errors": [],
    }

    target = Path(target_path).resolve()
    if not target.exists():
        result["errors"].append(f"Target path does not exist: {target}")
        return result
    if not target.is_dir():
        result["errors"].append(f"Target path is not a directory: {target}")
        return result

    try:
        family, version = resolve_agent_namespace(target, agent_family, agent_version)
    except ValueError as exc:
        result["errors"].append(f"Namespace resolution failed: {exc}")
        result["errors"].append(f"[AUDIT] namespace_policy_violation path={target}")
        return result

    node_path = target / NODE_DIRNAME
    namespace_path = node_path / family / version
    result["path"] = str(namespace_path)
    result["namespace"] = f"{family}/{version}"

    legacy_path = target / LEGACY_NODE_DIRNAME
    if legacy_path.exists():
        result["errors"].append(
            f"Legacy '{LEGACY_NODE_DIRNAME}/' already exists at: {legacy_path} "
            f"(expected '{NODE_DIRNAME}/')."
        )
        result["errors"].append(f"[AUDIT] namespace_policy_violation path={legacy_path}")
        return result

    if namespace_path.exists():
        result["errors"].append(f"Namespace already exists at: {namespace_path}")
        result["errors"].append(f"[AUDIT] namespace_policy_violation path={namespace_path}")
        return result

    try:
        if not node_path.exists():
            node_path.mkdir(parents=True)
            result["created"].append(f"{NODE_DIRNAME}/")

        namespace_path.mkdir(parents=True)
        result["created"].append(f"{NODE_DIRNAME}/{family}/{version}/")

        (namespace_path / "tickets").mkdir()
        result["created"].append(f"{NODE_DIRNAME}/{family}/{version}/tickets/")

        create_rule_md(namespace_path)
        result["created"].append(f"{NODE_DIRNAME}/{family}/{version}/RULE.md")

        create_troubleshooting_md(namespace_path)
        result["created"].append(f"{NODE_DIRNAME}/{family}/{version}/troubleshooting.md")

        if with_issue_notes:
            create_issue_notes(namespace_path)
            result["created"].append(f"{NODE_DIRNAME}/{family}/{version}/issue_notes/")
            result["created"].append(f"{NODE_DIRNAME}/{family}/{version}/issue_notes/RULE.md")

        if with_release_notes:
            create_release_notes(namespace_path)
            result["created"].append(f"{NODE_DIRNAME}/{family}/{version}/release_notes/")
            result["created"].append(f"{NODE_DIRNAME}/{family}/{version}/release_notes/RULE.md")

        result["success"] = True

    except PermissionError as exc:
        result["errors"].append(f"Permission denied: {exc}")
    except OSError as exc:
        result["errors"].append(f"OS error: {exc}")

    return result


def main():
    parser = argparse.ArgumentParser(description=f"Create {NODE_DIRNAME}/ namespace node structure")
    parser.add_argument("target_path", help=f"Path where {NODE_DIRNAME}/ will be created")
    parser.add_argument("--agent-family", default="", help="Agent family namespace key")
    parser.add_argument("--agent-version", default="", help="Agent version namespace key")
    parser.add_argument("--with-issue-notes", action="store_true", help="Include issue_notes/ directory")
    parser.add_argument("--with-release-notes", action="store_true", help="Include release_notes/ directory")
    parser.add_argument("--all", action="store_true", help="Include all optional directories")

    args = parser.parse_args()
    with_issue = args.with_issue_notes or args.all
    with_release = args.with_release_notes or args.all

    result = create_task_context_node(
        args.target_path,
        agent_family=args.agent_family,
        agent_version=args.agent_version,
        with_issue_notes=with_issue,
        with_release_notes=with_release,
    )

    if result["success"]:
        print(f"OK: Created namespace at {result['path']} (namespace={result['namespace']})")
        print("\nCreated:")
        for item in result["created"]:
            print(f"  - {item}")
    else:
        print("FAILED:", file=sys.stderr)
        for error in result["errors"]:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
