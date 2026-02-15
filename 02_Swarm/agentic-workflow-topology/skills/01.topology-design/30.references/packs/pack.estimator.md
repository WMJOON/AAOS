# Estimator Guide — Semantic Control Estimator 통합 가이드

## 개요

`scripts/estimator.py`는 **실행 시간(Runtime)** 에 워크플로우 노드의 반복마다
설계 시 예측한 θ_GT, RSV와 실제 측정값을 비교하여 피드백 루프를 닫는 도구다.

```
┌─────────────────────────────────────────────────────┐
│  Design-time (본 스킬)                               │
│  Phase 1~5 → Workflow Spec 산출                      │
│  (θ_GT band, rsv_target, stop_condition 설정)        │
└──────────────────┬──────────────────────────────────┘
                   │ Workflow Spec
                   ▼
┌─────────────────────────────────────────────────────┐
│  Runtime (실행 환경)                                  │
│  노드 실행 → normalized_output 스냅샷 저장           │
│  매 반복마다 estimator.py 실행                       │
│  → theta_gt_actual / delta_rsv / redundancy 측정     │
│  → Continue / Reframe / Stop 판단                    │
└─────────────────────────────────────────────────────┘
```

---

## 핵심 역할: Design-time 예측 ↔ Runtime 측정 연결

| 설계 시 필드 (Workflow Spec) | 실행 시 측정 (estimator) | 비교 판단 |
|------------------------------|--------------------------|-----------|
| `theta_gt_band.max` | `theta_gt_actual` | actual > max → 아직 수렴 안 됨, 반복 계속 |
| `theta_gt_band.min` | `theta_gt_actual` | actual < min → 과도 수렴, 정보 손실 가능 |
| `rsv_target` | `rsv_accumulated_next` | acc >= target → 이 노드의 DQ 충분히 닫힘 |
| `stop_condition` | `redundancy` | redundancy=true → 중복 증산 루프 진입, 강제 종료 |

---

## 사용법

### 기본 CLI

```bash
python3 scripts/estimator.py \
  --prev snapshots/iter_0.json \
  --curr snapshots/iter_1.json \
  --rsv-acc 0.0 \
  --expected-theta 0.5 \
  --rsv-total 6.5
```

### 파라미터

| 파라미터 | 설명 | 기본값 |
|----------|------|--------|
| `--prev` | 이전 반복의 normalized_output JSON | (필수) |
| `--curr` | 현재 반복의 normalized_output JSON | (필수, 또는 --stdin-curr) |
| `--rsv-acc` | 이전까지 누적된 RSV | 0.0 |
| `--expected-theta` | 설계 시 설정한 θ_GT band upper | (선택) |
| `--rsv-total` | 워크플로우 전체 RSV_total | (선택) |
| `--epsilon` | delta_entropy "무시 가능" 임계값 | 0.02 |
| `--redundancy-threshold` | redundancy_ratio 임계값 | 0.75 |

---

## normalized_output 스키마

estimator가 인식하는 6개 섹션:

```json
{
  "decision_questions": [
    {
      "id": "DQ1",
      "question": "이 노드가 답해야 하는 핵심 질문",
      "status": "open | partial | closed",
      "closure_strength": "strong | partial | weak"
    }
  ],
  "claims": [
    {
      "id": "C1",
      "text": "주장/사실 내용",
      "type": "fact | interpretation | recommendation",
      "source": "출처"
    }
  ],
  "assumptions": [
    {"id": "A1", "text": "가정 내용"}
  ],
  "constraints": [
    {"id": "K1", "text": "제약 조건"}
  ],
  "risks": [
    {"id": "R1", "text": "위험 내용", "severity": "low | med | high"}
  ],
  "tradeoffs": [
    {"id": "T1", "text": "트레이드오프 서술"}
  ]
}
```

### DQ status → RSV 매핑

| 전이 | delta_rsv 기여 |
|------|----------------|
| open → closed (strong) | +1.0 |
| open → closed (partial) | +0.5 |
| open → closed (weak) | +0.25 |
| open → partial | +0.5 |
| partial → closed (strong) | +1.0 |
| 변화 없음 | 0 |

---

## 출력 해석

### metrics (핵심 4개)

```json
{
  "theta_gt_actual": 0.504,    // 현재 의미적 분산도 (0~1)
  "delta_entropy": -0.183,     // 이전 대비 변화 (음수 = 수렴 중)
  "delta_rsv": 1.5,            // 이번 반복에서 닫힌 DQ 기여량
  "redundancy": false           // 중복 증산 루프 감지 여부
}
```

### Continue / Reframe / Stop 판단 규칙

```
if redundancy == true:
    → STOP (중복 증산 루프, output 스키마 강화 필요)

if theta_gt_actual > theta_gt_band.max:
    → CONTINUE (아직 수렴 안 됨)

if theta_gt_actual < theta_gt_band.min:
    → REFRAME (과도 수렴, DQ 재정의 또는 노드 분할 검토)

if rsv_accumulated_next >= rsv_target:
    → STOP (이 노드의 목표 달성)

if rsv_accumulated_next >= rsv_total:
    → STOP (워크플로우 전체 목표 달성)

else:
    → CONTINUE
```

---

## 알려진 한계 및 튜닝 포인트

### 1. 한국어 토큰화 (v0.1 한계)

현재 `_tokenize()`는 공백+구두점 기반 분리를 사용한다.
한국어 조사가 붙은 텍스트("시행" vs "시행됨", "보호법" vs "보호법이")는
Jaccard 유사도가 과소 평가되어 **리프레이즈를 새 유닛으로 오분류**할 수 있다.

**영향**: `redundancy` 감지 정확도 저하 (실제 중복인데 false로 나옴)

**임시 대응**:
- `--redundancy-threshold`를 0.5~0.6으로 낮추기
- delta_rsv = 0 이면서 delta_entropy ≈ 0인 경우를 추가 룰로 체크
- 향후: 형태소 분석기(mecab/konlpy) 연동 또는 n-gram 기반 유사도로 교체

### 2. prev theta 추정의 근사성

prev_theta를 계산할 때 "이전의 이전" 스냅샷이 없으므로, prev 자체 크기 기반 
heuristic(`sat(len/12)`)을 사용한다. 첫 반복에서 delta_entropy가 부정확할 수 있다.

**대응**: 첫 반복은 theta_gt_actual만 참고하고 delta_entropy는 무시 권장.

### 3. theta 계산 가중치

기본 가중치(`w_new=0.35, w_open=0.35, w_var=0.20, w_red=0.30`)는 초기 설정이다.
도메인별로 다를 수 있으며, 반복 경험을 통해 튜닝이 필요하다.

---

## Workflow Spec과의 연결 예시

설계 시 T3 노드가 다음과 같이 정의되었다면:

```json
{
  "node_id": "T3",
  "theta_gt_band": {"min": 0.2, "max": 0.6},
  "rsv_target": 1.0,
  "assigned_dqs": ["DQ3"],
  "stop_condition": "DQ3 closed 또는 redundancy 감지 시"
}
```

실행 중 estimator 출력이 이렇게 나오면:

```json
{
  "theta_gt_actual": 0.35,
  "delta_rsv": 1.0,
  "rsv_accumulated_next": 1.0,
  "redundancy": false
}
```

→ `theta_gt_actual(0.35)` ∈ `[0.2, 0.6]` 이고,
→ `rsv_accumulated_next(1.0)` >= `rsv_target(1.0)` 이므로,
→ **STOP** — 이 노드의 목표 달성.
