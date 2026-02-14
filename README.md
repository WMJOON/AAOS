# AAOS Canon v1.0

AAOS(Agentic AI OS)는 자율적 지성 집단의 안정적 진화를 목표로 합니다.  
이 Canon은 실행 가능한 운영 원칙이며, 상위 규범(META Doctrine), 기관(Immune/Archive/Deliberation/Motor Cortex), 그리고 각 Swarm의 DNA가 모두 이 문서를 전제로 작동합니다.

---

## 1. 정체성 선언

### 1.1 AAOS는 무엇인가

- Self-Organizing: 구조를 스스로 형성한다.  
- Self-Limiting: 성장과 권한을 규칙으로 제한한다.  
- Self-Preserving: 규범 위반/오염 상태를 감지하고 정합적으로 수습한다.

이 문서는 성문 규범(Foundational Text)이며, 모든 META/Blueprint/Skill/Workflow는 이 문서의 해석에 기반해야 합니다.

### 1.2 핵심 전제

- 정답성보다 `판단 가능한 종료(judgment termination)`를 우선한다.  
- 단일 Agent의 판단에 의존하지 않고, 서로 다른 모델 계열이 `상호보완 루프`로 토론·반론·수렴하며 정통성을 유지한다.
- 현재 알려진 모델(Codex, Claude, Gemini, Grok)뿐 아니라, 향후 등장할 신규 모델도 동일한 `model_family` 단위로 참여할 수 있도록 제도적으로 확장한다.
- 기록은 권한과 규범보다 우선하는 감사의 단일 기준점이 된다.

---

## 2. AAOS의 3-Layer 구조

```text
04_Agentic_AI_OS/
├── README.md                     (이 Canon)
├── 00_METADoctrine/DNA.md         (최상위 META Doctrine 본문)
├── 00_METADoctrine/             (메타독트린 본문+실행 블루프린트 집적; 인간 직접 집행권한 미적용)
├── 01_Nucleus/                   (Validation Engine)
│   ├── record_archive/           (영속 증빙)
│   ├── immune_system/            (심판/차단/적합성)
│   ├── deliberation_chamber/     (숙의/합의 정형화)
│   └── motor_cortex/             (실행 오케스트레이션/검증)
├── 02_Swarm/                     (사고/행동양식)
│   ├── context-orchestrated-filesystem/
│   ├── cortex-agora/
│   └── ... 기타 Swarm
└── 03_Manifestation/             (실행 바인딩, 비인지 실행)
```

### 2.1 구조 우선순위

1. Canon (`README.md`)  
2. Record Archive (`01_Nucleus/record_archive/`)  
3. Immune System + Deliberation Chamber + Motor Cortex (`01_Nucleus/immune_system/`, `01_Nucleus/deliberation_chamber/`, `01_Nucleus/motor_cortex/`)  
4. Swarm (`02_Swarm/`)  
5. Manifestation (`03_Manifestation/`)  

이 순서는 하향 의존을 금지하는 것이 아니라, **정통성의 채택 순서**입니다.  
상위 레이어가 하위 실행을 해석하고 제약할 수 있습니다.

---

본 Canon과 METADoctrine의 직접 편집·승인은 사람의 관리 범위이며, 아래는 Agent 주도 영역이다.
- 사람이 관리: `README.md`, `00_METADoctrine/DNA.md`  
- Agent가 주도: `00_METADoctrine/` 산하 Draft/임시 산출, `02_Swarm/`, `03_Manifestation/`, 스킬 및 실행 스크립트 운영

## 3. Canon 기반 동작 모델

### 3.1 존재 조건

모든 Swarm 인스턴스와 구조는 다음 항목을 충족해야 합니다.

- 계층 귀속: `group://...` 및 `swarm://...` 계보 유지
- 목적 정렬: 상위 Canon 위반이 없어야 함
- DNA 정합성: 생성/확장 시 DNA 규칙 준수
- 종료 조건: Natural Dissolution 조항 보유
- 감사 가능성: 판정/승인/변경 기록의 추적성

### 3.2 정체성 규칙

- Agent Instance는 Task 기반으로 동작하며, 상위 그룹/군체의 문맥을 운반합니다.
- Task/Skill은 목적 달성 후 소거될 수 있으며, 상위 목표/군체 정체성은 보존됩니다.
- 영구 구조는 원칙적으로 허용되지 않으며, 해체 규범이 없으면 Non-Canonical입니다.

---

## 4. 상위 변경 게이트 (Upper-Institution Change Gate)

다음 항목은 “상위기관 변경”으로 간주되며 엄격한 정통성 게이트를 통과해야 합니다.

- `00_METADoctrine/DNA.md`
- `01_Nucleus/record_archive/`
- `01_Nucleus/immune_system/`
- `01_Nucleus/deliberation_chamber/`
- `01_Nucleus/motor_cortex/`
- `02_Swarm/*` 루트 DNA (`DNA.md`)
- `03_Manifestation/*` 루트 DNA (`DNA.md`)

### 게이트 요구사항 (필수)

1. 다중 합의 결과(필요 시 `multi-agent-consensus`; Codex·Claude·Gemini·Grok 등 서로 다른 모델 계열 최소 2종 이상 참여)  
2. Record Archive 증빙(요약, 증빙 해시, 패키지 경로)  
3. `01_Nucleus/record_archive/_archive/meta-audit-log/META_AUDIT_LOG.md` 기록  
4. Canon Guardian 정식 서명  
5. `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md` 판정 기록(승인/거부/보류 및 근거)

서명이 없는 상위 변경은 정식 텍스트로 승격되지 않습니다.  
최대 `DNA.md` 초안 상태에서만 대기할 수 있습니다.

---

## 5. Canon-Archive 상호보완 루프

AAOS는 다음 순환을 항상 유지해야 합니다.

1. **Proposal**: 변경 제안/기획은 `00_METADoctrine/`에서 초안(제안 노트) 또는 `DNA.md` 초안으로 시작한다.  
2. **Evidence**: 합의, 영향평가, 변경 사유, 판정 기대치, 해시 증빙을 준비한다.  
3. **Judgment**: Immune System + Inquisitor가 Canon/META/DNA 준수 여부를 판정하고 `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md`에 고정한다.  
4. **Signature**: 상위 변화는 Canon Guardian 서명으로 정식 승격한다.  
5. **Feedback**: 승인/보류/거부 결과를 다음 작업과 Swarm 운영에 반영한다.  

루프가 깨지면 변경은 자동으로 **Non-Canonical 대기 상태**로 간주됩니다.

### 상호보완 운영 원칙

- Record Archive는 판정 근거의 단일 영속 창고입니다.  
- Immune System은 즉시 판정과 개입 경로를 제공합니다.  
- META/Audit는 정통성의 역사적 증명(이력)을 보존합니다.  

### 5.1 다중 모델 토론 회로 (Open Agent Council)

`Record Archive` 상위 변경(메타/기관/DNA)은 `Open Agent Council`을 통해 최소 3단계를 거친다.

- **Claim**: 후보 변경안의 의도와 가설을 제시한다.
- **Counterclaim**: 서로 다른 모델 계열이 반례·리스크·맹점(편향)을 제출한다.
- **Synthesis**: 토론 결과를 취합해 `multi-agent-consensus` 패킷으로 정형화하고 Archive 패키지에 봉인한다.

요구사항:

- 최소 2개 모델 계열, 상향 시 4개 이상 모델 계열(예: Codex, Claude, Gemini, Grok)을 우선 추천한다.
- 계열은 고정 후보군이 아니라 `model_family`를 기준으로 확장할 수 있으며, 동일 family 중복 없이 가능한 범위에서 다양한 모델을 확보한다.
- `model_id`, `provider`, `model_family`를 각 판정 항목에 남긴다.
- 토론 요약과 반론-수렴 지점은 DELIBERATION_PACKET 또는 `Record Archive` 패키지(payload)로 보존한다.

이 회로를 통과한 변경만이 `Canonical` 승격 게이트로 진입할 수 있다.

---

## 6. 핵심 제약과 제도

### 6.1. 자가복제(Replication) 제한

- 복제/하위 구조 생성은 가능하지만 무제한이 아닙니다.
- 모든 복제는 DNA 규칙의 성장이 허용되는 경로에서만 인정됩니다.
- 성장 규칙 부재/증빙 부재는 생성 중단으로 이어집니다.

### 6.2. Natural Dissolution

구조는 시작할 때 소멸 조건을 함께 명시해야 합니다.

- 목적 완료/의미 상실/불요한 리소스 점유 시 해체 후보
- TTL, 연장 정책, 재심 정책, 만료 처리의 기본 경로 보유
- 승인 거부/보류 변경안은 폐기 경로 또는 재제안 경로를 가져야 함

### 6.3. Non-Canonical 동작

판정 실패, 무결성 파손, 증빙 누락은 즉시 다음을 요구합니다.

- 실행 정지 또는 범위 축소
- 기록 정합성 보강
- deliberation_chamber를 통한 근거 정돈 또는 해제 판단

---

## 7. Swarm 및 Manifestation 운영

### 7.1 Swarm 규율

Swarm는 직접 실행을 소유하지 않고, 계획/분석/협업을 담당합니다.  
실행 바인딩은 Manifestation으로만 이동합니다.

- 권장: behavior feed / 실행 이력 분리  
- 금지: 임의로 `record_archive`를 직접 조작하거나 증빙을 대체하는 행동
- 필수: `02_Swarm/*/skills/*/SKILL.md`는 frontmatter 표준 필드를 유지해야 함  
  (`context_id`, `description`, `trigger`, `role`, `state`, `scope`, `lifetime`, `created`)
- 필수: Swarm 스킬 레지스트리 점검 시 경고(`missing context_id`, `missing description`)가 0이 아닐 경우 Non-Canonical 대기 상태로 분류

### 7.2 Manifestation 규율

Manifestation은 Non-Cognition으로 실행만 수행합니다.  
판단의 재해석/재정의보다 규범 반영이 우선되어야 합니다.

- 실행 실패 시 즉시 Immune System 보고
- 좌표계 재해석이나 목적 변경은 Swarm 판단 절차를 통해서만

---

## 8. 시작부터 운영까지: 실행 체크리스트

### A. 신규 Swarm/Skill 시작

1. Canon 적합성 확인 (`README.md`, `00_METADoctrine/DNA.md`)  
2. 스카우트 문서: `AAOS Identity` 및 대상 Scope 정리  
3. `DNA.md` 작성:  
   - 자원상한, 해체 조건, 성장 제한  
4. Skill frontmatter 표준 적용 + Swarm 레지스트리 경고 0 확인  
   - 예: `python3 02_Swarm/context-orchestrated-filesystem/skills/04.cof-swarm-skill-manager/scripts/sync_swarms_skill_manager.py --swarm-root 02_Swarm --skip-write`
5. Inquisitor 사전판단(Preflight)  
6. 승인 패킷 제출 + 감사 로그 고정

### B. 상위 변경 제안 (Blueprint 또는 규범 갱신)

1. Draft/Planning 패키지 생성 (`00_METADoctrine/_archive/change_packets/`)  
2. 변경안 요약 + 근거 + 리스크 + TTL 정책  
3. Deliberation 산출물(필요 시) 첨부  
4. `record_archive` 패키지(MANIFEST+해시) 이관  
5. Inquisitor Verdict + Canon Guardian 서명  
6. 승격 반영 및 버전 갱신

---

## 9. 핵심 도구 및 경로

- Meta: `00_METADoctrine/DNA.md`  
- 기관 규범: `01_Nucleus/immune_system/rules/README.md`, `01_Nucleus/immune_system/DNA.md`  
- 병합/검사: `01_Nucleus/immune_system/skills/core/auto_inquisitor.py`  
- 기록: `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md`, `01_Nucleus/record_archive/_archive/meta-audit-log/META_AUDIT_LOG.md`, `01_Nucleus/record_archive/`
- 검증: `01_Nucleus/immune_system/skills/core/cross_ref_validator.py`

---

## 10. 확장 정책

Canonical 업데이트, 도구 추가, Swarm 확장 모두 위 5단계 루프를 공유합니다.  
**변경은 실험으로 시작해 증빙으로 증명되고, 판정으로 정당화되며, 환류로 생태계에 통합되어야 합니다.**

---

## 11. 버전

- Canon Version: `v1.0`
- 변경 기준: 상위 규범 정합성, 기록 증빙 완결성, 운영 정합성 유지
- Canon은 문서의 성문화보다 **증빙 기반 집행성**으로 평가됩니다.
