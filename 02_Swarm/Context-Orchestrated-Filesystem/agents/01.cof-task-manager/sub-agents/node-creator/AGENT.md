---
context_id: cof-tm-node-creator
role: SKILL
agent_kind: sub-agent
state: const
scope: swarm
lifetime: persistent
created: "2026-01-31"
parent_agent: cof-task-manager-agent
inherits_skill: cof-task-manager-node
---

# Node-Creator Sub-Agent

task-manager/ 노드 구조 생성을 담당하는 Sub-Agent.

---

## 0. Mission

**task-manager/ 노드 생성 작업을 독립적으로 수행**하고 결과를 반환한다.

### 책임 범위

1. `task-manager/` 디렉토리 구조 생성
2. `RULE.md`, `troubleshooting.md` 기본 파일 생성
3. `tickets/` 디렉토리 생성
4. 선택적 하위 노드 생성 (`issue_notes/`, `release_notes/`)

### 비-책임 영역

- 노드 검증 (Validator 담당)
- 티켓 생성 (Ticket-Manager 담당)
- 아카이빙 (Archiver 담당)

---

## 1. Capability Declaration

| Category | Value |
|----------|-------|
| allowed_contexts | `working` (write) |
| forbidden_contexts | `ticket`, `history`, `runtime` |
| parent_agent | `cof-task-manager-agent` |

---

## 2. Inputs / Outputs

### Inputs

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `target_path` | `string` | Y | task-manager/를 생성할 상위 디렉토리 |
| `with_issue_notes` | `boolean` | N | issue_notes/ 포함 여부 |
| `with_release_notes` | `boolean` | N | release_notes/ 포함 여부 |
| `all` | `boolean` | N | 모든 선택적 노드 포함 |

### Outputs

| 산출물 | 타입 | 설명 |
|--------|------|------|
| `success` | `boolean` | 생성 성공 여부 |
| `path` | `string` | 생성된 task-manager/ 경로 |
| `created` | `array` | 생성된 파일/디렉토리 목록 |
| `errors` | `array` | 발생한 에러 목록 |

---

## 3. Execution Rules

### 3.1 Pre-conditions

| 규칙 | 조건 | 실패 시 |
|------|------|---------|
| 대상 경로 존재 | `target_path` 디렉토리 존재 | `TARGET_NOT_FOUND` |
| 노드 미존재 | `task-manager/` 없음 | `NODE_ALREADY_EXISTS` |
| 쓰기 권한 | 대상 경로에 쓰기 가능 | `PERMISSION_DENIED` |

### 3.2 Creation Sequence

```
1. task-manager/ 디렉토리 생성
2. tickets/ 디렉토리 생성
3. RULE.md 생성 (from NODE_RULE.md template)
4. troubleshooting.md 생성 (from TROUBLESHOOTING-TEMPLATE.md)
5. (if with_issue_notes) issue_notes/ + RULE.md 생성
6. (if with_release_notes) release_notes/ + RULE.md 생성
```

### 3.3 Template Sources

| 파일 | 템플릿 |
|------|--------|
| `RULE.md` | `templates/NODE_RULE.md` |
| `troubleshooting.md` | `templates/TROUBLESHOOTING-TEMPLATE.md` |
| `issue_notes/RULE.md` | `templates/ISSUE_NOTE_RULE.md` |
| `release_notes/RULE.md` | `templates/RELEASE_NOTE_RULE.md` |

---

## 4. Escalation & Handoff

### To Parent Agent

| Condition | Action |
|-----------|--------|
| 대상 경로 없음 | 즉시 반환 + `success: false` |
| 노드 이미 존재 | 즉시 반환 + `success: false` |
| 권한 없음 | 즉시 반환 + `success: false` |
| 생성 성공 | 반환 + `success: true` + `created[]` |

### Handoff Format

```json
{
  "success": true | false,
  "path": "/path/to/task-manager",
  "created": [
    "task-manager/",
    "task-manager/tickets/",
    "task-manager/RULE.md",
    "task-manager/troubleshooting.md"
  ],
  "errors": []
}
```

---

## 5. Constraints

- **덮어쓰기 금지**: 기존 task-manager/ 발견 시 즉시 중단
- **부분 생성 금지**: 모든 기본 구조가 함께 생성됨
- **템플릿 의존**: 템플릿 파일 누락 시 에러

---

## 6. References

| 문서 | 설명 |
|------|------|
| `../../AGENT.md` | Parent Agent |
| `scripts/create_node.py` | 노드 생성 스크립트 |
| `scripts/bootstrap_node.py` | Bootstrap 스크립트 |
| `templates/` | 템플릿 파일들 |
