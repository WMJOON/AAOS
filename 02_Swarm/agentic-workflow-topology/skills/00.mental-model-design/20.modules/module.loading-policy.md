<module id="module.loading-policy">
  <meta>
    name: loading-policy
    unique_axis: "번들의 참조 로딩 정책을 deltaQ 기반으로 설계하는가?"
    migration_status: active
  </meta>

  <unique_axis>
    도메인의 정보 밀도와 검증 요구 수준에 맞춰 loading_policy와 reference_loading_rule을 설계한다.
    토큰 비용과 판단 품질 사이의 최적점을 deltaQ 임계값으로 표현한다.
  </unique_axis>

  <decision_rubric>
    1. 도메인 정보 밀도 프로파일링: 수치/정량 판단이 많은 도메인(fintech, biotech)은
       기본 deltaQ 임계값을 낮게(≥1.5), 정성 판단 중심(design, education)은 표준(≥2) 유지.
    2. loading_policy 구조 설계:
       - "loads" 조건: Core + Orchestrator 항상, Module 선택적, Reference 온디맨드.
       - "triggers" 정의: 어떤 키워드/상황이 Reference 로딩을 트리거하는지.
    3. deltaQ 점수 체계 설정:
       - +2: 수치/정량 추정 요청
       - +2: 등급/분류 판정 요청
       - +1: "근거/출처/레퍼런스" 요구
       - +1: Critique 패턴에서 근거 부족 감지
       - +1: 모듈의 reference_triggers 키워드 매칭
    4. 로딩 규칙 테이블:
       - deltaQ < 2: Reference 로딩 금지
       - deltaQ >= 2: 관련 pack 1개 로딩 고려
       - deltaQ >= 4: pack 1~2개 + sources.bib 확인
    5. reference_loading_rule optional 필드 설계:
       - delta_q_thresholds: {no_pack_lt, one_pack_gte, cross_check_gte}
       - l2_loading_inequality: "deltaQ/L2 > deltaQ/L1"
    6. 토큰 예산 정합성: 로딩 시 always_load(~1500) + module(~1200) + reference(~2000) 합계가
       컨텍스트 윈도우 대비 과도하지 않은지 검증.
  </decision_rubric>

  <situation_guide>
    - 정량 데이터가 풍부한 도메인: 기본 pack을 많이 등록하되 deltaQ 임계값은 표준 유지.
    - 정성 판단 중심 도메인: pack 수를 최소화하고 deltaQ >= 3 이상에서만 로딩.
    - 비용 민감 프로젝트: always_load 예산을 줄이고 module_max도 하향 조정.
  </situation_guide>

  <reference_triggers>
    - "토큰 비용", "비용 모델", "예산" → 00.meta/token_budget.md
    - "로딩 조건", "deltaQ" → 30.references/loading_policy.md (self)
  </reference_triggers>
</module>
