# Changelog

## v2.2.0 (2026-02-15)

### Changed
- 정책 전환: `SKILL.md` self-contained runbook 폐기.
- `SKILL.md`를 4-Layer 최소 로더로 전환 (67줄).
- 상세 실행 규칙은 `10.core/`, `20.modules/`, `30.references/`, `40.orchestrator/`로 분리.

### Added (layer content population)
- `10.core/core.md`: 핵심 정의 테이블, 입력 인터페이스 JSON, 책임 범위, when_unsure 4규칙, cone-analyzer 관계.
- `20.modules/module.topology_selection.md`: 8 Topology 유형, 3-Signal 선택 규칙, 유형별 주의사항, 판단 루브릭.
- `20.modules/module.node_design.md`: 노드 분리 3-규칙, θ_GT band 설정, 스키마 강화, 9개 Output 타입, RSV 분배 패턴.
- `20.modules/module.loop_risk.md`: 정상 루프, 병리적 루프 5종(신호/위험/mitigation).
- `20.modules/module.handoff.md`: 허용/금지 포맷, 최소화 패턴, 판단 루브릭.
- `40.orchestrator/orchestrator.md`: 5-Phase 프로세스, 패턴 감지 6종, strategy gate, estimator 연동.
- `40.orchestrator/routing_rules.md`: Phase→Module 매핑, ΔQ 규칙, handoff 트리거.
- `30.references/loading_policy.md`: ΔQ 수치 조건, Pack 목록, 로딩 순서.
- `90.tests/test_cases.yaml`: 구조 검증 3건 + Topology 설계 테스트 10건.
- `90.tests/eval_rubric.md`: 6축 5점 척도, pass 기준, strategy 검증.
- `00.meta/manifest.yaml`: version, domain, modules, scripts, token_budget, related_skills 메타 보강.
- 토큰 예산 모델을 실제 내용 기준으로 재산정.

## v2.1.0 (2026-02-14)

### Added
- 전략/고위험 워크플로우 강제 게이트 도입:
  - PF1 preflight 첫 질문 고정(`멘탈모델 먼저 세팅할까요?`)
  - `H1/H2` 필수 노드
  - `T4 -> C1 -> H1` 필수 엣지
- H1 finalization validator 추가:
  - `scripts/validate_strategy_h1_gate.py`
- 웹 근거 템플릿 추가:
  - `30.references/packs/web_evidence.template.md`
- `workflow_topology_spec` 스키마 확장:
  - `preflight`, `workflow_profile`, `strategy_gate`

## v2.0.0 (2026-02-10)

### Added
- 5-Phase 구조화와 토폴로지 모듈 세분화.
- 모듈/참조팩 중심 운영 기반 확립.

## v1.0.0 (2026-02-09)
- 2-Layer -> 4-Layer 마이그레이션 시작
- estimator.py 통합 (Runtime Feedback Loop)
