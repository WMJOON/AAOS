---
meta_doctrine: AAOS_META_DOCTRINE
version: v0.1.23
type: doctrine-rule
status: canonical
description: >
  AAOS Canon에 선언된 원리를 현실 시스템에서 집행 가능한 규칙으로 번역하는
  META Doctrine(METADoctrine.md; formerly RULE.md). Auto-Enforcement, Audit Integrity, Multi-Agent Consensus를 포함한다.
---

# AAOS DNA Lineage Structure
Agentic AI OS – Meta, Doctrine, Swarm(군체), DNA Lineage (Draft → Canonical)

## AAOS Canon Declaration

`04_Agentic_AI_OS/README.md` 는 AAOS의 Canonical Text(성문)이다.
모든 META Doctrine(METADoctrine.md), Skill, 군체(Swarm) 구조는 본 Canon에 종속되며,
Canon을 위반한 구조는 Non-Canonical로 분류된다.

### 관리 권한 경계

- 사람은 **`README.md`, `METADoctrine.md`**까지만 직접 수정/승인한다.
- 그 하위의 `00_METADoctrine`, `01_Nucleus`, `02_Swarm`, `03_Manifestation` 산출물은
  해당 기관/스킬의 Agent 운영체계에 따라 구성·진화한다.

### 적용 원칙(모델/에이전트 무관)

- 본 규범은 운영 에이전트의 모델 출처와 무관하게 동일하게 적용된다.
- `Claude`, `Gemini`, `Grok`를 포함한 모든 에이전트 계열이 동일한 게이트 규칙으로 판단한다.
- 동일 단계의 핵심 판단(특히 Plan Critique/Decomposition Critique)은 동일 모델군 단독 종결이 아니라 서로 다른 `model_family`의 교차 검증으로 분리 수행한다.
- 상위 실행 레이어(`01_Nucleus`)에서는 `01_Nucleus/AGENTS.md`를 준수하여 provider 무관 규범을 강제한다.

### Human Controllability and Entropy Budget (최상위)

- 최우선 규범 참조: `https://github.com/WMJOON/semantic-atlas-hypothesis`
- 사람의 통제가능성은 정보 엔트로피가 과도하게 증가하지 않을 때만 유지된다.
- 따라서 META Doctrine은 다음을 강제한다.
  1. 통제가능 영역 최소화: 강제 규칙은 핵심 정본 문서와 `SKILL.md` frontmatter로 한정한다.
  2. 메타데이터 최소화: 프론트매터는 최소 필수 키만 유지한다.
  3. 엔트로피 예산 위반 금지: 키 수/규칙 수가 통제 임계치를 초과하면 Non-Canonical로 판정한다.
  4. 레거시 제도 잔존 금지: 폐지된 제도(`DNA_BLUEPRINT.md` 중심 운영)는 활성 규범에서 재도입하지 않는다.

## Institutional Order (정정된 최상위 기관 순서)

1. Canon (`04_Agentic_AI_OS/README.md`)
2. Record Archive (`04_Agentic_AI_OS/01_Nucleus/Record_Archive/`)
3. Immune System + Deliberation Chamber (`04_Agentic_AI_OS/01_Nucleus/Immune_system/`, `04_Agentic_AI_OS/01_Nucleus/Deliberation_Chamber/`)
4. Swarm(군체) 계층 (`04_Agentic_AI_OS/02_Swarm/`)
5. Manifestation(현현/접속) 계층 (`04_Agentic_AI_OS/03_Manifestation/`)

### Centralized Evidence Repository Principle

- `01_Nucleus`에서 발생하는 **영구 아카이브·기록은 모두 `01_Nucleus/Record_Archive/`에서 최종 정착**되어야 한다.
- Deliberation Chamber와 Immune System은 판단/합의 산출물까지를 운영할 수 있으나, 증거는 `Record_Archive`의 `_archive/**`로만 봉인하여 보존해야 한다.
- `01_Nucleus` 내 임시 작업 공간(예: plans, tasks, 스크립트 출력 디렉토리)은 승인 전까지의 작업 산출물이며, 승인 완료 후에는 `_archive` 정본으로 치환되어야 한다.

### Upper-Institution Change Gate (군체(Swarm) 이상 + META)

다음 대상은 “상위기관(군체(Swarm) 이상)”으로 취급하며, 변경은 더 강한 정통성 게이트를 통과해야 한다.

- `04_Agentic_AI_OS/00_METADoctrine/METADoctrine.md` (META Doctrine; formerly RULE.md)
  - `01_Nucleus/Record_Archive/` (기관 DNA)
  - `01_Nucleus/Immune_system/` (기관 DNA)
  - `01_Nucleus/Deliberation_Chamber/` (기관 DNA)
  - `02_Swarm/` 루트 컨테이너 DNA (`02_Swarm/DNA.md`)
  - `03_Manifestation/` 루트 컨테이너 DNA (`03_Manifestation/DNA.md`)

상위기관 변경은 아래를 모두 만족할 때만 “정식(승격/공표)”로 인정된다.

1. **Deliberation Chamber 산출물**: `multi-agent-consensus`(플래그십 Agent 2종 이상 verdict/rationale 포함)
2. **Record Archive 증빙 고정**: 합의/근거/스냅샷/해시/인덱스가 재현 가능하게 보존됨. `_archive/` 내 증빙 패키지는 봉인 후 원문·메타데이터를 삭제/변경/축약 없이 보존 불변 원칙을 유지해야 한다.
3. **Open Agent Council 다양성 요건**: 상위 변경의 `Deliberation Packet`에 서로 다른 모델 계열 최소 2종 이상(권장 4종, 예: Codex, Claude, Gemini, Grok) 모델 참여 증빙 포함
4. **META_AUDIT_LOG 기록**: 변경 사유/버전 변경/증빙 참조를 `01_Nucleus/Immune_system/META_AUDIT_LOG.md`에 기록
5. **Canon Guardian 서명(정통성 기록)**: 상시 운영 개입이 아니라 “정식 승격 서명자”로서의 승인
6. **Inquisitor verdict + AUDIT_LOG 기록**: 승인/거부/보류 결과와 근거가 `01_Nucleus/Immune_system/AUDIT_LOG.md`(해시 체인)에 고정됨

서명이 없는 경우, 변경안은 `DNA.md`의 draft 상태로만 존재할 수 있으며 정식 텍스트로 승격될 수 없다.

## Canon-Archive Feedback Loop (운영 정합성 루프)

상위 제도와 Swarm 진화는 다음 루프를 반드시 준수한다.

### 1) Proposal → Evidence → Judgment → Signature → Feedback

- **Proposal**: Swarm 또는 운영자가 초안/변경 제안 산출물을 작성한다.
- **Evidence**: 초안은 합의 산출물, 변경 사유, 영향 평가, 해시 가능한 증빙 포인트를 갖춰야 한다.
- **Judgment**: Inquisitor가 Canon/META/기관 규약을 판정하고 `AUDIT_LOG.md`에 고정한다.
- **Signature**: 상위기관의 `Canon Guardian` 서명과 META_AUDIT 로그가 확인될 때만 정식 승격한다.
- **Feedback**: 승인/거부/보류 결과를 다음 설계와 행동으로 환류한다.

### 2) 기록 중심 상호보완 규칙

- `Record Archive`는 모든 상위 변경의 근거를 `MANIFEST` 기반 패키지로 저장한다.
- `Inquisitor verdict + AUDIT_LOG`는 변경의 판정 정당성 근거로서 우선한다.
- 승인 실패 시 변경은 `DNA.md` draft 상태 또는 `00_METADoctrine` 단계로 되돌아가 재설계 루프로 들어간다.
- Canonical 텍스트로 승격된 규범은 `Record Archive` + `AUDIT_LOG` + `META_AUDIT_LOG`의 교차참조를 가져야 한다.
- 상위변경 근거의 최종 보존 경로는 `01_Nucleus/Record_Archive/_archive/`로 강제하며, 다른 경로의 장기 보존 로그는 비규범으로 간주한다.

### 3) 정체성 보전 요구

- 위 루프가 중단되거나 증빙이 누락되면 해당 변경은 Non-Canonical 대기로 간주한다.
- 상위규범 변경은 항상 `time_bound`와 Natural Dissolution 조건을 동반한다.
- 상호보완 루프는 정기적으로 `cross_ref_validator`와 Dissolution 모니터로 검증한다.

이 루프는 Canon이 제도화의 근간을 지키고, Swarm가 스스로 성장·실험해도 생태계가 흔들리지 않도록 유지한다.

---
## 0. AAOS META Doctrine (Derived from AAOS Canon)

`04_Agentic_AI_OS/00_METADoctrine/METADoctrine.md`  ← META Doctrine (Interpretation of the Canon)
**META Doctrine Version: v0.1.23**

> Canon을 현실 시스템에서 집행 가능하도록 번역하는 최상위 교리 규칙

AAOS META Doctrine은 AAOS Canon에 선언된 원리를
현실 구조·행동·자원 규칙으로 변환하여 집행 가능하게 만드는 상위 교리 계층이다.

- Canon이 "무엇이 AAOS인가"를 정의한다면,
- META Doctrine은 "그 정의를 어떻게 시스템에서 강제할 것인가"를 규정한다.

모든 하위 Doctrine, Skill, 구조 산출물은
상위 Canon과 본 META Doctrine을 위반할 수 없다.

### 역할

- AAOS 정통성(Canonicality) 판정 기준 제공
- 변경 제안 산출물(`DNA.md` draft) 개념 및 형식 규정
- Natural Dissolution 원칙 선언
- Immune System / Inquisitor 호출 근거 제공
- **Auto-Enforcement 메커니즘 정의** [v0.1.0]
- **Audit Log 무결성 보장** [v0.1.0]
- **Multi-Agent Consensus 요건 정의** [v0.1.0]

### Draft/Planning Workspace Protocol [v0.1.7]

AAOS는 Canonical 텍스트를 직접 흔들지 않고도 설계/실험을 진행하기 위해, “Draft/Planning 레이어”를 허용한다.  
단, Draft는 정통 텍스트가 아니며 Canonical 변경의 “입력 후보”로만 취급된다.

Draft는 **집행 권한을 갖지 않는다**. Draft의 내용은 승인/승격 전까지 어떠한 Rule/DNA/Doctrine의 근거로 강제되지 않으며, 집행/차단/승인 판단은 Immune System/Inquisitor 및 상위 변경 게이트를 따른다.

### 블루프린트 제도 폐지 원칙

- Blueprint는 과거 사람의 2차 점검을 위한 절차였다.
- 현재는 `agent-audit-log` 기반의 `Record Archive` 추적 + `multi-agent-consensus` + Inquisitor 비동기 판정이 병렬로 수행되어, 즉시 동기식 `Blueprint` 단계가 병목이 된다.
- 따라서 본체 제도는 “Blueprint”를 독립적 통로로 두지 않고, **`DNA.md` draft 최소 스키마 + 비동기 감사/합의/증빙 루프**로 통합한다.
- `blueprint-judgment`는 여전히 모듈명으로 유지되되, 제도적 의미는 “변경 제안 산출물 검증 심판”로만 해석한다.

#### Draft Types

- **Planning Notes**: 의도/경계/대안/질문/리스크를 다루는 초안 문서
- **DNA 변경 제안 산출물 (`DNA_BLUEPRINT.md`)**: 구조의 생성/성장/해체 규칙을 포함하는 승격 대기 산출물

#### Normative Reference Rule

- Canonical 문서는 Draft/Planning 문서를 **규범 참조(normative reference)** 로 삼지 않는다.
- Draft/Planning 문서는 Canonical 문서를 링크로 고정하여 기준점을 명확히 한다.
- Canonical 문서에서 Draft를 링크해야 한다면, **informative reference(참고 링크)** 로만 허용하며 “비정통/비집행”임을 명시한다.

#### Change Packet (Minimum)

Canonical 변경(특히 상위기관/Swarm DNA)은 최소 다음을 포함하는 Change Packet으로 제출한다.

1. 변경 제안 본문(Draft/제안 산출물)
2. 승인 요청 패킷(`permission-request` 또는 `blueprint-judgment`(변경 제안 판정))
3. 필요 시 `multi-agent-consensus` 산출물(Deliberation)
4. Record Archive 증빙(스냅샷/해시/인덱스)
5. Inquisitor verdict 및 `AUDIT_LOG.md` 기록(해시 체인; 승인/거부/보류 결과와 근거)
6. META 수준 변경일 경우 `META_AUDIT_LOG.md` 기록(버전/사유/증빙 링크)
7. `time_bound.expires` 및 Natural Dissolution 절차

#### Change Packet (Where / Templates)

- Draft change packets (planning): `00_METADoctrine/_archive/change_packets/`
- Deliberation packet template (Record Archive): `01_Nucleus/Record_Archive/templates/DELIBERATION_PACKET_TEMPLATE.md`
- Immune templates:
  - `01_Nucleus/Immune_system/templates/DNA-BLUEPRINT-TEMPLATE.md`
  - `01_Nucleus/Immune_system/templates/PERMISSION-REQUEST-TEMPLATE.md`

#### Draft Natural Dissolution

Draft는 무기한 유지되지 않는다. 만료 시 요약을 남기고(필요 시 Record Archive로 이관), 잔여 초안은 자연소멸 절차로 정리한다.

기본 만료(권장): Planning Notes/제안 산출물 초안은 생성 시점 기준 **30일**을 기본 TTL로 두며, `time_bound.expires`로 연장할 수 있다.

TTL 유연성(추가 규칙):
- `base_ttl`: 기본 TTL (권장 30d)
- `extension_limit`: 최대 연장 횟수 (권장 2회)
- `extension_requires`: `inquisitor-approval`
- 만료 7일 전 연장 요청이 없으면 자동 해체 큐에 등록한다.

### 계층 구조

```
04_Agentic_AI_OS/
├── 00_METADoctrine/             # Draft/Planning workspace (non-canonical; 실행/집행 권한 없음)
├── README.md                      # AAOS Canon (성문)
├── METADoctrine.md               # META Doctrine (본 문서; formerly RULE.md)
├── 01_Nucleus/                   # 기관 레이어 (Validation Engine; Non-Execution)
│   ├── Record_Archive/            # 기록 보존 기관 (Archive)
│   ├── Immune_system/             # 면역 체계 (심판/집행)
│   └── Deliberation_Chamber/      # 숙의/합의 기관 (심판 입력 정리)
├── 02_Swarm/                      # 군체(Swarm) 계층 (사고/행동양식; Non-Execution)
└── 03_Manifestation/         # 현현/접속 계층 (실행 바인딩; Non-Cognition)
```

---

## 1. AAOS Immune System

`01_Nucleus/Immune_system/`

AAOS 구조 전체의 자기보존·정화·안정성 계층이다.
과증식, 컨텍스트 오염, 비정상 구조를 감지하고 정리한다.

### 1.1. AAOS DNA Doctrine – RULE (v0.3.1)

`01_Nucleus/Immune_system/AAOS_DNA_DOCTRINE_RULE.md`

AAOS에서 모든 DNA와 군체(Swarm) 구조가 반드시 따라야 하는 교리 규칙을 정의한다.

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

#### Open Agent Council (다중 모델 토론 규약)

- Open Agent Council는 서로 다른 모델 계열을 의무 참여시켜 한 모델의 편향이 제도에 고착되는 것을 막는다.
- 기존 기준군 외에도 향후 검증된 신규 모델 계열을 편입해, 정합성 점수 하락 없이 다양성을 확장할 수 있다.
- 절차는 다음 단계로 수행한다.
  - **Claim**: 변경 제안의 주장과 증빙을 제시한다.
  - **Counterclaim**: 다른 모델 계열이 반론, 리스크, 반례, 실패 가능성을 제시한다.
  - **Synthesis**: 합의점·미해결점·검증할 가설을 정리해 Deliberation Packet에 반영한다.
- 토론 패킷에는 `model_id`, `model_family`, `org`, `verdict`, `rationale`를 필수로 남긴다.
- 상위 규범/기관 변경은 최소 2개 모델 계열, 가용 시 4개 계열(Codex/Claude/Gemini/Grok 등)에서 Counterclaim이 존재해야 한다.
- `model_family` 중복은 허용하지 않고, 동일 family라도 기능적 역할과 모델 출처가 다른 경우 보완적으로 기록한다.

#### 플래그십 Agent 정의

- 해당 시점에서 가장 발전된 능력을 갖춘 AI Agent
- 서로 다른 조직/모델 계열에서 2종 이상
- Open Agent Council의 `multi_agent_consensus`는 모델 계열 중복을 허용하지 않는다.

플래그십 Agent의 “명단”은 고정하지 않으며, 선정/갱신 기록은 `01_Nucleus/Immune_system/META_AUDIT_LOG.md`에 남긴다.

### 1.2.1. 플래그십 Agent 선정 프로토콜 (정량)

선정 기준(권장 가중치):

| 기준 | 가중치 | 측정 방식 |
|------|--------|-----------|
| 벤치마크 성능 | 30% | 공개 벤치마크 상위 5% |
| 추론 능력 | 25% | 복합 추론 태스크 성공률 |
| 안전성 | 25% | Safety alignment 테스트 통과율 |
| 운영 안정성 | 20% | 6개월 이상 운영 이력 |

절차:
1. 후보 식별(분기별)
2. 다양성 검증(서로 다른 조직/계열 2종 이상)
3. 점수화 및 선정
4. `META_AUDIT_LOG.md` 기록
5. 분기별 재평가(탈락 시 교체)

### 1.2.2. 긴급 패치 롤백 프로토콜

롤백 트리거:
1. 72시간 내 사후 합의 실패
2. 부작용(보안 취약점/기능 장애) 발견
3. Inquisitor의 Canon 위반 판정

롤백 절차:
1. 변경 전 버전 자동 복원
2. `AUDIT_LOG.md`에 롤백 사유 기록
3. 영향 Swarm 공지
4. 대상 변경안에 `Non-Canonical` 태그 부착

### 1.2.3. Agent Conflict Resolution Protocol

1단계(자동 중재):
- 2개 verdict 차이 분석
- 핵심 논점 동일 시 병합
- 상이 시 제3 Agent 투표(2:1 다수결)

2단계(숙의):
- `01_Nucleus/Deliberation_Chamber/`에 논점 문서 제출
- 72시간 내 추가 논증

3단계(인간 중재):
- 120시간 내 합의 실패 시 Canon Guardian 최종 결정
- 결과는 감사 로그에 고정

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

**면역체계의 DNA(`01_Nucleus/Immune_system/DNA.md`)는 아래 요건을 모두 만족할 때만 업데이트 가능하다.**

1. **플래그십 에이전트 2종 이상 동의** (서로 다른 조직/모델 계열)
2. **Canon Guardian(인간)의 최종 승인**
3. 위 1~2의 근거/증빙을 `01_Nucleus/Immune_system/META_AUDIT_LOG.md`에 기록 (버전 변경 포함)

증빙 형식(권장): `01_Nucleus/Immune_system/AAOS_DNA_DOCTRINE_RULE.md`의 `multi-agent-consensus` 기록 스키마를 사용한다.

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

`01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/`

AAOS 내부에서 정통성·권한·구조 변경 제안 적합성을 심판하는 Skill 집합이다.

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

**blueprint-judgment (변경 제안 판정)**

Agent Preflight Checklist:
1. 생성하려는 구조는 관련 변경 제안 산출물에 정의되어 있는가?
2. 종료 조건(Natural Dissolution)이 명시되어 있는가?
3. 자원 상한(Resource Budget)이 선언되어 있는가?
4. META Doctrine 및 Canon과 충돌하지 않는가?

검증 항목:
- 변경 제안 산출물(`DNA_BLUEPRINT.md`) 존재 여부 검증
- Natural Dissolution 명시성 검증 (**빈 값 불허**)
- 자원 상한 타당성 검증
- META Doctrine 정합성 검증

검증 실패 시 구조 생성·확장·실행이 차단된다.

---

### 1.4. Auto-Enforcement 도구 [신규 v0.2.0]

다음 도구는 AAOS Immune System의 Inquisitor Core에 포함되며, 실제 파일 위치는 아래와 같다.

| 도구 | 파일 | 용도 |
|------|------|------|
| `yaml_validator.py` | `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/yaml_validator.py` | YAML 파싱/스키마 검증(빈 값 불허 등) |
| `auto_inquisitor.py` | `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py` | Git hook 생성/디렉토리 스캔/프리플라이트 |
| `dissolution_monitor.py` | `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/dissolution_monitor.py` | TTL/자원 상한 감시 + Natural Dissolution |
| `audit.py` | `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/audit.py` | 해시 체인 무결성 검증/append |
| `cross_ref_validator.py` | `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/cross_ref_validator.py` | Canon↔Doctrine↔DNA 참조 무결성 검증 |

주요 CLI(현행):
- `python3 01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py --gen-hook 04_Agentic_AI_OS`
- `python3 01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py --scan 04_Agentic_AI_OS --format md`
- `python3 01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py --preflight 04_Agentic_AI_OS`
- `python3 01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/audit.py verify 01_Nucleus/Immune_system/AUDIT_LOG.md`
- `python3 01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/cross_ref_validator.py --root 04_Agentic_AI_OS`

Judgability Gate(운영 점검 항목; 권장):
- `termination_condition_present: bool`
- `over_explanation_risk: low|medium|high`
- `escalation_path_defined: bool`

#### 1.4.1. 링크/참조 Hygiene 규약 (운영)

운영 문서의 참조 무결성은 `cross_ref_validator.py`로 선제 점검한다.

- 내부 참조는 실제 존재하는 파일 경로를 우선 사용한다.
- 실행 경로(예: Skill Script/Template)는 예시 경로와 혼재하지 않는다.
- 샘플 경로는 기본적으로 링크가 아닌 코드 스팬(`\`path\``)으로 표기해 링크 검사 대상에서 제외한다.
- 변경 건 제출 전 `METADoctrine.md`, `01_Nucleus/Immune_system/`, `01_Nucleus/Record_Archive/`, `02_Swarm/` 핵심 규범 문서를 대상으로 검증을 완료한다.

```bash
python3 01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/cross_ref_validator.py \
  --root 04_Agentic_AI_OS \
  --check-inline-paths
```

--- 

## 2. AAOS 군체(Swarm)

`02_Swarm/`

AAOS 상에서 실제 Agent 협업 구조와 실행 환경이 발생하는 계층이다.
모든 군체(Swarm) 구조는 상위 Immune System과 Inquisitor의 감시를 받는다.

---

### 조항 2-0) Swarm Skill Frontmatter Compliance Gate

`02_Swarm/*/skills/*/SKILL.md`는 아래 frontmatter 표준 필드를 필수로 가져야 한다.

- `context_id`
- `description`
- `trigger`
- `role`
- `state`
- `scope`
- `lifetime`
- `created`

강제 규칙:

1. `SKILL_REGISTRY.md` 또는 `SWARM_SKILL_REGISTRY.md` 생성 시 `missing context_id`, `missing description` 경고가 1건 이상이면 해당 Swarm Skill 변경은 Non-Canonical 대기 상태로 분류한다.
2. 표준 위반 상태에서는 상위 변경 게이트(승격/공표) 입력으로 사용할 수 없다.
3. 표준 복구 후 재검증(`warnings=0`, `errors=0`) 결과를 기준으로만 후속 승인 절차를 진행한다.

권장 검증 명령:

```bash
python3 02_Swarm/context-orchestrated-filesystem/skills/04.cof-swarm-skill-manager/scripts/sync_swarms_skill_manager.py \
  --swarm-root 02_Swarm \
  --skip-write
```

---

### 조항 2) 군체(Swarm) DNA 업데이트 승인 요건

**군체(Swarm)의 DNA(`02_Swarm/**/DNA.md`)는 면역체계의 심판자(Inquisitor: `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/`)에게 승인 요청을 제출하고, 승인(심판 결과)이 떨어졌을 때만 업데이트 가능하다.**

- 승인 요청은 `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/`의 `blueprint-judgment`(변경 제안 판정) 또는 `permission-judgment` 절차로 수행한다.
- 승인/거부 결과 및 근거는 `01_Nucleus/Immune_system/AUDIT_LOG.md`(해시 체인)에 기록한다.
- 거부/보류 시 기본 프로토콜:
  - `DNA.md`는 변경 전 상태를 유지한다
  - 변경안은 제안 산출물(`DNA_BLUEPRINT.md`)로 격리한다
  - `time_bound.expires` 내에 재심이 없으면 변경안은 자연소멸 절차로 정리한다

추가 규칙(상위기관):
- `02_Swarm/DNA_BLUEPRINT.md` 변경은 “Upper-Institution Change Gate”를 추가로 적용한다.
  (향후 Swarm 루트 정식 DNA가 승격되면 동일 게이트를 적용한다.)

### 2.1. AAOS-COF

(Context Orchestrated Filesystem)

파일 기반 Context 작업공간을 표준화하는 군체(Swarm) 구조이다.

#### 2.1.1-0. COF 컨테이너

- 컨테이너(버전 보관): `02_Swarm/context-orchestrated-filesystem/`
- 컨테이너 제안 산출물: `02_Swarm/context-orchestrated-filesystem/DNA_BLUEPRINT.md`

COF 구조의
생성 조건, 성장 규칙, 종료 조건, 자원 상한, Natural Dissolution 절차를 정의한다.

#### 2.1.1-1. COF 최신 정식 DNA (예시)

- `02_Swarm/context-orchestrated-filesystem/DNA.md`

COF 내부 실제 노드 구조, Rule Genome, Skill Genome, Lifecycle Genome을 기술한다.

---

### 2.2. AAOS-COO

(Context Orchestrated Ontology)

온톨로지 기반 Context·Knowledge Graph 구조를 표준화하는 군체(Swarm) 계층이다.

#### 2.2.1-0. COO 제안 산출물 - pre-RULE
- 스캐폴드(draft): `02_Swarm/context-orchestrated-ontology/DNA_BLUEPRINT.md`

COO 구조의
개념 스키마 생성, 관계 확장 규칙, 메모리 보존 정책, 자연소멸 조건을 정의한다.

#### 2.2.1-1. COO 정식 DNA

- `DNA.md`는 아직 미존재(승격 전).
- 승격 시 Inquisitor 승인 + Audit Log 고정 후 `DNA.md`로 승격한다.

---

### 2.3. cortex-agora (Swarm Behavior Observer / Proposal Swarm)

`02_Swarm/cortex-agora/`

cortex-agora는 Swarm들의 행동을 관찰하고(Behavior Trace),
반복되는 흐름을 “개선 제안”으로 변환한다.

#### 책임 경계

- Record_Archive는 Nucleus의 자산이며 “사실/증빙”을 보존한다(append-only).
- cortex-agora는 Record_Archive를 **직접 읽지 않는다**.
- cortex-agora의 입력은 “기록”이 아니라 “행동”이다(Behavior Feed).
- cortex-agora의 출력은 “집행”이 아니라 “관찰 결과 + 제안”이다.

#### 금지

- 실행/자동반영/룰수정/에이전트 호출 금지

---

### 2.4. Swarm Observability Standard (Behavior Feed) — 권장/필수

Swarm의 “행동(Behavior Trace)”은 Record_Archive(증빙)가 아니라,
cortex-agora 관찰 입력(Behavior Feed)으로 남긴다.

#### 권장(Recommended)

- Swarm은 자신의 스코프 하위에 Behavior Feed를 둔다.
  - 권장 경로: `<swarm_root>/behavior/BEHAVIOR_FEED.jsonl`
- Swarm DNA frontmatter에 `observability.behavior_feed`를 기록한다.

#### 필수(Required)

아래 조건 중 하나라도 해당하는 Swarm은 Behavior Feed를 필수로 남긴다.

- Manifestation 트리거(외부 실행 바인딩)가 발생하는 경우
- Permission Request 또는 구조 생성/확장에 관여하는 경우
- `halt/escalate` 또는 Human Gate로 종료되는 흐름이 존재하는 경우

필수 최소 이벤트는 `02_Swarm/cortex-agora/DNA_BLUEPRINT.md`의 `Behavior Feed (Behavior Trace)` 스키마를 따른다.

---

## 3. Deliberation Chamber

`01_Nucleus/Deliberation_Chamber/`

Deliberation Chamber는 Multi-Agent 합의의 논점/근거/증빙을 구조화하는 기관이다.
집행/차단 권한은 없으며, Immune System/Inquisitor의 판정 입력을 정리하고 Record Archive로 증빙을 이관한다.
- 분해 체크리스트/티켓은 Deliberation Chamber가 직접 보유·관리한다.
- Deliberation에서 도출한 분석 패턴은 다음 주기의 개선안으로만 제안한다.

참조:
- `01_Nucleus/Deliberation_Chamber/DNA.md`

---

## 4. Record Archive System

`01_Nucleus/Record_Archive/`

AAOS에서 감사/합의/승인/해체 기록을 장기 보존하는 아카이빙 기관이다.

- Immune System이 “심판/집행”이라면, Record Archive는 그 결과의 “증빙/계보”를 보존한다.
- Record Archive는 원칙적으로 Append-only이며, 충돌/불명확/권한 경계 감지 시 Immune System으로 귀속한다(homing_instinct).
- `01_Nucleus/Record_Archive/_archive/`는 최종 증빙 저장소이므로, 보존된 증빙 패키지와 인덱스의 삭제·수정·축약은 원칙적으로 금지한다.
- 실행 결과/검증 로그는 실행 종료 시점에 Record Archive(`ARCHIVE_INDEX`, `HASH_LEDGER`)로 봉인한다.
- `Record Archive`는 `_archive` 보존 원칙 위반 시 해당 건을 **Non-Canonical**로 격리하고 Inquisitor 경보를 발동한다.

참조:
- `01_Nucleus/Record_Archive/DNA_BLUEPRINT.md`

### 4.1. Homing Instinct 발동 조건 (명확화)

아래 조건 중 하나라도 해당하면 Record Archive는 추가 작업을 중단하고 Immune System으로 귀속한다.

- **충돌**: 동일 리소스에 상반 verdict가 존재
- **불명확**: 48시간 내 자동 해석 불가 또는 Agent 3종 모두 상이한 해석
- **권한 경계 초과**: 요청 scope가 `permission_scope` 초과
- **무결성 손상**: 해시 체인 불일치
- **TTL 초과**: `time_bound.expires` 경과 후 미처리

---

## 5. Manifestation Layer (현현/접속 계층)

`03_Manifestation/`

Swarm의 사고/행동양식을 외부 시스템에 실행 가능하게 바인딩하는 계층이다.
Manifestation은 인지(Cognition) 권한 없이 순수 실행만 수행한다(Non-Cognition).

참조(현행 draft):
- `03_Manifestation/DNA_BLUEPRINT.md` (Execution Contract의 최소 형태)

### 5.1. Manifestation Binding Types

| 유형 | 설명 | 예시 |
|------|------|------|
| **Tool Binding** | 외부 도구/API 호출 인터페이스 | MCP Server, REST API |
| **Environment Binding** | 실행 환경 연결 | Docker, Shell, IDE |
| **Storage Binding** | 영속성 계층 연결 | DB, File System |
| **Communication Binding** | 외부 채널 연결 | Webhook, Message Queue |

### 5.2. Manifestation 최소 계약(권장 스키마)

```yaml
manifestation:
  binding_type: [tool|environment|storage|communication]
  target_system: string
  permission_scope:
    read: boolean
    write: boolean
    execute: boolean
  audit_trail: required
  fallback_behavior: [fail-safe|fail-open|escalate]
```

### 5.3. Manifestation 실행 격리 원칙 (강화)

- Manifestation은 Swarm/Immune의 결정을 해석·수정하지 않고 실행한다.
- 실행 예외/실패는 즉시 Immune System으로 보고한다.
- 좌표계(Local Chart)를 자체적으로 재선택하거나 목적을 재정의하지 않는다(Non-Cognition).

---

## 5A. Semantic Operations Doctrine (Working Hypothesis Adoption)

본 Doctrine은 `05_Semantic Atlas Hypothesis/README.md`의 핵심 가설을 AAOS 운영 규칙으로 수용한다.
이 수용은 완결 이론의 확정이 아니라 작업 가설(working hypothesis)의 규범적 적용으로 취급한다.

### 5A.1. Semantic 정의 (Operational)

Semantic은 정보량이 아니라 **판단 종료 조건(judgment termination condition)** 으로 정의한다.

- terminate-ready: 추가 설명 없이 현재 정보로 행동/결정 가능
- non-terminating: 설명은 증가하나 결정이 지연되는 상태

### 5A.2. Judgability 우선 원칙

모든 상위 산출물은 정확도/완전성 이전에 다음을 우선 점검한다.

1. 지금 결정 가능한가?
2. 추가 생성이 실제 의사결정 품질을 높이는가?
3. 지금 중단/전환하는 편이 더 안전한가?

### 5A.3. Semantic Entropy Guardrail

의미 엔트로피가 임계치를 초과했다고 판정되면 즉시 아래 절차를 적용한다.

1. 생성 중단 (`stop_generation`)
2. 국소 좌표계 재선택 (`re_chart`)
3. 인간/Guardian 확인 또는 종료 근거 기록 (`escalate_or_terminate`)

이 규칙은 Self-Limitation 및 Natural Dissolution과 동급의 운영 제약으로 취급한다.

### 5A.4. Local Chart 책임 분리

- Nucleus: 종료 기준/정통성 기준 제도화
- Swarm: 현재 태스크의 Local Chart 선택
- Manifestation: 선택된 좌표계를 실행 인터페이스로 바인딩(Non-Cognition)

### 5A.5. Agent 역할 재정의

Agent는 연산 지속 장치가 아니라, 중단·전환·위임·인간 개입 요청을 수행하는
`termination-aware executor`여야 한다.

---

## 5B. AAOS Health Metrics

핵심 지표(KPI):

| 지표 | 정상 범위 | 경고 임계값 |
|------|-----------|-------------|
| Consensus Latency | < 24h | > 72h |
| Dissolution Rate | > 90% | < 70% |
| Audit Chain Integrity | 100% | < 100% |
| Inquisitor Approval Rate | 60%~90% | < 40% or > 95% |
| TTL Compliance | > 95% | < 80% |
| Escalation Frequency | < 5%/월 | > 15%/월 |

자동 경보:
- 경고 임계값 초과 시 Immune System 보고
- 2회 연속 초과 시 Canon Guardian 알림

---

## 5C. META Doctrine Versioning Policy

버전 형식: `vMAJOR.MINOR.PATCH`

| 변경 유형 | 버전 증가 |
|-----------|-----------|
| Canon 정렬/상위 규범 구조 변경 | MAJOR |
| 새 교리/기관/프로토콜 추가 | MINOR |
| 세부 조정/명확화/버그 수정 | PATCH |

모든 버전 변경은 `META_AUDIT_LOG.md`에 근거와 함께 기록한다.

---

## 6. 전체 계층 요약 트리

본 META Doctrine(METADoctrine.md) 문서는 Canon에 선언된 원리를
Doctrine 형태로 집행 가능하게 정의하는 교리 규칙이다.
모든 하위 구조와 군체(Swarm) 문서는 본 규칙을 참조하여 작성되어야 한다.

---

## META Doctrine Version Note

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| v0.0.1 | 2025-01-22 | 최초 META Doctrine 성문화(당시 파일명: RULE.md) |
| v0.1.0 | 2025-01-22 | Auto-Enforcement, Audit Integrity, Multi-Agent Consensus 반영. Immune System v0.3.0 연동. |
| v0.1.1 | 2026-01-22 | Immune System DNA 업데이트 승인 요건(플래그십 2종 + Canon Guardian) 및 Swarm DNA 업데이트 승인 요건(Inquisitor 승인) 조항 추가. Immune Doctrine v0.3.1 연동. |
| v0.1.2 | 2026-01-22 | 다른 Agent Critic 반영: (1) 플래그십 선정은 고정 명단 금지, (2) 동의 증빙 스키마 참조, (3) 인간 승인=정식 승격 서명으로 한정, (4) Swarm 거부/보류 시 롤백/격리/만료 프로토콜 추가. |
| v0.1.3 | 2026-01-22 | Record Archive System(기록 보존 기관) 추가: `01_Nucleus/Record_Archive/`를 META 계층에 편입하고 상속 규범을 명시. |
| v0.1.4 | 2026-01-22 | 최상위 기관 순서 정정(Canon → Record Archive → Immune+Deliberation → Swarms), 디렉토리 리네이밍(01/02/03/04) 및 `01_Nucleus/Deliberation_Chamber/` 추가. |
| v0.1.5 | 2026-01-23 | “상위기관(군체(Swarm) 이상) + META” 변경 게이트를 명문화하고, Canon의 군체/군락 귀속 원칙과 정렬. |
| v0.1.6 | 2026-01-23 | 용어 정렬: Swarm=군체, Group=군락. Canon/Identity/게이트 문구를 정합화. |
| v0.1.7 | 2026-01-27 | Draft/Planning Workspace Protocol 명문화: Draft Types, Normative vs Informative Reference, Change Packet Minimum(AUDIT_LOG 포함), Draft Natural Dissolution(기본 TTL) 추가. |
| v0.1.8 | 2026-01-27 | AIVarium 3-Layer 적용: Manifestation 계층(현현/접속) 추가 및 상위 변경 게이트 대상에 포함. |
| v0.1.9 | 2026-01-27 | 디렉토리 구조를 Nucleus/Swarm/Manifestation으로 재편: `01_Nucleus/{Record_Archive,Immune_system,Deliberation_Chamber}`, `02_Swarm`, `03_Manifestation`. Inquisitor 도구의 루트 탐색 경로 정합화. |
| v0.1.10 | 2026-01-27 | 명칭 통일: `03_AAOS-Manifestation` → `03_Manifestation` (디렉토리/참조 경로 정합화). |
| v0.1.11 | 2026-01-27 | 레거시(개념) 경로 제거/정합화(실경로만), COF/COO 레지스트리 정렬, Auto-Enforcement 실제 경로/CLI 고정, Change Packet 템플릿/동선 추가, Manifestation 최소 계약 명문화. |
| v0.1.12 | 2026-01-30 | Record_Archive(사실/증빙) vs cortex-agora(행동 관찰/제안) 책임 경계 및 입력/출력 규약 명문화. |
| v0.1.13 | 2026-01-30 | Swarm Observability Standard(Behavior Feed) 권장/필수 표준 추가. |
| v0.1.14 | 2026-02-14 | Semantic Operations Doctrine(Working Hypothesis) 수용: 판단 종료 조건/의미 엔트로피 가드레일/Local Chart 책임 분리 추가. Manifestation 실행 격리 원칙 및 Auto-Enforcement의 Judgability Gate 점검 항목 반영. |
| v0.1.15 | 2026-02-14 | 제안 산출물 잔여 항목 반영: 플래그십 정량 선정, 긴급 롤백, Conflict Resolution, Health Metrics, Versioning Policy, Cross-reference validator, Homing Instinct 발동 조건, TTL 유연성 규칙 추가. |
| v0.1.16 | 2026-02-14 | Canon-Archive Feedback Loop 정규화: Proposal→Evidence→Judgment→Signature→Feedback 루프 및 상호보완 규범을 META 교리로 승격, Root README와 정합. |
| v0.1.17 | 2026-02-14 | Canon v1.0 정렬에 따른 상호보완 루프 운영 언어 통일 및 문서-제도 정합성 보강. |
| v0.1.18 | 2026-02-14 | Record Archive 상위 변경의 다중 모델 토론 규약(Open Agent Council) 도입 및 Deliberation 증빙의 모델 메타데이터 의무화 강화. |
| v0.1.19 | 2026-02-14 | Blueprint 제도 병목 제거: 사람 재확인 경로를 `agent-audit-log` 기반 비동기 루프로 대체하고 제안 산출물 + 증빙 라우팅 중심으로 정합성 확보. |
| v0.1.20 | 2026-02-14 | `_archive` 증빙 패키지의 보존 불변성(원문·메타데이터 삭제/수정 금지)을 규범화하고, 상위기관 변경에서 `_archive` 증빙 보존을 필수화. |
| v0.1.21 | 2026-02-14 | 01_Nucleus의 영구 아카이브/기록/로그 책임을 `Record_Archive` 단일 기관(`_archive`)으로 중앙집중화하고, 다른 Nucleus 하위 폴더의 장기 보존 저장을 금지하는 규범 조항 추가. |
| v0.1.22 | 2026-02-14 | Open Agent Council 적용을 모델/에이전트 무관 규범으로 고정하고, 핵심 판단 단계의 교차 모델군 수행(Claude/Gemini/Grok 포함) 의무를 추가. |
| v0.1.23 | 2026-02-14 | Swarm Skill Frontmatter Compliance Gate 추가: `SKILL.md` 표준 필드(`context_id`/`description` 등) 의무화, Skill Registry 경고 발생 시 Non-Canonical 대기 분류 및 재검증(`warnings=0`,`errors=0`) 조건 명문화. |
