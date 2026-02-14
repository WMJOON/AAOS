# Examples

## Example 1: 금융 규제 변경 대응 전략 수립

### Input
```json
{
  "goal": "새로운 금융 규제(가상자산 이용자보호법) 시행에 따른 자사 대응 전략 수립",
  "constraints": {
    "time_budget": "3일",
    "compliance": ["금융위원회 가이드라인 준수"]
  },
  "context": {
    "domain": "fintech",
    "audience": "경영진 + 법무팀",
    "risk_tolerance": "low"
  },
  "available_capabilities": {
    "llm": true,
    "retrieval": true,
    "human_in_the_loop": true
  }
}
```

### Output (요약)

**Topology**: `parallel + synthesis_centric`

**Decision Questions (6개, RSV_total = 6.5)**:
- DQ1: 자사 서비스 중 규제 적용 대상은? (1.5)
- DQ2: 운영 프로세스 변경 범위는? (1.0)
- DQ3: 고객 커뮤니케이션 시 법적 리스크는? (1.0)
- DQ4: 경쟁사 대응 현황은? (1.0)
- DQ5: 최적 대응 전략과 트레이드오프는? (1.5)
- DQ6: 타임라인과 우선순위는? (0.5)

**Task Graph**:
- T1: 법/정책 제약 리스트 (table, SE 낮음, θ_GT 좁음, RSV 1.5, DQ1)
- T2: 운영 영향 분석 (risk_register, SE 중간, θ_GT 중간, RSV 1.0, DQ2)
- T3: 고객 커뮤니케이션 위험/금지문구 (checklist, SE 중간, θ_GT 중간, RSV 1.0, DQ3)
- T4: 경쟁 사례 비교 (table, SE 중간, θ_GT 중간, RSV 1.0, DQ4)
- T5: 최종 Decision Memo 합성 (decision, SE 높음, θ_GT 넓음, RSV 2.0, DQ5+DQ6)

**구조**: {T1, T2, T3, T4} → T5

**Loop Risk**:
- redundancy_accumulation on T5 (high) → Output 스키마에 Trade-off Matrix + Boundary 필수
- exploration_spiral on T4 (low) → 경쟁사 3~5개로 상한 설정

**Handoff**: 단일 handoff at T5만 허용. T1~T4는 동일 스키마(table/risk_register)로 통일.

---

## Example 2: API 엔드포인트 설계 검토

### Input
```json
{
  "goal": "새 결제 API 엔드포인트 설계가 보안/성능/호환성 기준을 충족하는지 검증",
  "constraints": {
    "must_use_tools": ["code_review", "security_scan"]
  },
  "context": {
    "domain": "backend engineering",
    "audience": "테크리드",
    "risk_tolerance": "low"
  },
  "available_capabilities": {
    "llm": true,
    "retrieval": true
  }
}
```

### Output (요약)

**Topology**: `linear`

**Decision Questions (3개, RSV_total = 3.0)**:
- DQ1: 보안 취약점이 있는가? (1.5)
- DQ2: 성능 병목이 있는가? (1.0)
- DQ3: API 버전 호환성이 유지되는가? (0.5)

**Task Graph**:
- T1: 보안 검증 (checklist, SE 낮음, θ_GT 좁음, RSV 1.5, DQ1)
- T2: 성능 분석 (table, SE 낮음, θ_GT 좁음, RSV 1.0, DQ2)
- T3: 호환성 확인 (checklist, SE 낮음, θ_GT 좁음, RSV 0.5, DQ3)

**구조**: T1 → T2 → T3

**선택 근거**: 정답 공간 좁음(pass/fail), RSV 작음 → linear 충분.

**Loop Risk**: 없음 (모든 노드 SE 낮음, 반복 불필요)

---

## Example 3: AI 제품 시장 진입 전략

### Input
```json
{
  "goal": "AI 고객센터 솔루션의 한국 시장 진입 전략 수립",
  "constraints": {
    "token_budget": 100000,
    "compliance": ["개인정보보호법", "AI 기본법(예정)"]
  },
  "context": {
    "domain": "AI SaaS / AICC",
    "audience": "CEO + 투자자",
    "risk_tolerance": "medium"
  },
  "available_capabilities": {
    "llm": true,
    "retrieval": true,
    "human_in_the_loop": true
  }
}
```

### Output (요약)

**Topology**: `hierarchical + synthesis_centric` (composite)

**Decision Questions (8개, RSV_total = 10.0)**:
- DQ1: TAM-SAM-SOM은? (1.5)
- DQ2: 경쟁 구도와 차별화 포인트는? (1.5)
- DQ3: 규제 리스크와 대응 전략은? (1.0)
- DQ4: 기술 적합성(한국어 NLU, 통신사 연동)은? (1.0)
- DQ5: GTM 전략(채널, 파트너, 가격)은? (1.5)
- DQ6: 초기 타깃 세그먼트는? (1.0)
- DQ7: 투자 대비 수익 시나리오는? (1.0)
- DQ8: 최종 Go/No-Go 판단과 근거는? (1.5)

**Task Graph (계층 구조)**:
- Layer 1 (parallel): T1 시장분석, T2 경쟁분석, T3 규제분석, T4 기술적합성
- Layer 2 (synthesis): T5 중간합성 (decision_memo)
- Layer 3 (parallel): T6 GTM전략, T7 재무모델
- Layer 4 (synthesis): T8 최종 Go/No-Go Decision Memo

**Loop Risk**:
- rsv_inflation (med) → DQ가 8개로 많음, token_budget 소진 전 모든 DQ를 닫기 어려울 수 있음 → Reframe 규칙: DQ7 우선순위 하향 가능
- redundancy_accumulation on T5, T8 (high) → 합성 노드 Output 스키마 강화

**Human Gate**: T5 (중간합성 후 방향 확인), T8 (최종 판단)
