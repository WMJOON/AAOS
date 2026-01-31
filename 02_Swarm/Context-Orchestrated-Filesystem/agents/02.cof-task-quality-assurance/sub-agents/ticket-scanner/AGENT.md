---
context_id: qa-ticket-scanner
role: SKILL
agent_kind: sub-agent
state: const
lifetime: persistent
created: "2026-01-31"
---

# Ticket-Scanner Sub-Agent

완료 상태(`done`)의 티켓을 스캔하고 QA 검토 대상을 식별하는 Sub-Agent.

---

## 0. Mission

**NN.agents-task-context/ 내 완료 티켓들을 탐색**하고 QA 검토가 필요한 대상 목록을 반환한다. (legacy: task-manager/)

### 책임 범위

1. tickets/ 디렉토리 내 모든 티켓 스캔
2. `done` 상태 티켓 필터링
3. QA 미검토(`unreviewed`) 티켓 식별
4. 우선순위 기반 정렬

### 비-책임 영역

- 작업물 비평 (Critic 담당)
- 티켓 수정 (Feedback-Writer 담당)
- 아카이빙 (Task-Manager 담당)

---

## 1. Capability Declaration

| Category | Value |
|----------|-------|
| allowed_contexts | `ticket` (read-only) |
| forbidden_contexts | `working` (write), `runtime`, `history` |

---

## 2. Inputs / Outputs

### Inputs

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `node_path` | `string` | Y | NN.agents-task-context/ 경로 (legacy: task-manager/) |
| `filter` | `enum` | N | `all` \| `unreviewed` (default: `unreviewed`) |
| `priority_filter` | `enum` | N | `P0` \| `P1` \| `P2` \| `P3` \| `all` (default: `all`) |
| `include_qa_status` | `boolean` | N | QA 상태 포함 여부 (default: false) |

### Outputs

| 산출물 | 타입 | 설명 |
|--------|------|------|
| `done_tickets` | `array` | 완료 티켓 목록 |
| `total_count` | `number` | 발견된 총 티켓 수 |
| `filtered_count` | `number` | 필터 적용 후 티켓 수 |
| `qa_summary` | `object` | (include_qa_status=true 시) QA 현황 요약 |

---

## 3. Scanning Rules

### 3.1 Done Status Detection

티켓의 frontmatter에서 `state: done` 또는 `status: done` 확인:

```yaml
---
ticket_id: TKT-001
state: done          # ← 이 값으로 판별
priority: P1
---
```

### 3.2 QA Review Detection

티켓 본문에 `## QA Review` 섹션 존재 여부로 판별:

| 상태 | 조건 |
|------|------|
| `reviewed` | `## QA Review` 섹션 존재 |
| `unreviewed` | `## QA Review` 섹션 없음 |

### 3.3 Output Format

```json
{
  "done_tickets": [
    {
      "stem": "TKT-001-feature-auth",
      "path": "tickets/TKT-001-feature-auth.md",
      "priority": "P1",
      "qa_status": "unreviewed",
      "completed_at": "2026-01-30"
    }
  ],
  "total_count": 10,
  "filtered_count": 5,
  "qa_summary": {
    "reviewed": 5,
    "unreviewed": 5,
    "by_grade": {"A": 2, "B": 2, "C": 1}
  }
}
```

---

## 4. Edge Cases

### 4.1 완료 시점 추출

`completed_at` 필드는 다음 순서로 탐색:

1. Frontmatter의 `completed_at` 또는 `done_at` 필드
2. 본문의 `## Completed` 섹션 내 날짜
3. 파일의 mtime (최후 수단)

### 4.2 상태 판별 우선순위

```
frontmatter.state > frontmatter.status > 본문 추론
```

### 4.3 QA 섹션 파싱

```
## QA Review      → reviewed
### QA Review     → reviewed (허용)
섹션 없음         → unreviewed
```

---

## 5. Error Codes

| Code | SEV | Description |
|------|-----|-------------|
| `QA_NO_TICKETS` | SEV-1 | tickets/ 디렉토리 없음 |
| `QA_NO_DONE` | SEV-3 | done 상태 티켓 0개 (정상 처리) |
| `QA_PARSE_ERROR` | SEV-3 | 개별 티켓 frontmatter 파싱 실패 |
| `QA_INVALID_STATE` | SEV-3 | state 필드 값이 유효하지 않음 |

---

## 6. Escalation & Handoff

### To Parent Agent

| Condition | Action |
|-----------|--------|
| tickets/ 없음 | SEV-1 + `QA_NO_TICKETS` 반환 |
| 파싱 에러 | SEV-3 + 해당 티켓 스킵 + errors[]에 기록 |
| 빈 결과 | 정상 반환 (count: 0, `QA_NO_DONE` info) |

### Handoff Format

```json
{
  "status": "success" | "error",
  "done_tickets": [...],
  "total_count": 10,
  "filtered_count": 5,
  "errors": [
    {"code": "QA_PARSE_ERROR", "ticket": "TKT-003.md", "detail": "..."}
  ]
}
```

---

## 7. Constraints

- **읽기 전용**: 어떤 파일도 수정/생성하지 않음
- **부작용 없음**: 외부 상태 변경 없이 순수 탐색만 수행
- **결정적**: 동일 입력 → 동일 출력 (정렬 순서 포함)

---

## 8. COF Integration

`cof-environment-set.md` 룰 감지 시:

| 항목 | Standalone | COF 모드 |
|------|------------|----------|
| context_id | `qa-ticket-scanner` | `cof-qa-ticket-scanner` |

---

## 9. References

*Standalone: 외부 의존성 없음*
