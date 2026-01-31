# Skill Reference

본 에이전트 그룹은 `cof-task-manager-node` 스킬에서 위임받은 능력을 기반으로 동작한다.

---

## 상위 Skill 위치

```
../../skills/02.cof-task-manager-node/
├── SKILL.md        # 스킬 정의
├── SPEC.md         # 상세 스펙
└── templates/      # 문서 템플릿
    ├── NODE_RULE.md
    ├── TICKET-TEMPLATE.md
    ├── ISSUE_NOTE_RULE.md
    ├── RELEASE_NOTE_RULE.md
    └── TROUBLESHOOTING-TEMPLATE.md
```

---

## Sub-Agent ↔ Tool 매핑

본 에이전트 그룹은 **외부 스크립트 없이** 다음 도구만으로 동작한다.

| Sub-Agent | Primary Tools | 용도 |
|-----------|---------------|------|
| **Node-Creator** | `Glob`, `Bash(mkdir)`, `Read`, `Write` | 디렉토리 구조 생성, 템플릿 복사 |
| **Ticket-Manager** | `Glob`, `Read`, `Write` | 티켓 파일 생성, 중복/의존성 확인 |
| **Validator** | `Glob`, `Read` | 구조 검증, YAML 파싱, 의존성 그래프 분석 |
| **Archiver** | `Glob`, `Read`, `Write`, `Edit`, `Bash(rm)`, `Task` | 티켓 이동, 로그 기록, 병렬 처리 |

---

## 병렬화 지원

| Action | 병렬화 | 설명 |
|--------|:------:|------|
| `create-tickets` | ✅ | 여러 Ticket-Manager 병렬 호출 |
| `validate` (full) | ✅ | verify + dependency 검증 병렬 |
| `archive` 내부 | ✅ | 대상 식별 후 이동 작업 병렬 |

---

## 핵심 규칙 인용

### Ticket Dependencies (from SPEC.md)

> `dependencies`는 **의존 티켓의 파일 stem(확장자 `.md` 제외)** 목록이다.
> - 예: `"Implement-Parser"` (파일: `Implement-Parser.md`)
> - 금지: 경로 포함, 확장자 포함, 비결정적 별칭

### Guardrails (from SPEC.md)

> - `01.agents-task-context/` 또는 legacy `task-manager/`가 이미 존재하면 생성은 실패한다(덮어쓰기 금지).
> - 티켓 `dependencies`는 파일 stem 기준으로 검증 가능해야 한다.
> - 아카이빙은 `status: done`인 티켓만 대상으로 한다.
> - 아카이브 충돌 시 timestamp suffix로 회피한다.

---

## 외부 의존성 제거 (v2.0)

이전 버전은 Python 스크립트(`scripts/*.py`)에 의존했으나, 현재 버전은 모든 작업을 에이전트 도구(`Glob`, `Read`, `Write`, `Edit`, `Bash`, `Task`)로 직접 수행한다.

**이점:**
- 외부 런타임(Python) 불필요
- 다른 사람의 환경에서 즉시 사용 가능
- 에이전트 자체가 실행 주체 (스크립트 호출 오버헤드 제거)
