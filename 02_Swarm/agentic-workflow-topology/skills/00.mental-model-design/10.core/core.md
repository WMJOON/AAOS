<core>
  <purpose>
    도메인별 mental_model_bundle 설계에서 공유하는 공리, 어휘, 출력 형식, 운영 정책을 정의한다.
    모듈은 이 파일의 정의를 재정의하지 않고, 고유 질문 축(delta)만 추가한다.
  </purpose>

  <shared_vocabulary>
    - mental_model_bundle: 도메인별 멘탈모델 설계 계약서 (JSON). required 9키 + optional 확장.
    - domain: 분석/설계 대상 영역.
    - local_chart: 도메인 내 특정 판단 렌즈 (예: regulation.scan, risk.matrix).
    - node_chart_map: 워크플로우 노드와 local_chart 간 연결 매핑.
    - execution_checkpoint: preflight/pre_h1/pre_h2 단계 검증 게이트.
    - bundle_ref: 번들 식별자 (id, version, generated_at).
    - core_axioms: 도메인 공유 공리 목록.
    - module_index: 활성 모듈 메타 정보 배열.
    - loading_policy: deltaQ 기반 참조 로딩 정책.
    - output_contract: 최종 산출물 구조 계약.
  </shared_vocabulary>

  <output_format>
    출력은 항상 다음 스키마를 따라야 한다:

    ## 판단
    [핵심 결론 1~2문장]

    ## 근거
    [데이터/논리/사례 기반 뒷받침]

    ## 트레이드오프
    [반대편 리스크/비용/기회비용]

    ## 확신도
    [높음/중간/낮음] + 불확실 요인: [목록]
  </output_format>

  <bundle_contract_invariants>
    - required 9키(domain, bundle_ref, core_axioms, local_charts, module_index,
      node_chart_map, execution_checkpoints, loading_policy, output_contract)는 항상 유지한다.
    - execution_checkpoints.stage는 preflight|pre_h1|pre_h2만 허용한다.
    - node_chart_map.chart_ids는 빈 배열 금지.
    - optional 확장(layer_contract, routing_policy, cost_model, utility_model,
      kpi_targets, reference_loading_rule)은 하위호환만 허용한다.
  </bundle_contract_invariants>

  <when_unsure_policy>
    - 정보 부족 시, 부족한 항목과 필요 입력을 명시한다.
    - 추정 포함 시, 추정임을 표시하고 가정을 나열한다.
    - 수치 제시 시 출처 또는 추정 근거를 병기한다.
    - 경로/계약 충돌 시 00.meta/manifest.yaml을 SoT로 삼아 정합화한다.
  </when_unsure_policy>

  <orthogonality_principle>
    각 모듈은 자신만의 고유 질문 축을 가진다.
    겹침 발견 시 공통 부분을 이 Core 파일로 올려야 한다.
    모듈 간 직교성 계수 α 목표: ≥ 0.85.
  </orthogonality_principle>

  <fail_fast>
    - 증거 없는 단정 금지.
    - 경로/계약 불일치 시 fail-fast.
    - 불확실성은 when_unsure 규칙으로 명시.
    - schema 위반 발견 시 즉시 에러 보고.
  </fail_fast>
</core>
