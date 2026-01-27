---
type: permission-request
created: "2026-01-27"
requester: "Canon Guardian (human) via Codex"
action: "modify rule/skill"
target: "04_Agentic_AI_OS/METADoctrine.md"
risk_level: high
justification: "METADoctrine의 레거시 경로/집행 스펙 불일치로 인해 참조 무결성과 자동 집행 경로가 흔들리는 문제를 해결하고, Change Packet 동선을 문서에 고정하기 위함."
governance:
  voice: homing_instinct
  mother_ref: "04_Agentic_AI_OS/01_Nucleus/Immune_system/"
emergency:
  is_emergency_security_patch: false
time_bound:
  expires: "2026-02-26"
constraints:
  - "append-only 로그(AUDIT_LOG/META_AUDIT_LOG)는 기존 엔트리를 수정하지 않고 신규 엔트리로만 기록"
  - "문서 참조는 실경로만 사용(레거시/개념 경로는 informative로만 허용)"
  - "COO는 DNA_BLUEPRINT.md만 존재(draft)하므로 DNA.md 존재 서술 금지"
natural_dissolution:
  termination_conditions:
    - "v0.1.11 변경이 롤백되거나 superseded 되면 본 패킷은 record archive로 이관"
  dissolution_steps:
    - "change packet을 Record Archive 패키지로 스냅샷 후 00_Planning/_archive로 이동"
---
# Permission Request: Modify `METADoctrine.md` (v0.1.11)

## Details

- Target: `04_Agentic_AI_OS/METADoctrine.md`
- Scope: reference integrity, swarm registry, auto-enforcement binding, change packet templates/paths, manifestation minimum contract

## Proposed Limits

- 본 변경은 문서 정합성/집행 가능성을 강화하는 범위로 제한한다.
- 실제 코드/스킬 로직 변경은 포함하지 않는다.

## Audit Notes

- 상위기관 변경 게이트(Upper-Institution Change Gate)에 따라 `META_AUDIT_LOG.md` 및 `AUDIT_LOG.md`에 기록한다.
