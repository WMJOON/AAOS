# Cone Profiles Reference (v1.1)

θ_GT 스펙트럼별 판정 기준, 예시, mode·regime·종료 철학 매핑.

## 1. θ_GT 판정 기준

### L0: 극히 좁음 (θ_GT ≈ 0) — Convergent Regime

- **정답**: 하나. 벗어나면 오류.
- **판정 질문**: "출력이 1가지로 확정되는가?"
- **예시**: JSON 파싱, 규칙 적용, enum 분류, MERGE 쿼리 생성
- **mode**: `validate`
- **종료 타입**: `answer_convergence` — 정답 판정 즉시 종료
- **모델**: Haiku (비용 최적)
- **LLM 설정**: temp=0, structured output, max_tokens 최소화
- **logical_axes**: 보통 1개 (rule_application)

### L1: 좁음 (θ_GT: 0~0.2) — Convergent Regime

- **정답**: 소수의 허용 가능한 출력.
- **판정 질문**: "정답 후보가 3개 이내인가?"
- **예시**: 엔티티 추출, 요약, 번역, 키워드 매칭
- **mode**: `converge`
- **종료 타입**: `answer_convergence` — 결정 안정성 달성 시 종료
- **모델**: Haiku/Sonnet
- **LLM 설정**: temp 0~0.3, 구조화 출력 권장
- **logical_axes**: 1~2개 (entity_matching, boundary_detection 등)
- **종료 조건**: `Δsem(k) < δ_dec` (결정 안정성 단독 충분)

### L2: 중간 (θ_GT: 0.2~0.5) — Verificatory Regime

- **정답**: 다수의 합리적 출력 존재.
- **판정 질문**: "합리적 출력이 3~10개 범위인가?"
- **예시**: 분석, 추론, 구조화, 원인 진단
- **mode**: `diverge` → `converge` (2단계)
- **종료 타입**: `verification_pass` — 검증 기준을 통과하면 종료
- **모델**: Sonnet
- **LLM 설정**: 탐색 시 temp 0.5~0.7, 수렴 시 temp 0.2
- **logical_axes**: 2~4개
- **종료 조건**: 탐색 → 후보 생성 → 검증 기준 통과 여부 판정

### L3: 넓음 (θ_GT: 0.5~0.8) — Deliberative Regime ⭐

- **정답**: 정답 영역이 광범위. "정답 수렴"이 아닌 "충분한 탐색" 확인.
- **판정 질문**: "10개 이상의 서로 다른 합리적 접근이 가능한가?"
- **예시**: 전략 수립, 아이디어 생성, 시장 분석, 프레임 설계
- **mode**: `diverge`
- **종료 타입**: `decision_sufficiency` — 의사결정에 충분한 근거 확보 시 종료
- **모델**: Sonnet/Opus
- **LLM 설정**: temp 0.7~1.0, 자유 출력
- **logical_axes**: 5~7개 (D_min)
- **종료의 의미**: "더 나은 답이 없다"가 아니라 "충분히 탐색하여 판단할 수 있다"

### L4: 정의 불가 (θ_GT: undefined) — Deliberative Regime

- **정답**: 정답 cone 자체가 없음. 또는 cone 바깥에 가치가 존재.
- **판정 질문**: "정답의 기준 자체를 정의할 수 있는가?"
- **예시**: 예술 창작, 근본적 혁신, 패러다임 전환
- **종료 타입**: `decision_sufficiency` — 탐색 충분성만 선언 가능
- **판정**: ⚠️ AI 단독 처리 부적합. 사람 개입 필수.
- **설계**: AI 보조 + 사람 판단의 hybrid

## 2. Regime 분류 체계 (v1.1 신규)

| Regime | θ_GT | 종료 = | 잘못된 해석 ⚠️ |
|--------|------|--------|---------------|
| Convergent | L0, L1 | 정답에 도달함 | — |
| Verificatory | L2 | 기준을 통과함 | "더 좋은 답이 있을 수 있는데 멈춘 것"으로 오인 |
| Deliberative | L3, L4 | 판단에 충분함 | **"수렴 실패"로 오인** ← 가장 위험 |

Deliberative regime의 종료 선언은 "이것이 최선이다"가 아니라 "이 정도면 판단할 수 있다"이다. 이 차이를 출력 언어에 반드시 반영해야 한다.

## 3. 인접 θ_GT 차이(Δθ)별 분할 판단

| Δθ_GT | 판단 | Regime 전환 | 예시 |
|-------|------|-----------|------|
| < 0.1 | 분할 불필요 | 동일 regime | 추출 → 정규화 (둘 다 L1) |
| 0.1~0.3 | 분할 검토 | regime 경계 가능 | 요약 → 분석 (L1 → L2) |
| > 0.3 | 분할 강력 권장 | regime 전환 확실 | 추출 → 전략 추론 (L1 → L3) |

**추가 규칙**: Δθ가 작더라도 regime이 변하면(예: L1→L2) 분할을 검토해야 한다. 종료 철학이 다르기 때문이다.

## 4. 도메인별 θ_GT 레퍼런스

| 도메인 | θ_GT | Regime | 전형적 logical_axes |
|--------|------|--------|-------------------|
| 법률·규정 해석 | L0~L1 | Convergent | rule_application, precedent_matching |
| 의학 진단 보조 | L1 | Convergent | symptom_matching, protocol_adherence |
| 회계·재무 분석 | L1 | Convergent | rule_application, numeric_verification |
| 데이터 ETL | L1~L2 | Conv.→Verif. | extraction, transformation, validation |
| 철학·논리학 | L2 | Verificatory | formal_logic, interpretation, consistency |
| 전략 의사결정 | L3 | Deliberative | risk, feasibility, cost, timeline, stakeholder |
| 리서치·시장 분석 | L3 | Deliberative | market_size, competition, trend, regulation, tech |
| 예술·창작 | L4 | Deliberative | (정의 불가 — hybrid 설계) |

## 5. θ_GT 판정 진단 프롬프트 (v1.1 신규)

θ_GT 판정의 주관성을 줄이기 위한 구조화된 진단:

```
[θ_GT 진단 프롬프트]

이 태스크에 대해 답하라:

1. 이 태스크의 "정답"을 열거할 수 있는가?
   - 1개 → L0
   - 2~3개 → L1
   - 4~10개 → L2
   - 10+개 or 열거 불가 → L3/L4

2. 두 전문가가 독립적으로 수행하면 같은 결과가 나오는가?
   - 거의 동일 → L0~L1
   - 유사하나 표현 차이 → L2
   - 구조적으로 다를 수 있음 → L3
   - 완전히 다를 수 있고 둘 다 유효 → L4

3. 정답 기준(ground truth)을 사전에 정의할 수 있는가?
   - 명확히 가능 → L0~L2
   - 부분적으로 가능 → L3
   - 정의 자체가 불가 → L4

판정 결과: L_ (근거: ...)
```
