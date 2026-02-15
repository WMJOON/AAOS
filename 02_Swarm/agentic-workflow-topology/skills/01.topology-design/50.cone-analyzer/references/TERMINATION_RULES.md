# Termination Rules Reference (v1.1)

종료는 실패가 아니라 설계 결과이며, 판단의 포기가 아니라 판단의 완성이다.

## 0. 핵심 원칙

종료 선언(Termination Declaration)은 모든 노드의 **1급 산출물**이다.
"종료할 수 있다"가 아니라 "종료한다, 그리고 이것이 그 이유다"를 출력해야 한다.

**Termination Declaration 표준 형식:**

```json
{
  "termination_status": "terminate | continue",
  "termination_type": "answer_convergence | verification_pass | decision_sufficiency",
  "termination_rationale": {
    "orthogonality_score": "<float: 새 축의 한계직교성>",
    "semantic_expansion_delta": "<float: 의미 공간 확장률>",
    "decision_sensitivity": "<low | medium | high: 결론이 추가 탐색에 얼마나 민감한가>",
    "axes_explored": ["<탐색된 logical axes 목록>"],
    "axes_remaining_estimate": "<int: 미탐색 추정 축 수>"
  },
  "justification": "<자연어 종료 근거>"
}
```

## 1. Regime별 종료 전략

### 1.1 Convergent Regime (L0, L1) — `answer_convergence`

**종료의 의미**: 정답에 도달했다.

| Mode | 종료 조건 | 비고 |
|------|----------|------|
| `validate` (L0) | 즉시 종료 (1회 판정) | boolean 출력. 반복 없음. |
| `converge` (L1) | `Δsem(k) < δ_dec` | 결정 안정성 단독 충분 |

Converge 노드 반복 종료 조건 (v1.1 강화):

```
Terminate_converge(k) =
  Δsem(k) < δ_dec                    ← 결론이 안정화됨
  AND k ≥ 2                           ← 최소 2회 시도
  AND confidence(R(k)) > τ_conf       ← 자기 확신도 임계값
```

**오탐 방지**: k=1에서 안정성 달성 시에도 최소 1회 추가 확인.

### 1.2 Verificatory Regime (L2) — `verification_pass`

**종료의 의미**: 검증 기준을 통과했다.

```
Terminate_verificatory(k) =
  candidates(k) ≥ N_min               ← 최소 후보 수 확보
  AND verification_score(best) > τ     ← 최선 후보가 기준 통과
  AND margin(best, second) > δ_margin  ← 차선과 유의미한 차이
```

**`diverge→converge` 2단계 실행:**
1. Diverge phase: 후보 생성 (N_min개 이상)
2. Converge phase: 후보 평가 + 최선 선택 + 검증 기준 통과 확인

종료 선언 시, 탈락 후보와 그 이유도 명시해야 한다.

### 1.3 Deliberative Regime (L3, L4) — `decision_sufficiency` ⭐

**종료의 의미**: 의사결정에 충분한 근거를 확보했다.

이 regime에서의 종료는 "최선의 답을 찾았다"가 **아니다**. "충분히 탐색하여 합리적으로 판단할 수 있는 상태에 도달했다"이다.

```
Terminate_deliberative(k) =
  D(k) ≥ D_min(θ_GT)                              ← 사전조건: 최소 차원 확보
  AND orthogonality(n_k, {n_1..n_{k-1}}) < ε       ← ⭐ 핵심: 직교성 0 수렴
  AND (ΔC(k) < δ_cov  OR  Δsem(k) < δ_dec)        ← 보조: 커버리지 or 결정 안정성
  AND 쿨다운(연속 w회 포화)                           ← 안전: 비단조 패턴 대응
```

**핵심 차이점 (v1.0 → v1.1)**:
- v1.0: 차원 포화가 핵심 트리거, 직교성은 암묵적
- v1.1: **직교성 0 수렴이 핵심 트리거**, 차원 포화는 그 프록시

## 2. 직교성(Orthogonality) 모델 (v1.1 신규)

### 2.1 정의

```
orthogonality(n_k, {n_1..n_{k-1}}) =
  "k번째 반복이 기존 반복들과 독립적인 새로운 판단 축을 추가하는 정도"

  = max(0, 1 - max_similarity(axes(n_k), axes({n_1..n_{k-1}})))
```

직교성이 높으면(≈1): 완전히 새로운 관점. 탐색을 계속해야 함.
직교성이 낮으면(≈0): 기존 관점의 재탕. 종료 후보.

### 2.2 Logical Axes 추적

모든 diverge/deliberative 노드는 반복마다 `logical_axes`를 누적 추적한다:

```json
{
  "iteration": 3,
  "new_axes": ["regulatory_compliance"],
  "cumulative_axes": [
    "risk_evaluation",
    "cost_analysis",
    "regulatory_compliance"
  ],
  "orthogonality_score": 0.85,
  "D_current": 3,
  "D_min": 5
}
```

### 2.3 직교성 판정 프롬프트

```
[매 반복 종료 시 - 직교성 판정]

이전 반복들에서 사용된 판단 축:
{cumulative_axes 목록}

이번 반복에서 사용된 판단 축을 식별하라.

판정 기준:
- 기존 축과 독립적인 새로운 판단 기준인가?
- 기존 축의 선형결합(단순 조합)이 아닌가?
- 기존 축으로는 도달할 수 없는 결론을 가능하게 하는가?

출력:
- 새 축이 있다면: 축 이름, 기존 축과의 차이, orthogonality_score
- 새 축이 없다면: 'SATURATED', orthogonality_score = 0

주의: 같은 축의 다른 값(예: "위험 높음" vs "위험 낮음")은 새 축이 아니다.
```

### 2.4 직교성 자기평가의 한계와 보완

LLM 자기평가에는 "자기 탐색 포화를 과소평가"하는 편향이 있다. 보완 장치:

1. **D_min 사전조건**: 자기평가가 `SATURATED`여도 D_min 미달이면 perspective forcing
2. **쿨다운 윈도우**: 1회 `SATURATED`로 바로 종료하지 않음
3. **결정 민감도 교차 검증**: 결론이 추가 축에 민감한지 별도 판정

```
[결정 민감도 체크]

현재까지의 잠정 결론: {현재_결론}
탐색되지 않은 잠재 축: {미탐색_축_후보}

질문: 위 잠재 축 중 하나가 탐색되었을 때,
현재 결론이 뒤집히거나 크게 변할 가능성이 있는가?

- 있다면 (high sensitivity): 탐색 계속. SATURATED를 무시.
- 낮다면 (low sensitivity): 종료 정당.
```

## 3. D_min (최소 차원 요구량)

### 3.1 D_min 기준표

| θ_GT | Regime | D_min | 근거 |
|------|--------|-------|------|
| L2 (중간) | Verificatory | 3~4 | 주요 관점 2~3개 + 교차 검증 1개 |
| L3 (넓음) | Deliberative | 5~7 | 다면적 평가 필수 (MECE 수준) |
| L4 (정의불가) | Deliberative | 7~10 | 패러다임 수준 관점 전환 필요 |

### 3.2 D_min 미달 시: Perspective Forcing

D(k) < D_min인데 orthogonality < ε이면, LLM이 스스로 새 축을 못 찾는 것.

```
[perspective forcing 프롬프트]

현재까지 탐색된 판단 축: {cumulative_axes}
현재 D(k) = {현재_차원수}, D_min = {최소_차원수}

아직 탐색되지 않았을 수 있는 관점:
- 이해관계자를 바꿔보라 (고객→공급자→규제자→사회)
- 시간축을 바꿔보라 (단기→중기→장기)
- 추상화 수준을 바꿔보라 (전술→전략→비전)
- 반대 입장에서 보라 (찬성→반대→제3자)
- 도메인을 바꿔보라 (기술→경제→법률→윤리)

위 중 기존 축과 독립적인 새로운 판단 축을 식별하라.
식별 불가하면 'TRULY_SATURATED'를 반환하라.
```

TRULY_SATURATED 반환 시: D_min을 현재 D(k)로 하향 조정 후 종료 허용. 단, 이 사실을 Termination Declaration에 명시해야 한다.

## 4. 쿨다운 윈도우 (w)

비단조적 가치 곡선에 대응하기 위한 안전장치.

```
종료 조건: orthogonality < ε 가 연속 w회 유지될 때만 종료

w=1: 비단조 패턴에서 오탐 위험 (비권장)
w=2: 대부분 도메인에서 안전 (기본값 권장)
w=3: 고비용 탐색에서의 보수적 전략
```

## 5. 프록시 측정법 (임베딩 없이)

| 측정 대상 | 프록시 | 구현 위치 |
|----------|--------|---------|
| 직교성 | LLM 자기 평가 + 결정 민감도 교차 검증 | 종료 판정 프롬프트 |
| 차원 포화 | cumulative_axes 카운트 증분 | 반복 루프 내 |
| 커버리지 포화 | 반복 간 키워드/엔티티 중복률 | 후처리 |
| 결정 안정성 | 반복 간 잠정 결론의 구조적 차이 판정 | 종료 판정 프롬프트 |

## 6. 종료 판정 흐름도 (통합)

```
START: 반복 k 완료
│
├─ Regime = Convergent?
│  └─ Δsem < δ AND k ≥ 2 AND confidence > τ?
│     ├─ YES → terminate(answer_convergence)
│     └─ NO  → continue
│
├─ Regime = Verificatory?
│  └─ candidates ≥ N_min AND best > τ AND margin > δ?
│     ├─ YES → terminate(verification_pass)
│     └─ NO  → continue
│
└─ Regime = Deliberative?
   └─ D(k) ≥ D_min?
      ├─ NO → orthogonality < ε?
      │  ├─ YES → perspective_forcing → TRULY_SATURATED?
      │  │  ├─ YES → lower D_min → terminate(decision_sufficiency)
      │  │  └─ NO  → continue with new axis
      │  └─ NO  → continue
      └─ YES → orthogonality < ε 연속 w회?
         ├─ NO  → continue
         └─ YES → (ΔC < δ OR Δsem < δ)?
            ├─ YES → decision_sensitivity check
            │  ├─ LOW  → terminate(decision_sufficiency)
            │  └─ HIGH → continue (override SATURATED)
            └─ NO  → continue
```
