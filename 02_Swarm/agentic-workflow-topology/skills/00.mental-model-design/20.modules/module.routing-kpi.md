<module id="module.routing-kpi">
  <meta>
    name: routing-kpi
    unique_axis: "패턴 라우팅 규칙과 운영 KPI 목표를 도메인에 맞게 설계하는가?"
    migration_status: active
  </meta>

  <unique_axis>
    도메인의 의사결정 패턴 분포를 분석하여 routing_policy를 설계하고,
    토큰 절감/직교성/라우팅 정확도/효용 개선을 측정하는 kpi_targets를 정의한다.
  </unique_axis>

  <decision_rubric>
    1. 도메인 패턴 분포 분석: 6가지 패턴(Evaluate, Critique, Simulate, Translate,
       Prioritize, Arbitrate) 중 도메인에서 빈번하게 발생하는 패턴을 식별한다.
    2. routing_policy 설계:
       - patterns: 도메인에서 사용할 패턴 목록.
       - default_pattern: 모호한 입력 시 기본 패턴 (대부분 Evaluate).
       - pattern_confidence: 라우팅 판정 최소 신뢰도 (0.7~0.9).
       - combination_rules: 패턴별 모듈 조합 + 실행 모드 매핑.
    3. 패턴-모듈 조합 규칙:
       - Evaluate: 관련 모듈 1~2개 병렬, 각 렌즈 독립 판단.
       - Critique: 타겟 모듈 1개 생성 → 공격 모듈 1개 검증.
       - Translate: 원본 프레임 모듈 → 대상 프레임 모듈.
       - Prioritize: 핵심 모듈 1개 심층 분석.
       - Arbitrate: 상충 모듈 2개 → 조건부 결론.
       - Simulate: 페르소나 모듈 2~3개 병렬 시뮬레이션.
    4. kpi_targets 설정:
       - token_reduction_rate: >= 0.6 (풀로딩 대비 60% 절감)
       - alpha_min: >= 0.85 (직교성 계수)
       - routing_accuracy_min: >= 0.9 (패턴 감지 정확도)
       - utility_gain_min: >= 3.0 (효용 개선 배수)
    5. cost_model optional 필드:
       - variables: [Omega, L0, L1, L2, D_i, m_i, P, O, r, delta]
       - formulas: step_cost, total_cost, optimal_window
    6. utility_model optional 필드:
       - alpha, q1, q2, token_cost → utility_score = alpha * q1 * q2 / token_cost
  </decision_rubric>

  <situation_guide>
    - strategy/high_risk 도메인: 모든 6패턴을 등록하고 combination_rules를 상세 정의.
      kpi_targets에 cost_model, utility_model을 포함.
    - general 도메인: Evaluate + Prioritize + Arbitrate 3패턴 중심.
      kpi_targets만 포함하고 cost_model은 선택.
    - minimal 도메인: default_pattern만 설정. kpi_targets 미포함 가능.
  </situation_guide>

  <reference_triggers>
    - "비용 모델", "토큰 절감" → 00.meta/token_budget.md
    - "직교성", "alpha" → 10.core/core.md (orthogonality_principle)
    - "RACI 매핑", "역할 배정" → ref.raci-bridge
  </reference_triggers>
</module>
