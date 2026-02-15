# Glossary

## 도메인 용어

| 용어 | 정의 | 사용 모듈 |
|------|------|-----------|
| mental_model_bundle | 도메인별 멘탈모델 설계 계약서 (JSON). required 9키 + optional 확장 | 전체 |
| domain | 분석/설계 대상 영역 (예: fintech, security-audit) | bundle-contract |
| local_chart | 도메인 내 특정 판단 렌즈/분석 도구 (예: regulation.scan, risk.matrix) | bundle-contract |
| node_chart_map | 워크플로우 노드와 local_chart 간 연결 매핑 | bundle-contract |
| execution_checkpoint | preflight/pre_h1/pre_h2 단계에서의 검증 게이트 | bundle-contract |
| deltaQ (ΔQ) | Reference 로딩 필요도 점수 (0~5+) | loading-policy |
| routing_pattern | Orchestrator가 감지하는 6가지 의도 패턴 | routing-kpi |

## 출력 스키마 용어 (고정)

| 용어 | 정의 |
|------|------|
| 판단 | 분석 결과의 핵심 결론 (1~2문장) |
| 근거 | 판단을 뒷받침하는 데이터/논리/사례 |
| 트레이드오프 | 반대편 리스크/비용/기회비용 |
| 확신도 | 높음/중간/낮음 + 불확실 요인 |

## 패턴 용어 (고정)

| 패턴 | 정의 |
|------|------|
| Evaluate | 평가하고 점수/근거/리스크를 구조화 |
| Critique | 반박/취약점을 찾아 보완 제안 |
| Translate | 프레임 간 번역/재서술 |
| Prioritize | 우선순위화 |
| Arbitrate | 충돌 조정/중재 |
| Simulate | 시나리오 시뮬레이션 |

## 구조 용어 (고정)

| 용어 | 정의 |
|------|------|
| Layer 0 (Core) | 공유 공리/어휘/출력 형식. 항상 로딩 |
| Layer 1 (Module) | 고유 질문 축. 패턴에 따라 선택 로딩 |
| Layer 2 (Reference) | ΔQ ≥ 2일 때만 온디맨드 로딩 |
| Layer 3 (Orchestrator) | 패턴 감지 + 라우팅. 항상 로딩 |
| α (직교성 계수) | 모듈 간 간섭도 (0.5~0.9) |
