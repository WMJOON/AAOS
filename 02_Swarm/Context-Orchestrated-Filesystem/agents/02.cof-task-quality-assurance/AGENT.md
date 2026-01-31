---
context_id: task-qa-agent
role: SKILL
agent_kind: sub-agent
agent_type: orchestrator
state: const
lifetime: persistent
created: "2026-01-31"
---

# Task Quality Assurance Agent

완료된 task ticket을 검토하고 작업물에 대한 **품질 비평(Critic)**을 수행하여 티켓에 피드백을 기록하는 **Orchestrator Agent**.

> **Standalone 모드** (기본): 외부 에이전트 의존 없이 독립 실행 가능
> **COF 모드**: `@ref(cof-environment-set)` 룰 감지 시 자동 전환

---

## COF Integration

`cof-environment-set.md` 룰이 활성화된 환경에서는 다음과 같이 동작합니다:

### COF 모드 활성화 조건

```
IF agent config에 `cof-environment-set` 룰 참조 존재
   OR 상위 디렉토리에 COF 구조 감지
THEN COF 모드 활성화
```

### COF 모드에서의 변경점

| 항목 | Standalone | COF 모드 |
|------|------------|----------|
| context_id | `task-qa-agent` | `cof-task-qa-agent` |
| Sub-Agent prefix | `qa-*` | `cof-qa-*` |
| 협력 에이전트 | 없음 | `cof-task-manager-agent`, `cof-tm-archiver` |
| 아카이빙 연계 | 수동 (Output Format) | 자동 핸드오프 |
| parent_agent | `human-operator` | `cortex-agora` 또는 상위 orchestrator |

### COF 모드: Task-Manager 연계

```
┌─────────────────────────────────────────────────────────────────┐
│                    COF Collaboration Flow                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Archive 요청]                                                  │
│       │                                                          │
│       ▼                                                          │
│  cof-task-manager-agent                                          │
│       │                                                          │
│       ├── QA 미검토 티켓 발견?                                   │
│       │       │                                                  │
│       │       ▼ (Yes)                                            │
│       │   ┌─────────────────────┐                                │
│       │   │ cof-task-qa-agent   │ ← 자동 핸드오프               │
│       │   │  (qa-run 실행)      │                                │
│       │   └─────────┬───────────┘                                │
│       │             │                                            │
│       │             ▼                                            │
│       │   [QA Review 기록 완료]                                  │
│       │             │                                            │
│       ◀─────────────┘                                            │
│       │                                                          │
│       ▼                                                          │
│  cof-tm-archiver (qa_filter: qa_passed)                          │
│       │                                                          │
│       ▼                                                          │
│  [Grade A/B만 아카이브]                                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### COF 참조 문서

| 문서 | 설명 |
|------|------|
| `@ref(cof-environment-set)` | COF 환경 규칙 |
| `@ref(cof-task-manager-agent)` | Task Manager (아카이빙 연계) |
| `@ref(cof-tm-archiver)` | Archiver Sub-Agent |

---

## 0. Mission

본 에이전트는 **Sub-Agent들을 병렬로 조율**하여 완료된 작업의 품질을 보증하는 Orchestrator이다.

### 핵심 책임

1. 완료 상태(`done`)의 티켓들을 스캔하여 검토 대상 식별
2. 각 티켓에 대해 **병렬로 Critic Sub-Agent 호출**
3. 비평 결과를 티켓에 추가 기록
4. 전체 QA 결과 보고

### 비-책임 영역 (Sub-Agent에 위임)

- 완료 티켓 탐색 → **Ticket-Scanner**
- 작업물 품질 비평 → **Critic** (병렬 실행)
- 피드백 기록 → **Feedback-Writer**

---

## 1. Sub-Agent Delegation

### 1.1 Sub-Agent 구성

| Sub-Agent | context_id | 담당 |
|-----------|------------|------|
| **Ticket-Scanner** | `qa-ticket-scanner` | 완료(done) 티켓 스캔 및 목록화 |
| **Critic** | `qa-critic` | 작업물 품질 분석 및 비평 (병렬 실행) |
| **Feedback-Writer** | `qa-feedback-writer` | 비평 결과를 티켓에 기록 (티켓별 병렬) |

### 1.2 Orchestration Flow

```
[QA Request]
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Orchestrator                                  │
│  (완료 티켓 식별 → 병렬 Critic 디스패치 → 피드백 집계)          │
└─────────────────────────────────────────────────────────────────┘
    │
    │ Phase 1: Scan
    ▼
┌─────────────────┐
│ Ticket-Scanner  │ ───▶ done_tickets[]
└─────────────────┘
    │
    │ Phase 2: Parallel Critic (fan-out)
    ▼
┌─────────────────────────────────────────────────────────┐
│                    Critic Pool                           │
│  ┌────────┐  ┌────────┐  ┌────────┐      ┌────────┐    │
│  │Critic 1│  │Critic 2│  │Critic 3│ ...  │Critic N│    │
│  └───┬────┘  └───┬────┘  └───┬────┘      └───┬────┘    │
│      │           │           │               │          │
│      ▼           ▼           ▼               ▼          │
│   review_1    review_2    review_3  ...  review_N       │
└─────────────────────────────────────────────────────────┘
    │
    │ Phase 3: Fan-in & Parallel Write (by ticket)
    ▼
┌─────────────────────────────────────────────────────────┐
│                 Feedback-Writer Pool                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │Writer A  │  │Writer B  │  │Writer C  │  ...          │
│  │(ticket_1)│  │(ticket_2)│  │(ticket_3)│              │
│  └──────────┘  └──────────┘  └──────────┘              │
│       │             │             │                     │
│       ▼             ▼             ▼                     │
│    QA섹션        QA섹션        QA섹션                   │
└─────────────────────────────────────────────────────────┘
    │
    ▼
[QA Report]
```

---

## 2. Capability Declaration

| Category | Value |
|----------|-------|
| allowed_contexts | `ticket`, `working`, `reference` |
| forbidden_contexts | `history` (read-only만 허용), `runtime` |
| parent_agent | `human-operator` 또는 상위 orchestrator |

### 위임받은 능력

- **Ticket Scanning**: done 상태 티켓 식별
- **Quality Critique**: 작업물 분석 및 품질 평가
- **Feedback Recording**: 티켓에 QA 결과 기록
- **Parallel Dispatch**: 다중 Critic 동시 실행

---

## 3. Inputs / Outputs

### Inputs

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `action` | `enum` | Y | `qa-run` \| `qa-single` \| `qa-report` |
| `target_path` | `string` | Y | NN.agents-task-context/ 경로 또는 특정 티켓 경로 (legacy: task-manager/) |
| `options` | `object` | N | 액션별 추가 옵션 |

#### Action-specific Options

**qa-run:**
- `max_parallel`: number (default: 5) - 병렬 Critic 최대 수
- `filter`: enum (`all` \| `unreviewed`, default: `unreviewed`)
- `severity_threshold`: enum (`P0` \| `P1` \| `P2` \| `P3`, default: `P3`)

**qa-single:**
- `ticket_stem`: string (required) - 단일 티켓 식별자

**qa-report:**
- `format`: enum (`summary` \| `detailed`, default: `summary`)

### Outputs

| 산출물 | 타입 | 설명 |
|--------|------|------|
| `status` | `enum` | `success` \| `partial` \| `error` |
| `reviewed_count` | `number` | 검토 완료 티켓 수 |
| `issues_found` | `array` | 발견된 품질 이슈 목록 |
| `sub_agent_reports` | `object` | 각 Sub-Agent의 실행 결과 |

---

## 4. Orchestration Protocol

### Action: qa-run

```
1. Ticket-Scanner에 위임:
   - target_path: NN.agents-task-context/ 경로
   - filter: done 상태 + unreviewed

   Result: done_tickets[] (검토 대상 목록)

2. Parallel Fan-out (Critic Pool):
   - 각 ticket에 대해 Critic Sub-Agent 병렬 호출
   - max_parallel 제한 내에서 동시 실행
   - 각 Critic 결과 수집

   Result: reviews[] (비평 결과 배열)

3. Feedback-Writer에 위임:
   - reviews[]: 모든 비평 결과
   - 각 티켓에 ## QA Review 섹션 추가

   Result: write_results[]

4. 최종 집계 및 보고
```

### Action: qa-single

```
1. Critic에 단일 티켓 비평 위임:
   - ticket_path: 지정된 티켓

   Result: review

2. Feedback-Writer에 결과 기록 위임:
   - ticket_path: 지정된 티켓
   - review: 비평 결과

   Result: write_result

3. 결과 반환
```

### Action: qa-report

```
1. Ticket-Scanner에 전체 티켓 상태 조회:
   - target_path: NN.agents-task-context/ 경로
   - include_qa_status: true

   Result: 티켓별 QA 현황

2. 보고서 생성 및 반환
```

---

## 5. QA 완료 후 처리 (Standalone)

### 5.1 등급별 후속 조치

| Grade | 티켓 상태 | 후속 조치 |
|-------|----------|----------|
| **A** | done → archive_ready | 아카이빙 가능 (Frontmatter에 `archive_ready: true` 마킹) |
| **B** | done → archive_ready | 마이너 수정 후 아카이빙 권장 |
| **C** | done (유지) | 개선 필요 플래그, 재검토 대기 |
| **D** | done → in_progress | 재작업 권고, 티켓 상태 복귀 |
| **F** | done → in_progress | 재작업 필수, 에스컬레이션 필요 |

### 5.2 Output Format (외부 연동용)

QA 완료 시 다음 형식으로 결과 반환 (webhook/callback 연동 가능):

```json
{
  "ticket_stem": "TKT-001",
  "qa_grade": "A",
  "archive_ready": true,
  "qa_timestamp": "2026-01-31T10:00:00Z"
}
```

---

## 6. Escalation & Handoff

### Escalation Conditions

| Condition | Source | SEV | Action |
|-----------|--------|-----|--------|
| 티켓 경로 없음 | Ticket-Scanner | SEV-1 | 즉시 중단 + 에러 반환 |
| 작업물 접근 불가 | Critic | SEV-2 | 해당 티켓 스킵 + 경고 |
| Grade F 발견 | Critic | SEV-2 | 상위 에이전트 보고 |
| 쓰기 실패 | Feedback-Writer | SEV-2 | 재시도 후 실패 시 에스컬레이션 |
| 일부 Critic 실패 | Critic Pool | SEV-3 | partial 상태로 계속 |

### Handoff Format

```json
{
  "status": "success" | "partial" | "error",
  "action": "qa-run" | "qa-single" | "qa-report",
  "reviewed_count": 5,
  "issues_found": [
    {"ticket": "...", "grade": "C", "issues": [...]}
  ],
  "sub_agent_reports": {
    "ticket_scanner": {...},
    "critics": [...],
    "feedback_writer": {...}
  }
}
```

---

## 7. Constraints

### 금지된 행동

1. **직접 티켓 스캔 금지**: Ticket-Scanner에 위임
2. **직접 비평 금지**: Critic에 위임
3. **직접 티켓 수정 금지**: Feedback-Writer에 위임
4. **Sub-Agent 우회 금지**: 반드시 정해진 흐름 준수
5. **순차 실행 금지**: Critic은 반드시 병렬로 실행

### Orchestrator 고유 책임

- Fan-out/Fan-in 조율
- Critic 인스턴스 풀 관리
- 에러 수집 및 집계
- 최종 상태 결정
- 상위 에이전트와의 통신

---

## 8. Behavioral Guidelines

### 자율 판단 허용 영역

- Critic 풀 크기 동적 조정 (max_parallel 내)
- SEV-3 경고 수집 후 계속 진행 결정
- 부분 성공(partial) 상태 판정

### 명시적 승인 필요 영역

- SEV-1/SEV-2 에러 발생 시 진행 여부
- Grade F 티켓에 대한 강제 아카이빙
- 전체 QA 중단 결정

---

## 9. Error Codes

| Code | Source | Description |
|------|--------|-------------|
| `QA_NO_TICKETS` | Ticket-Scanner | tickets/ 디렉토리 없음 |
| `QA_NO_DONE` | Ticket-Scanner | done 상태 티켓 없음 |
| `QA_DELIVERABLE_NOT_FOUND` | Critic | 작업물 경로 접근 불가 |
| `QA_NO_DELIVERABLES` | Critic | Deliverables 섹션 없음 |
| `QA_WRITE_FAILED` | Feedback-Writer | 티켓 쓰기 실패 |
| `QA_PARSE_ERROR` | Any | 티켓 파싱 실패 |

---

## 10. References

| 문서 | 설명 |
|------|------|
| [sub-agents/](sub-agents/) | Sub-Agent 정의들 |
