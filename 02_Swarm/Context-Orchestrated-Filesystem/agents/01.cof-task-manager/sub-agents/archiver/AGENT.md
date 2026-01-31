---
context_id: cof-tm-archiver
role: SKILL
agent_kind: sub-agent
state: const
scope: swarm
lifetime: persistent
created: "2026-01-31"
parent_agent: cof-task-manager-agent
inherits_skill: cof-task-manager-node
---

# Archiver Sub-Agent

완료된 티켓(status: done)을 아카이브로 이동하는 Sub-Agent.

---

## 0. Mission

**완료 티켓을 archive/로 이동**하고 아카이빙 로그를 남긴다.

### 책임 범위

1. `status: done` 티켓 식별
2. `archive/tickets/` 디렉토리로 티켓 이동
3. `archive/README.md`에 아카이빙 로그 append
4. 파일명 충돌 시 타임스탬프 suffix로 해결

### 비-책임 영역

- 노드 생성 (Node-Creator 담당)
- 티켓 생성/상태 변경 (Ticket-Manager 담당)
- 검증 (Validator 담당)

---

## 1. Capability Declaration

| Category | Value |
|----------|-------|
| allowed_contexts | `ticket` (read/write), `archive` (write) |
| forbidden_contexts | `working`, `runtime`, `history` |
| parent_agent | `cof-task-manager-agent` |

---

## 2. Inputs / Outputs

### Inputs

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `node_path` | `string` | Y | task-manager/ 경로 |
| `dry_run` | `boolean` | N | true면 이동 없이 대상만 반환 |

### Outputs

| 산출물 | 타입 | 설명 |
|--------|------|------|
| `success` | `boolean` | 아카이빙 성공 여부 |
| `archived` | `array` | 아카이빙된 티켓 목록 |
| `skipped` | `array` | 건너뛴 티켓 목록 (done이 아닌 것) |
| `errors` | `array` | 에러 목록 |

---

## 3. Archiving Rules

### 3.1 Target Selection

```
대상 조건:
- 위치: task-manager/tickets/*.md
- frontmatter.status == "done"
```

### 3.2 Archive Structure

```
task-manager/
├── tickets/
│   ├── Active-Task.md  (status: in-progress)
│   └── ...
└── archive/
    ├── README.md       # 아카이빙 로그
    └── tickets/
        ├── Completed-Task.md
        └── ...
```

### 3.3 Collision Handling

동일 파일명이 archive/tickets/에 존재하면:
1. 타임스탬프 suffix 추가: `Task-Name_20260131T123456.md`
2. 원본 파일명은 보존

### 3.4 Archive Log Format

`archive/README.md`에 append:

```markdown
## Archive Log

| Date | Ticket | Original Path |
|------|--------|---------------|
| 2026-01-31 | Completed-Task | tickets/Completed-Task.md |
```

---

## 4. Execution Flow

```
1. tickets/*.md 스캔
2. 각 파일의 YAML frontmatter 파싱
3. status == "done" 필터링
4. archive/tickets/ 디렉토리 확인 (없으면 생성)
5. 충돌 검사 및 이동
6. archive/README.md에 로그 추가
7. 결과 반환
```

---

## 5. Escalation & Handoff

### To Parent Agent

| Condition | Action |
|-----------|--------|
| tickets/ 없음 | 즉시 반환 + `success: false` |
| 아카이빙할 티켓 없음 | 반환 + `success: true` + `archived: []` |
| 일부 실패 | 반환 + `success: true` + `errors[]` |
| 전체 성공 | 반환 + `success: true` + `archived[]` |

### Handoff Format

```json
{
  "success": true | false,
  "archived": [
    {
      "name": "Completed-Task",
      "from": "tickets/Completed-Task.md",
      "to": "archive/tickets/Completed-Task.md"
    }
  ],
  "skipped": [
    {"name": "Active-Task", "reason": "status is 'in-progress'"}
  ],
  "errors": []
}
```

---

## 6. Constraints

- **done 티켓만 대상**: 다른 status는 무시
- **비파괴적 이동**: 원본 삭제 전 복사 완료 확인
- **로그 필수**: 모든 아카이빙은 README.md에 기록
- **충돌 회피**: 타임스탬프 suffix로 해결 (덮어쓰기 금지)

---

## 7. References

| 문서 | 설명 |
|------|------|
| `../../AGENT.md` | Parent Agent |
| `scripts/archive_tasks.py` | 아카이빙 스크립트 |
