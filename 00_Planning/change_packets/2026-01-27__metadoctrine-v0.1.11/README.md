# Change Packet: METADoctrine v0.1.11

## Target

- Canonical: `../../../../METADoctrine.md`

## Summary

- 레거시(개념) 경로 제거/정합화: 실제 repo 경로만 사용하도록 정리
- Swarm 레지스트리 정합화: COF/COO의 현행 `02_Swarm/` 구조 반영(COO는 `DNA_BLUEPRINT.md`만 존재)
- Auto-Enforcement 바인딩 강화: Inquisitor Core 스크립트의 실제 경로를 METADoctrine에 고정
- Change Packet 동선 명시: 템플릿/보관 위치 링크를 METADoctrine에 추가
- Manifestation 최소 계약 명문화: `03_Manifestation/` 계층의 실행 바인딩(Non-Cognition) 최소 스키마/유형을 METADoctrine에 추가

## Applied Edits (핵심)

### Reference Integrity

- `AAOS_META_CANON/README.md` → `04_Agentic_AI_OS/README.md`
- `AAOS_META_DNA/METADoctrine.md`(개념 경로) → 제거 또는 `04_Agentic_AI_OS/METADoctrine.md`로 교체

### Auto-Enforcement Tools

- `yaml_validator.py`, `auto_inquisitor.py`, `dissolution_monitor.py`, `audit.py`를
  `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/` 아래 실제 경로로 명시
  - 주요 CLI 예시를 METADoctrine에 추가

### Swarm Registry

- COF: `02_Swarm/Context-Orchestrated-Filesystem/` 기반으로 링크 교정
- COO: `02_Swarm/Context-Orchestrated-Ontology/DNA_BLUEPRINT.md`만 존재(draft)임을 반영 (`DNA.md` 서술 제거)

### Change Packet Where/Templates

- Planning change packets: `00_Planning/change_packets/`
- Deliberation packet template: `01_Nucleus/Record_Archive/templates/DELIBERATION_PACKET_TEMPLATE.md`
- Immune templates:
  - `01_Nucleus/Immune_system/templates/DNA-BLUEPRINT-TEMPLATE.md`
  - `01_Nucleus/Immune_system/templates/PERMISSION-REQUEST-TEMPLATE.md`

## Evidence

- Permission request: `PERMISSION_REQUEST.md`
- Deliberation packet (draft): `DELIBERATION_PACKET.md`
- META audit log: `../../../../01_Nucleus/Immune_system/META_AUDIT_LOG.md`
- Inquisitor audit log: `../../../../01_Nucleus/Immune_system/AUDIT_LOG.md#5f62697f78e36003`

## References

- Blueprint (critic + 개선안): `../../METADoctrine_BLUEPRINT.md`
