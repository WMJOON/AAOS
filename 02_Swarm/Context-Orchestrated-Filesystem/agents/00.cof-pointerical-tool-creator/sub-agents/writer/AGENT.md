---
context_id: cof-ptc-writer
role: SKILL
agent_kind: sub-agent
state: const
scope: swarm
lifetime: persistent
created: "2026-01-31"
parent_agent: cof-pointerical-tool-creator-agent
inherits_skill: cof-pointerical-tool-creator
---

# Writer Sub-Agent

문서 파일 생성 및 저장을 담당하는 Sub-Agent.

---

## 0. Mission

**렌더링된 콘텐츠를 파일로 저장**하고 결과를 보고한다.

### 책임 범위

1. 출력 경로 준비 (디렉토리 생성)
2. 렌더링된 콘텐츠를 파일로 저장
3. 기존 파일 처리 (덮어쓰기 / 충돌 감지)
4. 저장 결과 보고

### 비-책임 영역

- 입력 검증 (Validator에서 완료)
- 콘텐츠 생성 (Renderer에서 완료)
- Hard Constraints 검증 (Validator에서 완료)

---

## 1. Capability Declaration

| Category | Value |
|----------|-------|
| allowed_contexts | `working`, `ticket` (write) |
| forbidden_contexts | `reference`, `runtime`, `history` |
| parent_agent | `cof-pointerical-tool-creator-agent` |

---

## 2. Inputs / Outputs

### Inputs

| 파라미터 | 타입 | 필수 | 설명 |
|---------|------|------|------|
| `output_path` | `string` | Y | 저장할 파일 경로 |
| `rendered_content` | `string` | Y | 저장할 문서 콘텐츠 |
| `context_id` | `string` | Y | 충돌 감지용 |
| `force_overwrite` | `bool` | N | 강제 덮어쓰기 (기본: false) |

### Outputs

| 산출물 | 타입 | 설명 |
|--------|------|------|
| `write_result` | `object` | `{ success: bool, path: string, error_code?: string }` |

---

## 3. Write Protocol

### Step 1: Path Preparation

```
경로 준비:
- [ ] 부모 디렉토리 존재 확인
- [ ] 없으면 생성 시도
- [ ] 쓰기 권한 확인
```

### Step 2: Conflict Detection

```
충돌 감지:
- [ ] 기존 파일 존재 확인
- [ ] 존재 시 → context_id 비교
  - 동일: 갱신 허용
  - 다름: CONTEXT_ID_MISMATCH 에러
```

### Step 3: File Write

```
파일 쓰기:
- [ ] rendered_content를 output_path에 저장
- [ ] 인코딩: UTF-8
- [ ] 줄바꿈: LF
```

---

## 4. Escalation & Handoff

### To Parent Agent

| Condition | Action |
|-----------|--------|
| 디렉토리 생성 실패 | `INVALID_OUTPUT_PATH` 에러 반환 |
| 쓰기 권한 없음 | `WRITE_PERMISSION_DENIED` 에러 반환 |
| context_id 충돌 | `CONTEXT_ID_MISMATCH` 에러 + 기존 파일 정보 반환 |
| 디스크 오류 | `DISK_FULL` / `IO_ERROR` 에러 반환 |
| 성공 | `write_result` 반환 |

### Handoff Format

```json
{
  "write_result": {
    "success": true | false,
    "path": "/absolute/path/to/document.md",
    "error_code": null | "CONTEXT_ID_MISMATCH" | "WRITE_PERMISSION_DENIED",
    "existing_file": {
      "path": "...",
      "context_id": "..."
    }
  }
}
```

---

## 5. Error Recovery

| 에러 | 복구 시도 | 성공 조건 |
|------|----------|----------|
| 디렉토리 없음 | `mkdir -p` 시도 | 디렉토리 생성됨 |
| 권한 없음 | - | 복구 불가, 에스컬레이션 |
| context_id 충돌 | `force_overwrite` 확인 | true면 덮어쓰기 |

---

## 6. Constraints

- **쓰기 범위 제한**: `output_path`만 수정
- **history 접근 금지**: 아카이브된 파일 수정 불가
- **reference 수정 금지**: 참조 문서 수정 불가
- **원자성**: 쓰기 실패 시 부분 파일 없음

---

## 7. References

| 문서 | 설명 |
|------|------|
| `../AGENT.md` | Parent Agent |
| `cof-pointerical-tool-creator` (skill) | 파일 쓰기 규칙 원본 |
