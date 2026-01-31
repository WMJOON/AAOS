# Agent Normative Interpretation

## 1. Purpose

이 문서는 COF 내에서 Agent 문서를 작성/해석할 때 적용하는 **규범적(Normative) 기준**을 정의한다.

Agent는 "작업을 수행하는 실행 주체"이며, Skill과 달리 **자율적 의사결정 능력**을 가진다.

---

## 2. Agent vs Skill: Normative Distinction

| 구분 | Skill | Agent |
|------|-------|-------|
| 정체성 | Capability 선언 | Behavior 정의 |
| Frontmatter role | `SKILL` | `SKILL` + `agent_kind: sub-agent` |
| 실행 주체 | 외부에서 호출됨 | 자율적으로 행동 |
| 의사결정 | 불가 | 조건부 가능 |
| 에스컬레이션 | 불필요 | 필수 정의 |

---

## 3. Document Identity (Pointer Model)

Agent 문서는 다음 규칙에 의해 식별/해석해야 한다.

1. Agent 문서는 YAML Frontmatter에 최소한 다음 필드를 포함해야 한다.

   ```yaml
   ---
   context_id: cof-xxxx-agent
   role: SKILL
   agent_kind: sub-agent
   state: const | mutable | active | frozen | archived
   scope: immune | agora | nucleus | swarm
   lifetime: ticket | persistent | archived
   inherits_from: cof-parent-skill  # optional
   ---
   ```

2. `context_id`는 전역 유일이며 변경 불가로 해석해야 한다.
3. `agent_kind: sub-agent`가 없으면 Agent로 해석해서는 안 된다.
4. `inherits_from`이 있으면 해당 Skill의 capability를 상속한다.

---

## 4. Behavioral Boundaries (Normative)

Agent 문서는 다음 행동 경계를 반드시 정의해야 한다.

### 4.1 MUST (필수 정의)

- **Mission**: 담당 역할과 책임 범위
- **Capability Declaration**: 허용/금지된 컨텍스트 접근
- **Inputs/Outputs**: 입출력 정의
- **Execution Protocol**: 실행 단계별 행동 정의
- **Escalation Rules**: 에스컬레이션 조건과 대상

### 4.2 MUST NOT (금지 사항)

- **코드 직접 실행**: 스크립트 실행은 Runtime에 위임
- **정책 강제**: 권한/위반 처리는 RULE 계층에 위임
- **Skill-Mediated Creation 위반**: 직접 생성/수정 지시 금지

### 4.3 Decision Authority

| 영역 | 자율 판단 | 에스컬레이션 |
|------|----------|-------------|
| 기본값 설정 | O | - |
| SEV-3 경고 처리 | O | - |
| SEV-2 오류 복구 | 시도 후 | 실패 시 |
| SEV-1 위반 대응 | - | 즉시 |
| 비표준 경로 사용 | - | 승인 필요 |

---

## 5. Escalation Protocol (Normative)

### 5.1 필수 요소

모든 Agent는 다음 에스컬레이션 정보를 정의해야 한다:

1. **parent_agent**: 보고 대상 에이전트
2. **escalation_conditions**: 에스컬레이션 발동 조건
3. **handoff_format**: 보고 메시지 형식

### 5.2 Severity Classification

| SEV | 정의 | 의무 행동 |
|-----|------|----------|
| SEV-1 | Critical | 즉시 중단 + 에스컬레이션 |
| SEV-2 | Major | 복구 시도 → 실패 시 에스컬레이션 |
| SEV-3 | Minor | 경고 로깅 후 계속 |

---

## 6. Inheritance Model (Normative)

### 6.1 Skill 상속

Agent가 `inherits_from` 필드로 Skill을 지정하면:

1. Skill의 모든 capability를 상속받는다
2. Agent는 capability를 **축소**할 수 있다 (확장 불가)
3. 상속받은 capability 범위 내에서만 행동한다

### 6.2 상속 불가 항목

다음 항목은 상속되지 않으며 Agent에서 새로 정의해야 한다:

- Execution Protocol
- Decision Matrix
- Escalation Rules
- Behavioral Boundaries

---

## 7. Validation Checklist

```
Agent Doc Validation:
- [ ] YAML Frontmatter에 context_id/role/agent_kind/state/scope/lifetime이 있다
- [ ] role이 SKILL이고 agent_kind가 sub-agent다
- [ ] Mission, Capability Declaration, Inputs/Outputs가 있다
- [ ] Execution Protocol이 정의되어 있다
- [ ] Escalation Rules가 정의되어 있다 (parent_agent, conditions, format)
- [ ] MUST NOT 항목을 위반하지 않는다
- [ ] inherits_from이 있다면 해당 Skill이 존재한다
```

---

## 8. References

- SPEC: `../SPEC.md`
- Rule Genome: `../../rules/cof-environment-set.md`
- Sub-Agent Normative: `../../skills/00.cof-pointerical-tool-creator/references/subagent-normative-interpretation.md`
- Skill Normative: `../../skills/00.cof-pointerical-tool-creator/references/skill-normative-interpretation.md`
