---
name: awt-topology-design
description: >
  Goal → DQ → RSV → Topology → Task Graph 설계.
  θ_GT × RSV 기반으로 비용/루프/hand-off를 최소화하는 Workflow Topology를 산출한다.
  strategy/high-risk 워크플로우는 PF1 preflight + H1/H2 HITL gate를 강제한다.
---

# awt-topology-design

## Purpose

Goal을 5-Phase 프로세스로 분해하여 `workflow_topology_spec` JSON을 산출한다.
리포트가 아닌 **"그래프 구조 + 노드 명세"**를 설계해 반환한다.

## Trigger

- "Topology 설계해줘", "태스크 그래프 만들어줘" 요청 시
- "이 작업을 어떤 구조로 나눠야 하나?", "Topology 뭘로 해야 하나?" 질문 시
- "노드 설계", "RSV 추정", "θ_GT 설정" 관련 요청 시
- Goal이 주어지고 실행 가능한 Workflow Spec이 필요할 때

## Non-Negotiable Invariants

- Task Node 경계는 **Explicit Output**으로만 정의 (내부 추론 기준 분리 금지)
- RSV 일관성: Σ(rsv_target) ≈ RSV_total (±10%)
- 증거 없는 단정 금지, 불확실 시 when_unsure 정책 적용
- strategy/high_risk 시: PF1(`멘탈모델 먼저 세팅할까요?`) + H1/H2 노드 + T4→C1→H1 엣지 필수
- `SKILL.md` 단독 실행 정책 폐기. 레이어 온디맨드 로딩 기본

## Layer Index

| Layer | File | Role |
|-------|------|------|
| 00.meta | `00.meta/manifest.yaml` | 버전, 모듈, 토큰 예산 메타 |
| 10.core | `10.core/core.md` | 핵심 정의(θ_GT/RSV/DQ), 입력 인터페이스, when_unsure |
| 20.modules | `20.modules/modules_index.md` | topology/node/loop_risk/handoff 모듈 |
| 30.references | `30.references/loading_policy.md` | ΔQ 기반 참조 로딩 규칙 |
| 40.orchestrator | `40.orchestrator/orchestrator.md` | 5-Phase 프로세스, 패턴 감지, 라우팅 |

## Quick Start

**설계 흐름** (5-Phase):

```
Phase 1: Goal → DQ 분해 → RSV_total
Phase 2: 3-Signal로 Topology 선택 (→ module.topology_selection)
Phase 3: Task Graph 노드/엣지 설계 (→ module.node_design)
Phase 4: 루프 위험 + Hand-off 분석 (→ module.loop_risk, module.handoff)
Phase 5: Workflow Spec JSON 산출
```

**strategy/high-risk 검증**:

```bash
python3 scripts/validate_strategy_h1_gate.py \
  --workflow-spec /path/to/spec.json \
  --agent-family claude --agent-version 4.0 --proposal-id P-SWARM-XXXX
```

**완성 예시**: `90.tests/golden_outputs/examples.md` (금융 규제 대응, API 검토, 시장 진입 전략)

## When Unsure

- Goal 모호 → "Goal을 구체화해 주세요" + 예시 DQ 제안
- Topology 동점 → 두 후보의 트레이드오프 제시 후 사용자 선택 요청
- θ_GT 불확실 → band 넓게 + "estimator로 보정 권장"
- RSV 과대 의심 → "이 Goal은 2개 Workflow로 분할 검토" 제안
- 상세 규칙은 각 모듈 문서(`20.modules/module.*.md`)를 참조
