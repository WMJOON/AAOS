# Routing Rules — Mental Model Design

## 1. Entry Point Routing

### PF1 Preflight Gate
모든 요청은 PF1 질문으로 시작한다: **"멘탈모델 먼저 세팅할까요?"**

| PF1 응답 | 라우팅 | 비고 |
|---|---|---|
| yes | 이 스킬 진입 → Phase 2 (Intent Classification) | 표준 경로 |
| no | 01.topology-design으로 직행 | bundle 없이 topology 설계 |
| 이미 bundle 있음 | bundle 버전 확인 → 수정/검증 모드 진입 | 기존 bundle 재활용 |

### 직접 진입 (PF1 생략)
- topology/execution 설계 중 "chart-map이 없다" 에러 → 이 스킬로 역참조 진입.
- 기존 bundle이 있으나 도메인 변경 → 새 bundle 설계 모드.

## 2. Intent → Pattern Mapping

| Pattern | 의도 | 트리거 키워드 | 기본 신뢰도 |
|---|---|---|---|
| Evaluate | 번들 설계를 평가/검증 | "평가", "검토", "검증", "분석" | 0.85 |
| Critique | 기존 번들의 약점 공격 | "비판", "허점", "반박", "위험" | 0.80 |
| Translate | 한 도메인을 다른 관점으로 재해석 | "변환", "관점으로", "재해석" | 0.80 |
| Prioritize | 번들 요소 중 핵심 우선순위화 | "우선순위", "핵심", "먼저" | 0.85 |
| Arbitrate | 설계 옵션 간 트레이드오프 조정 | "비교", "트레이드오프", "vs" | 0.75 |
| Simulate | 도메인 시나리오로 유효성 시뮬레이션 | "시나리오", "시뮬레이션", "가정하고" | 0.80 |

### 패턴 우선순위 규칙
1. 명시적 키워드가 있으면 해당 패턴을 우선한다.
2. 키워드가 모호하면 **Evaluate**를 기본값으로 사용한다.
3. 복합 요청은 **주 패턴 + 부 패턴**으로 분리한다 (예: "번들 평가하고 약점도 찾아줘" → Evaluate + Critique).
4. `pattern_confidence < 0.7`이면 사용자에게 의도를 확인한다.

## 3. Pattern → Module Routing

| Pattern | 활성 모듈 | 실행 모드 |
|---|---|---|
| Evaluate | bundle-contract + loading-policy 병렬 | 각 렌즈 독립 판단 |
| Critique | bundle-contract 생성 → routing-kpi 검증 | 적대적 순차 검증 |
| Translate | 원본 프레임 모듈 → 대상 프레임 모듈 | 프레임 변환 |
| Prioritize | bundle-contract 단독 심층 | 깊이 분석 |
| Arbitrate | loading-policy vs routing-kpi 트레이드오프 | 상충점 추출 후 조건부 결론 |
| Simulate | 3개 모듈 페르소나로 도메인 시나리오 | 병렬 시뮬레이션 |

### 요청 유형별 모듈 조합

| 요청 유형 | 활성 모듈 | 근거 |
|---|---|---|
| 새 번들 설계 (전체) | bundle-contract + loading-policy + routing-kpi | 9키 + optional 전체 설계 |
| 새 번들 설계 (기본) | bundle-contract + loading-policy | 9키 + 로딩 정책만 |
| 번들 구조 검토/수정 | bundle-contract 단독 | 구조 변경만 |
| 로딩 정책 설계/수정 | loading-policy 단독 | deltaQ/참조 관리만 |
| 라우팅/KPI 설계/수정 | routing-kpi 단독 | 패턴/성능 지표만 |
| 전체 번들 검증 | bundle-contract + loading-policy + routing-kpi | 교차 검증 |
| 번들 비교/트레이드오프 | loading-policy + routing-kpi | 비용 vs 성능 |

## 4. workflow_profile.class별 기본 라우팅

| Class | 기본 패턴 | 기본 모듈 | Checkpoint | Optional 확장 |
|---|---|---|---|---|
| strategy / high_risk | Evaluate + Critique | 3개 전부 | preflight + pre_h1 + pre_h2 | 6개 전부 권장 (`layer_contract`, `routing_policy`, `cost_model`, `utility_model`, `kpi_targets`, `reference_loading_rule`) |
| general | Evaluate | bundle-contract + loading-policy | preflight + pre_h1 | `routing_policy`, `kpi_targets` 권장 |
| minimal | Prioritize | bundle-contract 단독 | preflight | optional 미포함 가능 |

### Optional 확장 결정 로직
```
IF workflow_profile.class == strategy OR high_risk:
  → routing-kpi 모듈 활성화
  → cost_model, utility_model 포함
  → kpi_targets 필수

ELIF workflow_profile.class == general:
  → routing-kpi는 사용자 요청 시만 활성화
  → routing_policy, kpi_targets 권장
  → cost_model 선택

ELSE (minimal):
  → bundle-contract만으로 충분
  → optional 확장 포함 시 사용자 명시 필요
```

## 5. deltaQ 기반 Reference 로딩 라우팅

> loading_policy.md의 deltaQ 규칙을 라우팅 의사결정에 통합한다.

| 라우팅 시점 | deltaQ 계산 | 로딩 판단 |
|---|---|---|
| Module 실행 중 수치/정량 요청 감지 | +2 | `deltaQ ≥ 2` → schema 로딩 고려 |
| Critique 패턴에서 근거 부족 감지 | +1 (누적) | `deltaQ ≥ 2` → 관련 pack 로딩 |
| "RACI", "역할 매핑" 키워드 | +1 (누적) | `deltaQ ≥ 2` → raci_bridge 로딩 |
| 등급/분류 판정 요청 | +2 | 즉시 관련 reference 로딩 |

**로딩 부등식 검증**: Reference 로딩은 `deltaQ/L2 > deltaQ/L1`일 때만 정당화된다.
즉, Reference가 Module 시그널만으로는 도달할 수 없는 품질 향상을 제공해야 한다.

## 6. Downstream 계약 인식

이 스킬의 output `mental_model_bundle`은 다음 스킬에 소비된다:

| Downstream Skill | 소비하는 키 | 라우팅 시 검증 사항 |
|---|---|---|
| 01.topology-design | `charts`, `execution_checkpoints`, `node_chart_map` | chart_ids 빈 배열 금지, checkpoint stage 유효성 |
| 02.execution-design | `bundle_ref` (전체 bundle) | id + version + generated_at 필수 |

**라우팅 체크포인트**:
- 번들 생성 완료 시 downstream 소비 계약을 자동 검증한다.
- `node_chart_map.chart_ids`가 빈 배열이면 완료 불가.
- `execution_checkpoints.stage`가 허용 값(`preflight|pre_h1|pre_h2`) 외이면 완료 불가.

## 7. 충돌 처리

| 충돌 유형 | 처리 방식 |
|---|---|
| 모듈 간 상충 결론 | **Arbitrate 패턴**으로 전환 → 조건부 결론 제시 |
| loading-policy vs routing-kpi | 예: "참조팩 추가" 권장 vs "토큰 예산 초과" 경고 → 트레이드오프 구조화 |
| schema 위반 감지 | 즉시 에러 보고, 계속 진행 금지 |
| 입력 부족 | when_unsure 정책: 가정을 명시하고 필요 입력을 요청 |
| high_risk checkpoint 미통과 | 다음 단계 진행 금지, 실패 사유 보고 |

## 8. 라우팅 시나리오 예시

### 예시 A — Fintech 도메인, strategy class
```
입력: "fintech 도메인 멘탈모델을 설계해줘. 규제 리스크가 높아."
→ PF1: yes (이미 진입)
→ Intent: Evaluate (설계 요청)
→ Class: strategy (high_risk 키워드)
→ 모듈: bundle-contract + loading-policy + routing-kpi (3개 전부)
→ Optional: 6개 전부 포함
→ Checkpoint: preflight + pre_h1 + pre_h2
→ deltaQ: "규제" → +2 (등급 판정) → schema 로딩
```

### 예시 B — Education 도메인, minimal class
```
입력: "교육 커리큘럼 멘탈모델 기본 구조만 빠르게."
→ PF1: yes
→ Intent: Prioritize ("기본", "빠르게")
→ Class: minimal
→ 모듈: bundle-contract 단독
→ Optional: 미포함
→ Checkpoint: preflight만
→ deltaQ: 0 → reference 로딩 없음
```

### 예시 C — 기존 번들 비평
```
입력: "이 번들 허점 찾아줘. 비용 효율도 점검해."
→ PF1: 기존 bundle 있음 → 수정/검증 모드
→ Intent: Critique + Arbitrate (복합)
→ 모듈: bundle-contract → routing-kpi (적대적 검증 + 비용 트레이드오프)
→ deltaQ: "비용" → +1, Critique 근거 부족 → +1 = 2 → pack 로딩 고려
```
