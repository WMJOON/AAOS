---
name: skill-governance
description: AAOS에서 SKILL을 설계/생성/이식/변경할 때 지켜야 하는 규칙(규법)을 제공하고, 정통성(Canonicality) 관점에서 최소 요건을 점검한다.
trigger: on_request
---
# Skill Governance (SKILL 규칙)

본 스킬은 “SKILL을 만드는 규칙”을 정의한다.
AAOS에서 SKILL은 단순 문서가 아니라 **집행 가능한 행동 단위**이므로, Canon/META Doctrine/Doctrine(RULE)에 종속된다.

---

## 0. 적용 범위

- 대상: `SKILL.md`를 포함하는 모든 skill 폴더
- 위치: 군체(Swarm) 내부(`02_Swarm/.../skills/`) 또는 Immune System 내부(`01_Nucleus/Immune_system/.../`)

---

## 1. Canonical SKILL 최소 요건

Canonical SKILL로 인정되려면 아래를 만족해야 한다.

### 1.1. 파일/폴더 요건

- (필수) `SKILL.md`
- (선택) `scripts/` (자동화가 있을 때만)
- (선택) `templates/` (입력/출력 템플릿이 있을 때만)
- (선택) `references/` (외부 근거/사양 문서가 있을 때만)

### 1.2. `SKILL.md` Frontmatter 요건

`SKILL.md`는 YAML frontmatter를 포함해야 하며, 최소 키를 포함한다.

```yaml
---
name: <kebab-case>
description: <1-line>
trigger: on_request | always_on
---
```

권장 키:
- `version`
- `scope`
- `requires` (의존 스킬/런타임)
- `permissions` (Tool/API/FS/네트워크 등)
- `natural_dissolution` (장기 구조/파일 생성 시 필수)

---

## 2. Permission Principal (권한 교리) 준수

SKILL이 아래 행위를 포함하면 **permission-judgment**를 전제로 설계한다.

- Tool/API 접근
- 구조 생성/확장
- 장기 저장(영구 보관)
- RULE/SKILL 변경으로 계보 영향

권장: `templates/PERMISSION-REQUEST.md` 사용 또는 상위 템플릿 링크.

---

## 3. Natural Dissolution (자연소멸) 준수

SKILL이 파일/폴더/로그를 생성하거나, 자동화로 지속 실행되는 경우:

- 생성물은 Blueprint/Rule에 의해 **종료 조건과 정리 절차**가 정의되어야 한다.
- 영구 보관은 기본값이 될 수 없다.

예외:
- Canon 직접 보증(bootstrap) 구조는 `permanent` 보존이 가능하나, 반드시 `meta_exception` 근거가 명시되어야 한다.

---

## 4. Audit Integrity (감사 무결성) 준수

SKILL이 판정/차단/해체 같은 집행 행위를 하면:

- `AUDIT_LOG.md` 기록을 남긴다.
- 기록은 append-only이며, 가능한 경우 해시체인 무결성을 사용한다.

Immune System 내부에서는 `_shared/audit.py`의 `safe_append_audit_entry()`를 표준으로 한다.

---

## 5. 공유 코드/의존성 규칙 (이식 가능성)

### 5.1. `_shared`는 “코어 스킬”로 취급한다

Inquisitor 내부 공유 런타임은 `inquisitor-core`로 간주한다.
따라서 단일 skill 폴더만 복사하면 동작하지 않을 수 있다.

- 의존 스킬: `SWARM_INQUISITOR_SKILL/_shared/` (`inquisitor-core`)
- 판단 스킬: `permission-judgment`, `blueprint-judgment`

### 5.2. 이식(Transplant) 체크리스트

- [ ] 의존 폴더(`_shared/`)를 함께 복사했는가?
- [ ] 상대경로 import가 새 위치에서도 유효한가?
- [ ] audit log 경로가 새 AAOS 루트 기준으로 올바른가?
- [ ] “strict mode” 정책이 필요한가?

---

## 6. 변경 절차(특히 Immune System 내부)

Immune System은 bootstrap 구조이므로, 내부 SKILL 변경이라도 최소한 다음을 권장한다.

- `META_AUDIT_LOG.md`에 변경 기록
- (필요 시) 플래그십 Agent 2종 이상 합의 + 인간 승인

---

## 7. Quick Check (로컬)

```bash
python3 scripts/verify_skill.py <skill_dir>
```
