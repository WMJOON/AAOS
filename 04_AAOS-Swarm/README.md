---
name: aaos-swarm
description: AAOS 군체(Swarm) 계층. 실제 협업 구조/실행 환경이 발생하며, 모든 하위 구조는 Immune System 규범을 참조(계승)해야 한다.
---
# AAOS 군체(Swarm)

군체(Swarm)는 AAOS에서 실제 구조(프로젝트/노드/온톨로지/워크플로우)가 발생하고 성장하는 계층이다.
모든 군체(Swarm) 하위 구조는 **Canon → META Doctrine → Immune Doctrine → Inquisitor** 순서의 규범을 참조하여 “면역체계 계승”을 보장해야 한다.

## 필수 원칙

- 군체(Swarm) 구조는 반드시 `DNA.md`(정식) 또는 `DNA_BLUEPRINT.md`(제안)를 가진다. (둘 다 없으면 Non-Canonical)
- Blueprint에는 Natural Dissolution(종료/해체)과 Resource Limits(상한)를 명시한다.
- Blueprint/권한 요청은 Inquisitor의 검증을 전제로 한다.

## 규범 참조(계승) 표준

군체(Swarm) 구조의 `DNA.md`/`DNA_BLUEPRINT.md` frontmatter에 아래 “규범 참조”를 **권장**한다.

```yaml
canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/METADoctrine.md"
immune_doctrine_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/AAOS_DNA_DOCTRINE_RULE.md"
inquisitor_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/02_AAOS-Immune_system/AUDIT_LOG.md"
```

이 참조들은 “면역체계가 어디서부터 상속되는지”를 구조 자체에 각인한다.

## 검증

- Blueprint 검증(권장): `python3 04_Agentic_AI_OS/02_AAOS-Immune_system/SWARM_INQUISITOR_SKILL/_shared/yaml_validator.py <DNA.md|DNA_BLUEPRINT.md>`
- 전체 스캔 리포트: `python3 04_Agentic_AI_OS/02_AAOS-Immune_system/SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py --scan 04_Agentic_AI_OS --format md`
