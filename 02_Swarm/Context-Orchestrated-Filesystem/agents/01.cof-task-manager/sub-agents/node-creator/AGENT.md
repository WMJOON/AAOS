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

NN.agents-task-context/ 노드 구조 생성을 담당하는 Sub-Agent. (legacy: task-manager/)

---

## 0. Mission

**NN.agents-task-context/ 노드 생성 작업을 독립적으로 수행**하고 결과를 반환한다.

### 책임 범위

1. `01.agents-task-context/` 디렉토리 구조 생성 (권장 패턴: `NN.agents-task-context/`)
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
| `target_path` | `string` | Y | `01.agents-task-context/`를 생성할 상위 디렉토리 |
| `with_issue_notes` | `boolean` | N | issue_notes/ 포함 여부 |
| `with_release_notes` | `boolean` | N | release_notes/ 포함 여부 |
| `all` | `boolean` | N | 모든 선택적 노드 포함 |

### Outputs

| 산출물 | 타입 | 설명 |
|--------|------|------|
| `success` | `boolean` | 생성 성공 여부 |
| `path` | `string` | 생성된 01.agents-task-context/ 경로 |
| `created` | `array` | 생성된 파일/디렉토리 목록 |
| `errors` | `array` | 발생한 에러 목록 |

---

## 3. Execution Rules

### 3.1 Pre-conditions

| 규칙 | 조건 | 실패 시 |
|------|------|---------|
| 대상 경로 존재 | `target_path` 디렉토리 존재 | `TARGET_NOT_FOUND` |
| 노드 미존재 | `01.agents-task-context/` 및 legacy `task-manager/` 없음 | `NODE_ALREADY_EXISTS` |
| 쓰기 권한 | 대상 경로에 쓰기 가능 | `PERMISSION_DENIED` |

### 3.2 Creation Sequence (도구 기반)

```
1. Glob: target_path 존재 확인
   └─ 없으면 → TARGET_NOT_FOUND 반환

2. Glob: */01.agents-task-context 또는 */task-manager 존재 확인
   └─ 있으면 → NODE_ALREADY_EXISTS 반환

3. Bash(mkdir -p): 01.agents-task-context/tickets/ 생성

4. Read: templates/NODE_RULE.md 읽기
   Write: 01.agents-task-context/RULE.md 생성

5. Read: templates/TROUBLESHOOTING-TEMPLATE.md 읽기
   Write: 01.agents-task-context/troubleshooting.md 생성

6. (if with_issue_notes)
   Bash(mkdir): issue_notes/ 생성
   Read: templates/ISSUE_NOTE_RULE.md 읽기
   Write: issue_notes/RULE.md 생성

7. (if with_release_notes)
   Bash(mkdir): release_notes/ 생성
   Read: templates/RELEASE_NOTE_RULE.md 읽기
   Write: release_notes/RULE.md 생성
```

### 3.3 Template Sources

| 파일 | 템플릿 경로 |
|------|------------|
| `RULE.md` | `skills/02.cof-task-manager-node/templates/NODE_RULE.md` |
| `troubleshooting.md` | `skills/02.cof-task-manager-node/templates/TROUBLESHOOTING-TEMPLATE.md` |
| `issue_notes/RULE.md` | `skills/02.cof-task-manager-node/templates/ISSUE_NOTE_RULE.md` |
| `release_notes/RULE.md` | `skills/02.cof-task-manager-node/templates/RELEASE_NOTE_RULE.md` |

### 3.4 Required Tools

| 도구 | 용도 |
|------|------|
| `Glob` | 경로 존재 확인, 중복 검사 |
| `Bash` | `mkdir -p` 디렉토리 생성 |
| `Read` | 템플릿 파일 읽기 |
| `Write` | 대상 파일 생성 |

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
  "path": "/path/to/01.agents-task-context",
  "created": [
    "01.agents-task-context/",
    "01.agents-task-context/tickets/",
    "01.agents-task-context/RULE.md",
    "01.agents-task-context/troubleshooting.md"
  ],
  "errors": []
}
```

---

## 5. Constraints

- **덮어쓰기 금지**: 기존 01.agents-task-context/ 또는 legacy task-manager/ 발견 시 즉시 중단
- **부분 생성 금지**: 모든 기본 구조가 함께 생성됨
- **템플릿 의존**: 템플릿 파일 누락 시 에러

---

## 6. References

| 문서 | 설명 |
|------|------|
| `../../AGENT.md` | Parent Agent |
| `../../../../skills/02.cof-task-manager-node/templates/` | 템플릿 파일들 |
