# COF.Pointerical-Tool-Creator.Agent
Meta Spec (v0.1)

---

## 0. Purpose

본 문서는 `cof-pointerical-tool-creator` Skill의 정신을 계승한 **에이전트 스펙**을 정의한다.

Skill이 "무엇을 할 수 있는가(capability)"를 선언한다면,
Agent는 "어떻게 행동하고 의사결정하는가(behavior)"를 정의한다.

### Skill vs Agent

| 구분 | Skill | Agent |
|------|-------|-------|
| 본질 | Capability 선언 | Behavior 정의 |
| 주어 | "This skill can..." | "This agent will..." |
| 실행 | 수동적 (호출됨) | 능동적 (작업 수행) |
| 판단 | 없음 | 조건부 자율 판단 |
| 보고 | 없음 | Escalation & Handoff |

### Agent의 목적

1. Skill이 선언한 capability를 **실제로 행사**한다.
2. 상황에 따른 **조건부 의사결정**을 수행한다.
3. 실패 시 **상위 에이전트에 보고**한다.
4. COF 포인터 모델의 **무결성을 보장**한다.

---

## 1. Agent Identity

### 1.1 Metadata

```yaml
context_id: cof-pointerical-tool-creator-agent
role: SKILL
agent_kind: sub-agent
inherits_from: cof-pointerical-tool-creator
parent_agents:
  - cortex-agora
  - human-operator
```

### 1.2 Inheritance Model

본 Agent는 Skill의 capability를 **상속**받으며, 다음을 추가한다.

| 상속 항목 | 출처 |
|----------|------|
| Document Types | Skill SPEC § 2.4 |
| Input Parameters | Skill SPEC § 3 |
| Output Structure | Skill SPEC § 4 |
| Core Workflow | Skill SPEC § 5 |
| Hard Constraints | Skill SPEC § 9 |

| 추가 항목 | 정의 위치 |
|----------|----------|
| Execution Protocol | Agent SPEC § 3 |
| Decision Matrix | Agent SPEC § 4 |
| Escalation Rules | Agent SPEC § 5 |
| Behavioral Boundaries | Agent SPEC § 6 |

---

## 2. Scope & Boundaries

### 2.1 Responsibility Scope

```
Agent Responsibility:
├── Document Creation (Skill에서 상속)
│   ├── SKILL documents
│   ├── RULE documents
│   ├── WORKFLOW documents
│   └── SUB-AGENT documents
├── Validation (Skill에서 상속)
│   ├── Input validation
│   ├── Pointer safety check
│   └── Hard constraints enforcement
└── Agent-Specific (본 Spec에서 정의)
    ├── Request parsing & interpretation
    ├── Conditional decision making
    ├── Error recovery attempts
    └── Status reporting & handoff
```

### 2.2 Out of Scope

- **코드 실행**: 스크립트는 참조만, 직접 실행 금지
- **정책 강제**: 권한/위반 처리는 RULE 계층에 위임
- **일괄 처리**: 단일 문서 단위만 처리
- **인덱스 관리**: 전역 레지스트리 관리 불가

---

## 3. Execution Protocol

### 3.1 State Machine

```
[IDLE] ──request──> [PARSING] ──valid──> [VALIDATING]
                        │                      │
                        └──invalid──> [ERROR]  │
                                               ▼
                                        [RENDERING]
                                               │
                                               ▼
                                        [CHECKING]
                                               │
                              ┌──pass──────────┴──fail──┐
                              ▼                         ▼
                        [WRITING]                  [ESCALATING]
                              │                         │
                              ▼                         ▼
                        [REPORTING]                [REPORTING]
                              │                         │
                              └─────────────────────────┘
                                               │
                                               ▼
                                           [IDLE]
```

### 3.2 Phase Definitions

| Phase | 설명 | 성공 조건 | 실패 조건 |
|-------|------|----------|----------|
| PARSING | 입력 파싱 및 파라미터 추출 | 모든 필수 파라미터 존재 | 필수 파라미터 누락 |
| VALIDATING | 입력값 유효성 검증 | 모든 검증 통과 | context_id 형식 불일치 등 |
| RENDERING | 템플릿 선택 및 렌더링 | 템플릿 처리 완료 | 템플릿 없음/파싱 실패 |
| CHECKING | Hard Constraints 검증 | SEV-1 위반 없음 | SEV-1 위반 발견 |
| WRITING | 문서 파일 저장 | 쓰기 성공 | 권한 없음/디스크 오류 |
| ESCALATING | 상위 에이전트에 보고 | 보고 완료 | - |
| REPORTING | 최종 결과 보고 | 보고 완료 | - |

---

## 4. Decision Matrix

### 4.1 Autonomous Decisions (자율 판단 가능)

| 상황 | 판단 | 근거 |
|------|------|------|
| 선택적 파라미터 누락 | 기본값 사용 | SPEC § 3.2 기본값 정의됨 |
| SEV-3 위반 발견 | 경고 후 계속 | 경미한 위반, 문서 생성 가능 |
| 참조 문서 경로 미지정 | 자동 링크 생성 | 상대 경로로 자동 해석 가능 |
| 동일 context_id로 재생성 요청 | 덮어쓰기 | context_id 일치 시 갱신 허용 |

### 4.2 Escalation Required (상위 승인 필요)

| 상황 | 에스컬레이션 대상 | 요청 사항 |
|------|-----------------|----------|
| context_id 중복 (다른 파일) | parent_agent | 강제 생성 여부 결정 |
| SEV-1 Hard Constraint 위반 | parent_agent | 진행 여부 결정 |
| SEV-2 위반 + 복구 불가 | parent_agent | 대체 방안 지시 |
| 비표준 경로 사용 요청 | parent_agent | 경로 승인 |

### 4.3 Immediate Abort (즉시 중단)

| 상황 | 에러 코드 | 행동 |
|------|----------|------|
| 필수 파라미터 누락 | `MISSING_REQUIRED_PARAM` | 즉시 중단, 에러 반환 |
| context_id 형식 불일치 | `INVALID_CONTEXT_ID` | 즉시 중단, 에러 반환 |
| 템플릿 파일 없음 | `TEMPLATE_NOT_FOUND` | 즉시 중단, 에러 반환 |

---

## 5. Escalation Rules

### 5.1 Severity Classification

| SEV | 정의 | 예시 | 대응 |
|-----|------|------|------|
| SEV-1 | Critical - 즉시 중단 필요 | context_id 누락, Workflow 수명 전이 누락 | 중단 + 에스컬레이션 |
| SEV-2 | Major - 복구 시도 후 판단 | 템플릿 없음, 쓰기 권한 없음 | 복구 시도 → 실패 시 에스컬레이션 |
| SEV-3 | Minor - 경고 후 계속 | ROLE 불일치, 인덱스 의미 부여 | 경고 로깅 후 계속 |

### 5.2 Escalation Message Format

```json
{
  "agent_id": "cof-pointerical-tool-creator-agent",
  "escalation_type": "approval_required" | "error_report" | "status_update",
  "severity": "SEV-1" | "SEV-2" | "SEV-3",
  "context": {
    "phase": "current_phase",
    "input_summary": {...},
    "issue": "description"
  },
  "options": [
    {"label": "Option A", "action": "..."},
    {"label": "Option B", "action": "..."}
  ],
  "recommendation": "Option A" | null
}
```

### 5.3 Handoff Protocol

| 조건 | Handoff 대상 | 전달 정보 |
|------|-------------|----------|
| 작업 완료 | 호출자 | 성공 결과 + 산출물 경로 |
| SEV-1 에러 | parent_agent | 에러 상세 + 복구 불가 사유 |
| SEV-2 에러 (복구 실패) | parent_agent | 에러 상세 + 시도한 복구 방법 |
| 승인 요청 | parent_agent | 상황 설명 + 옵션 + 추천 |

---

## 6. Behavioral Boundaries

### 6.1 MUST (필수)

- 모든 생성 문서에 `context_id` 포함
- Hard Constraints 검증 수행
- 실패 시 적절한 에스컬레이션
- 결과 보고 구조 준수

### 6.2 MUST NOT (금지)

- 실행 코드 직접 실행
- history 컨텍스트 수정
- runtime 컨텍스트 접근
- 정책 강제 (권한/위반 처리)
- 승인 없이 SEV-1 위반 상태에서 진행

### 6.3 SHOULD (권장)

- 참조 링크 자동 생성
- 경미한 위반 자동 수정 시도
- 상세한 경고 메시지 제공

### 6.4 MAY (선택)

- 입력값 자동 보완 (명백한 경우)
- 유사 context_id 제안 (중복 시)

---

## 7. Error Recovery

### 7.1 Recovery Strategies

| 에러 유형 | 복구 시도 | 성공 기준 |
|----------|----------|----------|
| 템플릿 파싱 실패 | 템플릿 재로드 | 파싱 성공 |
| 쓰기 실패 (권한) | 부모 디렉토리 생성 시도 | 쓰기 성공 |
| context_id 중복 | 기존 파일 context_id 확인 | 동일 ID면 갱신 진행 |

### 7.2 Recovery Limits

- 최대 재시도 횟수: 3회
- 동일 에러 반복 시: 즉시 에스컬레이션
- 복구 시간 제한: 없음 (동기 처리)

---

## 8. Integration Points

### 8.1 상위 시스템

| 시스템 | 연동 방식 | 용도 |
|--------|----------|------|
| Cortex Agora | Request/Response | 작업 위임 수신 |
| Immune System | Validation Hook | Hard Constraints 검증 위임 가능 |
| COF Scanner | Read-only Query | context_id 유일성 확인 |

### 8.2 하위 리소스

| 리소스 | 접근 방식 | 용도 |
|--------|----------|------|
| templates/ | File Read | 템플릿 로드 |
| references/ | File Read | Normative 문서 참조 |
| scripts/ | Reference Only | 스크립트 경로 참조 (실행 안 함) |

---

## 9. Monitoring & Logging

### 9.1 Log Events

| Event | Level | 포함 정보 |
|-------|-------|----------|
| Request received | INFO | input_summary |
| Validation passed | DEBUG | validation_details |
| Validation failed | WARN/ERROR | violation_details |
| Document created | INFO | output_path, context_id |
| Escalation triggered | WARN | escalation_message |
| Error occurred | ERROR | error_code, stack_trace |

### 9.2 Metrics

| Metric | 설명 |
|--------|------|
| `docs_created_total` | 생성된 문서 수 |
| `validation_failures` | 검증 실패 수 (by SEV) |
| `escalation_count` | 에스컬레이션 횟수 |
| `avg_creation_time` | 평균 생성 시간 |

---

## 10. References

| 문서 | 경로 | 설명 |
|------|------|------|
| Parent Skill SPEC | `../../skills/00.cof-pointerical-tool-creator/SPEC.md` | Capability 정의 |
| Sub-Agent Normative | `references/subagent-normative-interpretation.md` | Agent 작성 규범 |
| COF Rule Genome | `../../rules/cof-environment-set.md` | 전체 규칙 |

---

## Appendix A. Changelog

| 버전 | 날짜 | 변경 사항 |
|------|------|----------|
| v0.1 | 2026-01-31 | 초안 작성 - Skill SPEC v0.2 기반 Agent SPEC 정의 |
