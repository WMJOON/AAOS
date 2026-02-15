# Orchestrator -- AWT Skill Governance

## 3-Phase 프로세스

```
Phase 1: Metadata Validation  -> module.metadata-validation
Phase 2: Contract Sync        -> module.contract-sync
Phase 3: Registry Runbook     -> module.registry-runbook
```

---

## Phase 1: Metadata Validation

**모듈 로딩**: `metadata-validation`
**참조 로딩**: `skill_system_manifest.schema.yaml` (manifest 검증 시)

1. AWT `skills/` 하위 4개 governed skill 디렉토리 열거
2. 각 스킬에 대해 frontmatter/sidecar/4-layer 체크리스트 실행
3. Phase A/B 정책에 따라 severity 결정
4. 위반 항목을 governance_check_report.metadata_checks에 기록

**산출물**: `metadata_checks` 섹션 완성

**분기 규칙**:
- FAIL 항목 존재 -> Phase 2 진행 전 사용자에게 FAIL 항목 보고
- FAIL 없음 -> Phase 2 직행

---

## Phase 2: Contract Sync

**모듈 로딩**: `contract-sync`
**참조 로딩**: 각 skill의 schema 파일 (references/ 디렉토리)

1. 00.meta/manifest.yaml의 `contract_coupling_map` (CC-01~CC-05) 순회
2. 각 coupling point의 체크리스트 항목 실행
3. schema 파일 교차 검증 (key type, required status, minItems 등)
4. feedback loop closure(CC-05) 검증: Skill 03 -> 01/02 경로 확인
5. 위반 항목을 governance_check_report.dependency_checks에 기록

**산출물**: `dependency_checks` 섹션 완성

---

## Phase 3: Registry Runbook

**모듈 로딩**: `registry-runbook`

1. AWT 로컬 레지스트리 vs 실제 디렉토리 대조
2. Swarm-level 레지스트리 일치 확인
3. cross-swarm context_id 중복 검사
4. 불일치 시 재생성 절차 안내
5. governance_check_report.registry_sync_status 기록

**산출물**: `registry_sync_status` 섹션 완성

---

## 최종 산출물 조합

Phase 1~3 결과를 `references/governance_check_report.template.md` 형식으로 통합:

```
governance_check_report:
  metadata_checks:      (Phase 1)
  dependency_checks:    (Phase 2)
  compatibility_checks: (Phase 2 부산물)
  registry_sync_status: (Phase 3)
  action_items:         (전체 FAIL/WARN 요약)
  generated_at:         ISO8601
```

---

## 패턴 감지 (라우팅 최상위 키)

| 패턴 | Phase | 설명 |
|------|-------|------|
| **Validate** | 1 | 메타데이터/구조 정합성 점검 |
| **Sync** | 2 | 스킬 간 계약 결합 정합성 검증 |
| **Audit** | 3 | 레지스트리 vs 실제 상태 대조 |
| **Report** | 1-3 | 점검 결과 보고서 생성 |
