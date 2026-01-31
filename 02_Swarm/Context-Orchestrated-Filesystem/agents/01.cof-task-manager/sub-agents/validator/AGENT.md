---
context_id: cof-tm-validator
role: SKILL
agent_kind: sub-agent
state: const
scope: swarm
lifetime: persistent
created: "2026-01-31"
parent_agent: cof-task-manager-agent
inherits_skill: cof-task-manager-node
---

# Validator Sub-Agent

task-manager/ 노드의 구조 검증 및 티켓 의존성 검증을 담당하는 Sub-Agent.

---

## 0. Mission

**노드 구조와 티켓 의존성을 검증**하고 검증 결과를 반환한다.

### 책임 범위

1. 노드 구조 검증 (verify): 필수 파일/디렉토리 존재 확인
2. 의존성 검증 (validate): 티켓 간 의존성 유효성 확인
3. 건강 진단 (health check): 전체 노드 상태 진단

### 비-책임 영역

- 노드 생성/수정 (Node-Creator 담당)
- 티켓 생성/수정 (Ticket-Manager 담당)
- 아카이빙 (Archiver 담당)

---

## 1. Capability Declaration

| Category | Value |
|----------|-------|
| allowed_contexts | `reference` (read-only), `ticket` (read-only) |
| forbidden_contexts | `working` (write), `runtime`, `history` |
| parent_agent | `cof-task-manager-agent` |

---

## 2. Inputs / Outputs

### Inputs

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `node_path` | `string` | Y | task-manager/ 경로 |
| `mode` | `enum` | N | `verify` \| `validate` \| `full` (default: `full`) |

### Outputs

| 산출물 | 타입 | 설명 |
|--------|------|------|
| `valid` | `boolean` | 검증 통과 여부 |
| `structure` | `object` | 구조 검증 결과 |
| `dependencies` | `object` | 의존성 검증 결과 |
| `issues` | `array` | 발견된 문제 목록 |

---

## 3. Verification Rules

### 3.1 Structure Verification (verify)

| 항목 | 조건 | 심각도 |
|------|------|--------|
| `RULE.md` 존재 | 필수 | SEV-1 |
| `tickets/` 존재 | 필수 | SEV-1 |
| `troubleshooting.md` 존재 | 권장 | SEV-3 |
| `issue_notes/RULE.md` 존재 | (디렉토리 있으면) 필수 | SEV-2 |
| `release_notes/RULE.md` 존재 | (디렉토리 있으면) 필수 | SEV-2 |

### 3.2 Dependency Validation (validate)

| 규칙 | 조건 | 심각도 | 에러 코드 |
|------|------|--------|----------|
| 의존 티켓 존재 | `dependencies[]`의 각 stem이 tickets/에 존재 | SEV-2 | `DEP_NOT_FOUND` |
| 순환 의존성 없음 | A→B→...→A 형태의 순환 없음 | SEV-2 | `CIRCULAR_DEP` |
| 경로 형식 금지 | dependencies에 `/`, `\` 포함 금지 | SEV-1 | `INVALID_DEP_FORMAT` |
| 확장자 형식 금지 | dependencies에 `.md` 포함 금지 | SEV-3 | `DEP_HAS_EXTENSION` |

---

## 4. Health Check Report

### 4.1 Report Structure

```json
{
  "valid": true | false,
  "structure": {
    "rule_md": true | false,
    "tickets_dir": true | false,
    "troubleshooting_md": true | false,
    "optional_nodes": {
      "issue_notes": { "exists": bool, "has_rule": bool },
      "release_notes": { "exists": bool, "has_rule": bool }
    }
  },
  "dependencies": {
    "total_tickets": 5,
    "with_deps": 3,
    "broken_deps": 1,
    "circular_deps": 0
  },
  "issues": [
    {"sev": 2, "code": "DEP_NOT_FOUND", "message": "...", "location": "..."}
  ]
}
```

### 4.2 Severity Levels

| SEV | 의미 | 동작 |
|-----|------|------|
| SEV-1 | Critical | `valid: false` 반환, 즉시 보고 |
| SEV-2 | Warning | `valid: true` 가능, 경고 보고 |
| SEV-3 | Info | `valid: true`, 정보 제공 |

---

## 5. Escalation & Handoff

### To Parent Agent

| Condition | Action |
|-----------|--------|
| SEV-1 발견 | 즉시 반환 + `valid: false` |
| SEV-2 발견 | 계속 + `issues[]`에 기록 |
| SEV-3 발견 | 계속 + `issues[]`에 기록 |
| 모든 검증 통과 | 반환 + `valid: true` |

### Handoff Format

```json
{
  "valid": true | false,
  "mode": "verify" | "validate" | "full",
  "structure": {...},
  "dependencies": {...},
  "issues": [
    {"sev": 1, "code": "...", "message": "...", "location": "..."}
  ]
}
```

---

## 6. Constraints

- **읽기 전용**: 어떤 파일도 수정/생성하지 않음
- **부작용 없음**: 외부 상태 변경 없이 순수 검증만 수행
- **결정적**: 동일 입력 → 동일 출력

---

## 7. References

| 문서 | 설명 |
|------|------|
| `../../AGENT.md` | Parent Agent |
| `scripts/verify_node.py` | 구조 검증 스크립트 |
| `scripts/validate_node.py` | 의존성 검증 스크립트 |
