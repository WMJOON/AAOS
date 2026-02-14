---
context_id: cof-task-solver-agent-group-readme
role: REFERENCE
state: const
scope: swarm
lifetime: persistent
created: "2026-01-31"
version: "1.2"
parent_skill: cof-task-solver-agent-group
---

# COF Task Solver Agent Group (해례본)

> "티켓 파일을 읽고 → 필요한 맥락을 모아 → 적당한 에이전트(들)에게 맡기고 → 결과를 다시 티켓에 적어 넣는 자동 집행관"

---

## 핵심 원칙

**One Group, One Ticket** — 하나의 에이전트 그룹이 하나의 티켓을 해결한다.

---

## 언제 쓰나

| 상황 | 이 스킬 사용 |
|------|-------------|
| `tickets/`에 todo 티켓이 있고 에이전트에게 맡기고 싶을 때 | O |
| 티켓 해결 과정을 자동으로 기록하고 싶을 때 | O |
| 티켓을 새로 만들고 구조를 잡을 때 | X → `@skill(cof-task-manager-node)` |
| 결과 품질을 평가/QA할 때 | X → `@agent(cof-task-qa)` |
| 여러 티켓을 병렬 처리할 때 | X (지원 안 함) |

---

## Group 개념 (핵심)

| Type | 구성 | 실행 방식 | 언제 쓰나 |
|------|------|----------|----------|
| **Single** | 1 agent | 단일 실행 | 명확한 단일 작업 |
| **Council** | N agents | 병렬 | 교차 검증, 리뷰, 합의 |
| **Sequential** | N agents | 순차 (컨텍스트 계승) | 누적적 사고, 반복 정제 |

**태그 기반 자동 선택**:
- `security`, `audit` → claude
- `performance`, `optimization` → gemini
- `architecture`, `refactor` → codex
- `review`, `critique` → council (all)
- `sequential`, `iterative` → sequential

---

## Quick Start

```bash
# 기본 실행 (태그 기반 자동 선택)
python3 scripts/solve_ticket.py --ticket "./01.agents-task-context/tickets/my-task.md"

# Council 모드 (모든 에이전트)
python3 scripts/solve_ticket.py --ticket "..." --all

# 실행 없이 계획만 확인
python3 scripts/solve_ticket.py --ticket "..." --dry-run
```

---

## 문서 구조

| 파일 | 목적 | 대상 독자 |
|------|------|----------|
| **README.md** (본 문서) | 왜/언제/무엇 | 비개발자, 처음 보는 사람 |
| **SKILL.md** | 어떻게 쓰나 | 사용자 |
| **SPEC.md** | 정확한 규칙/설계 | 개발자, 유지보수자 |
| **scripts/** | 실제 코드 | 개발자 |

상세 사용법은 `@ref(cof-task-solver-agent-group)` (SKILL.md) 참조.

---

## 주요 의존점

- `@ref(cof-glob-indexing)` — 컨텍스트 경계 식별
- `@ref(call-cli-agents)` — 에이전트 디스패치

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-01-31 | Initial README |
| v1.1 | 2026-01-31 | 해례본 스타일로 재작성 |
| v1.2 | 2026-01-31 | 중복 콘텐츠 제거, 역할 명확화 |
