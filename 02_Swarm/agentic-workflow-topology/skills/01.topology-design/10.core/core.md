# Core — Agentic Workflow Topology Designer

## 고정 문장
이 스킬은 리포트를 생성하지 않는다.
리포트를 생성할 "그래프 구조(Topology) + 노드 명세"를 설계해 반환한다.

---

## 핵심 정의

| 개념 | 정의 |
|------|------|
| **Workflow** | Task Node들의 유향 그래프(Task Graph) |
| **Task Node 경계** | 외부에서 관측 가능한 **Explicit Output**으로 정의. 내부 추론/토큰은 경계 기준이 아님 |
| **θ_GT** | Node의 Explicit Output이 허용하는 의미적 분산도의 기대 범위. SE 높으면 넓고, 낮으면 좁음 |
| **RSV** | Goal 달성에 필요한 의미 기여 총량. "Decision Questions를 닫는 의미 단위의 총합"으로 근사 |
| **DQ** | Decision Question. RSV의 기본 단위. RSV_total = Σ(DQ_weight) |

---

## 공유 출력 스키마

모든 모듈은 이 스키마를 따라 산출물을 반환한다:

```
{판단, 근거, 트레이드오프, 확신도}
```

Workflow Spec 전체 JSON 스키마 → `30.references/packs/pack.output_contract.md`

---

## 입력 인터페이스

```json
{
  "goal": "string",
  "workflow_profile": {
    "class": "strategy | high_risk | general",
    "risk_tolerance": "low | medium | high"
  },
  "preflight": {
    "questions": [
      {"id": "PF1", "question": "멘탈모델 먼저 세팅할까요?", "required": true}
    ]
  },
  "constraints": {
    "time_budget": "optional string",
    "token_budget": "optional number",
    "must_use_tools": ["optional"],
    "must_not_use_tools": ["optional"],
    "compliance": ["optional"]
  },
  "context": {
    "domain": "optional string",
    "audience": "optional string",
    "risk_tolerance": "low | medium | high"
  },
  "available_capabilities": {
    "llm": true,
    "retrieval": true,
    "embedding": "optional",
    "human_in_the_loop": "required_when_strategy_or_high_risk"
  }
}
```

---

## 전략/고위험 강제 게이트

- `workflow_profile.class in {strategy, high_risk}` 또는 `risk_tolerance=high`인 경우:
  - `H1`, `H2` 노드를 기본 포함한다.
  - `T4 -> C1 -> H1` 엣지를 강제한다.
  - `web_evidence_YYYY-MM-DD.md`가 없으면 `H1` 승인 불가.
  - COWI 산출물(`relation_context_map`, `skill_usage_adaptation_report`)이 없으면 `H1` finalization 불가.

## 책임 범위

### In-Scope
- Goal → DQ 분해 → RSV_total 추정
- Topology 선택 + 근거
- Task Node 설계: Explicit Output, θ_GT, RSV 기여 목표
- 루프 위험 + mitigation
- Hand-off 전략
- 실행 가능한 Workflow Spec 산출

### Out-of-Scope
- 도메인 결론 생성
- 실제 검색/도구 실행
- 모델 선택/배포/인프라

---

## when_unsure 정책

| 상황 | 행동 |
|------|------|
| Goal이 모호하여 DQ 분해 불가 | "Goal을 구체화해 주세요" + 예시 DQ 제안 |
| Topology 후보가 2개 이상 동점 | 두 후보의 트레이드오프를 제시하고 사용자 선택 요청 |
| θ_GT 추정이 불확실 | band를 넓게 설정 + "첫 반복 후 estimator로 보정 권장" 코멘트 |
| RSV_total 과대 추정 의심 | Reframe 신호 + "이 Goal은 2개 Workflow로 분할 검토" 제안 |

---

## cone-analyzer와의 관계

| 관심사 | 본 스킬 (Topology Designer) | cone-analyzer |
|--------|---------------------------|---------------|
| 분석 단위 | 그래프 전체 | 개별 노드 |
| 핵심 질문 | "어떤 구조로 연결할까" | "이 노드를 더 나눌까, 언제 멈출까" |
| θ_GT 사용 | Node-level 기대 폭 설정 | 서브태스크 프로파일링 + 종료 판정 |
| 연계 방식 | Phase 3 노드 설계 후 → cone-analyzer로 노드 내부 상세 설계 위임 가능 |
