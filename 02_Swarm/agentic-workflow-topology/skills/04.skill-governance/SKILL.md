---
name: awt-skill-governance
description: >
  Govern the AWT pipeline skills (00~03) by validating metadata/sidecar contracts,
  inter-skill schema coupling (CC-01~CC-05), and registry consistency.
  Policy + checklist based; no auto-enforcement.
  Use when skill structure changes or contract drift is suspected.
---

# awt-skill-governance

## Purpose

- AWT 4개 설계 스킬(00~03)의 메타데이터, 스킬 간 계약 결합, 레지스트리 정합성을 점검한다.
- 자동 수정 없이 정책+체크리스트 기반으로 운영한다.
- 본 문서는 최소 로더이며 점검 로직은 레이어 모듈 문서에서 수행한다.

## Trigger

- AWT 스킬 구조(디렉토리/파일/스키마) 변경 후 정합성 점검이 필요할 때
- 스킬 간 계약 결합(schema coupling) drift가 의심될 때
- AWT SKILL_REGISTRY.md 또는 SWARM_SKILL_REGISTRY.md 재생성/검증이 필요할 때
- 새 스킬 추가 또는 기존 스킬 deprecation 시 거버넌스 점검

## Non-Negotiable Invariants

- 각 AWT 스킬은 `name`, `description` frontmatter + `SKILL.meta.yaml` sidecar를 가져야 한다.
- `SKILL.meta.yaml`의 `context_id`는 불변이며 frontmatter `name`과 일치해야 한다.
- 4-Layer 필수 디렉토리 누락은 Phase A warning, Phase B error.
- `node_chart_map.chart_ids`의 모든 ID는 `mental_model_bundle.local_charts[].id`에 존재해야 한다.
- `theta_gt_band`를 참조하는 Skill 02는 Skill 01의 `workflow_topology_spec`에 해당 필드가 있어야 한다.
- 자동 수정/자동 차단 금지. 점검 결과를 governance_check_report로 산출한다.

## Layer Index

| Layer | File | Role |
|-------|------|------|
| 00.meta | `00.meta/manifest.yaml` | 거버넌스 메타, 대상 스킬 목록, CC map |
| 10.core | `10.core/core.md` | AWT 거버넌스 원칙, 정의, 출력 형식 |
| 20.modules | `20.modules/modules_index.md` | metadata-validation / contract-sync / registry-runbook |
| 30.references | `30.references/loading_policy.md` | 참조 로딩 트리거 |
| 40.orchestrator | `40.orchestrator/orchestrator.md` | 3-Phase 거버넌스 라우팅 |

## Quick Start

3-Phase 점검 파이프라인:

1. **Phase 1 -- Metadata Validation**: 각 스킬의 frontmatter/sidecar/4-layer 체크리스트 실행
2. **Phase 2 -- Contract Sync**: 5개 inter-skill 결합점(CC-01~CC-05) 정합성 체크리스트 실행
3. **Phase 3 -- Registry Runbook**: AWT 레지스트리 vs 실제 디렉토리 일치 검증

레지스트리 재생성 시 (COF 스크립트 사용):

```bash
python3 02_Swarm/context-orchestrated-filesystem/skills/04.skill-governance/scripts/sync_swarms_skill_manager.py \
  --swarm-root 02_Swarm --dry-run
```

## When Unsure

- frontmatter vs sidecar 충돌 시 `SKILL.meta.yaml`을 식별 SoT로 우선한다.
- 결합점 위반의 심각도가 불명확하면 `warning`으로 기록하고 remediation 항목을 남긴다.
- 정책 충돌은 `00.meta/manifest.yaml` + DNA.md 거버넌스 계약을 따른다.
