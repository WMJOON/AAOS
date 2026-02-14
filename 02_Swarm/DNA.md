---
name: "AAOS-Swarm"
version: "0.1.3"
scope: "04_Agentic_AI_OS/02_Swarm"
owner: "AAOS Canon"
created: "2026-01-21"
status: canonical

# Governance (homing instinct)
governance:
  voice: homing_instinct
  mother_ref: "04_Agentic_AI_OS/01_Nucleus/immune_system/"
  precedence:
    - "AAOS Canon"
    - "META Doctrine"
    - "Immune Doctrine"
    - "This document"
  on_conflict: "halt_and_escalate_to_audit"

# Normative References (inherit Immune System)
canon_reference: "04_Agentic_AI_OS/README.md"
meta_doctrine_reference: "04_Agentic_AI_OS/00_METADoctrine/DNA.md"
immune_doctrine_reference: "04_Agentic_AI_OS/01_Nucleus/immune_system/rules/README.md"
inquisitor_reference: "04_Agentic_AI_OS/01_Nucleus/immune_system/SWARM_INQUISITOR_SKILL/"
audit_log_reference: "04_Agentic_AI_OS/01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md"

natural_dissolution:
  purpose: "군체(Swarm) 하위 체계(COF/COO 등)가 생성·성장하는 실행 계층의 컨테이너"
  termination_conditions:
    - "AAOS 군체(Swarm) 계층이 구조적으로 대체될 때"
  dissolution_steps:
    - "하위 체계별로 승계 DNA를 확정하고, 본 컨테이너는 요약본만 남긴다"
    - "구 군체(Swarm) 트리는 `_archive/`로 이동 후 정리"
  retention:
    summary_required: true
    max_days: 365

resource_limits:
  max_files: 2000
  max_folders: 300
  max_log_kb: 1024

inquisitor:
  required: true
  audit_log: "../01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md"
---
# AAOS 군체(Swarm) DNA

본 폴더는 군체(Swarm) 계층의 “루트 컨테이너”이며, 하위 체계는 각자 `DNA.md`를 통해 면역체계를 계승한다.

## Institutional Boundary: record_archive vs cortex-agora

AAOS는 “기억(증빙)”과 “행동 관찰(습관)”을 분리한다.

- `01_Nucleus/record_archive/`는 **Nucleus의 자산**이며, 해석 없이 **사실/증빙을 보존**한다.
- `02_Swarm/cortex-agora/`는 **Swarm의 관찰자**이며, Swarm들의 **행동(Behavior Trace)** 을 수집·요약·제안한다.

### Hard Boundary Rules

- cortex-agora는 record_archive를 **직접 읽지 않는다**.
- cortex-agora의 입력은 “기록”이 아니라 “행동”이다. (Behavior Feed / Behavior Trace)
- cortex-agora의 출력은 “집행/자동반영”이 아니라 **관찰 결과 + 제안**이다.

### Two Kinds of Logs (Conceptual)

| 구분 | 성격 | 소속 | 예시 |
|---|---|---|---|
| record_archive | 사실/증빙(append-only, immutable) | Nucleus | Agent 호출 이벤트, 모델 선택 이벤트, Human Gate 통과 여부, 승인/거부 판정 참조 |
| Behavior Feed | 행동 단위(전이/반복/선택 패턴 중심) | Swarm(Agora 입력) | “불확실성 ↑일 때 Sub-Agent 호출 비율”, “항상 인간介入으로 종료되는 흐름” |

### Governance Flow

Swarm 행동  
→ cortex-agora (관찰·요약·제안)  
→ Human / Deliberation  
→ Rules / Skills (선별적 반영; 승인/승격 필요)

## Swarm Observability Standard (Behavior Feed)

Swarm의 “행동(Behavior Trace)”은 cortex-agora 관찰 입력으로 남긴다.
이는 record_archive(증빙)와 분리된 Swarm 표준이다.

### Recommended (권장)

- 각 Swarm은 자신의 스코프 하위에 Behavior Feed를 둔다.
  - 권장 경로: `<swarm_root>/behavior/BEHAVIOR_FEED.jsonl`
- 각 Swarm의 `DNA.md` frontmatter에 `observability.behavior_feed`를 기록한다.

### Required (필수)

아래 중 하나라도 해당하면 Behavior Feed는 필수이다.

- Manifestation 트리거(외부 실행 바인딩)가 발생하는 Swarm
- Permission Request 또는 구조 생성/확장에 관여하는 Swarm
- `halt/escalate` 또는 Human Gate로 종료되는 흐름이 존재하는 Swarm

필수 최소 이벤트는 `02_Swarm/cortex-agora/DNA.md`의 `Behavior Feed (Behavior Trace)` 섹션을 따른다.

## Version Note

- v0.1.0 : 군체(Swarm) 루트 컨테이너 DNA 최초 성문화
- v0.1.1 : governance.voice=homing_instinct 및 mother_ref(모체) 기반 귀속 규칙 추가
- v0.1.2 : record_archive(사실/증빙) vs cortex-agora(행동 관찰/제안) 책임 경계 및 입력/출력 규약 명문화
- v0.1.3 : Swarm Observability Standard(Behavior Feed) 권장/필수 표준 추가
