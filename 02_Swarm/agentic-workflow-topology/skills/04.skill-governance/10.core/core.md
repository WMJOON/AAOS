# Core -- AWT Skill Governance

## 고정 문장

이 스킬은 AWT 파이프라인을 실행하지 않는다.
스킬 메타데이터, 스킬 간 계약 결합, 레지스트리 정합성을 **점검(Validate)**하고
**보고(Report)**한다. 수정은 사람이 판단한다.

---

## 핵심 정의

| 용어 | 정의 |
|------|------|
| **Governed Skill** | 점검 대상 AWT 스킬 (00~03). 04는 자기 자신이므로 제외. |
| **Contract Coupling (CC)** | 두 스킬 간에 schema key가 생산-소비 관계로 결합된 지점. |
| **CC Risk Level** | HIGH: 누락 시 downstream 실패. MEDIUM: 기능 저하. LOW: cosmetic. |
| **Governance Check Report** | 점검 결과를 표준 형식으로 구조화한 산출물. |
| **SoT Priority** | `SKILL.meta.yaml` > `SKILL.md frontmatter` > `SKILL_REGISTRY.md` |
| **4-Layer Compliance** | 필수 디렉토리(00.meta, 10.core, 20.modules, 30.references, 40.orchestrator, 90.tests) 존재 여부 |

---

## 공유 출력 스키마

모든 점검 결과는 다음 형식으로 구조화한다:

```
{판단, 근거, 트레이드오프, 확신도}
```

- **판단**: PASS / WARN / FAIL + 항목 ID
- **근거**: 어떤 파일의 어떤 필드를 검사했는가
- **트레이드오프**: 해당 위반을 허용할 때의 리스크
- **확신도**: high / medium / low

최종 통합 산출물: `references/governance_check_report.template.md` 형식 사용.

---

## 점검 대상 (Governed Skills)

| # | Skill | Schema Ref | Output Artifact |
|---|-------|-----------|-----------------|
| 00 | mental-model-design | `mental_model_bundle.schema.yaml` | `mental_model_bundle` |
| 01 | topology-design | `workflow_topology_spec.schema.json` | `workflow_topology_spec` |
| 02 | execution-design | `workflow_mental_model_execution_plan.schema.json` | `workflow_mental_model_execution_plan` |
| 03 | observability-evolution | (implicit: IP schema) | `improvement_proposal` |

---

## Contract Coupling Map

| CC ID | From Skill | From Key | To Skill | To Key | Risk |
|-------|-----------|----------|----------|--------|------|
| CC-01 | 00 | `local_charts[].id` | 02 | `node_chart_map[].chart_ids` | HIGH |
| CC-02 | 01 | `theta_gt_band` | 02 | `node_mode_policy` | HIGH |
| CC-03 | 01 | `explicit_output.type` | 02 | mode selection | MEDIUM |
| CC-04 | 02 | `node_chart_map` | 03 | observability baseline | MEDIUM |
| CC-05 | 03 | `improvement_proposal.target_skill` | 01/02 | feedback receiver | HIGH |

---

## Global Invariants

1. 증거 없는 단정 금지 -- 점검 항목에는 반드시 검사 경로와 기대값을 명시한다.
2. 경로/계약 불일치 시 fail-fast -- 파일 누락이나 schema mismatch는 즉시 FAIL.
3. 불확실성은 `when_unsure` 규칙으로 명시.
4. 자동 수정 금지 -- 점검 결과를 보고할 뿐, 파일을 수정하지 않는다.
5. 자기 자신(04) 점검은 manifest + loader 구조만 (계약 결합 해당 없음).

---

## when_unsure 정책

| 상황 | 행동 |
|------|------|
| frontmatter vs sidecar 값 충돌 | `SKILL.meta.yaml`을 SoT로 우선, frontmatter 수정 권고를 WARN으로 기록 |
| 결합점 위반의 심각도 불명확 | warning으로 기록 + remediation 항목 + 수동 검토 요청 |
| 스킬 schema가 양쪽 모두 변경 중 | 양쪽 변경 내역을 나란히 제시, 어느 쪽이 SoT인지 사용자 판단 요청 |
| 레지스트리에 없는 새 스킬 발견 | 레지스트리 갱신 필요를 WARN으로 기록 |
