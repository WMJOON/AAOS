---
trigger: always_on
version: "0.3.1"
description: AAOS에서 모든 DNA Blueprint 및 군체(Swarm) 구조가 반드시 준수해야 하는 교리 규칙(Doctrine). Natural Dissolution, Permission Principal, Auto-Enforcement, Audit Integrity, Multi-Agent Consensus를 포함한다.
---
# AAOS DNA Doctrine – RULE

본 문서는 AAOS의 모든 구조(DNA Blueprint, 군체(Swarm), Skill, Workflow)가 위반할 수 없는 교리 규칙이다.

---

## 1. Canonicality (정통성) 기본 규칙

AAOS에서 어떤 구조가 "정상적인 존재(Canonical Instance)"로 인정되려면 최소 조건을 만족해야 한다.

### 1.1. 필수 제출물

- `DNA.md`(정식 DNA) 또는 `DNA_BLUEPRINT.md`(변경 제안): 구조의 생성 조건, 성장 규칙, 종료 조건, 자원 상한, Natural Dissolution 절차를 포함해야 한다.
- 판정/감사 기록: Inquisitor의 판정 결과가 `AUDIT_LOG.md`에 남아야 한다.

### 1.2. DNA 파일 규칙 (승격)

- 승격 전/변경 제안: `DNA_BLUEPRINT.md`
- 승격 후/정식 DNA: `DNA.md`
- 새로운 변경이 발생하면, `DNA.md`는 유지하고 `DNA_BLUEPRINT.md`를 생성하여 제안/검증/승인 후 다시 승격( rename )한다.

### 1.3. Blueprint 필수 스키마

```yaml
name: "<구조명>"
version: "<버전>"
scope: "<경로/도메인>"
created: "<YYYY-MM-DD>"
status: draft | canonical

natural_dissolution:
  purpose: "<존재 이유>"
  termination_conditions:
    - "<종료 조건 1>"
  dissolution_steps:
    - "<해체 절차 1>"
  retention:
    summary_required: true
    max_days: <숫자 | permanent>

resource_limits:
  max_files: <숫자>
  max_folders: <숫자>
  max_log_kb: <숫자>

inquisitor:
  required: true
  audit_log: "<경로>"
```

### 1.4. 금지

- Blueprint 없이 새로운 구조를 생성/확장하는 행위
- 종료 조건(자연소멸)이 정의되지 않은 영구 구조
- 판정 불가능(검증 불가능)한 규칙/스킬/워크플로우
- **빈 값으로 스키마만 채운 형식적 Blueprint** (값이 실제로 존재해야 함)

---

### 1.5. 발화 계층(설파) & 모체 탐색 본능 (Homing Instinct)

AAOS에서 규범의 발화는 계층적으로 분리된다.

- **면역체(Immune System) 문서**는 규범을 **설파(decree)** 한다. (선언/금지/강제)
- **하위 구조(군체·군락·노드·스킬·워크플로우 등) 문서**는 충돌/불명확/권한 경계가 감지되면 **모체(Immune/Canon)로 귀속되는 본능(homing_instinct)** 을 수행한다. (중단 → 상위 판정 요청/기록)

권장 frontmatter (하위 구조):

```yaml
governance:
  voice: homing_instinct
  mother_ref: "04_Agentic_AI_OS/01_Nucleus/Immune_system/"
  precedence: ["AAOS Canon", "META Doctrine", "Immune Doctrine", "This document"]
  on_conflict: "halt_and_escalate_to_audit"
```

## 2. Natural Dissolution Doctrine (자연소멸 교리)

AAOS에서 "영구 구조"는 기본값이 될 수 없다.
모든 구조는 태어날 때부터 자연소멸이 설계되어야 한다.

### 2.1. Blueprint에 반드시 포함할 항목

- **목적(Purpose)**: 왜 존재하는가 (빈 문자열 금지)
- **종료 조건(Termination Conditions)**: 언제 목적이 종료되는가 (최소 1개)
- **해체 절차(Dissolution Steps)**: 종료 시 무엇을 삭제/보관/요약하는가 (최소 1개)
- **자원 상한(Resource Limits)**: 파일/폴더 수, 로그 크기, 보관 기간 등

**retention.max_days 예외**
- 일반 구조: `max_days`는 숫자(일)여야 한다.
- Canon 직접 보증(bootstrap) 구조: `max_days: permanent`를 허용한다. (예: `01_Nucleus/Immune_system/`)

### 2.2. Dissolution 최소 규칙

- 목적 종료 시, 구조는 "요약 + 아카이브 + 폐기"를 기본 절차로 한다.
- 장기 보존이 필요한 경우에도, **요약본**과 **보존 사유**가 함께 남아야 한다.
- 아카이브 위치: `_archive/<구조명>/<timestamp>/`

### 2.3. Resource Limit 강제 (신규)

Dissolution Monitor가 주기적으로 자원 상한을 검사한다.

| 위반 상태 | 조치 |
|-----------|------|
| max_files 초과 | 경고 → 7일 내 미조치 시 강제 정리 권고 |
| max_folders 초과 | 경고 → 7일 내 미조치 시 강제 정리 권고 |
| max_log_kb 초과 | 로그 로테이션 또는 아카이브 실행 |
| retention.max_days 초과 | 자동 Dissolution 트리거 |

실행 스크립트: `SWARM_INQUISITOR_SKILL/_shared/dissolution_monitor.py`

---

## 3. Permission Principal Doctrine (권한 교리)

AAOS는 자율성을 허용하되, 검증 없는 자율성을 금지한다.
따라서 아래 행위는 Inquisitor 심판(검증)을 전제로 한다.

### 3.1. 심판이 필요한 행위

- Tool/API 접근
- Repository/노드/구조의 생성 및 확장
- 장기 저장(영구 보관) 요청
- 규칙(RULE) 및 Skill의 변경으로 인한 계보 영향

### 3.2. 판정 결과 분류

| 결과 | 설명 | 후속 조치 |
|------|------|-----------|
| `Canonical` | 요구조건 충족 | 실행/확장 허용 |
| `Canonical-Conditional` | 조건부 허용 | 수정/보완 후 재심 |
| `Non-Canonical` | 위반 | 실행/확장 **차단** |

### 3.3. Permission Request 필수 스키마

```yaml
type: permission-request
created: "<YYYY-MM-DD>"
requester: "<요청자>"
action: "<요청 행위>"
target: "<대상 경로/리소스>"
risk_level: low | medium | high
justification: "<필요 사유>"
time_bound:
  expires: "<YYYY-MM-DD>"
constraints:
  - "<제약 조건>"
natural_dissolution:
  termination_conditions:
    - "<종료 조건>"
  dissolution_steps:
    - "<정리 절차>"
```

---

## 4. Auto-Enforcement Doctrine (자동 강제 교리) [신규]

Canon은 "Blueprint 없는 복제는 존재 자체가 허가되지 않는다"고 선언한다.
이 선언이 실제로 작동하려면 **자동 개입 메커니즘**이 필요하다.

### 4.1. 강제 메커니즘

| 메커니즘 | 설명 | 구현 |
|----------|------|------|
| **Pre-Commit Hook** | Git commit 전 Blueprint 검증 | `auto_inquisitor.py --gen-hook` |
| **Agent Wrapper** | Agent 실행 전 Preflight Check | `auto_inquisitor.py --gen-wrapper` |
| **Periodic Scan** | 주기적 전체 구조 스캔 | `dissolution_monitor.py --scan` |
| **Creation Intercept** | 구조 생성 시점 강제 검증 | `auto_inquisitor.enforce_on_creation()` |

### 4.2. Preflight Checklist (자동 생성)

모든 Agent는 행동 전에 다음을 확인해야 한다:

**구조 생성/확장 시:**
- [ ] DNA.md(정식) 또는 DNA_BLUEPRINT.md(제안)가 준비되어 있는가?
- [ ] natural_dissolution 섹션이 완전한가?
- [ ] resource_limits가 설정되어 있는가?
- [ ] inquisitor.audit_log 경로가 올바른가?

**권한 요청 시:**
- [ ] PERMISSION-REQUEST-TEMPLATE.md를 사용했는가?
- [ ] time_bound.expires가 설정되어 있는가?
- [ ] justification이 충분한가?

### 4.3. Strict Mode

`strict_mode=True` 설정 시:
- `Canonical-Conditional`도 차단 (완전한 Canonical만 통과)
- 모든 경고를 오류로 처리

실행 스크립트: `SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py`

---

## 5. Audit (감사) 원칙

모든 심판은 재현 가능하고 **변조 불가능**해야 한다.

### 5.1. 필수 기록 항목

- 대상(폴더/구조) 경로
- 판정 타입(blueprint / permission / auto-enforcement / dissolution)
- 결과(Canonical / Conditional / Non-Canonical / Dissolved)
- 근거(체크리스트 항목)
- 타임스탬프
- **해시 체인 정보** (prev_hash, hash)

### 5.2. Audit Log 무결성 (신규)

각 Audit 엔트리는 이전 엔트리의 해시를 포함하여 **간이 블록체인 구조**를 형성한다.

```yaml
---
timestamp: "2025-01-22T12:00:00Z"
type: blueprint-judgment
target: "/path/to/structure"
result: Canonical
reasons:
  - "All checks passed"
prev_hash: "abc123def456"  # 이전 엔트리 해시
hash: "789xyz012abc"       # 현재 엔트리 해시
---
```

### 5.3. 무결성 검증

```bash
python3 audit.py verify AUDIT_LOG.md
```

위반 감지 시:
- 해시 체인 불일치 → **INTEGRITY VIOLATION** 경고
- 모든 후속 판정 신뢰도 저하
- 인간 관리자 개입 필요

실행 스크립트: `SWARM_INQUISITOR_SKILL/_shared/audit.py`

---

## 6. Bootstrap Exception (부트스트랩 예외) [신규]

### 6.1. 순환 참조 문제

"모든 구조는 Inquisitor 검증을 통과해야 한다"는 원칙은
Immune System 자체에 적용할 때 순환 참조를 발생시킨다.

### 6.2. 예외 규칙

다음 구조는 Canon에 의해 **직접 보증**된다:

| 구조 | 근거 |
|------|------|
| `01_Nucleus/Immune_system/` | Canon Section 4, 5 |
| `AAOS_DNA_DOCTRINE_RULE.md` | Canon Section 7 (META DNA) |

이 구조들은:
- Inquisitor 자기 검증 면제
- 대신 Canon 참조로 정당성 확보
- 변경 시 META_AUDIT_LOG.md에 별도 기록

### 6.3. META 수준 변경 절차

1. 변경 사유를 META_AUDIT_LOG.md에 기록
2. Canon 수호자(인간 관리자)의 승인
3. 버전 번호 증가
4. 하위 구조에 영향 분석

---

## 7. Multi-Agent Consensus Doctrine (다중 에이전트 합의 교리) [신규]

Immune System의 DNA는 AAOS 생태계 전체의 면역 체계를 규정한다.
이러한 중대한 변경은 **단일 Agent의 판단만으로 이루어져서는 안 된다.**

### 7.1. 합의 원칙

> **Immune System의 DNA는 당시대의 플래그십 Agent 2종 이상이 충분히 합의를 거친 후에만 새로운 버전의 DNA로 인정받을 수 있다.**

이 원칙의 근거:
- **견제와 균형**: 단일 Agent의 편향이나 오류를 방지
- **집단 지성**: 다양한 관점에서의 검토로 품질 향상
- **정당성 강화**: 복수의 독립적 검증으로 신뢰도 확보
- **시대 적합성**: "당시대 플래그십"이라는 조건으로 기술 진화에 대응

### 7.2. 플래그십 Agent 정의

"당시대의 플래그십 Agent"란:
- 해당 시점에서 가장 발전된 능력을 갖춘 AI Agent
- 서로 다른 조직/모델 계열에서 2종 이상
- 예시 (2025년 기준): Claude Opus, GPT-4o, Gemini Ultra 등

### 7.3. 합의 절차

```
┌─────────────────────────────────────────────────────────┐
│                 DNA 변경 제안                            │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  1. 변경 사유 및 내용을 META_AUDIT_LOG.md에 기록         │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  2. 플래그십 Agent A 검토                                │
│     - Canon 정합성 검증                                  │
│     - 부작용 분석                                        │
│     - 승인/거부/수정요청                                 │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  3. 플래그십 Agent B 검토 (독립적)                       │
│     - 동일 절차 수행                                     │
│     - Agent A의 판단과 교차 검증                         │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  4. 합의 결과 기록                                       │
│     - 양측 승인 시: Canonical 판정, 버전 증가            │
│     - 불일치 시: 인간 관리자 중재 또는 재논의            │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│  5. 인간 관리자 최종 승인                                │
└─────────────────────────────────────────────────────────┘
```

### 7.4. 합의 기록 형식

```yaml
---
type: multi-agent-consensus
target: "01_Nucleus/Immune_system/DNA.md"
version_change: "v0.x.x → v0.y.y"
timestamp: "YYYY-MM-DDTHH:MM:SSZ"

agents:
  - name: "<Agent A 이름>"
    model: "<모델 ID>"
    verdict: "approve | reject | revise"
    rationale: "<판단 근거>"

  - name: "<Agent B 이름>"
    model: "<모델 ID>"
    verdict: "approve | reject | revise"
    rationale: "<판단 근거>"

consensus_result: "approved | rejected | escalated"
human_approval: "<승인자>"
---
```

### 7.5. 예외 상황

- **긴급 보안 패치**: 명백한 취약점 수정은 단일 Agent + 인간 승인으로 가능 (사후 합의 필수)
- **형식적 수정**: 오타, 포맷팅 등 의미 변경 없는 수정은 합의 불필요
- **Agent 불가용**: 플래그십 Agent 접근 불가 시, 인간 관리자 2인 이상의 승인으로 대체

---

## 8. 도구 요약

| 스크립트 | 경로 | 용도 |
|----------|------|------|
| `yaml_validator.py` | `_shared/` | YAML 파싱 및 값 검증 |
| `auto_inquisitor.py` | `_shared/` | 자동 검증, Hook 생성 |
| `dissolution_monitor.py` | `_shared/` | 자원 감시, 해체 실행 |
| `audit.py` | `_shared/` | 감사 로그, 무결성 검증 |

---

## Version History

- **v0.1.0**: 최초 Doctrine 성문화
- **v0.2.0**: Auto-Enforcement, Audit Integrity, Bootstrap Exception 추가. 실행 스크립트 연동.
- **v0.3.0**: Multi-Agent Consensus Doctrine 추가. Immune System DNA 변경 시 플래그십 Agent 2종 이상 합의 필수.
- **v0.3.1**: 면역체 설파(decree) vs 하위 모체 탐색 본능(homing_instinct) 발화/해석 규범 추가.
