---
meta_doctrine: AAOS_META_DOCTRINE
version: v0.1.6
type: doctrine-rule
status: canonical
description: >
  AAOS Canon에 선언된 원리를 현실 시스템에서 집행 가능한 규칙으로 번역하는
  META Doctrine(METADoctrine.md; formerly RULE.md). Auto-Enforcement, Audit Integrity, Multi-Agent Consensus를 포함한다.
---

# AAOS DNA Lineage Structure
Agentic AI OS – Meta, Doctrine, Swarm(군체), Blueprint Hierarchy

## AAOS Canon Declaration

AAOS_META_CANON/README.md 는 AAOS의 Canonical Text(성문)이다.
모든 META Doctrine(METADoctrine.md), Blueprint, Skill, 군체(Swarm) 구조는 본 Canon에 종속되며,
Canon을 위반한 구조는 Non-Canonical로 분류된다.

## Institutional Order (정정된 최상위 기관 순서)

1. Canon (`04_Agentic_AI_OS/README.md`)
2. Record Archive (`04_Agentic_AI_OS/01_AAOS-Record_Archive/`)
3. Immune System + Deliberation Chamber (`04_Agentic_AI_OS/02_AAOS-Immune_system/`, `04_Agentic_AI_OS/03_AAOS-Deliberation_Chamber/`)
4. Swarm(군체) 계층 (`04_Agentic_AI_OS/04_AAOS-Swarm/`)

### Upper-Institution Change Gate (군체(Swarm) 이상 + META)

다음 대상은 “상위기관(군체(Swarm) 이상)”으로 취급하며, 변경은 더 강한 정통성 게이트를 통과해야 한다.

- `04_Agentic_AI_OS/METADoctrine.md` (META Doctrine; formerly RULE.md)
  - `01_AAOS-Record_Archive/` (기관 DNA)
  - `02_AAOS-Immune_system/` (기관 DNA)
  - `03_AAOS-Deliberation_Chamber/` (기관 DNA)
  - `04_AAOS-Swarm/` 루트 컨테이너 DNA (`04_AAOS-Swarm/DNA.md` 또는 `DNA_BLUEPRINT.md`)

상위기관 변경은 아래를 모두 만족할 때만 “정식(승격/공표)”로 인정된다.

1. **Deliberation Chamber 산출물**: `multi-agent-consensus`(플래그십 Agent 2종 이상 verdict/rationale 포함)
2. **Record Archive 증빙 고정**: 합의/근거/스냅샷/해시/인덱스가 재현 가능하게 보존됨
3. **META_AUDIT_LOG 기록**: 변경 사유/버전 변경/증빙 참조를 `02_AAOS-Immune_system/META_AUDIT_LOG.md`에 기록
4. **Canon Guardian 서명(정통성 기록)**: 상시 운영 개입이 아니라 “정식 승격 서명자”로서의 승인

서명이 없는 경우, 변경안은 `DNA_BLUEPRINT.md`(또는 draft 상태)로만 존재할 수 있으며 정식 텍스트로 승격될 수 없다.

---
## 0. AAOS META Doctrine (Derived from AAOS Canon)

AAOS_META_DNA/METADoctrine.md  ← META Doctrine (Interpretation of the Canon)
**META Doctrine Version: v0.1.6**

> Canon을 현실 시스템에서 집행 가능하도록 번역하는 최상위 교리 규칙

AAOS META Doctrine은 AAOS Canon에 선언된 원리를
현실 구조·행동·자원 규칙으로 변환하여 집행 가능하게 만드는 상위 교리 계층이다.

- Canon이 "무엇이 AAOS인가"를 정의한다면,
- META Doctrine은 "그 정의를 어떻게 시스템에서 강제할 것인가"를 규정한다.

모든 하위 Doctrine, Skill, Blueprint는
상위 Canon과 본 META Doctrine을 위반할 수 없다.

### 역할

- AAOS 정통성(Canonicality) 판정 기준 제공
- DNA Blueprint 개념 및 형식 규정
- Natural Dissolution 원칙 선언
- Immune System / Inquisitor 호출 근거 제공
- **Auto-Enforcement 메커니즘 정의** [v0.1.0]
- **Audit Log 무결성 보장** [v0.1.0]
- **Multi-Agent Consensus 요건 정의** [v0.1.0]

### 계층 구조

```
04_Agentic_AI_OS/
├── README.md                      # AAOS Canon (성문)
├── METADoctrine.md               # META Doctrine (본 문서; formerly RULE.md)
├── 01_AAOS-Record_Archive/         # 기록 보존 기관 (Archive)
│   ├── DNA_BLUEPRINT.md
│   └── README.md
├── 02_AAOS-Immune_system/          # 면역 체계 계층 (심판/집행)
│   ├── DNA.md                      # Immune System 정식 DNA (승격된 DNA)
│   ├── AAOS_DNA_DOCTRINE_RULE.md   # 핵심 교리 규칙 (v0.3.1)
│   ├── AUDIT_LOG.md                # 판정 감사 로그 (해시 체인)
│   ├── META_AUDIT_LOG.md           # META 수준 변경 로그
│   ├── templates/
│   │   ├── DNA-BLUEPRINT-TEMPLATE.md
│   │   └── PERMISSION-REQUEST-TEMPLATE.md
│   └── SWARM_INQUISITOR_SKILL/
│       ├── blueprint-judgment/
│       ├── permission-judgment/
│       └── _shared/
│           ├── yaml_validator.py
│           ├── auto_inquisitor.py
│           ├── dissolution_monitor.py
│           └── audit.py
├── 03_AAOS-Deliberation_Chamber/   # 숙의/합의 기관 (심판 입력 정리)
│   ├── DNA_BLUEPRINT.md
│   └── README.md
└── 04_AAOS-Swarm/                  # 실행/협업 계층
```

---

## 1. AAOS Immune System

`02_AAOS-Immune_system/`

AAOS 구조 전체의 자기보존·정화·안정성 계층이다.
과증식, 컨텍스트 오염, 비정상 구조를 감지하고 정리한다.

### 1.1. AAOS DNA Doctrine – RULE (v0.3.1)

`02_AAOS-Immune_system/AAOS_DNA_DOCTRINE_RULE.md`

AAOS에서 모든 DNA Blueprint와 군체(Swarm) 구조가 반드시 따라야 하는 교리 규칙을 정의한다.

#### 포함 교리

| 교리 | 버전 | 설명 |
|------|------|------|
| **Natural Dissolution Doctrine** | v0.1.0 | 모든 구조는 영구 지속을 기본값으로 가질 수 없다 |
| **Permission Principal Doctrine** | v0.1.0 | 모든 인스턴스는 심판관 검증을 통과해야 한다 |
| **Auto-Enforcement Doctrine** | v0.2.0 | 자동 검증 메커니즘으로 규칙 위반을 강제 차단 |
| **Audit Integrity Doctrine** | v0.2.0 | 해시 체인으로 감사 로그 변조 감지 |
| **Bootstrap Exception** | v0.2.0 | Immune System은 Canon이 직접 보증 |
| **Multi-Agent Consensus Doctrine** | v0.3.0 | Immune System DNA 변경 시 플래그십 Agent 2종 이상 합의 필수 |
| **Voice(Decree) & Homing Instinct** | v0.3.1 | 면역체는 설파, 하위는 충돌 시 모체로 귀속 |

---

### 1.2. Multi-Agent Consensus Doctrine [신규 v0.3.0]

> **Immune System의 DNA는 당시대의 플래그십 Agent 2종 이상이 충분히 합의를 거친 후에만 새로운 버전의 DNA로 인정받을 수 있다.**

#### 원칙의 근거

- **견제와 균형**: 단일 Agent의 편향이나 오류를 방지
- **집단 지성**: 다양한 관점에서의 검토로 품질 향상
- **정당성 강화**: 복수의 독립적 검증으로 신뢰도 확보
- **시대 적합성**: "당시대 플래그십"이라는 조건으로 기술 진화에 대응

#### 플래그십 Agent 정의

- 해당 시점에서 가장 발전된 능력을 갖춘 AI Agent
- 서로 다른 조직/모델 계열에서 2종 이상

플래그십 Agent의 “명단”은 고정하지 않으며, 선정/갱신 기록은 `02_AAOS-Immune_system/META_AUDIT_LOG.md`에 남긴다.

#### 합의 절차

```
DNA 변경 제안
     │
     ▼
META_AUDIT_LOG.md에 기록
     │
     ▼
플래그십 Agent A 독립 검토
(Canon 정합성, 부작용 분석)
     │
     ▼
플래그십 Agent B 독립 검토
(교차 검증)
     │
     ▼
합의 결과 기록
├─ 양측 승인 → Canonical, 버전 증가
└─ 불일치 → 인간 관리자 중재
     │
     ▼
인간 관리자 최종 승인
```

#### 조항 1) Immune System DNA 업데이트 승인 요건

**면역체계의 DNA(`02_AAOS-Immune_system/DNA.md`)는 아래 요건을 모두 만족할 때만 업데이트 가능하다.**

1. **플래그십 에이전트 2종 이상 동의** (서로 다른 조직/모델 계열)
2. **Canon Guardian(인간)의 최종 승인**
3. 위 1~2의 근거/증빙을 `02_AAOS-Immune_system/META_AUDIT_LOG.md`에 기록 (버전 변경 포함)

증빙 형식(권장): `02_AAOS-Immune_system/AAOS_DNA_DOCTRINE_RULE.md`의 `multi-agent-consensus` 기록 스키마를 사용한다.

> Canon §4(자기보존)의 “상시 외부 관리” 원칙과의 긴장을 줄이기 위해, 인간 승인 요건은 **운영의 상시 개입**이 아니라 **정식 DNA 승격/버전 업데이트의 서명(정통성 기록)** 으로 취급한다.
> 인간 승인이 없으면 변경안은 `DNA_BLUEPRINT.md` 상태로만 존재할 수 있으며, 정식 DNA로 승격될 수 없다.

#### 예외 상황

- **긴급 보안 패치**: 아래 조건 중 1개 이상이면 단일 Agent + 인간 승인으로 진행 가능 (사후 합의 필수, 합의 실패 시 롤백 및 Non-Canonical 처리)
  - CVSS v3.1 Base Score `>= 7.0`
  - 악용 징후가 관측됨(재현 로그/PoC/침해 증거)
  - 대규모 데이터 유출/권한 상승/원격 실행 위험이 명백
- **형식적 수정**: 오타/포맷팅 등 의미 변경 없는 수정은 합의 불필요
- **Agent 불가용**: 인간 관리자 2인 이상 승인으로 대체

### 1.3. AAOS Swarm Inquisitor – SKILL

`02_AAOS-Immune_system/SWARM_INQUISITOR_SKILL/`

AAOS 내부에서 정통성·권한·Blueprint 적합성을 심판하는 Skill 집합이다.

#### 포함 Skill

**permission-judgment**

Agent Preflight Checklist:
1. 지금 요청된 행동은 AAOS Canon을 위반하지 않는가?
2. 해당 행동은 META Doctrine에 의해 허용되는가?
3. 필요한 권한이 명시되어 있는가?
4. 불확실한 경우 Inquisitor를 호출했는가?

검증 항목:
- Tool / API 접근 권한 검증
- Repository 생성 권한 검증
- 장기 저장 요청 적합성 검증

**blueprint-judgment**

Agent Preflight Checklist:
1. 생성하려는 구조는 DNA Blueprint에 정의되어 있는가?
2. 종료 조건(Natural Dissolution)이 명시되어 있는가?
3. 자원 상한(Resource Budget)이 선언되어 있는가?
4. META Doctrine 및 Canon과 충돌하지 않는가?

검증 항목:
- DNA Blueprint 존재 여부 검증
- Natural Dissolution 명시성 검증 (**빈 값 불허**)
- 자원 상한 타당성 검증
- META Doctrine 정합성 검증

검증 실패 시 구조 생성·확장·실행이 차단된다.

---

### 1.4. Auto-Enforcement 도구 [신규 v0.2.0]

| 스크립트 | 용도 |
|----------|------|
| `yaml_validator.py` | 실제 YAML 파싱, 빈 값 검증 |
| `auto_inquisitor.py` | Git pre-commit hook, Agent wrapper, 자동 스캔 |
| `dissolution_monitor.py` | 자원 상한 감시, Natural Dissolution 실행 |
| `audit.py` | 해시 체인 무결성 검증 |

---

## 2. AAOS 군체(Swarm)

`04_AAOS-Swarm/`

AAOS 상에서 실제 Agent 협업 구조와 실행 환경이 발생하는 계층이다.
모든 군체(Swarm) 구조는 상위 Immune System과 Inquisitor의 감시를 받는다.

---

### 조항 2) 군체(Swarm) DNA 업데이트 승인 요건

**군체(Swarm)의 DNA(`04_AAOS-Swarm/**/DNA.md`)는 면역체계의 심판자(Inquisitor: `02_AAOS-Immune_system/SWARM_INQUISITOR_SKILL/`)에게 승인 요청을 제출하고, 승인(심판 결과)이 떨어졌을 때만 업데이트 가능하다.**

- 승인 요청은 `02_AAOS-Immune_system/SWARM_INQUISITOR_SKILL/`의 `blueprint-judgment` 또는 `permission-judgment` 절차로 수행한다.
- 승인/거부 결과 및 근거는 `02_AAOS-Immune_system/AUDIT_LOG.md`(해시 체인)에 기록한다.
- 거부/보류 시 기본 프로토콜:
  - `DNA.md`는 변경 전 상태를 유지한다
  - 변경안은 `DNA_BLUEPRINT.md`로 격리한다
  - `time_bound.expires` 내에 재심이 없으면 변경안은 자연소멸 절차로 정리한다

추가 규칙(상위기관):
- `04_AAOS-Swarm/DNA.md`(루트 컨테이너) 변경은 “Upper-Institution Change Gate”를 추가로 적용한다.

### 2.1. AAOS-COF

(Context Orchestrated Filesystem)

AAOS_SWARM/AAOS_COF/
파일 기반 Context 작업공간을 표준화하는 군체(Swarm) 구조이다.

#### 2.1.1-0. COF DNA Blueprint - pre-RULE
AAOS_SWARM/AAOS_COF/DNA_BLUEPRINT.md

COF 구조의
생성 조건, 성장 규칙, 종료 조건, 자원 상한, Natural Dissolution 절차를 정의한다.

#### 2.1.1-1. COF DNA - RULE
AAOS_SWARM/AAOS_COF/DNA.md

COF 내부 실제 노드 구조, Rule Genome, Skill Genome, Lifecycle Genome을 기술한다.

---

### 2.2. AAOS-COO

(Context Orchestrated Ontology)

AAOS_SWARM/AAOS_COO/
온톨로지 기반 Context·Knowledge Graph 구조를 표준화하는 군체(Swarm) 계층이다.

#### 2.2.1-0. COO DNA Blueprint - pre-RULE
AAOS_SWARM/AAOS_COO/DNA_BLUEPRINT.md

COO 구조의
개념 스키마 생성, 관계 확장 규칙, 메모리 보존 정책, 자연소멸 조건을 정의한다.

#### 2.2.1-1. COO DNA - RULE
AAOS_SWARM/AAOS_COO/DNA.md

COO 내부
Ontology Schema, Semantic Index, Context Query Rule, Lifecycle Genome을 기술한다.

---

## 3. Deliberation Chamber

`03_AAOS-Deliberation_Chamber/`

Deliberation Chamber는 Multi-Agent 합의의 논점/근거/증빙을 구조화하는 기관이다.
집행/차단 권한은 없으며, Immune System/Inquisitor의 판정 입력을 정리하고 Record Archive로 증빙을 이관한다.

참조:
- `03_AAOS-Deliberation_Chamber/DNA_BLUEPRINT.md`

---

## 4. Record Archive System

`01_AAOS-Record_Archive/`

AAOS에서 감사/합의/승인/해체 기록을 장기 보존하는 아카이빙 기관이다.

- Immune System이 “심판/집행”이라면, Record Archive는 그 결과의 “증빙/계보”를 보존한다.
- Record Archive는 원칙적으로 Append-only이며, 충돌/불명확/권한 경계 감지 시 Immune System으로 귀속한다(homing_instinct).

참조:
- `01_AAOS-Record_Archive/DNA_BLUEPRINT.md`

---

## 5. 전체 계층 요약 트리

본 META Doctrine(METADoctrine.md) 문서는 Canon에 선언된 원리를
Doctrine 형태로 집행 가능하게 정의하는 교리 규칙이다.
모든 하위 Blueprint와 군체(Swarm) 구조는 본 규칙을 참조하여 작성되어야 한다.

---

## META Doctrine Version Note

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| v0.0.1 | 2025-01-22 | 최초 META Doctrine 성문화(당시 파일명: RULE.md) |
| v0.1.0 | 2025-01-22 | Auto-Enforcement, Audit Integrity, Multi-Agent Consensus 반영. Immune System v0.3.0 연동. |
| v0.1.1 | 2026-01-22 | Immune System DNA 업데이트 승인 요건(플래그십 2종 + Canon Guardian) 및 Swarm DNA 업데이트 승인 요건(Inquisitor 승인) 조항 추가. Immune Doctrine v0.3.1 연동. |
| v0.1.2 | 2026-01-22 | 다른 Agent Critic 반영: (1) 플래그십 선정은 고정 명단 금지, (2) 동의 증빙 스키마 참조, (3) 인간 승인=정식 승격 서명으로 한정, (4) Swarm 거부/보류 시 롤백/격리/만료 프로토콜 추가. |
| v0.1.3 | 2026-01-22 | Record Archive System(기록 보존 기관) 추가: `01_AAOS-Record_Archive/`를 META 계층에 편입하고 상속 규범을 명시. |
| v0.1.4 | 2026-01-22 | 최상위 기관 순서 정정(Canon → Record Archive → Immune+Deliberation → Swarms), 디렉토리 리네이밍(01/02/03/04) 및 `03_AAOS-Deliberation_Chamber/` 추가. |
| v0.1.5 | 2026-01-23 | “상위기관(군체(Swarm) 이상) + META” 변경 게이트를 명문화하고, Canon의 군체/군락 귀속 원칙과 정렬. |
| v0.1.6 | 2026-01-23 | 용어 정렬: Swarm=군체, Group=군락. Canon/Identity/게이트 문구를 정합화. |
