<orchestrator>
  <purpose_detection>
    사용자 입력에서 목적 신호를 감지하고 패턴을 판정한다.
    이 스킬은 mental_model_bundle "설계"를 수행하므로, 입력의 intent/constraints/workflow_profile을 분석하여
    어떤 모듈 조합이 필요한지 결정한다.
  </purpose_detection>

  <patterns>
    | 패턴 | 의도 | 트리거 키워드 |
    |------|------|-------------|
    | Evaluate | 번들 설계를 평가/검증 | "평가", "검토", "검증", "분석" |
    | Critique | 기존 번들/계약의 약점 공격 | "비판", "허점", "반박", "위험" |
    | Translate | 한 도메인 번들을 다른 관점으로 재해석 | "변환", "관점으로", "재해석" |
    | Prioritize | 번들 요소 중 핵심을 우선순위화 | "우선순위", "핵심", "먼저" |
    | Arbitrate | 설계 옵션 간 트레이드오프 조정 | "비교", "트레이드오프", "vs" |
    | Simulate | 도메인 시나리오로 번들 유효성 시뮬레이션 | "시나리오", "시뮬레이션", "가정하고" |
  </patterns>

  <routing>
    1. Layer 0(Core)는 항상 로드한다.
       → 공유 어휘, 출력 형식, bundle 불변 계약을 보장.
    2. Layer 1(Module)은 modules_index.md를 참조하여 1~3개 선택 로드한다.
       → 번들 설계 요청: bundle-contract 필수 + loading-policy or routing-kpi 선택.
       → 전체 번들 설계: 3개 모듈 모두 활성.
       → 부분 수정: 해당 모듈만 활성.
    3. Layer 2(References)는 loading_policy.md의 deltaQ 규칙에 따라 로드한다.
       → deltaQ >= 2: schema 또는 raci_bridge 로드 고려.
  </routing>

  <execution_flow>
    1. Intent classification: 입력에서 패턴을 감지한다.
    2. Module routing: 패턴 + 입력 내용으로 활성 모듈을 결정한다.
    3. Reference loading decision: deltaQ를 계산하여 참조 로딩 여부를 판단한다.
    4. Module execution: 선택된 모듈의 decision_rubric에 따라 판단을 수행한다.
    5. Contract output assembly: Core의 출력 형식(판단/근거/트레이드오프/확신도)으로 조립한다.
    6. Conflict resolution: 모듈 간 상충 시 Arbitrate 패턴으로 전환하여 조건부 결론 제시.
  </execution_flow>

  <workflow_class_routing>
    workflow_profile.class에 따라 번들 구성이 달라진다:
    - strategy/high_risk: 3개 모듈 모두 활성. optional 확장 전체 포함 권장. checkpoint 3단계.
    - general: bundle-contract + 1개 모듈. routing_policy/kpi_targets 권장. checkpoint 2단계.
    - minimal: bundle-contract 단독. optional 미포함 가능. checkpoint 1단계.
  </workflow_class_routing>
</orchestrator>
