# COF.Task-Manager-Node.skill
Meta Spec (v0.2)

---

## 0. Purpose

본 문서는 COF(Context-Orchestrated Filesystem)에서 작업 맥락을 관리하기 위한 `task-manager/` 노드의 생성·검증·티켓 발행·아카이빙을 수행하는 스킬 `cof-task-manager-node`의 스펙을 정의한다.

목표:

1. 작업 시작 시 `task-manager/` 노드(및 최소 구조)를 빠르게 생성한다.
2. 표준 티켓 포맷(YAML frontmatter 포함)을 강제한다.
3. 티켓 의존성(dependencies)을 검증 가능하게 기록한다.
4. 완료(done) 티켓을 아카이브로 이동하고, 아카이브 로그를 남긴다.

---

## 1. Scope

- 대상: 임의의 작업 디렉토리(프로젝트/노트/레포 등)
- 생성 위치: 대상 디렉토리의 자식으로 `task-manager/`를 생성
- 산출물:
  - `task-manager/RULE.md`
  - `task-manager/troubleshooting.md`
  - `task-manager/tickets/` (+ 티켓 파일들)
  - (선택) `task-manager/issue_notes/` + `RULE.md`
  - (선택) `task-manager/release_notes/` + `RULE.md`
  - (아카이빙 시) `task-manager/archive/tickets/` + `task-manager/archive/README.md`

---

## 2. Definitions

### 2.1 Task-Manager Node

`task-manager/`는 특정 작업 범위의 티켓과 작업 중 기록(이슈/릴리즈/트러블슈팅)을 모아, 후속 에이전트가 작업을 이어갈 수 있도록 하는 로컬 컨텍스트 노드이다.

### 2.2 Ticket

티켓은 `task-manager/tickets/*.md`로 저장되는 단위 작업 문서이며, 최소 YAML frontmatter를 포함한다.

#### Dependencies (핵심 규칙)

`dependencies`는 **의존 티켓의 파일 stem(확장자 `.md` 제외)** 목록이다.

- 예: `"Implement-Parser"` (파일: `Implement-Parser.md`)
- 금지: 경로 포함, 확장자 포함, 비결정적 별칭

---

## 3. Inputs

### 3.1 Node Creation

- `target_path` (required): `task-manager/`를 만들 상위 디렉토리 경로
- 옵션:
  - `--with-issue-notes`
  - `--with-release-notes`
  - `--all` (위 옵션 모두 포함)

### 3.2 Ticket Creation

- `name` (required): 티켓 제목
- `--dir` (default: `.`): 기준 디렉토리
  - 허용: `task-manager/`, `task-manager/tickets/`, 또는 그 상위(스クリ프트가 탐색)
- `--deps` (optional): 의존 티켓 목록(입력은 자동 정규화되어 `dependencies`에 기록됨)
- `--priority` (default: `P2`)

### 3.3 Verify / Validate / Archive

- `path` (required): `task-manager/` 경로

---

## 4. Outputs

### 4.1 Ticket File

`task-manager/tickets/<sanitized-title>.md`

- 파일명은 sanitize 규칙을 따른다(공백→하이픈, 허용 문자 외 제거).
- frontmatter의 `dependencies`는 sanitize된 티켓 stem 목록으로 기록한다.

### 4.2 Archive Log

`task-manager/archive/README.md`에 아카이빙 이벤트를 append한다.

---

## 5. Workflow (Checklist)

```
Task-Manager Node Workflow:
- [ ] Step 1: Create node structure (create_node.py)
- [ ] Step 2: Verify structure (verify_node.py)
- [ ] Step 3: Create tickets (create_ticket.py)
- [ ] Step 4: Validate dependencies (validate_node.py)
- [ ] Step 5: Archive done tickets (archive_tasks.py)
```

---

## 6. Guardrails (Hard Constraints)

- `task-manager/`가 이미 존재하면 생성은 실패한다(덮어쓰기 금지).
- 티켓 `dependencies`는 파일 stem 기준으로 검증 가능해야 한다(비결정적 문자열 금지).
- 아카이빙은 `status: done`인 티켓만 대상으로 한다.
- 아카이브 충돌(동명 파일)이 발생하면 timestamp suffix로 회피한다.

---

## 7. References

- Rule Genome: `../../RULE.md`
- COF Doctrine: `../../COF_DOCTRINE.md`
