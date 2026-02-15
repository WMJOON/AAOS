---
name: aaos-cortex-agora
description: Swarm 행동(Behavior Trace)을 관찰·요약하고 “반복되는 습관/패턴”을 제안 형태로 언어화하는 관찰/제안 군체. 실행/자동반영은 하지 않는다.
---
# cortex-agora

`02_Swarm/cortex-agora/`는 Swarm들의 행동을 관찰하고, 반복되는 흐름을 **제안**으로 변환하는 관찰/제안 계층이다.
핵심 역할은 "작업공간 중심 관찰자(workspace observer)"이며, 실행 계층이 아니다.

## 핵심 선언

- record_archive는 Nucleus의 자산이며 “사실/증빙”을 보존한다.
- cortex-agora는 Swarm의 “행동(Behavior Trace)”을 관찰한다.
- cortex-agora는 실행/자동반영/룰수정/에이전트 호출을 하지 않는다.
- cortex-agora output 우선 원칙에 따라 `context-orchestrated-workflow-intelligence`가 1차 소비한다.
- 동일 출력은 Deliberation/COF/AWT 등 다수 소비자가 재사용할 수 있다.
- Behavior Feed는 Agora-First로 수집·관찰한다.

## Inputs / Outputs

- Input: Behavior Feed (행동 이벤트/전이/중단/인간介入 신호)
- Output: 관찰 결과(반복) + 해석(가능성) + 제안(선택지)

### Output Consumption Model

- Primary consumer: `02_Swarm/context-orchestrated-workflow-intelligence`
- Reusable consumers: `01_Nucleus/deliberation_chamber`, `02_Swarm/context-orchestrated-filesystem`, `02_Swarm/agentic-workflow-topology`
- 소비 방식: downstream이 cortex-agora 산출물을 pull(download)하여 재사용한다.
- 우선순위 원칙: downstream 개선안은 cortex-agora 출력(`agora_ref`)을 source-of-truth로 사용한다.
- COWI pull trigger: `IMPROVEMENT_DECISIONS` 신규 이벤트 발생 시 + 일일 수동 배치 1회
- COWI runbook: `02_Swarm/context-orchestrated-workflow-intelligence/skills/00.agora-consumption-bridge/scripts/pull_agora_feedback.py`

## Change Archive Device

cortex-agora는 변경기록/비판/개선 결정을 로컬 append-only 이벤트로 보존한다.
장기 immutable SoT는 `record_archive seal` 결과이며, cortex-agora는 `stage_then_seal` 브릿지로 주기 봉인한다.

- local log root: `02_Swarm/cortex-agora/change_archive/`
- events:
  - `events/CHANGE_EVENTS.jsonl`
  - `events/PEER_FEEDBACK.jsonl`
  - `events/IMPROVEMENT_DECISIONS.jsonl`
- index: `indexes/CHANGE_INDEX.md`
- bridge tool: `scripts/change_archive_bridge.py`

### Optional Critique Policy

- 비판/리뷰는 권장이며 필수 차단 게이트가 아니다(optional critique).
- feedback 없이도 decision 기록은 가능하다.
- feedback이 존재하면 `feedback_refs`로 역추적 가능해야 한다.

### Bridge to Record Archive

1. `record-change` / `record-feedback` / `record-decision`으로 로컬 append-only 기록
2. `build-package`로 기간별 staging package 생성
3. `stage_then_seal` 정책으로 승인된 패키지에 대해 `seal-to-record-archive` 실행
4. `CHANGE_INDEX.md`에 `record_archive_package_ref`를 반영

## Canonical Reference

- DNA: `04_Agentic_AI_OS/02_Swarm/cortex-agora/DNA.md`
- Swarm Root: `04_Agentic_AI_OS/02_Swarm/README.md`
- Nucleus Root: `04_Agentic_AI_OS/01_Nucleus/README.md`
