---
context_id: cof-task-solver-agent-group-spec
role: REFERENCE
state: const
scope: swarm
lifetime: persistent
created: "2026-01-31"
version: "1.2"
parent_skill: cof-task-solver-agent-group
---

# COF.Task-Solver-Agent-Group.skill
Meta Spec (v1.1)

---

## 0. Purpose

본 문서는 `cof-task-solver-agent-group` 스킬의 상세 설계 스펙을 정의한다.

**핵심 원칙**: 하나의 에이전트 그룹이 하나의 티켓을 해결한다 (One Group, One Ticket).
**정의 보강(AAOS Canon 정합)**: Group(군락)은 티켓 해결 과정에서 **컨텍스트 연속성을 유지하는 단위**이며, Agent Instance는 그 컨텍스트를 운반(carrier)하는 실행 단위이다.

이 스킬의 목적:

1. `NN.agents-task-context/tickets/` 내의 티켓을 읽고 파싱한다
2. `cof-glob-indexing`으로 컨텍스트 경계를 식별하고 인덱싱한다
3. 티켓 태그를 기반으로 적절한 에이전트를 자동 선택한다
4. `call-cli-agents/collaborate.py`로 에이전트를 디스패치한다
5. 결과를 티켓에 기록하고 상태를 갱신한다

---

## 1. Scope

- **입력**: `NN.agents-task-context/tickets/` 내의 티켓 파일 (status: `todo` | `in-progress`)
- **산출물**:
  - 티켓 내 `## Execution Result` 섹션 추가
  - 티켓 frontmatter `status` 갱신
  - `NN.agents-task-context/AGENT_LOG.md` 실행 로그
- **경계**: cof-glob-indexing이 결정한 노드 경계 내로 제한

---

## 2. Definitions

### 2.1 Agent Group

에이전트 그룹(군락, Group)은 하나 이상의 AI CLI(claude, codex, gemini)로 구성된 실행 단위이며, **티켓 해결 과정에서 컨텍스트의 연속성을 유지**한다.

```
Agent Instance ──(N:1)──► Group (군락) ──(N:1)──► Swarm (군체)
```

- Group은 병렬 실행만을 의미하지 않는다. 동일 티켓에 대해 **순차 실행(컨텍스트 계승)** 또한 Group의 실행 방식이다.
- 티켓을 쪼갤 수 있어도, "왜 그렇게 결정했는가" 같은 암묵지(tacit knowledge)가 손실될 수 있으므로 Sequential Group이 필요한 경우가 있다.

| Group Type | Composition | Execution | Use Case |
|------------|-------------|-----------|----------|
| Single | 1 agent | - | 명확한 단일 작업, 전문성 요구 |
| Council | N agents | 병렬 | 교차 검증, 리뷰, 합의 필요 |
| Sequential | N agents | 순차 | 컨텍스트 계승, 누적적 사고, 반복 정제 |

Sequential Group이 특히 필요한 상황:
1. **컨텍스트 누적이 필수**인 작업 (분석 → 설계 → 구현)
2. 단일 인스턴스의 **컨텍스트 한계 초과** (컨텍스트 윈도우 초과)
3. **반복 정제(Iterative Refinement)** (초안 → 비평 → 수정 → 비평 → 최종)

Sequential Group의 컨텍스트 전달 방식은 `full | summary | delta` 중 하나로 정의한다 (추후 확정).

### 2.2 Ticket-Agent Binding

```
ticket ──(1:1)──► agent_group_plan
                     │
                     ├── type: single | council | sequential
                     ├── agents: [claude, codex, gemini]  # council: parallel, sequential: ordered
                     └── context_passing: full|summary|delta  # sequential only
```

- 하나의 티켓은 정확히 하나의 에이전트 그룹에 바인딩된다
- 에이전트 그룹은 티켓이 완료(done) 또는 차단(blocked)될 때까지 해당 티켓만 처리한다
- 바인딩은 실행 시점에 결정되며 티켓에 기록된다

### 2.3 Tag-Based Agent Selection

태그 기반 에이전트 선택은 다음 우선순위를 따른다:

```python
AVAILABLE_PROVIDERS = ["claude", "codex", "gemini"]

# 단일 실행(기본): 특정 provider 1개 선택
SINGLE_PROVIDER_TAG_MAP = {
    # Security domain
    "security": "claude",
    "audit": "claude",
    "compliance": "claude",
    "vulnerability": "claude",

    # Performance domain
    "performance": "gemini",
    "optimization": "gemini",
    "benchmark": "gemini",
    "profiling": "gemini",

    # Architecture domain
    "architecture": "codex",
    "refactor": "codex",
    "design": "codex",
    "structure": "codex",
}

DEFAULT_AGENT = "claude"

# Group execution tags
COUNCIL_TAGS = {"review", "critique", "consensus"}
SEQUENTIAL_TAGS = {"sequential", "iterative", "refinement"}
```

### 2.4 Context Assembly

```
Context = NODE_INDEX.md + ROLE_EVIDENCE.md + Ticket Content
```

| Component | Source | Description |
|-----------|--------|-------------|
| `NODE_INDEX.md` | cof-glob-indexing | 노드 구조, 역할 디렉토리, 앵커 정보 |
| `ROLE_EVIDENCE.md` | cof-glob-indexing | 역할 판단 근거 (JSON 포함) |
| Ticket Content | ticket file | Description + Action Items + DoD |

컨텍스트 템플릿:

```markdown
# Task Context

## Node Structure
{NODE_INDEX.md content}

## Role Evidence
{ROLE_EVIDENCE.md content}

## Ticket
{ticket content}

---

Please complete the action items above. Follow the Definition of Done criteria.
```

---

## 3. State Transitions

### 3.1 Ticket Status State Machine

```
                    ┌─────────────────┐
                    │  Ticket (todo)  │
                    └────────┬────────┘
                             │ solve_ticket.py invoked
                             │ Step 1: Parse ticket
                             ▼
                    ┌─────────────────┐
                    │   in-progress   │◄───────────────┐
                    └────────┬────────┘                │
                             │ Step 2-3: Index context │ retry
                             ▼                         │
                    ┌─────────────────┐                │
                    │ Context Ready   │                │
                    └────────┬────────┘                │
                             │ Step 4: Select group    │
                             ▼                         │
                    ┌─────────────────┐                │
                    │ Group Selected  │                │
                    └────────┬────────┘                │
                             │ Step 5: Dispatch        │
                             ▼                         │
                    ┌─────────────────┐                │
                    │   Executing     │────────────────┘
                    └────────┬────────┘   (timeout/error)
                             │ Step 6-7: Integrate result
                             ▼
              ┌──────────────┴──────────────┐
              ▼                             ▼
     ┌────────────────┐           ┌────────────────┐
     │      done      │           │     blocked    │
     └────────────────┘           └────────────────┘
```

### 3.2 Step Details

#### Step 1: Parse Ticket

입력 검증 및 파싱:

```python
@dataclass
class TicketData:
    path: str
    frontmatter: Dict[str, Any]
    title: str
    description: str
    action_items: List[str]
    definition_of_done: List[str]

    # Extracted from frontmatter
    status: str  # todo | in-progress | done | blocked
    priority: str  # P0 | P1 | P2 | P3
    tags: List[str]
    dependencies: List[str]
    target_path: Optional[str]
```

검증 규칙:
- `status`가 `done`이면 즉시 종료 (exit 0)
- `status`가 없으면 `todo`로 간주
- frontmatter 파싱 실패 시 SEV-2 에러

#### Step 2: Update Status to In-Progress

티켓 status를 `in-progress`로 갱신하고 execution metadata 추가:

```yaml
status: in-progress
execution:
  started_at: "2026-01-31T12:00:00Z"
  agent_group:
    type: single  # single | council | sequential
    agents: [claude]
    context_passing: summary  # sequential only (full|summary|delta)
    max_iterations: 1         # iterative refinement only
```

#### Step 3: Index Context

cof-glob-indexing 호출:

```bash
python3 {COF}/skills/01.cof-glob-indexing/scripts/cof_glob_indexing.py \
  --target-dir "{ticket.target_path or ticket_directory}" \
  --max-depth {context_depth}
```

결과 처리:
- `status: success` -> NODE_INDEX.md, ROLE_EVIDENCE.md 경로 획득
- `status: partial` -> 경고와 함께 계속 진행
- `status: error` -> minimal context fallback 또는 abort

Minimal Context Fallback:
```markdown
# Minimal Context

Unable to perform full context indexing.
Working with ticket content only.

## Ticket
{ticket content}
```

#### Step 4: Select Agent Group Plan

```python
@dataclass
class AgentGroupPlan:
    type: Literal["single", "council", "sequential"]
    agents: List[str]  # council: parallel, sequential: ordered
    context_passing: Literal["full", "summary", "delta"] = "summary"  # sequential only
    max_iterations: int = 1  # iterative refinement only


def select_group_plan(ticket: TicketData, args: Args) -> AgentGroupPlan:
    # Explicit override
    if args.all:
        return AgentGroupPlan(type="council", agents=AVAILABLE_PROVIDERS)
    if args.provider:
        return AgentGroupPlan(type="single", agents=[args.provider])

    tags = {t.lower() for t in ticket.tags}

    # Group execution selection
    if tags & COUNCIL_TAGS:
        return AgentGroupPlan(type="council", agents=AVAILABLE_PROVIDERS)
    if tags & SEQUENTIAL_TAGS:
        return AgentGroupPlan(type="sequential", agents=AVAILABLE_PROVIDERS, context_passing="summary")

    # Default: single provider selection
    for tag in ticket.tags:
        tag_lower = tag.lower()
        if tag_lower in SINGLE_PROVIDER_TAG_MAP:
            return AgentGroupPlan(type="single", agents=[SINGLE_PROVIDER_TAG_MAP[tag_lower]])

    return AgentGroupPlan(type="single", agents=[DEFAULT_AGENT])
```

Council mode 처리:
- 모든 사용 가능한 provider에 동시 디스패치
- 결과를 종합하여 기록

Sequential mode 처리:
- `agents` 순서대로 실행
- 각 단계는 이전 단계의 출력을 컨텍스트로 계승
- 중간 Agent 실패 시 시퀀스 중단 (부분 결과 기록)

**Sequential Group 설계 확정 (v1.2)**:

| 항목 | 결정 | 근거 |
|------|------|------|
| 컨텍스트 전달 방식 | `summary` (기본값) | 컨텍스트 윈도우 효율성, full은 대용량 시 문제 |
| 반복 종료 조건 | 고정 횟수 (`max_iterations=1`) | 품질 기준은 주관적, 추후 QA agent 연계로 확장 |
| 실패 처리 | 시퀀스 중단 + 부분 결과 기록 | 롤백은 복잡도 증가, 부분 완료가 실용적 |
| Council + Sequential 혼합 | 미지원 (v1.x) | 복잡도 대비 효용 불명확, v2에서 재검토 |

컨텍스트 전달 방식 상세:
- `full`: 이전 모든 결과를 원본 그대로 전달
- `summary`: 이전 결과를 2000자로 요약하여 전달 (기본값)
- `delta`: 마지막 결과만 전달

#### Step 5: Dispatch

Single agent:
```bash
python3 {SUMMON_AGENTS}/skill/sa-call-cli-agents/scripts/collaborate.py run \
  -p {agent} \
  --context {context_file} \
  -m "{prompt}" \
  --format json \
  --timeout {timeout}
```

Council mode:
```bash
python3 {SUMMON_AGENTS}/skill/sa-call-cli-agents/scripts/collaborate.py run \
  --all \
  --context {context_file} \
  -m "{prompt}" \
  --format json \
  --timeout {timeout}
```

Sequential mode (conceptual):
```bash
for agent in {agents_in_order}; do
  python3 {SUMMON_AGENTS}/skill/sa-call-cli-agents/scripts/collaborate.py run \
    -p "${agent}" \
    --context {rolling_context_file} \
    -m "{prompt}" \
    --format json \
    --timeout {timeout}
  # integrate agent output into rolling_context_file (full|summary|delta)
done
```

Prompt 구성:
```
{action_items_text}

## Definition of Done
{dod_text}

Please complete all action items and ensure all DoD criteria are met.
```

#### Step 6: Integrate Result

JSON 응답 파싱:
```python
@dataclass
class AgentResult:
    id: str
    provider: str
    success: bool
    returncode: Optional[int]
    timed_out: bool
    output: str
    error: str
    execution_time: float
    timestamp: str
```

티켓에 Execution Result 섹션 추가:
```markdown
## Execution Result

- **Agent Group Type**: {single|council|sequential}
- **Agents**: {agents}
- **Timestamp**: {timestamp}
- **Execution Time**: {execution_time}s
- **Status**: {success | failed | timed_out}

### Output

{agent_output}

### Errors (if any)

{error_output}
```

#### Step 7: Update Status

성공/실패 판정:
- `success: true` AND `returncode: 0` -> `status: done`
- `timed_out: true` -> retry once, then `status: blocked`
- `success: false` -> `status: blocked`

Frontmatter 갱신:
```yaml
status: done  # or blocked
execution:
  started_at: "2026-01-31T12:00:00Z"
  completed_at: "2026-01-31T12:05:00Z"
  agent_group:
    type: single
    agents: [claude]
    context_passing: summary
  execution_time: 300.5
  result: success  # or failed, timed_out
```

#### Step 8: Log to AGENT_LOG.md

```markdown
## [2026-01-31T12:05:00Z] ticket-name.md

- **Agent Group**: single / [claude]
- **Execution Time**: 300.5s
- **Result**: success
- **Ticket Path**: ./01.agents-task-context/tickets/ticket-name.md

---
```

---

## 4. Output Formats

### 4.1 Ticket Update Template

```markdown
---
title: {original_title}
status: done
priority: {priority}
tags: [{tags}]
dependencies: [{dependencies}]
execution:
  started_at: "{iso_timestamp}"
  completed_at: "{iso_timestamp}"
  agent_group:
    type: {single|council|sequential}
    agents: [{agents}]
    context_passing: {full|summary|delta}
    max_iterations: {n}
  execution_time: {seconds}
  result: {success|failed|timed_out}
---

# {title}

{original_content}

## Execution Result

- **Agent Group Type**: {single|council|sequential}
- **Agents**: {agents}
- **Timestamp**: {timestamp}
- **Execution Time**: {execution_time}s
- **Status**: {status}

### Output

{agent_output}
```

### 4.2 AGENT_LOG.md Entry Template

```markdown
## [{timestamp}] {ticket_filename}

- **Agent Group**: {single|council|sequential} / [{agents}]
- **Execution Time**: {execution_time}s
- **Result**: {result}
- **Ticket Path**: {relative_path}
- **Exit Code**: {exit_code}

---
```

### 4.3 JSON Output (--format json)

```json
{
  "status": "success",
  "ticket": {
    "path": "/path/to/ticket.md",
    "title": "Ticket Title",
    "original_status": "todo",
    "final_status": "done"
  },
  "execution": {
    "agent_group": {
      "type": "single",
      "agents": ["claude"],
      "context_passing": "summary",
      "max_iterations": 1
    },
    "started_at": "2026-01-31T12:00:00Z",
    "completed_at": "2026-01-31T12:05:00Z",
    "execution_time": 300.5,
    "context_file": "/path/to/context.md"
  },
  "agent_result": {
    "success": true,
    "returncode": 0,
    "output": "...",
    "error": ""
  },
  "warnings": []
}
```

---

## 5. Error Handling

### 5.1 Error Classification

| Error Type | SEV | Exit Code | Recovery Strategy |
|------------|-----|-----------|-------------------|
| Ticket not found | SEV-1 | 2 | Abort immediately |
| Invalid YAML frontmatter | SEV-2 | 2 | Abort with parse error |
| Missing required fields | SEV-2 | 2 | Abort with validation error |
| Context indexing failed | SEV-2 | 3 | Minimal context fallback |
| No agents available | SEV-2 | 4 | Abort with availability error |
| Agent timeout | SEV-2 | 5 | Retry once (+60s), then block |
| Agent execution error | SEV-3 | 5 | Mark blocked, log error |
| File write error | SEV-2 | 1 | Retry once, then abort |

### 5.2 Retry Policy

```python
RETRY_CONFIG = {
    "agent_timeout": {
        "max_retries": 1,
        "timeout_increment": 60,  # seconds
    },
    "file_write": {
        "max_retries": 1,
        "delay": 1,  # seconds
    },
    "context_indexing": {
        "max_retries": 0,  # fallback instead
        "fallback": "minimal_context",
    },
}
```

### 5.3 Error Response Format

```json
{
  "status": "error",
  "error_code": "TICKET_NOT_FOUND",
  "error_message": "Ticket file does not exist: /path/to/ticket.md",
  "ticket": {
    "path": "/path/to/ticket.md"
  },
  "recoverable": false,
  "suggestions": [
    "Check if the ticket path is correct",
    "Ensure the ticket file exists in NN.agents-task-context/tickets/"
  ]
}
```

---

## 6. Integration Points

### 6.1 cof-glob-indexing

**Purpose**: 컨텍스트 경계 식별 및 인덱싱

**Interface**:
```bash
python3 scripts/cof_glob_indexing.py \
  --target-dir {path} \
  --max-depth {depth}
```

**Output**: JSON to stdout
```json
{
  "status": "success",
  "artifacts": {
    "node_index": "/path/to/NODE_INDEX.md",
    "role_evidence": "/path/to/ROLE_EVIDENCE.md"
  }
}
```

### 6.2 call-cli-agents/collaborate.py

**Purpose**: AI CLI 에이전트 디스패치

**Interface**:
```bash
python3 collaborate.py run \
  -p {provider} \
  --context {file} \
  -m {message} \
  --format json \
  --timeout {seconds}
```

**Output**: JSON to stdout (TaskResult array)

### 6.3 cof-task-manager-node

**Purpose**: 티켓 생성/관리 (이 스킬의 upstream)

**Handoff**: 티켓 파일 경로

---

## 7. Configuration

### 7.1 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `COF_ROOT` | auto-detect | COF 루트 디렉토리 |
| `SUMMON_AGENTS_ROOT` | auto-detect | summon-agents 루트 |
| `DEFAULT_TIMEOUT` | 300 | 기본 타임아웃 (초) |
| `DEFAULT_CONTEXT_DEPTH` | 10 | 기본 인덱싱 깊이 |
| `AGENT_LOG_MAX_ENTRIES` | 1000 | 로그 최대 항목 수 |

### 7.2 Config File (Optional)

`~/.config/cof/task-solver.yaml`:
```yaml
default_provider: claude
default_group_type: single  # single|council|sequential
timeout: 300
context_depth: 10
available_providers: [claude, codex, gemini]
council_agents: [claude, codex, gemini]
sequential_agents: [claude, codex, gemini]
sequential:
  context_passing: summary  # full|summary|delta
  max_iterations: 1
agent_tag_map:
  security: claude
  performance: gemini
  architecture: codex
retry:
  agent_timeout_increment: 60
  max_retries: 1
```

---

## 8. Hard Constraints

1. **One Group, One Ticket**: 단일 실행에서 하나의 티켓만 처리한다.
   - Sequential Group은 여러 agent step/iteration으로 실행되더라도 하나의 티켓 실행으로 간주한다.

2. **Status Integrity**: 상태 전이는 `todo -> in-progress -> done|blocked` 순서를 따른다. 역방향 전이 금지.

3. **Result Recording**: 모든 실행 결과는 티켓에 기록되어야 한다. Silent failure 금지.

4. **Context Boundary**: 컨텍스트는 cof-glob-indexing이 결정한 노드 경계 내로 제한된다.

5. **Idempotency**: `done` 상태 티켓 재실행은 no-op이다.

6. **Log Append-Only**: AGENT_LOG.md는 append-only이다. 기존 로그 수정 금지.

---

## 9. Non-Goals

- 병렬 티켓 처리 (단일 실행당 하나의 티켓)
- 티켓 생성 (cof-task-manager-node 역할)
- 에이전트 학습/튜닝
- 결과 품질 평가 (cof-task-qa 역할)
- 전역 인덱스 생성

---

## 10. Security Considerations

1. **Input Validation**: 티켓 경로는 `NN.agents-task-context/tickets/` 내로 제한
2. **Context Isolation**: 노드 경계 외부 파일 참조 금지
3. **Credential Handling**: API 키는 환경 변수에서만 로드
4. **Output Sanitization**: 에이전트 출력에서 민감 정보 필터링 (선택적)

---

## 11. References

| Document | Context Reference | Description |
|----------|-------------------|-------------|
| Parent Skill | `@ref(cof-task-solver-agent-group)` | 스킬 메인 문서 |
| cof-glob-indexing | `@ref(cof-glob-indexing)` | 컨텍스트 인덱싱 |
| cof-task-manager-node | `@ref(cof-task-manager-node)` | 티켓 관리 |
| call-cli-agents | `@ref(call-cli-agents)` | 에이전트 디스패치 |
| AAOS Canon | `@ref(aaos-canon)` | Group(군락) / Swarm(군체) 정의 |
| Rule Genome | `@ref(cof-environment-set)` | COF 환경 규칙 |
| Skill Normative | `@ref(skill-normative-interpretation)` | 스킬 작성 규범 |

---

## Appendix A. Changelog

| Version | Date | Changes |
|---------|------|---------|
| v0.1 | 2026-01-31 | Initial draft |
| v1.0 | 2026-01-31 | Complete rewrite: added detailed state transitions, error handling, configuration, security considerations |
| v1.1 | 2026-01-31 | Align group semantics with AAOS Canon; add Sequential Group type and extend selection/metadata/templates |
| v1.2 | 2026-01-31 | Sequential Group 설계 확정; 미해결 질문 해소; @ref() 참조 통일; AgentGroupPlan 코드 동기화 |
