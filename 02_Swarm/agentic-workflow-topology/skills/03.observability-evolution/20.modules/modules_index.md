# Modules Index

## 직교 질문 축

| Module | Question Axis | Phase |
|---|---|---|
| observation-policy | 어떤 신호를 어떤 소스에서 언제 관찰할 것인가? | 1, 2 |
| hitl-interaction | 관찰 결과를 사용자에게 어떻게 제시하고 피드백을 수집할 것인가? | 3 |
| improvement-proposal | 어떤 구체적 개선안을 어떤 근거로 제안할 것인가? | 4 |
| evolution-tracking | 제안이 설계 스킬로 어떻게 환류되고 피드백 루프가 어떻게 추적되는가? | 5 |

## 직교성 매트릭스

| 개념 | observation | hitl | proposal | evolution |
|------|-------------|------|----------|-----------|
| 신호 수집/분류 | **소유** | -- | -- | -- |
| 사용자 상호작용 | -- | **소유** | -- | -- |
| 개선 제안 생성 | -- | -- | **소유** | -- |
| 환류 추적 | -- | -- | -- | **소유** |
| Anomaly Signal(AS) | 분류 소유 | 심각도→트리거 | 패턴→원인 | -- |
| HITL Checkpoint(HC) | OP가 시점 정의 | 프로토콜 정의 | 피드백 수집 | -- |
| Improvement Proposal(IP) | -- | 사용자 검증 | 생성 | 라이프사이클 추적 |
| Evolution Cycle(EC) | -- | -- | -- | 상태 전이 소유 |

## 파일 레지스트리

| Module | File |
|---|---|
| module.observation-policy | `20.modules/module.observation-policy.md` |
| module.hitl-interaction | `20.modules/module.hitl-interaction.md` |
| module.improvement-proposal | `20.modules/module.improvement-proposal.md` |
| module.evolution-tracking | `20.modules/module.evolution-tracking.md` |

## 로딩 규칙

- 모듈은 Core를 재정의하지 않는다. 고유 판단 축(delta)만 기술.
- Phase별 필요 시 온디맨드 로딩.
- 동시에 2개 이상 모듈 로딩 가능 (Phase 4에서 hitl + proposal 동시 참조 등).
