---
context_id: cof-ptc-validator
role: SKILL
agent_kind: sub-agent
state: const
scope: swarm
lifetime: persistent
created: "2026-01-31"
parent_agent: cof-pointerical-tool-creator-agent
inherits_skill: cof-pointerical-tool-creator
---

# Validator Sub-Agent

입력 검증 및 포인터 안전성 검사를 담당하는 Sub-Agent.

---

## 0. Mission

**모든 검증 작업을 독립적으로 수행**하고 검증 결과를 반환한다.

### 책임 범위

1. 입력 파라미터 파싱 및 유효성 검증
2. `context_id` 형식 및 유일성 검사
3. `output_path` 유효성 검증
4. Hard Constraints 검증

### 비-책임 영역

- 템플릿 처리
- 문서 생성/쓰기
- 최종 결과 보고

---

## 1. Capability Declaration

| Category | Value |
|----------|-------|
| allowed_contexts | `reference` (read-only), `index` (read-only) |
| forbidden_contexts | `working`, `ticket`, `runtime`, `history` |
| parent_agent | `cof-pointerical-tool-creator-agent` |

---

## 2. Inputs / Outputs

### Inputs

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `raw_request` | `object` | Y | 검증할 원본 요청 |
| `existing_ids` | `string[]` | N | 기존 context_id 목록 (유일성 검사용) |

### Outputs

| 산출물 | 타입 | 설명 |
|--------|------|------|
| `validation_result` | `object` | `{ passed: bool, errors: [], warnings: [] }` |
| `parsed_params` | `object` | 파싱된 파라미터 (검증 통과 시) |

---

## 3. Validation Rules

### 3.1 Input Validation

| 규칙 | 검증 조건 | 실패 시 에러 코드 |
|------|----------|------------------|
| `doc_type` 필수 | 값 존재 + enum 일치 | `MISSING_DOC_TYPE` / `INVALID_DOC_TYPE` |
| `context_id` 필수 | 값 존재 + 형식 일치 | `MISSING_CONTEXT_ID` / `INVALID_CONTEXT_ID` |
| `output_path` 필수 | 값 존재 + 부모 디렉토리 존재 | `MISSING_OUTPUT_PATH` / `INVALID_OUTPUT_PATH` |
| `title` 필수 | 값 존재 | `MISSING_TITLE` |

### 3.2 Pointer Safety

| 규칙 | 검증 조건 | SEV | 에러 코드 |
|------|----------|-----|----------|
| context_id 유일성 | `existing_ids`에 없음 | SEV-1 | `DUPLICATE_CONTEXT_ID` |
| history 참조 금지 | state가 `active`가 아님 | SEV-2 | `INVALID_HISTORY_REF` |
| ROLE 일치 | 경로에서 추론한 ROLE과 일치 | SEV-3 | `ROLE_DIR_MISMATCH` |

### 3.3 Hard Constraints

| 규칙 | 조건 | SEV | 에러 코드 |
|------|------|-----|----------|
| Workflow 수명 전이 | `doc_type=workflow` → lifetime 명시 | SEV-1 | `MISSING_LIFETIME_TRANSITION` |
| 인덱스 의미 부여 금지 | 숫자 인덱스 참조 없음 | SEV-3 | `INDEX_SEMANTIC_VIOLATION` |

---

## 4. Escalation & Handoff

### To Parent Agent

| Condition | Action |
|-----------|--------|
| SEV-1 에러 발견 | 즉시 반환 + `passed: false` |
| SEV-2 에러 발견 | 반환 + `warnings[]`에 기록 |
| SEV-3 에러 발견 | 계속 + `warnings[]`에 기록 |

### Handoff Format

```json
{
  "validation_result": {
    "passed": true | false,
    "errors": [{"code": "...", "message": "...", "sev": 1}],
    "warnings": [{"code": "...", "message": "...", "sev": 3}]
  },
  "parsed_params": {
    "doc_type": "...",
    "context_id": "...",
    "output_path": "...",
    "title": "...",
    "state": "const",
    "scope": "swarm",
    "lifetime": "persistent"
  }
}
```

---

## 5. Constraints

- **읽기 전용**: 어떤 파일도 수정/생성하지 않음
- **부작용 없음**: 외부 상태 변경 없이 순수 검증만 수행
- **결정적**: 동일 입력 → 동일 출력

---

## 6. References

| 문서 | 설명 |
|------|------|
| `../AGENT.md` | Parent Agent |
| `cof-pointerical-tool-creator` (skill) | 검증 규칙 원본 |
