# Context-Orchestrated Ontology

Context-Orchestrated Ontology는 AI 실행 컨텍스트를 본질 단위(context node)로 분해하고,
관계형 지식 그래프로 조직·해석하기 위한 Swarm 하위 체계이다.

## 임무

- 문서/티켓/실행맥락을 정합성 있게 연결해, Swarm 판단의 이유 연결 고리를 보존한다.
- 행동 관찰 데이터와 조합하여 의미론적 재사용성이 높은 규칙 후보를 만들 수 있는
  온톨로지 토대를 유지한다.
- 스크립트/툴은 실행이 아니라 **정의와 정합성**을 중심으로 관리한다.

## 역할 범위

### 포함 영역

- Context 객체 설계
- Relation 타입 정의 및 식별자 규약
- Ontology-aware Skill/Workflow 연결성 설계
- Swarm/Manifestation 경계에서 사용되는 컨텍스트 키의 정합성 검증 보조

### 제외 영역

- Record Archive의 사실 기록/봉인/보관은 `record_archive`가 담당한다.
- Swarm 자동 실행 오케스트레이션은 `context-orchestrated-filesystem`의
  Task/Resolver 계층과 Nucleus governance loop가 담당한다.

## 핵심 산출물

- SKILL_REGISTRY
- Ontology 규칙/스키마(필요 시 신규 문서로 분리)
- 컨텍스트 정합성 판단 노트

## Canonical references

- Canon: `04_Agentic_AI_OS/README.md`
- META Doctrine: `04_Agentic_AI_OS/00_METADoctrine/DNA.md`
- Immune Doctrine: `04_Agentic_AI_OS/01_Nucleus/immune_system/rules/README.md`
- Swarm Root DNA: `04_Agentic_AI_OS/02_Swarm/DNA.md`
