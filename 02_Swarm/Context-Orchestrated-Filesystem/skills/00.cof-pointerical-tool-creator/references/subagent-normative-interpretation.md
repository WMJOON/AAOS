# Sub-Agent Normative Interpretation

## 1. Purpose

이 문서는 COF 내에서 Sub-Agent 문서를 작성/해석할 때 적용하는 **규범적(Normative) 기준**을 정의한다.  
Sub-Agent는 "작업을 위임받는 실행 주체"이지만, 문서 자체는 COF 포인터 모델에서 **Skill의 한 형태**로 취급한다.

---

## 2. Document Identity (Pointer Model)

Sub-Agent 문서는 다음 규칙에 의해 식별/해석해야 한다.

1. Sub-Agent 문서는 YAML Frontmatter에 최소한 다음 필드를 포함해야 한다.

   ```yaml
   ---
   context_id: cof-xxxx
   role: SKILL
   agent_kind: sub-agent
   state: const | mutable | active | frozen | archived
   scope: immune | agora | nucleus | swarm
   lifetime: ticket | persistent | archived
   ---
   ```

2. `context_id`는 전역 유일이며 변경 불가로 해석해야 한다.
3. `agent_kind: sub-agent`가 없는 문서는 Sub-Agent로 해석해서는 안 된다.

---

## 3. Responsibility Boundary (Normative)

Sub-Agent 문서는 다음 책임 경계를 반드시 포함해야 한다.

1. Sub-Agent는 자신의 임무(Mission)와 범위를 명시해야 한다.
2. Sub-Agent는 입력/출력(Inputs/Outputs)을 포인터 관점에서 명시해야 한다.
3. Sub-Agent는 허용된/금지된 컨텍스트 접근을 명시해야 한다.
4. Sub-Agent는 실패 조건과 상위 에이전트 보고 방식(Escalation & Handoff)을 포함해야 한다.

> 해설: Sub-Agent는 "할 수 있는 것"과 "하면 안 되는 것"이 문서 레벨에서 고정되어야 한다.  
> 그래야 상위 에이전트가 위임 시 책임과 리스크를 추적할 수 있다.

---

## 4. Safety & Policy Separation (Normative)

1. Sub-Agent 문서는 정책 강제 로직(권한/위반 처리)을 포함해서는 안 된다.  
   위반 처리와 권한 정책은 RULE/Policy 계층에서 정의하고, Sub-Agent는 그 전제를 따른다고만 선언한다.
2. Sub-Agent 문서는 실행 코드(소스코드)를 포함해서는 안 된다.  
   (필요하다면 `scripts/` 또는 외부 런타임에 위임하고, 문서에는 참조만 둔다.)
3. COF의 "Skill-Mediated Creation Only" 원칙을 위반하는 직접 생성/수정 지시를 포함해서는 안 된다.

---

## 5. Scope Declaration (Glob) (Normative)

Sub-Agent가 파일 시스템 범위를 선언할 때, Glob 패턴은 Read Scope(참조 가능 범위)를 선언하기 위한 용도로만 사용해야 한다.  
Glob 해석 규범은 아래 문서를 우선한다.

- `rule-normative-interpretation.md`
- `glob-patterns.md`

---

## 6. Validation Checklist

```
Sub-Agent Doc Validation:
- [ ] YAML Frontmatter에 context_id/role/agent_kind/state/scope/lifetime가 있다
- [ ] role이 SKILL이고 agent_kind가 sub-agent다
- [ ] Mission, Inputs/Outputs, Allowed/Forbidden Contexts, Escalation & Handoff가 있다
- [ ] 정책 강제/위반 처리 로직을 포함하지 않는다
- [ ] Glob은 Read Scope로만 해석되며 루트 무제한 패턴을 기본값으로 사용하지 않는다
```

---

## 7. References

- Spec: `../SPEC.md`
- Rule Genome: `../../RULE.md`
- Skill Normative: `skill-normative-interpretation.md`
- Glob: `glob-patterns.md`
- Glob Normative: `rule-normative-interpretation.md`
