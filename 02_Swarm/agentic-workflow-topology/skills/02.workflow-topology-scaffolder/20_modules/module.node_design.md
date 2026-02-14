# Module: Node Design

**질문 축**: "노드를 어떻게 분리하고 θ_GT/RSV를 설정할 것인가?"

---

## 노드 분리 3-규칙

### 규칙 1: Explicit Output 단위로 분리

"생각 단위"가 아니라 "명시적 산출물 단위"로 분리한다.

**판단 테스트:**
- Output을 외부에서 독립 검증 가능? → Yes면 노드 존재 정당
- 두 Output이 항상 함께 생성? → Yes면 합치기
- Output이 다른 노드의 Input으로 명확히 사용? → Yes면 분리 유지

### 규칙 2: θ_GT 설정

| SE 예상 | θ_GT band | 비고 |
|---------|-----------|------|
| 해석 자유도 큼 | 넓게 (0.4~0.9) | 합리적 다양성 허용 |
| 기준 명확 | 좁게 (0.0~0.2) | 수렴 보장 |
| 중복 증산 위험 | band 넓히지 말고 **Output 스키마 강화** | 구조로 통제 |

**스키마 강화 전략** — 중복 증산 위험 노드:
```json
{
  "required_sections": ["trade_off_matrix", "boundary_conditions", "confidence_level", "dissenting_view"],
  "acceptance_criteria": ["trade_off_matrix에 최소 3개 축", "boundary_conditions에 뒤집히는 조건 1개 이상"]
}
```

### 규칙 3: RSV 타깃 할당

- 각 노드는 "어떤 DQ를 닫는가" 명시 (`assigned_dqs`)
- Σ(rsv_target) ≈ RSV_total (±10% 허용)
- 합성 노드는 DQ 간 관계 정리 역할로 RSV 기여

---

## Explicit Output 타입

| type | 용도 | θ_GT 경향 |
|------|------|----------|
| memo | 의사결정 배경 문서 | 중~넓음 |
| table | 구조화된 비교/정리 | 좁음~중간 |
| checklist | 항목별 확인 목록 | 좁음 |
| spec | 기술/요구사항 명세 | 좁음~중간 |
| risk_register | 위험+영향/확률/대응 | 중간 |
| policy | 정책/규칙 정의 | 중간~넓음 |
| decision | 최종 판단+근거 | 넓음 |
| summary | 요약 (hand-off 시에만) | 중간 |
| state | 상태 객체 | 좁음 |

---

## RSV 분배 패턴 (Topology별)

| Topology | RSV 분배 |
|----------|---------|
| linear | 균등 또는 점진적 증가 |
| parallel | 각 병렬 노드에 독립 DQ 할당 |
| fanout_fanin | fanout에 탐색 RSV, fanin에 합성 RSV |
| hierarchical | 계층별 RSV 예산, 하위로 세분화 |
| synthesis_centric | 수집 노드 RSV 낮음, 합성 노드 높음 |

---

## 판단 루브릭

```
{
  판단: "노드 분리/합치기 결정 + θ_GT band + rsv_target",
  근거: "Explicit Output 단위 테스트 결과 + SE 추정 + DQ 할당",
  트레이드오프: "분리 시 hand-off cost vs 합칠 시 노드 과부하",
  확신도: "SE 추정 불확실 시 낮음 → estimator로 보정 권장"
}
```
