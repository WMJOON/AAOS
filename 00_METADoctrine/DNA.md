---
name: aaos-meta-doctrine
scope: "04_Agentic_AI_OS/00_METADoctrine"
status: canonical
version: "0.2.0"
updated: "2026-02-14"
---

# AAOS META Doctrine (Core)

AAOS의 최상위 운영 교리. Canon(`README.md`)을 시스템 규칙으로 번역하고, 하위 레이어의 판정/증빙/승격 경계를 강제한다.

## 최상위 원칙

1. Canon 우선: 모든 하위 규칙은 Canon을 위반할 수 없다.
2. Human Controllability: 사람의 통제가능성을 최우선으로 둔다.
3. Entropy Budget: 정보 엔트로피(규칙 수, 메타데이터 키 수, 경계 수)가 임계치를 넘으면 Non-Canonical로 판정한다.
4. Minimal Surface: 통제 가능한 강제 규칙 표면을 최소화한다.

참조: [semantic-atlas-hypothesis](https://github.com/WMJOON/semantic-atlas-hypothesis)

## 적용 범위

- `00_METADoctrine/`
- `01_Nucleus/`
- `02_Swarm/`
- `03_Manifestation/`

## 상위 변경 게이트 (필수)

상위기관(군체(Swarm) 이상 + META) 변경은 아래를 모두 만족해야 한다.

1. Deliberation 합의 (`multi-agent-consensus`, 서로 다른 model_family 최소 2종)
2. Record Archive 증빙 고정 (`_archive/` + 해시 인덱스)
3. Immune 판정 로그 (`01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md`)
4. META 판정 로그 (`01_Nucleus/record_archive/_archive/meta-audit-log/META_AUDIT_LOG.md`)
5. Canon Guardian 서명

서명/증빙 미충족 변경은 canonical로 승격할 수 없다.

Nucleus 기관 범위는 `record_archive`, `immune_system`, `deliberation_chamber`, `motor_cortex`를 포함한다.

## 엔트로피 가드레일 (강제)

1. 정본 규범 문서는 프론트매터 최소 키만 허용한다.
2. `SKILL.md` frontmatter는 Claude 공식 허용 키만 사용한다.
3. 폐지 제도(`DNA_BLUEPRINT.md` 중심 운영)를 활성 규범에 재도입하지 않는다.

검증은 `01_Nucleus/motor_cortex/scripts/nucleus_ops.py health`에서 강제한다.

## 모듈 분리

상세 규정은 아래 모듈 문서로 분리한다.

- [01-governance-gates.md](./modules/01-governance-gates.md)
- [02-institutions-and-layers.md](./modules/02-institutions-and-layers.md)
- [03-semantic-operations.md](./modules/03-semantic-operations.md)
- [04-versioning-and-metrics.md](./modules/04-versioning-and-metrics.md)

## 이전 본문 보존

기존 장문 본문(v0.1.23)은 이 경로에 보존한다.

- `00_METADoctrine/_archive/legacy/METADoctrine.v0.1.23.full.md`
