#!/usr/bin/env python3
import argparse
from datetime import date
from pathlib import Path

ROLE_BY_TYPE = {
    "skill": "SKILL",
    "rule": "RULE",
    "workflow": "WORKFLOW",
    "sub-agent": "SKILL",
}

STATE_DEFAULT = "const"
SCOPE_DEFAULT = "swarm"
LIFETIME_DEFAULT = "persistent"


def build_frontmatter(context_id, role, state, scope, lifetime, created, extra=None):
    lines = [
        "---",
        f"context_id: {context_id}",
        f"role: {role}",
        f"state: {state}",
        f"scope: {scope}",
        f"lifetime: {lifetime}",
        f"created: \"{created}\"",
    ]
    if extra:
        lines.extend(extra)
    lines.append("---")
    return "\n".join(lines)


def template_skill(title, frontmatter):
    body = f"""{frontmatter}

# {title}

## 0. Purpose
- 목적과 범위를 간결히 서술한다.

## 1. Capability Declaration
- allowed_contexts:
- forbidden_contexts:
- consumers: immune | agora | agent

## 2. Inputs / Outputs
- inputs:
- outputs:

## 3. Constraints
- 금지된 포인터 접근 명시
- 실행 코드 포함 금지

## 4. References
- 관련 Rule/Workflow 링크
"""
    return body


def template_rule(title, frontmatter):
    body = f"""{frontmatter}

# {title}

## 0. Scope
- 대상 포인터 타입
- 적용 범위

## 1. Access Control
- who:
- what:
- condition:

## 2. Violation Handling
- severity: SEV-?
- 대응/기록 방식

## 3. References
- 관련 Skill/Workflow 링크
"""
    return body


def template_workflow(title, frontmatter):
    body = f"""{frontmatter}

# {title}

## 0. Entry Context
- 입력 포인터 명시

## 1. Transition Steps
1. [step] 포인터 상태 전이 명시
2. [step] 포인터 상태 전이 명시

## 2. Exit Rule
- 종료 조건 및 최종 상태

## 3. Lifetime Transition
- from: <state> -> to: <state>

## 4. References
- 관련 Rule/Skill 링크
"""
    return body


def template_sub_agent(title, frontmatter):
    body = f"""{frontmatter}

# {title}

## 0. Mission
- 담당 역할과 범위를 명시

## 1. Inputs / Outputs
- inputs:
- outputs:

## 2. Allowed / Forbidden Contexts
- allowed_contexts:
- forbidden_contexts:

## 3. Escalation & Handoff
- 실패 조건
- 상위 에이전트 보고 방식

## 4. References
- 관련 Rule/Workflow/Skill 링크
"""
    return body


def main():
    parser = argparse.ArgumentParser(description="Create pointer-safe COF documents.")
    parser.add_argument("--type", required=True, choices=["skill", "rule", "workflow", "sub-agent"])
    parser.add_argument("--title", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--context-id", required=True)
    parser.add_argument("--role", default=None)
    parser.add_argument("--state", default=STATE_DEFAULT)
    parser.add_argument("--scope", default=SCOPE_DEFAULT)
    parser.add_argument("--lifetime", default=LIFETIME_DEFAULT)
    parser.add_argument("--created", default=date.today().isoformat())

    args = parser.parse_args()

    role = args.role or ROLE_BY_TYPE[args.type]
    extra = []
    if args.type == "sub-agent":
        extra.append("agent_kind: sub-agent")

    frontmatter = build_frontmatter(
        context_id=args.context_id,
        role=role,
        state=args.state,
        scope=args.scope,
        lifetime=args.lifetime,
        created=args.created,
        extra=extra,
    )

    if args.type == "skill":
        content = template_skill(args.title, frontmatter)
    elif args.type == "rule":
        content = template_rule(args.title, frontmatter)
    elif args.type == "workflow":
        content = template_workflow(args.title, frontmatter)
    else:
        content = template_sub_agent(args.title, frontmatter)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()
