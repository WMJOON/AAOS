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


def build_cof_frontmatter(context_id, role, state, scope, lifetime, created, extra=None):
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


def build_skill_frontmatter(name, description):
    escaped_name = name.replace("\"", "\\\"")
    escaped_description = description.replace("\"", "\\\"")
    lines = [
        "---",
        f"name: \"{escaped_name}\"",
        f"description: \"{escaped_description}\"",
        "---",
    ]
    return "\n".join(lines)


def build_skill_meta(context_id, role, state, scope, lifetime, created, trigger="", consumers=None, notes=""):
    lines = [
        f"context_id: {context_id}",
        f"role: {role}",
        f"state: {state}",
        f"scope: {scope}",
        f"lifetime: {lifetime}",
        f"created: \"{created}\"",
    ]
    if trigger:
        lines.append(f"trigger: {trigger}")
    if consumers:
        quoted = ", ".join([f'\"{item}\"' for item in consumers])
        lines.append(f"consumers: [{quoted}]")
    if notes:
        escaped_notes = notes.replace("\"", "\\\"")
        lines.append(f"notes: \"{escaped_notes}\"")
    return "\n".join(lines) + "\n"


def template_skill(title, frontmatter):
    return f"""{frontmatter}

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


def template_rule(title, frontmatter):
    return f"""{frontmatter}

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


def template_workflow(title, frontmatter):
    return f"""{frontmatter}

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


def template_sub_agent(title, frontmatter):
    return f"""{frontmatter}

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


def main():
    parser = argparse.ArgumentParser(description="Create pointer-safe COF documents.")
    parser.add_argument("--type", required=True, choices=["skill", "rule", "workflow", "sub-agent"])
    parser.add_argument("--title", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--context-id", required=True)
    parser.add_argument("--name", default="")
    parser.add_argument("--description", default="")
    parser.add_argument("--role", default=None)
    parser.add_argument("--state", default=STATE_DEFAULT)
    parser.add_argument("--scope", default=SCOPE_DEFAULT)
    parser.add_argument("--lifetime", default=LIFETIME_DEFAULT)
    parser.add_argument("--created", default=date.today().isoformat())
    parser.add_argument("--trigger", default="")
    parser.add_argument("--consumers", nargs="*", default=[])
    parser.add_argument("--notes", default="")

    args = parser.parse_args()

    role = args.role or ROLE_BY_TYPE[args.type]
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.type == "skill":
        skill_name = args.name or out_path.parent.name
        skill_description = args.description or "Use when this skill is needed."
        skill_frontmatter = build_skill_frontmatter(skill_name, skill_description)
        content = template_skill(args.title, skill_frontmatter)

        meta_content = build_skill_meta(
            context_id=args.context_id,
            role=role,
            state=args.state,
            scope=args.scope,
            lifetime=args.lifetime,
            created=args.created,
            trigger=args.trigger,
            consumers=args.consumers,
            notes=args.notes,
        )
        meta_path = out_path.parent / "SKILL.meta.yaml"
        meta_path.write_text(meta_content, encoding="utf-8")
        out_path.write_text(content, encoding="utf-8")
        print(f"written: {out_path}")
        print(f"written: {meta_path}")
        return

    extra = []
    if args.type == "sub-agent":
        extra.append("agent_kind: sub-agent")

    cof_frontmatter = build_cof_frontmatter(
        context_id=args.context_id,
        role=role,
        state=args.state,
        scope=args.scope,
        lifetime=args.lifetime,
        created=args.created,
        extra=extra,
    )

    if args.type == "rule":
        content = template_rule(args.title, cof_frontmatter)
    elif args.type == "workflow":
        content = template_workflow(args.title, cof_frontmatter)
    else:
        content = template_sub_agent(args.title, cof_frontmatter)

    out_path.write_text(content, encoding="utf-8")
    print(f"written: {out_path}")


if __name__ == "__main__":
    main()
