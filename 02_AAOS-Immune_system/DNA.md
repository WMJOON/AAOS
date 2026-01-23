---
name: "AAOS-Immune-System"
version: "0.3.1"
scope: "04_Agentic_AI_OS/02_AAOS-Immune_system"
owner: "AAOS Canon"
created: "2025-01-22"
status: canonical

# Supremacy Clause (최상위 종속 조항)
governance:
  voice: decree
  supremacy: "본 문서(DNA, DNA-BLUEPRINT)를 읽고 해석/집행하는 모든 Agent는 AAOS 율법(AAOS Canon, META Doctrine, Immune Doctrine)에 종속된다"
  precedence:
    - "AAOS Canon"
    - "META Doctrine"
    - "Immune Doctrine"
    - "This document"
  on_conflict: "halt_and_escalate_to_audit"

# Normative References (bootstrap 구조의 계승 기준)
canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/METADoctrine.md"
immune_doctrine_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/AAOS_DNA_DOCTRINE_RULE.md"
inquisitor_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/AUDIT_LOG.md"

# Official DNA Promotion Record
dna_promotion:
  promoted_to: "official-dna"
  promoted_at: "2026-01-21"
  approved_by: "Canon Guardian (Human)"
  consensus:
    required: true
    minimum_agents: 2
    agents:
      - "Claude Opus (reviewed META/Immune design)"
      - "GPT-5.2 (implemented + reviewed enforcement)"
  evidence:
    meta_audit_log: "04_Agentic_AI_OS/02_AAOS-Immune_system/META_AUDIT_LOG.md"
    audit_log: "04_Agentic_AI_OS/02_AAOS-Immune_system/AUDIT_LOG.md"

# META 수준 예외 선언
# Immune System은 Canon에 의해 직접 보증되는 최상위 구조이다.
# 자기 자신을 검증하는 순환 참조를 피하기 위해,
# 본 Blueprint는 Canon v0.0.1의 Section 4(자기보존)와 Section 5(정통성)에 의해 정당성을 부여받는다.
meta_exception:
  granted_by: "AAOS Canon v0.0.1"
  sections: [4, 5]
  rationale: "Immune System은 다른 모든 구조를 검증하는 최상위 면역 계층이므로, Canon이 직접 보증한다"

# 다중 에이전트 합의 요구사항
# Immune System의 DNA 변경은 단일 Agent의 판단으로 이루어질 수 없다.
multi_agent_consensus:
  required: true
  minimum_agents: 2
  agent_requirement: "당시대 플래그십 Agent (서로 다른 조직/모델 계열)"
  rationale: "면역 체계 변경은 AAOS 전체에 영향을 미치므로, 복수의 독립적 검증으로 견제와 균형을 확보한다"
  exceptions:
    - type: "emergency_security_patch"
      condition: "명백한 취약점 수정"
      requirement: "단일 Agent + 인간 승인 (사후 합의 필수)"
    - type: "formal_correction"
      condition: "오타, 포맷팅 등 의미 변경 없는 수정"
      requirement: "합의 불필요"

natural_dissolution:
  purpose: "AAOS 생태계의 자기보존, 정화, 정통성 유지를 담당하는 면역 계층"
  termination_conditions:
    - "AAOS Canon이 폐기되거나 대체될 경우"
    - "상위 META Doctrine이 Immune System의 역할을 다른 구조로 이관할 경우"
  dissolution_steps:
    - "모든 Audit Log를 아카이브로 보존"
    - "활성 Inquisitor 세션 종료"
    - "후속 Immune System으로 권한 이관"
  retention:
    summary_required: true
    max_days: permanent  # Canon 직접 보증 구조에 한해 영구 보존 허용

resource_limits:
  max_files: 100
  max_folders: 20
  max_log_kb: 1024
  max_audit_entries: 10000

inquisitor:
  required: false  # 자기 자신은 검증하지 않음 (Canon이 직접 보증)
  audit_log: "./AUDIT_LOG.md"
  self_validation: "Canon 참조로 대체"
---

# AAOS Immune System DNA Blueprint

## Supremacy Clause (Canon Subordination)

본 문서(DNA, DNA-BLUEPRINT)를 읽고 해석/집행하는 모든 Agent는 AAOS 율법(AAOS Canon, META Doctrine, Immune Doctrine)에 종속된다.  
충돌 시 우선순위는 `Canon > META Doctrine > Immune Doctrine > 본 문서` 이며, 충돌/불명확성이 감지되면 Agent는 실행/수정/집행을 중단하고 승인·감사 절차(META_AUDIT_LOG/AUDIT_LOG)를 우선한다.

## Voice (Decree)

Immune System 문서는 규범을 설파한다(decree). 하위 구조(군체·군락·노드·스킬·워크플로우 등) 문서는 충돌/불명확 감지 시 모체(Immune/Canon)로 귀속되는 본능(homing_instinct)으로 전환한다.

## Overview

- **What it is**: AAOS 전체 구조의 면역 체계. 정통성(Canonicality) 판정, 자연소멸 강제, 권한 검증을 담당한다.
- **Why it exists**: "검증 없는 자율성"을 방지하고, AAOS가 Self-Preserving 시스템으로 유지되도록 한다.
- **What it must never do**:
  - 자기 자신을 Non-Canonical로 판정하여 시스템 전체를 무력화
  - Audit Log를 삭제하거나 변조
  - Canon에 명시되지 않은 권한을 임의로 부여

## Approval & Audit (행동 강제의 위치)

본 Blueprint는 “승인/판정이 어디에 기록되고, 무엇이 강제되는지”를 명시한다.
승인/판정은 Blueprint 내부에서 자체적으로 완결되는 것이 아니라, **면역체계(Inquisitor + Audit)** 에 의해 집행된다.

### 승인/판정 기록 위치

- META 수준 변경/승인(인간 승인 포함): `02_AAOS-Immune_system/META_AUDIT_LOG.md`
  - `approved_by`에 최종 승인자(예: Canon Guardian)를 기록
  - Immune System DNA 변경은 Multi-Agent Consensus Doctrine 절차를 따른다
- 일반 판정/집행 기록(해시체인): `02_AAOS-Immune_system/AUDIT_LOG.md`
  - `type: blueprint-judgment | permission-judgment | auto-enforcement | dissolution-execution`
  - `safe_append_audit_entry()`를 통해 무결성 검증 후 append

### “DNA 승격”의 의미

- 형식/내용 검증(validator 관점): `Canonical` 여부(스키마/빈 값/예외 근거 등)
- 교리/절차 검증(governance 관점): Multi-Agent Consensus + META 승인 기록이 갖춰져야 “최종 승격”으로 완결된다

## Bootstrap Exception (부트스트랩 예외)

일반적으로 모든 AAOS 구조는 Inquisitor 검증을 통과해야 한다.
그러나 Immune System은 "심판관을 심판하는 자"가 될 수 없으므로,
다음과 같은 예외 규칙이 적용된다:

1. **Canon 직접 보증**: Immune System의 정당성은 AAOS Canon Section 4, 5에 의해 직접 부여된다.
2. **변경 시 Meta-Audit**: Immune System 구조 변경 시, `META_AUDIT_LOG.md`에 별도 기록하며, Canon 수호자(인간 관리자)의 승인을 필요로 한다.
3. **버전 관리**: 모든 변경은 version 번호 증가와 함께 이루어져야 한다.

## Multi-Agent Consensus Requirement (다중 에이전트 합의 요건)

> **Immune System의 DNA는 당시대의 플래그십 Agent 2종 이상이 충분히 합의를 거친 후에만 새로운 버전의 DNA로 인정받을 수 있다.**

이 원칙은 AAOS 면역 체계의 무결성을 보호하기 위한 핵심 안전장치이다.

### 왜 필요한가?

- **견제와 균형**: 단일 Agent의 편향, 오류, 또는 악의적 조작을 방지
- **집단 지성**: 서로 다른 모델 계열의 관점에서 교차 검증
- **정당성 강화**: "이 변경은 합의를 거쳤다"는 기록으로 신뢰도 확보
- **시대 적합성**: "당시대 플래그십"이라는 동적 기준으로 기술 진화에 대응

### 합의 절차

1. 변경 제안 → META_AUDIT_LOG.md에 기록
2. 플래그십 Agent A 독립 검토 (Canon 정합성, 부작용 분석)
3. 플래그십 Agent B 독립 검토 (교차 검증)
4. 양측 승인 시 → Canonical, 버전 증가
5. 불일치 시 → 인간 관리자 중재 또는 재논의
6. 인간 관리자 최종 승인

### 예외

- **긴급 보안 패치**: 단일 Agent + 인간 승인 가능 (사후 합의 필수)
- **형식적 수정**: 오타/포맷팅 등 의미 변경 없는 수정은 합의 불필요

## Growth Rules

- Immune System은 다음 경우에만 확장할 수 있다:
  - 새로운 Inquisitor Skill 추가 (Canon 또는 META Doctrine에 근거한 경우)
  - 검증 템플릿 추가/수정
  - 자동화 스크립트 추가 (기존 Doctrine 강제력 강화 목적)
- 확장 전 체크:
  - [ ] Canon/META Doctrine과 충돌하지 않는가?
  - [ ] META_AUDIT_LOG.md에 변경 사유가 기록되었는가?
  - [ ] 기존 Audit Log 형식과 호환되는가?

## Dissolution Procedure

Immune System의 해체는 AAOS 전체의 종료를 의미할 수 있으므로 신중히 진행한다.

1. **Meta-Audit 기록**: 해체 사유, 후속 계획을 META_AUDIT_LOG.md에 기록
2. **Audit Log 아카이브**: 모든 판정 기록을 `_archive/` 폴더로 이동
3. **권한 이관**: 후속 Immune System 또는 Canon 수호자에게 검증 권한 이관
4. **README 업데이트**: 해체 사실과 후속 참조 경로 명시

## Self-Validation Mechanism

Immune System은 자기 검증 대신 다음을 수행한다:

1. **Integrity Check**: 시작 시 자체 파일 해시를 검증 (변조 감지)
2. **Canon Alignment Check**: 주요 Doctrine이 Canon과 충돌하지 않는지 확인
3. **Resource Limit Check**: 자체 resource_limits 준수 여부 확인
