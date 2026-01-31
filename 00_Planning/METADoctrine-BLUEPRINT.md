---
type: meta-doctrine-blueprint
name: METADoctrine-vNext-Design
status: implemented
created: "2026-01-26"
implemented: "2026-01-27"
target:
  canonical_file: "04_Agentic_AI_OS/METADoctrine.md"
  current_version: "v0.1.6"
  proposed_version: "v0.1.7"
scope: "AAOS 전체 (META Doctrine 확장)"
owner: "Canon Guardian (human signer)"
governance:
  voice: homing_instinct
  mother_ref: "04_Agentic_AI_OS/METADoctrine.md"
  precedence:
    - "AAOS Canon"
    - "META Doctrine (current canonical)"
    - "Immune Doctrine"
    - "This blueprint (draft)"
  on_conflict: "halt_then_home_to_meta_doctrine"
references:
  canon: "../README.md"
  meta_doctrine: "../METADoctrine.md"
  immune_templates:
    dna_blueprint_template: "../01_Nucleus/Immune_system/templates/DNA-BLUEPRINT-TEMPLATE.md"
    permission_request_template: "../01_Nucleus/Immune_system/templates/PERMISSION-REQUEST-TEMPLATE.md"
  deliberation_chamber: "../01_Nucleus/Deliberation_Chamber/README.md"
  record_archive: "../01_Nucleus/Record_Archive/README.md"
  cof_latest_dna: "../02_Swarm/01_context-orchestrated-filesystem/DNA.md"
---

# METADoctrine Extension Blueprint (Draft)

이 문서는 `04_Agentic_AI_OS/METADoctrine.md`에 **“추가될 내용”을 설계도(blueprint) 형태로 정리**한 초안이다.  
목표는 **정통 텍스트(META Doctrine)의 집행력은 유지**하면서도, 실제 작업 흐름에서 필요한 **Draft/Planning 레이어 프로토콜**을 META Doctrine에 명문화하는 것이다.

## Critic Pass (what to fix vs v0.1.6)

- Change Packet에 **Inquisitor verdict/AUDIT_LOG**가 빠져 있어, “승인/거부 결과의 정합한 고정 위치”가 모호했다.
- Draft Natural Dissolution에 **기본 만료(기본 TTL)** 이 없어, “무한 적치”를 막는 장치가 약했다.
- “Draft는 Canonical에서 normative reference로 금지”는 좋지만, **informative 링크(참고용 링크)** 허용/표기 규칙이 없었다.
- Draft/Planning 문서가 **집행 권한이 없음(Non-executable)** 을 더 강하게 선언할 필요가 있었다(규칙처럼 오용 방지).

## 0) Goal / Non-Goal

### Goal

- META Doctrine에 **Draft/Planning 레이어**를 “정식 작업 흐름(프리-게이트)”로 편입한다.
- Canonical 변경을 위한 **Change Packet**(증빙/합의/감사/만료)의 최소 요건을 “문서 레벨”에서 고정한다.
- `DNA_BLUEPRINT.md`와 일반 설계 초안(Planning Notes)을 구분하고, 둘의 관계/승격 경로를 표준화한다.

### Non-Goal

- 기존 Canon/META/Immune/Deliberation/Record Archive의 **권한 구조를 재배치하지 않는다**.
- 기존 조항(Upper-Institution Change Gate, Inquisitor 승인, Audit Log)의 **요건을 완화하지 않는다**.
- `04_Agentic_AI_OS/` 내부 파일들의 대규모 재구성/리네이밍을 목표로 하지 않는다.

## 1) Problem Statement (왜 필요한가)

현행 `METADoctrine.md`는 “정식 변경 게이트”는 강하지만, 실제 설계/초안 생산을 위한 **공인된 Draft 레이어의 규약**이 명시적이지 않다.  
그 결과, 다음이 반복적으로 발생할 수 있다.

- 초안이 곧바로 Canonical 문서를 흔드는 형태로 작성됨(정통성/감사/버전 관리가 흐려짐)
- Draft와 `DNA_BLUEPRINT.md`(승격 대기) 문서가 혼재되어 “어떤 단계의 문서인지” 불명확
- 승격에 필요한 증빙(합의/감사/만료)이 문서마다 다른 방식으로 산재

이 Blueprint는 위 공백을 채우기 위해 META Doctrine에 **Draft/Planning Protocol**을 추가한다.

## 2) Proposed Additions to `METADoctrine.md` (변경 설계)

### 2.1. 새 섹션 추가: “Draft/Planning Workspace Protocol”

METADoctrine에 아래를 추가한다.

- Draft/Planning 문서의 정의(Planning Notes vs DNA Blueprint)
- “작업대(Planning)” ↔ “승격 대기(DNA_BLUEPRINT)” ↔ “정식(DNA.md / canonical text)” 관계
- Draft에 대한 Natural Dissolution(만료/정리) 기본 규칙
- Canonical 문서가 Draft를 “정규 참조(normative reference)”로 삼지 못하게 하는 링크 규약

### 2.2. Change Packet 최소 요건 명문화

상위기관/Swarm 변경을 위한 “필수 산출물”을 문서 수준에서 고정한다.

- `permission-request`(또는 `blueprint-judgment`) 패킷
- `multi-agent-consensus`(해당되는 경우)
- Record Archive 증빙 고정(스냅샷/해시/인덱스)
- **Inquisitor verdict + `AUDIT_LOG.md` 기록**(해시 체인): 승인/거부/보류 결과와 근거
- `META_AUDIT_LOG.md` 기록(버전/사유/증빙 링크; META 수준 변경일 때 필수)
- Draft 만료(`time_bound.expires`) 및 자연소멸 절차

### 2.3. 문서 상태 표기 규격 추가(선택)

문서 헤더(frontmatter)를 강제하지는 않되, Draft/Blueprint는 다음 중 하나를 권장한다.

- `status: draft | canonical`
- `target: <canonical_file>`
- `proposed_version: ...`
- `time_bound.expires: YYYY-MM-DD` (만료가 중요한 초안일수록 권장)

### 2.4. File-Level Patch Plan (METADoctrine.md에 실제로 들어갈 수정)

- Frontmatter `version: v0.1.6` → `version: v0.1.7` (승격 시점에 확정)
- 본문에 새 섹션 추가(권장 위치): `## 5. 전체 계층 요약 트리` 이후, `## META Doctrine Version Note` 이전
- `META Doctrine Version Note` 테이블에 v0.1.7 행 추가(변경 요약 + “Draft/Planning Protocol” 명시)

## 3) Definitions (용어)

- **Canonical text**: 승인/승격/공표가 완료된 정식 텍스트(예: `DNA.md`, `METADoctrine.md`).
- **Draft (Planning Notes)**: 구상/설계/질문/대안 비교 중심의 초안 문서. 정통성 게이트의 입력 후보.
- **DNA Blueprint (`DNA_BLUEPRINT.md`)**: “구조 생성/성장/해체 규칙”을 갖춘 승격 대기 문서(템플릿 기반).
- **Change Packet**: Canonical 변경을 위해 필요한 증빙/합의/감사/만료를 한 번에 묶은 패킷(문서+링크 집합).
- **Normative reference**: “이 링크의 내용이 규칙/근거로 강제된다”는 수준의 참조.
- **Informative reference**: 참고/배경 설명용 참조(정통성/집행 근거로 강제되지 않음).

## 4) Workspace Model (경계/경로)

> METADoctrine 본문에는 “경로 예시”로만 넣고, 강제는 최소화한다(환경마다 루트가 다를 수 있음).

- **Canonical workspace**: `04_Agentic_AI_OS/` (정통 텍스트가 존재하는 루트)
- **Planning workspace (non-canonical)**: `04_Agentic_AI_OS/00_Planning/` (초안/설계/제안 작업대)
- **Execution workspace**: Swarm별 작업공간(예: COF 티켓/컨텍스트 폴더)

### 링크/참조 규칙(제안)

- Canonical 문서는 Draft/Planning 문서를 **normative reference로 참조하지 않는다**.
- Canonical 문서가 Draft를 링크해야 한다면, **informative reference**로만 허용하며 “참고/비정통”을 명시한다.
- Draft/Planning 문서는 Canonical 문서를 **항상 링크로 고정**한다(“최신”이 아니라 “어떤 정본을 기준으로 하는지” + 가능하면 문서의 `version` 명시).

## 5) Promotion Flow (승격 흐름)

### 5.1. 기본 흐름

1. Draft(Planning Notes)에서 의도/경계/리스크를 먼저 정리한다.
2. “구조/규칙” 변경이면 `DNA_BLUEPRINT.md`로 번역한다(템플릿 준수).
3. Deliberation Chamber 산출물로 합의/근거를 구조화한다(필요 시).
4. Record Archive로 증빙을 고정한다(스냅샷/해시/인덱스).
5. Immune System/Inquisitor 절차로 승인 요청 및 감사 로그 기록을 완료한다.
6. Canon Guardian 서명(정통성 기록)으로 승격/공표한다(상위기관 대상).

### 5.2. 실패/보류/만료 프로토콜

- 승인 실패/보류 시: Canonical 파일은 유지, 변경안은 `DNA_BLUEPRINT.md` 또는 Draft로 격리.
- `time_bound.expires` 내 재심 없으면: 요약 후 자연소멸(삭제/아카이브) 수행.
- 기본 만료(권장): Planning Notes/DNA Blueprint 초안은 **30일**을 기본 TTL로 두고, 필요 시 `time_bound.expires`로 연장한다.

## 6) Ready-to-Paste Draft Text (METADoctrine에 들어갈 “추가 본문” 초안)

아래는 `04_Agentic_AI_OS/METADoctrine.md`에 **새 섹션으로 추가**할 수 있는 형태의 문안 초안이다.

---

### (Proposed) 6. Draft/Planning Workspace Protocol

AAOS는 Canonical 텍스트를 직접 흔들지 않고도 설계/실험을 진행하기 위해, “Draft/Planning 레이어”를 허용한다.  
단, Draft는 정통 텍스트가 아니며, Canonical 변경의 “입력 후보”로만 취급된다.

Draft는 **집행 권한을 갖지 않는다**. Draft의 내용은 승인/승격 전까지 어떠한 Rule/DNA/Doctrine의 근거로 강제되지 않으며, 집행/차단/승인 판단은 Immune System/Inquisitor 및 상위 게이트를 따른다.

#### 6.1. Draft Types

- **Planning Notes**: 의도/경계/대안/질문/리스크를 다루는 초안 문서.
- **DNA Blueprint (`DNA_BLUEPRINT.md`)**: 구조의 생성/성장/해체 규칙을 포함하는 승격 대기 문서.

#### 6.2. Normative Reference Rule

- Canonical 문서는 Draft/Planning 문서를 **규범 참조(normative reference)** 로 삼지 않는다.
- Draft/Planning 문서는 Canonical 문서를 링크로 고정하여 기준점을 명확히 한다.
- Canonical 문서에서 Draft를 링크해야 한다면, **informative reference(참고 링크)** 로만 허용하며 “비정통/비집행”임을 명시한다.

#### 6.3. Change Packet (Minimum)

Canonical 변경(특히 상위기관/Swarm DNA)은 최소 다음을 포함하는 Change Packet으로 제출한다.

1. 변경 제안 본문(Draft/Blueprint)
2. 승인 요청 패킷(`permission-request` 또는 `blueprint-judgment`)
3. 필요 시 `multi-agent-consensus` 산출물(Deliberation)
4. Record Archive 증빙(스냅샷/해시/인덱스)
5. Inquisitor verdict 및 `AUDIT_LOG.md` 기록(해시 체인; 승인/거부/보류 결과와 근거)
6. META 수준 변경일 경우 `META_AUDIT_LOG.md` 기록(버전/사유/증빙 링크)
7. `time_bound.expires` 및 Natural Dissolution 절차

#### 6.4. Draft Natural Dissolution

Draft는 무기한 유지되지 않는다.  
만료 시 요약을 남기고(필요 시 Record Archive로 이관), 잔여 초안은 자연소멸 절차로 정리한다.

기본 만료(권장): Planning Notes/DNA Blueprint 초안은 생성 시점 기준 **30일**을 기본 TTL로 두며, `time_bound.expires`로 연장할 수 있다.

---

### (Proposed) META Doctrine Version Note (v0.1.7 행 추가)

`## META Doctrine Version Note` 표에 아래 행을 추가한다.

| v0.1.7 | 2026-01-26 | Draft/Planning Workspace Protocol(프리-게이트) 명문화: Draft Types/Normative vs Informative Reference/Change Packet Minimum(AUDIT_LOG 포함)/Draft Natural Dissolution(기본 TTL) 추가. |

## 7) Local Planning Pointers (현재 작업대)

- Planning root: `04_Agentic_AI_OS/00_Planning/AAOS_DOCS_INDEX.md`
- COF planning notes: `04_Agentic_AI_OS/00_Planning/AAOS.Swarm.COF(Context Orchestrated Filesystem).md`
- Nucleus draft map: `04_Agentic_AI_OS/00_Planning/AAOS.Nucleus.md`

## 8) Acceptance Criteria (v0.1.7로 승격될 때)

- “Draft/Planning 문서가 무엇인지”와 “어떤 권한이 없는지(Non-executable)”가 META Doctrine에 명시된다.
- Canonical 변경 시 Change Packet 최소 구성에 **Inquisitor verdict + `AUDIT_LOG.md`** 가 포함된다.
- Draft의 기본 만료(TTL)와 만료 시 처리(요약/이관/자연소멸)가 명시된다.
- Canonical ↔ Draft 링크 규칙이 “normative 금지 + informative 허용(표기 필수)”로 명확해진다.
