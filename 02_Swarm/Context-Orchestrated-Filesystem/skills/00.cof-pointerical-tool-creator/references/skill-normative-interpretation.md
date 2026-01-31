# Skill Normative Interpretation

## 1. Purpose

이 문서는 COF 내에서 Skill 문서를 작성/해석할 때 적용하는 **규범적(Normative) 기준**을 정의한다.  
Skill 문서는 "무엇을 할 수 있는가(capability)"를 선언하는 문서이며, "어떻게 실행되는가(implementation)"는 원칙적으로 문서 밖(스크립트/런타임/정책 계층)에 위치해야 한다.

---

## 2. Document Identity (Pointer Model)

Skill 문서는 COF 포인터 모델의 "Context Pointer"로 해석한다.

1. Skill 문서는 YAML Frontmatter에 최소한 다음 필드를 포함해야 한다.

   ```yaml
   ---
   context_id: cof-xxxx
   role: SKILL
   state: const | mutable | active | frozen | archived
   scope: immune | agora | nucleus | swarm
   lifetime: ticket | persistent | archived
   ---
   ```

2. `context_id`는 전역 유일이며 변경 불가로 해석해야 한다.
3. 파일 경로/파일명 변경은 `context_id`의 동일성을 변경하지 않는 것으로 해석해야 한다.

---

## 3. Capability-Only Principle (Normative)

Skill 문서는 다음 규칙에 의해 해석해야 한다.

1. Skill 문서는 포인터 연산 능력(capability)만을 선언해야 한다.
2. Skill 문서는 실행 코드(소스코드), 런타임 판단(동적 의사결정), 정책 강제 로직(권한/위반 처리)을 포함해서는 안 된다.
3. Skill 문서는 허용된/금지된 컨텍스트 접근을 명시해야 한다.
4. Skill 문서는 예상 소비자(Immune / Agora / Agent)를 명시해야 한다.

> 해설: Skill 문서가 "규칙"이나 "워크플로우"를 잠식하지 않도록, 역할(Responsibility)을 분리한다.  
> 권한/위반 처리는 RULE/Policy 계층에서 정의하고, Skill은 그 범위 내에서의 capability만 선언한다.

---

## 4. Scope Declaration (Glob) (Normative)

Skill 문서가 파일 시스템 범위를 선언할 때, Glob 패턴은 다음 방식으로 해석해야 한다.

1. Glob 패턴은 Read Scope(참조 가능 범위)를 선언하기 위한 용도로만 사용해야 한다.
2. Glob 패턴은 기본적으로 include 기준으로 해석해야 한다.
3. `**`(globstar)를 사용하는 경우, 루트 무제한(`**/*`) 탐색을 기본값으로 사용해서는 안 된다.
4. 정책/아카이브 디렉토리는 매칭되더라도 기본적으로 Read-only Context로 해석해야 한다.

Glob 해석의 상세 규범은 아래 문서를 우선한다.
- `rule-normative-interpretation.md`
- `glob-patterns.md`

---

## 5. Recommended Skill Document Skeleton (Non-normative)

아래는 권장 섹션이다(형식은 바뀌어도 되지만 의미는 유지한다).

1. `Purpose`: 이 스킬의 목적과 범위
2. `Capability Declaration`: allowed/forbidden contexts, consumers
3. `Inputs / Outputs`: 입력 포인터/출력 포인터
4. `Constraints`: 안전 제약(예: "history는 읽기 전용")
5. `References`: 관련 Rule/Workflow/Policy 링크

---

## 6. Validation Checklist

```
Skill Doc Validation:
- [ ] YAML Frontmatter에 context_id/role/state/scope/lifetime가 있다
- [ ] role이 SKILL이다
- [ ] capability(allowed/forbidden/consumers)가 명시되어 있다
- [ ] 정책 강제/위반 처리 로직을 포함하지 않는다
- [ ] Glob은 Read Scope로만 해석되며 루트 무제한 패턴을 기본값으로 사용하지 않는다
```

---

## 7. References

- Spec: `../SPEC.md`
- Rule Genome: `../../rules/cof-environment-set.md`
- Glob: `glob-patterns.md`
- Glob Normative: `rule-normative-interpretation.md`
