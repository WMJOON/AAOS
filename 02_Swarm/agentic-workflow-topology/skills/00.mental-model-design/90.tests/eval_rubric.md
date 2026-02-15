# Evaluation Rubric

## 1. 구조 정합성 (30점)
- 필수 레이어 디렉토리 존재 (00.meta ~ 40.orchestrator)
- manifest.yaml에 layers/io_contract/token_budget/modules 명시
- SKILL.md 120줄 이내 + 필수 5개 섹션 존재

## 2. 번들 계약 준수 (20점)
- 출력이 mental_model_bundle.schema.yaml에 valid
- required 9키 모두 포함
- execution_checkpoints.stage가 허용값만 사용
- node_chart_map.chart_ids 빈 배열 없음

## 3. 라우팅/로딩 정책 일관성 (20점)
- 패턴 감지 정확도 >= 90%
- deltaQ 규칙에 따른 Reference 로딩/스킵 적절성
- workflow_profile.class별 모듈/checkpoint 라우팅 정합성

## 4. 출력 스키마 준수 (20점)
- {판단, 근거, 트레이드오프, 확신도} 4필드 포함
- 모듈 간 출력 형식 통일
- 불확실성 명시 (when_unsure 정책 준수)

## 5. 직교성/토큰 효율 (10점)
- 모듈 간 직교성 계수 alpha >= 0.85
- 토큰 예산 초과 없음 (always_load ~1500, module ~1200, reference ~2000)

## 종합 점수 공식
```
종합 = (구조 × 0.30) + (계약 × 0.20) + (라우팅 × 0.20) + (스키마 × 0.20) + (직교성 × 0.10)
```

통과 기준: >= 85점
