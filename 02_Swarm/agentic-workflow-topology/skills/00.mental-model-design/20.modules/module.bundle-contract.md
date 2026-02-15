<module id="module.bundle-contract">
  <meta>
    name: bundle-contract
    unique_axis: "번들의 9키 구조를 도메인에 맞게 설계하고, optional 확장 포함 여부를 결정하는가?"
    migration_status: active
  </meta>

  <unique_axis>
    도메인 입력(domain, intent, constraints)으로부터 mental_model_bundle의 필수 9키를 구체화하고,
    workflow_profile.class(strategy/general/minimal)에 따라 optional 확장 포함 범위를 결정한다.
  </unique_axis>

  <decision_rubric>
    1. domain 해석: 입력된 domain을 judgability 기준으로 해석한다. 어떤 판단이 필요한 영역인지 명시.
    2. core_axioms 도출: 도메인에서 반복적으로 참인 공리를 3~7개 추출한다.
    3. local_charts 정의: 도메인 내 필요한 판단 렌즈를 chart로 정의한다.
       각 chart에는 id, purpose, selection_rule이 필수.
    4. module_index 구성: 활성 모듈 목록과 각각의 question_axis를 기술한다.
    5. node_chart_map 매핑: 워크플로우 노드(T1, T2, C1, H1 등)에 chart를 연결한다.
       chart_ids 빈 배열 금지.
    6. execution_checkpoints 설정: strategy/high_risk는 preflight+pre_h1+pre_h2 3단계,
       general은 preflight+pre_h1, minimal은 preflight만.
    7. optional 확장 결정: workflow_profile.class에 따라 아래 포함 여부 판단.
       - strategy/high_risk: layer_contract, routing_policy, cost_model, utility_model, kpi_targets, reference_loading_rule 모두 권장
       - general: routing_policy, kpi_targets 권장
       - minimal: optional 미포함도 유효
  </decision_rubric>

  <situation_guide>
    - PF1 응답에서 "멘탈모델 선행 설계 필요"로 판정된 경우 이 모듈이 주 모듈.
    - topology/execution 설계 전 단계에서 chart-map/checkpoint 계약을 확정해야 할 때.
    - 기존 번들을 확장할 때는 required 9키 불변 원칙을 먼저 확인.
  </situation_guide>

  <reference_triggers>
    - "스키마", "required keys", "검증" → ref.mental-model-bundle-schema
    - "RACI", "워크플로우 연결" → ref.raci-bridge
  </reference_triggers>
</module>
