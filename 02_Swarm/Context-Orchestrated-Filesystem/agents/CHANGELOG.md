# COF Agents Changelog

모든 에이전트의 주요 변경 사항을 기록합니다.

---

## [2026-01-31] 병렬 처리 및 환경 감지 패턴 적용

### 변경 개요

모든 Orchestrator와 Sub-Agent에 **병렬 처리(Parallel Execution)**와 **COF 환경 감지(Environment Detection)** 패턴을 적용했습니다.

### 변경된 에이전트

#### 00.cof-pointerical-tool-creator

| 파일 | 변경 사항 |
|------|----------|
| `AGENT.md` | Phase -1 환경 감지, Batch Mode 병렬 처리, `force_mode` 파라미터 추가 |
| `SPEC.md` | Batch Mode State Machine 추가 |
| `sub-agents/validator/AGENT.md` | 내부 병렬 검증, 모드별 조건부 규칙 적용 |
| `sub-agents/renderer/AGENT.md` | `execution_mode` 입력, 모드별 템플릿/Frontmatter |
| `sub-agents/writer/AGENT.md` | (기존 유지) |

#### 01.cof-task-manager (`.claude/agents/`)

| 파일 | 변경 사항 |
|------|----------|
| `AGENT.md` | (기존) Section 0 Environment Detection 있음 |
| `sub-agents/node-creator/AGENT.md` | COF Integration 섹션 추가 |
| `sub-agents/ticket-manager/AGENT.md` | COF Integration 섹션 추가 |
| `sub-agents/validator/AGENT.md` | COF Integration 섹션 추가 |
| `sub-agents/archiver/AGENT.md` | COF Integration 섹션 추가 |

#### 02.cof-task-quality-assurance (`.claude/agents/`)

| 파일 | 변경 사항 |
|------|----------|
| `AGENT.md` | (기존) COF Integration 섹션 있음 |
| `sub-agents/critic/AGENT.md` | (기존) Section 5 COF Integration 있음 |
| `sub-agents/ticket-scanner/AGENT.md` | (기존) Section 5 COF Integration 있음 |
| `sub-agents/feedback-writer/AGENT.md` | (기존) Section 6 COF Integration 있음 |

---

### 새로운 패턴

#### 1. 환경 감지 (Environment Detection)

```
cof-environment-set.md 존재?
├─ Yes → COF Mode (전체 규칙 적용)
└─ No  → Standalone Mode (최소 규칙)
```

#### 2. 모드별 동작 차이

| 항목 | COF Mode | Standalone Mode |
|------|----------|-----------------|
| `context_id` | 필수 (SEV-1) | 권장 (SEV-3) |
| `context_id` 형식 | `cof-[a-z0-9-]+` | 자유 형식 |
| Pointer Safety | 적용 | 생략 |
| Hard Constraints | 적용 | 생략 |
| Frontmatter | 전체 필드 | 최소 필드 |
| 스킬 호출 | `@skill()` 위임 | 직접 실행 |

#### 3. 병렬 처리 (Parallel Execution)

**Batch Mode (다중 요청)**
```
Pipeline[0]: [V] → [R] → [W] ──┐
Pipeline[1]: [V] → [R] → [W] ──┼── 동시 실행 (parallel_limit)
Pipeline[2]: [V] → [R] → [W] ──┘
```

**Validator 내부 병렬화**
```
┌─────────────┬─────────────┬───────────┐
│ Input Check │ Pointer Safe│ Hard Const│  ← 3개 검증 동시 실행
└─────────────┴─────────────┴───────────┘
```

---

### 새로운 Input 파라미터

| 파라미터 | 적용 대상 | 설명 |
|---------|----------|------|
| `force_mode` | Orchestrator | `cof` \| `standalone` (환경 감지 무시) |
| `batch_requests` | pointerical-tool-creator | 다중 문서 요청 배열 |
| `parallel_limit` | Orchestrator | 동시 처리 상한 (기본: 3) |
| `fail_strategy` | Orchestrator | `fail_fast` \| `continue` |
| `execution_mode` | Sub-Agents | Orchestrator에서 전달받은 모드 |

---

## [2026-01-31] 초기 버전

### 생성된 에이전트

- `00.cof-pointerical-tool-creator` - Skill/Rule/Workflow/Sub-Agent 문서 생성
- `01.cof-task-manager` - NN.agents-task-context/ 노드 관리
- `02.cof-task-quality-assurance` - 완료 티켓 품질 비평 및 피드백
