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
| `execution_mode` | `enum` | Y | `cof` \| `standalone` (Orchestrator에서 전달) |

### Outputs

| 산출물 | 타입 | 설명 |
|--------|------|------|
| `validation_result` | `object` | `{ passed: bool, errors: [], warnings: [], mode: "cof"\|"standalone" }` |
| `parsed_params` | `object` | 파싱된 파라미터 (검증 통과 시) |

---

## 3. Validation Rules

### 3.0 Internal Parallel Execution

Validator 내부에서 3개의 검증 작업을 **병렬로 실행**합니다.

```
[raw_request + execution_mode]
      │
      ▼
┌─────────────────────────────────────────────┐
│           Validator (Parallel)              │
│  ┌─────────────┬─────────────┬───────────┐  │
│  │ Input Check │ Pointer Safe│ Hard Const│  │  ← 병렬 실행
│  │  (3.1)      │   (3.2)*    │   (3.3)*  │  │    * COF Mode Only
│  └──────┬──────┴──────┬──────┴─────┬─────┘  │
│         └─────────────┴────────────┘        │
│                       │                      │
│                 Merge Results                │
│                       │                      │
└───────────────────────┼──────────────────────┘
                        ▼
              [validation_result]
```

**병렬화 이점:**
- 각 검증이 독립적이므로 동시 실행 가능
- 전체 검증 시간 단축
- 모든 에러를 한 번에 수집 (fail-fast 아님)

---

### 3.1 Input Validation (공통)

**모든 모드에서 적용**되는 기본 검증입니다.

| 규칙 | COF Mode | Standalone Mode | 에러 코드 |
|------|----------|-----------------|----------|
| `doc_type` 필수 | SEV-1 | SEV-1 | `MISSING_DOC_TYPE` |
| `output_path` 필수 | SEV-1 | SEV-1 | `MISSING_OUTPUT_PATH` |
| `title` 필수 | SEV-1 | SEV-1 | `MISSING_TITLE` |
| `context_id` 필수 | SEV-1 | **SEV-3 (권장)** | `MISSING_CONTEXT_ID` |
| `context_id` 형식 | `cof-[a-z0-9-]+` 강제 | **자유 형식** | `INVALID_CONTEXT_ID` |

#### Standalone Mode 특수 처리

```
context_id 처리:
- 값 없음 → 자동 생성 (doc_type-{timestamp})
- 값 있음 → 형식 검증 생략
- 경고 추가: "context_id 권장됨"
```

---

### 3.2 Pointer Safety (COF Mode Only)

**COF Mode에서만 적용**됩니다. Standalone Mode에서는 **전체 생략**.

| 규칙 | 검증 조건 | SEV | 에러 코드 |
|------|----------|-----|----------|
| context_id 유일성 | `existing_ids`에 없음 | SEV-1 | `DUPLICATE_CONTEXT_ID` |
| history 참조 금지 | state가 `active`가 아님 | SEV-2 | `INVALID_HISTORY_REF` |
| ROLE 일치 | 경로에서 추론한 ROLE과 일치 | SEV-3 | `ROLE_DIR_MISMATCH` |

```
Standalone Mode:
- Pointer Safety 전체 생략
- 경고 없이 통과
```

---

### 3.3 Hard Constraints (COF Mode Only)

**COF Mode에서만 적용**됩니다. Standalone Mode에서는 **전체 생략**.

| 규칙 | 조건 | SEV | 에러 코드 |
|------|------|-----|----------|
| Workflow 수명 전이 | `doc_type=workflow` → lifetime 명시 | SEV-1 | `MISSING_LIFETIME_TRANSITION` |
| 인덱스 의미 부여 금지 | 숫자 인덱스 참조 없음 | SEV-3 | `INDEX_SEMANTIC_VIOLATION` |

```
Standalone Mode:
- Hard Constraints 전체 생략
- 경고 없이 통과
```

---

### 3.4 Mode-Based Validation Summary

| 검증 카테고리 | COF Mode | Standalone Mode |
|--------------|----------|-----------------|
| Input Validation (3.1) | 전체 적용 | 완화 적용 |
| Pointer Safety (3.2) | 전체 적용 | **생략** |
| Hard Constraints (3.3) | 전체 적용 | **생략** |

---

### 3.5 Result Merge Strategy

```
병렬 결과 병합:
1. 모든 검증 완료 대기
2. errors[] 배열 통합 (SEV 순 정렬)
3. warnings[] 배열 통합
4. passed = (SEV-1 에러 없음)
```

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
