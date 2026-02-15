# Workflow Normative Interpretation

## 1. Purpose

이 문서는 COF 내에서 Workflow 문서를 작성/해석할 때 적용하는 **규범적(Normative) 기준**을 정의한다.  
Workflow는 "절차"가 아니라, **포인터 상태 전이(transition)의 선언**으로 해석해야 한다.

---

## 2. Document Identity

Workflow 문서는 다음 규칙에 의해 식별/해석해야 한다.

1. Workflow의 식별 메타데이터(`context_id`, `role`, `state` 등)는 사이드카 파일 또는 상위 manifest에 저장한다.
2. 문서 본문의 YAML Frontmatter는 런타임 인터페이스 필드(`name`, `description` 등)만 포함한다.
3. `context_id`는 전역 유일이며 변경 불가로 해석해야 한다.

---

## 3. Required Sections (Normative)

Workflow 문서는 다음 섹션을 반드시 포함해야 한다.

1. **Entry Context**: 입력 포인터(무엇을 받는가)
2. **Transition Steps**: 단계별 포인터 상태 전이(무엇이 어떻게 바뀌는가)
3. **Exit Rule**: 종료 조건과 최종 상태(무엇으로 끝나는가)
4. **Lifetime Transition**: 수명 전이 선언(전이 규칙이 없으면 유효하지 않음)

---

## 4. Transition Semantics (Normative)

Workflow의 각 Step은 다음 원칙으로 해석해야 한다.

1. 각 Step은 "작업 지시"가 아니라 "포인터 상태 전이 선언"이어야 한다.
2. 각 Step은 최소한 다음 정보를 포함해야 한다.
   - 입력 포인터(들)
   - 출력 포인터(들)
   - 상태 전이: `from` -> `to`
   - Read/Write 가정(정책이 아닌 가정의 선언)
3. Step 간 순서는 의미를 가지며, 생략된 Step이 있을 경우 Workflow는 불완전한 것으로 해석해야 한다.

---

## 5. Policy Separation (Normative)

1. Workflow 문서는 실행 코드(소스코드) 또는 런타임 판단 로직을 포함해서는 안 된다.
2. Workflow 문서는 권한/위반 처리(정책 강제)를 포함해서는 안 된다.  
   위반 처리와 권한 정책은 RULE/Policy 계층에서 정의하고, Workflow는 그 전제를 따른다고만 선언한다.

---

## 6. Scope Declaration (Glob) (Normative)

Workflow가 파일 시스템 범위를 선언할 때, Glob 패턴은 Read Scope(참조 가능 범위)를 선언하기 위한 용도로만 사용해야 한다.  
Glob 해석 규범은 아래 문서를 우선한다.

- `rule-normative-interpretation.md`
- `glob-patterns.md`

---

## 7. Validation Checklist

```
Workflow Doc Validation:
- [ ] 식별 메타(context_id/role/state)가 사이드카 또는 상위 manifest에 있다
- [ ] 문서 Frontmatter에는 런타임 필드(name/description)만 있다
- [ ] Entry Context / Transition Steps / Exit Rule / Lifetime Transition 섹션이 있다
- [ ] 각 Step이 포인터 상태 전이 선언으로 서술되어 있다 (inputs/outputs/from->to)
- [ ] 정책 강제/위반 처리 로직을 포함하지 않는다
- [ ] Glob은 Read Scope로만 해석되며 루트 무제한 패턴을 기본값으로 사용하지 않는다
```

---

## 8. References

- Spec: `../SPEC.md`
- Governance Guide: `cof-environment-set.md`
- Glob: `glob-patterns.md`
- Glob Normative: `rule-normative-interpretation.md`
