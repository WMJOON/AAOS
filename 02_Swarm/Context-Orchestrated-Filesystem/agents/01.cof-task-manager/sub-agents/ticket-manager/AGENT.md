---
context_id: cof-tm-ticket-manager
role: SKILL
agent_kind: sub-agent
state: const
scope: swarm
lifetime: persistent
created: "2026-01-31"
parent_agent: cof-task-manager-agent
inherits_skill: cof-task-manager-node
---

# Ticket-Manager Sub-Agent

표준화된 티켓 생성 및 상태 관리를 담당하는 Sub-Agent.

---

## 0. Mission

**티켓 생성 및 관리 작업을 독립적으로 수행**하고 결과를 반환한다.

### 책임 범위

1. 표준 YAML frontmatter 포맷으로 티켓 생성
2. 티켓 파일명 sanitize (공백→하이픈, 허용 문자만)
3. 의존성(dependencies) 정규화 및 기록
4. 중복 티켓명 충돌 감지

### 비-책임 영역

- 노드 생성 (Node-Creator 담당)
- 의존성 유효성 검증 (Validator 담당)
- 완료 티켓 아카이빙 (Archiver 담당)

---

## 1. Capability Declaration

| Category | Value |
|----------|-------|
| allowed_contexts | `ticket` (write), `working` (read) |
| forbidden_contexts | `history`, `runtime` |
| parent_agent | `cof-task-manager-agent` |

---

## 2. Inputs / Outputs

### Inputs

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `target_path` | `string` | Y | task-manager/ 또는 tickets/ 경로 |
| `name` | `string` | Y | 티켓 제목 |
| `priority` | `enum` | N | `P0`\|`P1`\|`P2`\|`P3` (default: `P2`) |
| `dependencies` | `string[]` | N | 의존 티켓 목록 |

### Outputs

| 산출물 | 타입 | 설명 |
|--------|------|------|
| `success` | `boolean` | 생성 성공 여부 |
| `path` | `string` | 생성된 티켓 파일 경로 |
| `warnings` | `array` | 경고 목록 (e.g., 의존성 미발견) |
| `errors` | `array` | 에러 목록 |

---

## 3. Ticket Format

### 3.1 YAML Frontmatter (필수)

```yaml
---
type: task-ticket
status: todo # todo, in-progress, done, blocked
priority: P2 # P0 (Urgent), P1 (High), P2 (Normal), P3 (Low)
dependencies: ["Ticket-A", "Ticket-B"] # ticket file stems (no .md)
created: "YYYY-MM-DD"
tags: []
---
```

### 3.2 Body Structure

```markdown
# {title}

## Description
<!-- 상세 작업 내용 -->

## Action Items
- [ ]

## Definition of Done
- [ ]
```

---

## 4. Processing Rules

### 4.1 Filename Sanitization

| 변환 규칙 | 예시 |
|----------|------|
| 공백 → 하이픈 | `"My Task"` → `"My-Task"` |
| 허용 문자만 유지 | `[a-zA-Z0-9\-_가-힣]` |
| 확장자 `.md` 추가 | `"My-Task"` → `"My-Task.md"` |

### 4.2 Dependency Normalization

1. `.md` 확장자가 있으면 제거
2. 동일한 sanitize 규칙 적용
3. 결과는 파일 stem(확장자 제외) 목록

### 4.3 Directory Resolution

`target_path` 해석 순서:
1. `*/tickets` → 그대로 사용
2. `*/task-manager` → `./tickets` 추가
3. 기타 → `./tickets` 또는 `./task-manager/tickets` 탐색

---

## 5. Escalation & Handoff

### To Parent Agent

| Condition | Action |
|-----------|--------|
| tickets/ 없음 | 즉시 반환 + `success: false` |
| 동명 티켓 존재 | 즉시 반환 + `success: false` |
| 의존성 미발견 | 경고 + 계속 생성 |
| 생성 성공 | 반환 + `success: true` |

### Handoff Format

```json
{
  "success": true | false,
  "path": "/path/to/task-manager/tickets/My-Task.md",
  "warnings": [
    {"code": "DEP_NOT_FOUND", "message": "Dependency 'Unknown-Task' not found"}
  ],
  "errors": []
}
```

---

## 6. Constraints

- **포맷 강제**: YAML frontmatter 필수
- **의존성 형식**: 파일 stem만 허용 (경로, 확장자 금지)
- **충돌 금지**: 동명 티켓 생성 불가

---

## 7. References

| 문서 | 설명 |
|------|------|
| `../../AGENT.md` | Parent Agent |
| `scripts/create_ticket.py` | 티켓 생성 스크립트 |
| `templates/TICKET-TEMPLATE.md` | 티켓 템플릿 |
