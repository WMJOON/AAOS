# Skill Reference

본 에이전트 그룹은 `cof-task-manager-node` 스킬에서 위임받은 능력을 기반으로 동작한다.

## 상위 Skill 위치

```
../../skills/02.cof-task-manager-node/
├── SKILL.md        # 스킬 정의
├── SPEC.md         # 상세 스펙
├── scripts/        # 실행 스크립트
│   ├── bootstrap_node.py
│   ├── create_node.py
│   ├── create_ticket.py
│   ├── verify_node.py
│   ├── validate_node.py
│   ├── add_optional.py
│   └── archive_tasks.py
└── templates/      # 문서 템플릿
    ├── NODE_cof-environment-set.md
    ├── TICKET-TEMPLATE.md
    ├── ISSUE_NOTE_cof-environment-set.md
    ├── RELEASE_NOTE_cof-environment-set.md
    └── TROUBLESHOOTING-TEMPLATE.md
```

## Sub-Agent ↔ Script 매핑

| Sub-Agent | Primary Script | Secondary Scripts |
|-----------|----------------|-------------------|
| Node-Creator | `create_node.py` | `bootstrap_node.py`, `add_optional.py` |
| Ticket-Manager | `create_ticket.py` | - |
| Validator | `verify_node.py` | `validate_node.py` |
| Archiver | `archive_tasks.py` | - |

## 핵심 규칙 인용

### Ticket Dependencies (from SPEC.md)

> `dependencies`는 **의존 티켓의 파일 stem(확장자 `.md` 제외)** 목록이다.
> - 예: `"Implement-Parser"` (파일: `Implement-Parser.md`)
> - 금지: 경로 포함, 확장자 포함, 비결정적 별칭

### Guardrails (from SPEC.md)

> - `task-manager/`가 이미 존재하면 생성은 실패한다(덮어쓰기 금지).
> - 티켓 `dependencies`는 파일 stem 기준으로 검증 가능해야 한다.
> - 아카이빙은 `status: done`인 티켓만 대상으로 한다.
> - 아카이브 충돌 시 timestamp suffix로 회피한다.
