# Orchestrator -- cortex-agora Skill Governance

## 3-Phase 프로세스

```
Phase 1: Metadata Validation       -> module.metadata-validation
Phase 2: Archive Integrity          -> module.archive-integrity
Phase 3: Consumption Contract       -> module.consumption-contract
```

---

## Phase 1: Metadata Validation

**모듈 로딩**: `metadata-validation`

1. cortex-agora `skills/` 하위 governed skill(instruction-nucleus) 열거
2. SKILL.md frontmatter 체크리스트(FM-01~FM-07) 실행
3. SKILL.meta.yaml sidecar 체크리스트(SC-01~SC-08) 실행
4. 4-Layer 구조 체크(4L-01~4L-08): 현재 flat 구조면 SKIP 기록
5. Phase A/B 정책에 따라 severity 결정

**산출물**: `metadata_checks` 섹션 완성

**분기 규칙**:
- FAIL 항목 존재 → Phase 2 진행 전 사용자에게 FAIL 항목 보고
- FAIL 없음 → Phase 2 직행

---

## Phase 2: Archive Integrity

**모듈 로딩**: `archive-integrity`
**참조 로딩**: change_archive JSONL 3종, templates 3종, bridge script

1. CHANGE_EVENTS.jsonl 스키마 검증(AE-01~AE-08)
2. PEER_FEEDBACK.jsonl 스키마 검증(AF-01~AF-08) + CC-02 참조 무결성
3. IMPROVEMENT_DECISIONS.jsonl 스키마 검증(AD-01~AD-07) + CC-03 참조
4. Bridge script 명령 coverage 검증(AB-01~AB-06)
5. CHANGE_INDEX.md 일관성 검증(AI-01~AI-05)
6. Append-only / 단조증가 불변조건 검증(AM-01~AM-04)

**산출물**: `archive_integrity_checks` 섹션 완성

**분기 규칙**:
- CC-01/CC-02 FAIL (HIGH risk) → 즉시 사용자 보고
- 그 외 → Phase 3 진행

---

## Phase 3: Consumption Contract

**모듈 로딩**: `consumption-contract`
**참조 로딩**: BEHAVIOR_FEED.jsonl, DNA.md, COWI skill 참조

1. BEHAVIOR_FEED.jsonl 스키마 검증(BF-01~BF-10)
2. COWI pull interface 계약 검증(CP-01~CP-08) + CC-05
3. Cross-swarm recording completeness 검증(XR-01~XR-06)

**산출물**: `consumption_contract_checks` 섹션 완성

**분기 규칙**:
- CC-05 FAIL (HIGH risk) → COWI 소비 중단 가능성 flag

---

## 최종 산출물 조합

Phase 1~3 결과를 `30.references/governance_check_report.template.md` 형식으로 통합:

```
governance_check_report:
  metadata_checks:              (Phase 1)
  archive_integrity_checks:     (Phase 2)
  consumption_contract_checks:  (Phase 3)
  registry_sync_status:         (lightweight, single-skill)
  action_items:                 (전체 FAIL/WARN 요약)
  generated_at:                 ISO8601
```

---

## 패턴 감지 (라우팅 최상위 키)

| 패턴 | Phase | 설명 |
|------|-------|------|
| **Validate** | 1 | 메타데이터/구조 정합성 점검 |
| **Integrity** | 2 | 아카이브 데이터 무결성 + append-only 불변조건 |
| **Contract** | 3 | 소비 인터페이스 + cross-swarm recording |
| **Report** | 1-3 | 전체 거버넌스 점검 보고서 생성 |
