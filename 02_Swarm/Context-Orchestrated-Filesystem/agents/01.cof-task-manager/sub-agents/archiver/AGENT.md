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
| `node_path` | `string` | Y | NN.agents-task-context/ 경로 (legacy: task-manager/) |
| `dry_run` | `boolean` | N | true면 이동 없이 대상만 반환 |
| `qa_filter` | `enum` | N | `all` \| `qa_passed` (default: `qa_passed`) |
| `qa_threshold` | `enum` | N | `A` \| `B` \| `C` (default: `B`) |

### Outputs

| 산출물 | 타입 | 설명 |
|--------|------|------|
| `success` | `boolean` | 아카이빙 성공 여부 |
| `archived` | `array` | 아카이빙된 티켓 목록 |
| `skipped` | `array` | 건너뛴 티켓 목록 (done이 아닌 것) |
| `qa_skipped` | `array` | QA 미통과로 제외된 티켓 목록 |
| `errors` | `array` | 에러 목록 |

---

## 3. Archiving Rules

### 3.1 Target Selection

```
대상 조건:
- 위치: NN.agents-task-context/tickets/*.md (legacy: task-manager/tickets/*.md)
- frontmatter.status == "done"
- (qa_filter == 'qa_passed') ?
    └─ frontmatter.qa_grade in ['A', 'B'] (또는 qa_threshold 이상)
    └─ 또는 ## QA Review 섹션 존재 + Grade 확인
- (qa_filter == 'all') ?
    └─ QA 상태 무관 (강제 아카이브)
```

**QA Grade 확인 우선순위:**
1. `frontmatter.qa_grade`
2. 본문 `## QA Review` 섹션 내 Grade 파싱
3. 둘 다 없으면 → `unreviewed` (qa_passed 필터 시 제외)

### 3.2 Archive Structure

```
NN.agents-task-context/
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

## 4. Execution Flow (도구 기반, 병렬)

```
[Phase 1: 대상 식별] (순차)
1. Glob: tickets/*.md 목록 수집

2. 각 티켓에 대해:
   Read: 티켓 파일 → YAML frontmatter 파싱
   - status == "done" 확인
   - qa_grade 또는 ## QA Review 섹션 확인
   - qa_filter 조건 충족 여부 판정

3. 대상 티켓 목록 확정 (done + QA 통과)

[Phase 2: 아카이브 준비] (순차)
4. Glob: archive/tickets/ 존재 확인
   └─ 없으면 → Bash(mkdir -p): archive/tickets/ 생성

5. 각 대상 티켓에 대해:
   Glob: archive/tickets/{name}.md 충돌 확인
   └─ 충돌 시 → 타임스탬프 suffix 결정

[Phase 3: 이동] (병렬)
6. 대상 티켓들을 병렬로 이동:
   각 티켓마다:
   ├─ Read: tickets/{name}.md
   ├─ Write: archive/tickets/{final_name}.md
   └─ Bash(rm): tickets/{name}.md 삭제

[Phase 4: 로그] (순차)
7. Read: archive/README.md (없으면 생성)
   Edit: 아카이빙 로그 append

8. 결과 반환
```

### 4.1 Required Tools

| 도구 | 용도 |
|------|------|
| `Glob` | 티켓 목록 수집, 충돌 확인 |
| `Read` | 티켓 파일/README.md 읽기, YAML 파싱 |
| `Write` | 아카이브 파일 생성 |
| `Edit` | README.md 로그 append |
| `Bash` | `mkdir -p`, `rm` (디렉토리 생성, 원본 삭제) |
| `Task` | 이동 작업 병렬 호출 |

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
- **QA 통과 기본 필수**: `qa_filter: qa_passed`가 기본값
- **비파괴적 이동**: 원본 삭제 전 복사 완료 확인
- **로그 필수**: 모든 아카이빙은 README.md에 기록
- **충돌 회피**: 타임스탬프 suffix로 해결 (덮어쓰기 금지)
- **QA 미통과 강제 아카이브 금지**: `qa_filter: all`은 Orchestrator에서만 설정 가능

---

## 7. References

| 문서 | 설명 |
|------|------|
| `../../AGENT.md` | Parent Agent |
| `cof-task-qa-agent` | QA Agent (아카이브 전 품질 검토) |
