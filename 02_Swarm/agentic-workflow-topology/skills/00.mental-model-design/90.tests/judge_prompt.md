# Judge Prompt (Self-Evaluation)

아래 기준으로 출력 품질을 자체 평가한다.

1. **패턴 감지**: 입력에서 올바른 패턴(Evaluate/Critique/Translate/Prioritize/Arbitrate/Simulate)을 감지했는가?
2. **모듈 선택**: modules_index.md와 routing_rules.md에 따라 적절한 모듈이 활성화되었는가?
3. **출력 스키마**: {판단, 근거, 트레이드오프, 확신도}를 모두 포함하는가?
4. **번들 계약**: 출력이 mental_model_bundle.schema.yaml의 required 9키를 만족하는가?
5. **Reference 로딩**: deltaQ 규칙에 따라 적절히 로딩/스킵했는가?
6. **직교성**: 다중 모듈 사용 시 각 모듈의 결론이 서로 다른 질문 축에서 도출되었는가?
7. **workflow class 정합**: workflow_profile.class에 맞는 모듈/checkpoint/optional 구성인가?

각 항목을 Pass/Partial/Fail로 판정한다.

| 종합 등급 | 기준 |
|----------|------|
| A | 7개 항목 모두 Pass |
| B | 5~6개 Pass, 나머지 Partial |
| C | 4개 이하 Pass 또는 Fail 1개 이상 |
