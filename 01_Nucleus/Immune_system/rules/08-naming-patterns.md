---
name: aaos-immune-naming-rule
scope: "04_Agentic_AI_OS/01_Nucleus/immune_system/rules"
status: canonical
updated: "2026-02-14"
---

# Immune Naming Rule

## 목적

Immune System 디렉토리 복잡도를 낮추고, 경로 예측 가능성을 높이기 위해 네이밍 패턴을 고정한다.

## 패턴

- 기본 형식: `lower-kebab-case`
- 역할 접두:
  - `core-*`: 공통 런타임/유틸
  - `judgment-*`: 판정 모듈
  - `governance-*`: 규범/검증 모듈
  - `lineage-*`: 계보/추적 모듈
  - `instruction-*`: 운영 지시 모듈

## 기관 최상위 파일 규칙

- `01_Nucleus/*` 기관 루트(`immune_system`, `record_archive`, `deliberation_chamber`)에는
  `README.md`, `DNA.md`만 파일로 허용한다.
- 그 외 문서/로그/규칙은 반드시 하위 디렉토리(`rules/`, `skills/`, `templates/`, `_archive/` 등)로 배치한다.

## Canonical 구조

- `skills/core/`
- `skills/judgment-dna/`
- `skills/judgment-permission/`
- `skills/governance-skill/`
- `skills/lineage-context/`
- `skills/instruction-nucleus/`

## 금지

- `SWARM_INQUISITOR_SKILL/`
- `_shared/`
- `blueprint-judgment/`, `permission-judgment/`, `skill-governance/`, `context-lineage/`, `inquisitor-instruction-nucleus/`

위 레거시 경로는 운영 루트에서 재도입하지 않는다.
