---
context_id: cof-task-solver-agent-group-spec
role: REFERENCE
state: const
scope: swarm
lifetime: persistent
created: "2026-01-31"
parent_skill: cof-task-solver-agent-group
---

# COF.Task-Solver-Agent-Group.skill
Meta Spec (v0.1)

---

## 0. Purpose

본 문서는 `task-solver-agent-group` 스킬의 상세 설계 스펙을 정의한다.

**핵심 원칙**: 하나의 에이전트 그룹은 하나의 티켓을 해결한다.

---

## 1. Scope

- **대상**: `task-manager/tickets/` 내의 티켓 파일 (status: `todo` | `in-progress`)
- **산출물**:
  - 티켓 내 `## Execution Result` 섹션 추가
  - 티켓 frontmatter `status` 갱신
  - `task-manager/AGENT_LOG.md` 실행 로그

---

## 2. Definitions

### 2.1 Agent Group

에이전트 그룹은 하나 이상의 AI CLI(claude, codex, gemini)로 구성된 실행 단위이다.

| Group Type | Composition | Use Case |
|------------|-------------|----------|
| Single | 1 agent | 명확한 단일 작업 |
| Council | 3 agents (all) | 교차 검증, 리뷰, 합의 필요 |

### 2.2 Ticket-Agent Binding

```
ticket ──(1:1)──► agent_group
                     │
                     ├── claude (single)
                     ├── codex (single)
                     ├── gemini (single)
                     └── all (council)
```

- 하나의 티켓은 정확히 하나의 에이전트 그룹에 바인딩된다
- 에이전트 그룹은 티켓이 완료(done) 또는 차단(blocked)될 때까지 해당 티켓만 처리한다

### 2.3 Context Assembly

```
Context = NODE_INDEX.md + ROLE_EVIDENCE.md + Ticket Content
```

| Component | Source | Description |
|-----------|--------|-------------|
| `NODE_INDEX.md` | cof-glob-indexing | 노드 구조 인덱스 |
| `ROLE_EVIDENCE.md` | cof-glob-indexing | 역할 디렉토리 및 anchor 정보 |
| Ticket Content | ticket file | Description + Action Items |

---

## 3. State Transitions

```
                    ┌─────────────────┐
                    │  Ticket (todo)  │
                    └────────┬────────┘
                             │ Step 1: Parse ticket
                             ▼
                    ┌─────────────────┐
                    │   in-progress   │
                    └────────┬────────┘
                             │ Step 2: Index context
                             ▼
                    ┌─────────────────┐
                    │ Context Ready   │
                    └────────┬────────┘
                             │ Step 3: Select agent
                             ▼
                    ┌─────────────────┐
                    │ Agent Selected  │
                    └────────┬────────┘
                             │ Step 4: Dispatch
                             ▼
                    ┌─────────────────┐
                    │   Executing     │
                    └────────┬────────┘
                             │ Step 5: Integrate result
                             ▼
              ┌──────────────┴──────────────┐
              ▼                             ▼
     ┌────────────────┐           ┌────────────────┐
     │      done      │           │     blocked    │
     └────────────────┘           └────────────────┘
```

### Step Details

#### Step 1: Parse Ticket

- 티켓 frontmatter 파싱 (status, priority, dependencies, tags)
- Description, Action Items, Definition of Done 추출
- status가 `done`이면 즉시 종료

#### Step 2: Index Context

```bash
python3 {COF}/skills/01.cof-glob-indexing/scripts/cof_glob_indexing.py \
  --target-dir "{ticket.target_path}" \
  --max-depth {context-depth}
```

- NODE_INDEX.md, ROLE_EVIDENCE.md 생성
- 실패 시 minimal context로 fallback

#### Step 3: Select Agent

```python
def select_agent(ticket, args):
    tags = ticket.frontmatter.get('tags', [])

    if args.get('all'):
        return 'all'
    if args.get('provider'):
        return args['provider']

    # Auto selection by tags
    if any(t in tags for t in ['security', 'audit']):
        return 'claude'
    if any(t in tags for t in ['performance', 'optimization']):
        return 'gemini'
    if any(t in tags for t in ['architecture', 'refactor']):
        return 'codex'
    if any(t in tags for t in ['review', 'critique']):
        return 'all'

    return 'claude'  # default
```

#### Step 4: Dispatch

```bash
# Single agent
python3 {SUMMON_AGENTS}/skill/call-cli-agents/scripts/collaborate.py run \
  -p {agent} \
  --context {context_file} \
  -m "{prompt}" \
  --format json \
  --timeout {timeout}

# Council mode
python3 ... run --all --context ... -m "..." --format json
```

#### Step 5: Integrate Result

- JSON 응답 파싱
- 티켓에 Execution Result 섹션 추가
- success → `status: done`
- failure → `status: blocked`
- AGENT_LOG.md에 로그 append

---

## 4. Output Formats

### 4.1 Ticket Update

```markdown
## Execution Result

- **Agent**: claude
- **Timestamp**: 2026-01-31T12:00:00
- **Status**: success | failed

### Output

{agent_output}
```

### 4.2 Agent Log Entry

```markdown
## [2026-01-31T12:00:00] ticket-name.md

- **Agent Group**: claude
- **Execution Time**: 45.2s
- **Result**: success
```

---

## 5. Error Handling

| Error | SEV | Detection | Recovery |
|-------|-----|-----------|----------|
| Ticket not found | SEV-1 | File access | Abort, report |
| Invalid ticket format | SEV-2 | YAML parse | Skip, report |
| Context indexing failure | SEV-2 | Script exit code | Minimal context fallback |
| Agent selection ambiguous | SEV-3 | Multiple matches | Use priority order |
| Agent timeout | SEV-2 | Timeout exceeded | Retry with `--timeout +60` |
| Agent execution error | SEV-3 | Non-zero exit | Mark blocked, log error |
| Result integration failure | SEV-2 | File write error | Retry, then abort |

---

## 6. Integration with Summon-Agents

### 6.1 call-cli-agents Patterns

| Pattern | When to Use |
|---------|-------------|
| Single Provider | 명확한 전문성 필요 |
| Council of Elders | 교차 검증, 합의 필요 |
| Parallel Specialized | 다중 관점 동시 수집 |

### 6.2 Context Template

```markdown
# Task Context

## Node Structure
{NODE_INDEX.md content}

## Role Evidence
{ROLE_EVIDENCE.md content}

## Ticket
{ticket content}

---

Please complete the action items above.
```

---

## 7. Antigravity Integration

### 7.1 Directory Mapping

| Antigravity | COF Equivalent |
|-------------|----------------|
| `.agent/rules/` | RULE pointer |
| `.agent/workflows/` | WORKFLOW pointer |
| `.agent/skills/` | SKILL pointer |
| `task-manager/tickets/` | Task tickets |

### 7.2 Resilience Pattern

실패 시 example output 패턴을 주입하여 재시도:

```yaml
failure_recovery:
  inject_example: .agent/examples/expected_output.md
  retry_with_pattern: true
  max_retries: 2
```

---

## 8. References

- Parent Skill: `SKILL.md`
- Rule Genome: `../../rules/cof-environment-set.md`
- COF Doctrine: `../../COF_DOCTRINE.md`
- cof-glob-indexing SPEC: `../01.cof-glob-indexing/SPEC.md`
- cof-task-manager-node SPEC: `../02.cof-task-manager-node/SPEC.md`
- call-cli-agents REFERENCE: `../../../03_Manifestation/Summon-Agents/skill/call-cli-agents/REFERENCE.md`
- Skill Normative: `../00.cof-pointerical-tool-creator/references/skill-normative-interpretation.md`
