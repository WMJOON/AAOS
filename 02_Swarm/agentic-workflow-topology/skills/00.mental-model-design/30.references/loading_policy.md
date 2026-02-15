<loading_policy>
  <principle>
    Reference는 항상 로드하지 않는다.
    수치 검증, 분류 판정, 체크리스트 적용이 필요한 경우에만 로드한다.
  </principle>

  <layer_loading_order>
    1. Layer 3 (Orchestrator) + Layer 0 (Core): 항상 로드. ~1,500tok.
    2. Layer 1 (Modules): 패턴 라우팅 결과에 따라 1~3개 선택 로드. ~1,200tok/개.
    3. Layer 2 (References): deltaQ 규칙 충족 시에만 온디맨드 로드. ~2,000tok/개.
  </layer_loading_order>

  <delta_q_definition>
    deltaQ 점수 규칙:
    - +2: 수치/정량 추정 요청 (예: "TAM 추정", "TRL 등급 판정")
    - +2: 등급/분류 판정 (예: "위험도 분류", "성숙도 평가")
    - +1: "근거/출처/레퍼런스" 요구
    - +1: Critique 패턴에서 근거 부족 감지
    - +1: 모듈의 reference_triggers 키워드 매칭
  </delta_q_definition>

  <loading_rules>
    | deltaQ 범위 | 로딩 판단 |
    |------------|----------|
    | deltaQ < 2 | 로딩 금지. 모듈 시그널만으로 판단. |
    | deltaQ >= 2 | 관련 pack 1개 로딩 고려 |
    | deltaQ >= 4 | pack 1~2개 + sources.bib 확인 |
  </loading_rules>

  <l2_loading_inequality>
    Reference 로딩의 수학적 판단 기준:
    deltaQ/L2 > deltaQ/L1
    즉, Reference 로딩으로 인한 품질 향상이 Module 시그널만으로 얻는 향상보다 클 때만 로딩한다.
  </l2_loading_inequality>

  <available_references>
    | Reference | 파일 | 트리거 키워드 |
    |-----------|------|-------------|
    | mental_model_bundle schema | references/mental_model_bundle.schema.yaml | "스키마", "검증", "required keys" |
    | RACI bridge | references/raci_bridge.md | "RACI", "워크플로우 연결", "역할 매핑" |
  </available_references>
</loading_policy>
