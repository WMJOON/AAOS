# Golden Outputs — awt-mental-model-design

## Example A: Strategy / High Risk

입력 요약:
- domain: fintech strategy
- intent: regulation response decision
- workflow_profile.class: strategy

출력 핵심:
- execution_checkpoints: preflight, pre_h1, pre_h2
- node_chart_map: T1/T2/T4/C1/H1/H2 chart 매핑
- layer_contract: L3/L0 always, L1 selective, L2 on-demand
- routing_policy: Evaluate + Critique 조합, pattern_confidence 기록
- loading_policy: deltaQ 기준 명시
- reference_loading_rule: `deltaQ/L2 > deltaQ/L1`
- cost_model: `C_i`, `T_total`, `K*` 메타 포함
- utility_model: alpha/q1/q2/token_cost/utility_score 포함
- kpi_targets: token 절감, alpha, 라우팅 정확도, 효용 개선 목표
- quality_gate: checkpoint consistency / mapping completeness / minimal loading

## Example B: General Workflow

입력 요약:
- domain: backend engineering
- intent: API design review
- workflow_profile.class: general

출력 핵심:
- execution_checkpoints: preflight 중심
- node_chart_map: 보안/성능/호환성 노드 최소 매핑
- routing_policy: Prioritize 또는 Evaluate 단일/병렬 선택
- loading_policy: deltaQ<2 no-pack, deltaQ>=2 selective
- compat: consumers hint 포함 가능

## Example C: Minimal Backward-Compatible Bundle

입력 요약:
- domain: infra ops
- intent: on-call runbook 개선
- include_required_only: true

출력 핵심:
- required 9키만 포함해도 schema valid
- 아키텍처 optional 필드는 미포함이어도 유효
- 기존 소비자(`01.topology-design`, `02.execution-design`) 파싱 영향 없음
