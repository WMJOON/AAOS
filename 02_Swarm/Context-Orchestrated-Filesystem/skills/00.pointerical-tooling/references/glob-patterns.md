# Glob Directory & File Patterns

## Scope
- 목적: VS Code glob 패턴 규칙을 COF 문서 생성 시 참고하기 위함
- 상태: 초안 (필요 시 업데이트)

## Glob Syntax (VS Code)
- `/` : 경로 구분자
- `*` : 경로 세그먼트 내 0개 이상 문자 매칭
- `?` : 경로 세그먼트 내 1개 문자 매칭
- `**` : 경로 세그먼트 여러 개(없어도 됨) 매칭
- `{a,b}` : 그룹 매칭 (예: `{**/*.html,**/*.txt}`)
- `[0-9]` : 문자 범위 매칭 (예: `example.[0-9]`)
- `[!0-9]` : 문자 범위 부정 매칭

## Special Cases (VS Code)
- Windows에서도 경로 구분자는 `/`를 사용한다. 매칭 시에는 `/`와 `\\` 모두와 매치된다.
- Search view는 `**` 접두어를 암묵적으로 포함한다.
- 설정(`files.exclude`, `search.exclude`)은 워크스페이스 루트 기준이며, 하위 폴더 매칭에는 `**/example` 형태가 필요하다.
- 특수문자 `[` `]` 를 리터럴로 매칭하려면 `[[]` `[]]` 형태로 감싼다.

## COF Usage Notes
- 포인터 타입 디렉토리 매칭은 `**/00.index/**` 같은 패턴으로 표현한다.
- 파일명 역할/수명 매칭은 접미사/접두사 규칙과 조합한다.

## References
- VS Code Glob Patterns (reference):
```
https://code.visualstudio.com/docs/editor/glob-patterns
```

---

# Glob Pattern Interpretation Rules (Normative)

본 규칙에서 정의하는 Glob 패턴은 COF(Context-Orchestrated Filesystem) 내에서  
스킬이 접근·참조·탐색할 수 있는 파일 범위를 **선언적으로 제한**하기 위한 규칙으로 해석해야 한다.

1. Glob 패턴은 파일의 **참조 가능 범위(Read Scope)**를 정의하는 용도로만 사용해야 한다.  
   매칭된 파일은 스킬이 읽고 분석할 수 있는 후보가 되지만,  
   해당 파일이 수정·삭제·이동 가능한 대상임을 의미해서는 안 된다.  
   수정 가능 여부는 반드시 별도의 Policy 계층(Fixing Policy, Hand-off Policy, History Policy 등)에 의해 판단되어야 한다.
2. Glob 패턴은 기본적으로 **포함(include)** 기준으로 해석해야 한다.  
   제외(exclude) 또는 부정 패턴은 Glob 해석의 기본 규칙으로 사용해서는 안 되며,  
   불가피한 경우라도 정책 문서에서 명시적으로 정의된 경우에만 제한적으로 허용해야 한다.
3. `**`(globstar)가 포함된 패턴은 **재귀 탐색을 허용**하는 것으로 해석해야 한다.  
   따라서 `**`를 사용하는 경우, 스킬 정의자는 반드시 **상위 디렉토리의 범위**를 명시해야 하며,  
   루트 기준(`**/*`)의 무제한 탐색 패턴을 기본값으로 사용해서는 안 된다.
4. Glob 패턴은 파일의 의미적 역할(role)을 직접 표현하지 못한다는 점을 전제로 해석해야 한다.  
   따라서 COF 해석 시에는 파일명 규칙, 디렉토리 구조, 접두·접미 규칙 등  
   사전 합의된 구조적 컨벤션과 결합하여 의미를 부여해야 한다.
5. 정책 디렉토리 및 아카이브 디렉토리는 Glob 패턴에 매칭되더라도  
   기본적으로 **읽기 전용(Read-only Context)**으로 취급해야 한다.  
   이는 Glob 패턴이 접근 권한을 표현하지 못하는 구조적 한계를  
   정책 계층에서 보완하기 위한 필수 규칙이다.

---

# Skill Metadata with Glob Scope (Example)

```yaml
skill:
  id: cof-pointerical-tooling
  version: 0.1.3
  description: >
    COF 구조 내에서 포인터성 파일 및 인덱스 컨텍스트를
    탐색·분석하기 위한 보조 스킬

scope:
  filesystem:
    readable:
      - "skills/**/references/**/*.md"
      - "**/00.index/**"
    policy_assumptions:
      read_only:
        - "01_hand-off-policy/**"
        - "99_history-policy/**"

constraints:
  glob_interpretation:
    recursive_allowed: true
    root_unbounded_glob: false
    negation_allowed: false
```

해석 기준 (YAML 기준)
- `scope.filesystem.readable`: 스킬이 참조 가능한 파일 범위를 Glob 패턴으로 선언한다.  
  이 목록에 포함되지 않은 파일은 스킬이 탐색해서는 안 된다.
- `policy_assumptions.read_only`: Glob 매칭 여부와 무관하게 항상 읽기 전용으로 취급해야 하는 디렉토리를 선언한다.  
  RULE 문서의 정책 해석을 메타데이터 수준에서 재확인하는 장치다.
- `constraints.glob_interpretation`: Glob 해석 전제를 명시하여 구현체 간 해석 차이를 줄인다.

---

# Design Summary
- RULE 문서: Glob을 **어떻게 해석해야 하는가**에 대한 규범 제공
- Skill YAML: Glob을 **어디까지 적용하는가**에 대한 선언 제공

이렇게 분리하면 Glob 자체는 단순하게 유지되고,  
의미·권한·책임은 Policy와 Metadata가 떠안으며,  
Agent 구현체가 바뀌어도 해석 일관성이 유지된다.
