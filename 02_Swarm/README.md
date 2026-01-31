---
name: aaos-swarm
description: AAOS 군체(Swarm) 계층. 의식적 사고/행동양식(계획/대화/패턴/스킬)을 담당하며, 실제 실행 바인딩은 Manifestation 계층을 통해 수행된다.
---
# AAOS 군체(Swarm)

군체(Swarm)는 AAOS에서 의식적 사고/행동양식이 발생하고, 하위 구조(프로젝트/노드/온톨로지/워크플로우)가 성장하는 계층이다.
모든 군체(Swarm) 하위 구조는 **Canon → META Doctrine → Immune Doctrine → Inquisitor** 순서의 규범을 참조하여 “면역체계 계승”을 보장해야 한다.

> 실행(하드웨어/OS/네트워크/런타임 바인딩)은 Swarm이 직접 수행하지 않으며, `03_Manifestation/` 계층으로 위임한다.

## 책임 경계: Record_Archive vs Cortex_Agora

- `01_Nucleus/Record_Archive/`는 **사실/증빙**을 보존하는 Nucleus 자산이다(append-only).
- `02_Swarm/Cortex_Agora/`는 Swarm들의 **행동(Behavior Trace)** 을 수집·요약하고 “반복되는 습관”을 **제안**으로 만든다.
- Cortex_Agora는 실행/자동반영/룰수정/에이전트 호출을 하지 않는다.
- Cortex_Agora는 Record_Archive를 직접 읽지 않는다(입력은 Behavior Feed).

## Swarm Observability Standard (Behavior Feed) — 권장/필수

Swarm은 “증빙(Record_Archive)”이 아니라 “행동(Behavior Trace)”을 남긴다.
이 로그는 Cortex_Agora가 관찰하기 위한 입력이며, Nucleus의 Record_Archive로 직접 흘리지 않는다.

### 권장(Recommended)

- 각 Swarm은 자신의 스코프 하위에 Behavior Feed를 둔다:
  - 경로 표준(권장): `<swarm_root>/behavior/BEHAVIOR_FEED.jsonl`
  - 대안(권장): `<swarm_root>/behavior/BEHAVIOR_FEED.md` (append-only; 요약/집계 중심)
- Swarm `DNA.md`/`DNA_BLUEPRINT.md` frontmatter에 아래를 추가(권장):

```yaml
observability:
  behavior_feed:
    path: "<swarm_root>/behavior/BEHAVIOR_FEED.jsonl"
    format: "jsonl"
    append_only: true
    retention_days: 30
```

### 필수(Required)

아래 조건 중 하나라도 만족하는 Swarm은 Behavior Feed를 **필수**로 남긴다.

- Manifestation을 통해 외부 실행 바인딩(툴/OS/네트워크/API)을 트리거하는 경우
- Permission Request(권한 요청) 또는 구조 생성/확장에 관여하는 경우
- Human Gate(인간介入)로 종료되거나, `halt/escalate`로 종료되는 흐름이 존재하는 경우

필수 이벤트(최소):

- `model_select`, `tool_call`, `subagent`, `gate`, `stop`, `retry`, `handoff`
- 이벤트는 최소한 `ts`, `swarm_id`, `group_id`, `kind`, `outcome.status`, `outcome.human_intervention`을 포함한다.

## 필수 원칙

- 군체(Swarm) 구조는 반드시 `DNA.md`(정식) 또는 `DNA_BLUEPRINT.md`(제안)를 가진다. (둘 다 없으면 Non-Canonical)
- Blueprint에는 Natural Dissolution(종료/해체)과 Resource Limits(상한)를 명시한다.
- Blueprint/권한 요청은 Inquisitor의 검증을 전제로 한다.

## 규범 참조(계승) 표준

군체(Swarm) 구조의 `DNA.md`/`DNA_BLUEPRINT.md` frontmatter에 아래 “규범 참조”를 **권장**한다.

```yaml
canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/METADoctrine.md"
immune_doctrine_reference: "04_Agentic_AI_OS/01_Nucleus/Immune_system/AAOS_DNA_DOCTRINE_RULE.md"
inquisitor_reference: "04_Agentic_AI_OS/01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/01_Nucleus/Immune_system/AUDIT_LOG.md"
```

이 참조들은 “면역체계가 어디서부터 상속되는지”를 구조 자체에 각인한다.

## 검증

- Blueprint 검증(권장): `python3 04_Agentic_AI_OS/01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/yaml_validator.py <DNA.md|DNA_BLUEPRINT.md>`
- 전체 스캔 리포트: `python3 04_Agentic_AI_OS/01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py --scan 04_Agentic_AI_OS --format md`
