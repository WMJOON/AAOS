#!/usr/bin/env python3
"""
Validate strategy/high-risk H1 finalization gate requirements.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path
from typing import Any


PF1_QUESTION = "멘탈모델 먼저 세팅할까요?"

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
AWT_ROOT = SKILL_ROOT.parent.parent.parent
DEFAULT_COWI_ROOT = AWT_ROOT.parent / "context-orchestrated-workflow-intelligence"


def sanitize_token(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip().lower())
    return cleaned.strip("-")


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("workflow spec must be a JSON object")
    return payload


def detect_strategy_or_high_risk(spec: dict[str, Any]) -> tuple[bool, str]:
    profile = spec.get("workflow_profile", {})
    cls = str(profile.get("class", "")).strip().lower()
    profile_risk = str(profile.get("risk_tolerance", "")).strip().lower()
    context = spec.get("context", {})
    context_risk = str(context.get("risk_tolerance", "")).strip().lower()
    explicit_flag = bool(profile.get("is_strategy_or_high_risk"))
    goal = str(spec.get("goal", "")).strip().lower()
    strategy_keywords = ("전략", "strategy", "go-to-market", "시장 진입", "사업 전략")
    has_keyword = any(token in goal for token in strategy_keywords)

    if cls in {"strategy", "high_risk"}:
        return True, f"workflow_profile.class={cls}"
    if explicit_flag:
        return True, "workflow_profile.is_strategy_or_high_risk=true"
    if profile_risk == "high" or context_risk == "high":
        return True, "risk_tolerance=high"
    if has_keyword:
        return True, "strategy keyword in goal"
    return False, "general workflow"


def get_nodes(spec: dict[str, Any]) -> set[str]:
    graph = spec.get("task_graph", {})
    nodes = graph.get("nodes") if isinstance(graph, dict) else None
    if nodes is None:
        nodes = spec.get("nodes", [])
    output: set[str] = set()
    if not isinstance(nodes, list):
        return output
    for item in nodes:
        if not isinstance(item, dict):
            continue
        node_id = (
            str(item.get("node_id", "")).strip()
            or str(item.get("id", "")).strip()
            or str(item.get("name", "")).strip()
        )
        if node_id:
            output.add(node_id)
    return output


def get_edges(spec: dict[str, Any]) -> set[tuple[str, str]]:
    graph = spec.get("task_graph", {})
    edges = graph.get("edges") if isinstance(graph, dict) else None
    if edges is None:
        edges = spec.get("edges", [])
    output: set[tuple[str, str]] = set()
    if not isinstance(edges, list):
        return output
    for item in edges:
        if not isinstance(item, dict):
            continue
        src = str(item.get("from", "")).strip()
        dst = str(item.get("to", "")).strip()
        if src and dst:
            output.add((src, dst))
    return output


def has_artifact_for_proposal(path: Path, proposal_id: str) -> bool:
    if not path.exists():
        return False
    proposal_token = sanitize_token(proposal_id)
    for item in path.glob("*"):
        if not item.is_file():
            continue
        if proposal_token and proposal_token in item.name.lower():
            return True
    return False


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate strategy/high-risk H1 gate")
    parser.add_argument("--workflow-spec", required=True)
    parser.add_argument("--agent-family", required=True)
    parser.add_argument("--agent-version", required=True)
    parser.add_argument("--proposal-id", required=True)
    parser.add_argument("--evidence-date", default=dt.date.today().isoformat())
    parser.add_argument("--awt-root", default=str(AWT_ROOT))
    parser.add_argument("--cowi-root", default=str(DEFAULT_COWI_ROOT))
    return parser


def main() -> int:
    args = build_parser().parse_args()

    spec_path = Path(args.workflow_spec).expanduser().resolve()
    awt_root = Path(args.awt_root).expanduser().resolve()
    cowi_root = Path(args.cowi_root).expanduser().resolve()

    spec = load_json(spec_path)

    is_target, reason = detect_strategy_or_high_risk(spec)
    if not is_target:
        print(f"PASS: strategy gate skipped ({reason})")
        return 0

    failures: list[str] = []

    preflight = spec.get("preflight", {})
    questions = preflight.get("questions", []) if isinstance(preflight, dict) else []
    if not isinstance(questions, list) or not questions:
        failures.append("preflight.questions is missing")
    else:
        first = questions[0] if isinstance(questions[0], dict) else {}
        if str(first.get("id", "")).strip() != "PF1":
            failures.append("preflight.questions[0].id must be PF1")
        if str(first.get("question", "")).strip() != PF1_QUESTION:
            failures.append("preflight.questions[0].question must match PF1 fixed text")

    nodes = get_nodes(spec)
    for must_have in ("H1", "H2"):
        if must_have not in nodes:
            failures.append(f"required node missing: {must_have}")

    edges = get_edges(spec)
    if ("T4", "C1") not in edges:
        failures.append("required edge missing: T4 -> C1")
    if ("C1", "H1") not in edges:
        failures.append("required edge missing: C1 -> H1")

    strategy_gate = spec.get("strategy_gate", {})
    if not isinstance(strategy_gate, dict) or not strategy_gate.get("enabled", False):
        failures.append("strategy_gate.enabled must be true for strategy/high-risk workflow")

    evidence_path = (
        awt_root
        / "agents"
        / args.agent_family
        / args.agent_version
        / "artifacts"
        / "web_evidence"
        / f"web_evidence_{args.evidence_date}.md"
    )
    if not evidence_path.exists():
        failures.append(f"web evidence missing: {evidence_path}")

    rel_dir = (
        cowi_root
        / "agents"
        / args.agent_family
        / args.agent_version
        / "artifacts"
        / "relation_context_map"
    )
    if not has_artifact_for_proposal(rel_dir, args.proposal_id):
        failures.append(f"COWI relation_context_map missing for proposal: {args.proposal_id}")

    report_dir = (
        cowi_root
        / "agents"
        / args.agent_family
        / args.agent_version
        / "artifacts"
        / "skill_usage_adaptation_report"
    )
    if not has_artifact_for_proposal(report_dir, args.proposal_id):
        failures.append(
            f"COWI skill_usage_adaptation_report missing for proposal: {args.proposal_id}"
        )

    if failures:
        print("FAIL: strategy/high-risk H1 finalization gate check failed")
        for item in failures:
            print(f"- {item}")
        return 1

    print("PASS: strategy/high-risk H1 finalization gate check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
