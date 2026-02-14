# Changelog

## v2.0.0 (2026-02-10)

### Breaking Change: SKILL.md → Self-Contained Runbook

v1.0의 SKILL.md는 "목차+로딩 안내"로, 실행에 3~5회 추가 파일 로딩이 필요했다.
v2.0에서는 **SKILL.md 단독으로 5-Phase 전체를 실행 가능**하도록 재설계했다.

### 변경 요약

| 항목 | v1.0 | v2.0 |
|------|------|------|
| SKILL.md 역할 | 목차 + 로딩 가이드 | **Self-contained runbook** |
| 실행에 필요한 최소 파일 수 | 3~5개 (core + orch + modules) | **1개** (SKILL.md) |
| 핵심 로직 위치 | 모듈 파일에 분산 | **SKILL.md에 인라인** |
| 모듈 파일 역할 | 필수 로딩 | **상세 참조용** (필요 시만) |
| 트리거 키워드 | cone-analyzer와 충돌 | **"Topology" 키워드로 분리** |
| Quick Example | 없음 | **추가** |
| description에 cone-analyzer 차이 | 없음 | **명시** |

### 인라인된 핵심 로직

- Phase 2: 8가지 Topology 유형 + 3-Signal 선택 규칙
- Phase 3: 노드 분리 3-규칙 + θ_GT band + Output 타입
- Phase 4: 병리적 루프 5종 + Hand-off 허용/금지 포맷
- Phase 5: Workflow Spec JSON 구조 (축약)

### 모듈 파일은 그대로 유지

모듈/참조팩 파일은 변경 없이 유지. SKILL.md 인라인은 "요약"이 아니라
실행에 필요한 핵심 규칙만 추출한 것. 상세 트레이드오프 비교, 시뮬레이션,
스키마 강화 상세 등은 여전히 모듈 파일을 참조한다.

---

## v1.0.0 (2026-02-09)
- 2-Layer → 4-Layer 마이그레이션 완료
- estimator.py 통합 (Runtime Feedback Loop)
- 모듈 4개 분리: topology_selection, node_design, loop_risk, handoff
- 참조팩 2개: output_contract, estimator
- 테스트 케이스 10개 작성

### 2-Layer 원본 대비 변경
- Core에 공유 어휘(θ_GT, RSV, DQ, Explicit Output) 집중
- Orchestrator에 5-Phase 프로세스 + 라우팅 규칙 분리
- 모듈별 고유 질문 축만 delta로 유지
