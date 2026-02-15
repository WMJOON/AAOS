---
name: awt-mental-model-design
description: Design domain mental models using Four-Layer Orchestrator architecture. Produces backward-compatible `mental_model_bundle` with layer/routing/cost/utility/KPI optional extensions.
---

# awt-mental-model-design

## Purpose
- 도메인별 `mental_model_bundle` 설계 계약을 만든다.
- `SKILL.md`는 최소 로더이며, 상세 규칙은 4-Layer 문서에서 읽는다.

## Trigger
- PF1 답변이 yes여서 멘탈모델 선행 설계가 필요할 때
- topology/execution 설계 전에 chart-map/checkpoint 계약을 정해야 할 때
- high_risk/strategy에서 routing/kpi를 명시해야 할 때

## Non-Negotiable Invariants
- required 9 keys(`domain`~`output_contract`)는 유지한다.
- `execution_checkpoints.stage`는 `preflight|pre_h1|pre_h2`만 허용한다.
- `node_chart_map.chart_ids`는 빈 배열 금지.
- optional 확장(`layer_contract`, `routing_policy`, `cost_model`, `utility_model`, `kpi_targets`, `reference_loading_rule`)은 하위호환만 허용한다.

## Layer Index
| Layer | File | Role |
|---|---|---|
| 00.meta | `00.meta/manifest.yaml` | 레이아웃/검증 정책 |
| 10.core | `10.core/core.md` | 공통 계약/출력 규칙 |
| 20.modules | `20.modules/modules_index.md` | 모듈 실행 인덱스 |
| 30.references | `30.references/loading_policy.md` | deltaQ 로딩 규칙 |
| 40.orchestrator | `40.orchestrator/orchestrator.md` | 패턴 라우팅 제어 |

## Quick Start
```bash
python3 02_Swarm/agentic-workflow-topology/skills/00.mental-model-design/scripts/scaffold.py \
  --domain fintech --output /tmp/mental-pack --modules regulation,risk --packs evidence
```

## When Unsure
- 부족한 입력을 명시하고 가정/확신도를 분리한다.
- 경로/계약 충돌 시 `00.meta/manifest.yaml`을 SoT로 삼아 정합화한다.
- 상세 계산식/예시는 `20.modules/`와 `30.references/` 문서에서만 확장한다.
