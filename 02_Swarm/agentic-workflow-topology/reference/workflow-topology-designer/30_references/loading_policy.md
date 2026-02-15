# Loading Policy

## ΔQ 기반 Reference Pack 로딩

| Pack | 트리거 조건 | ΔQ 최소 |
|------|-----------|---------|
| pack.output_contract.md | Phase 5 산출 시 JSON 스키마 검증, 또는 사용자가 출력 스키마 질문 | ≥ 2 |
| pack.estimator.md | Runtime feedback loop 설계 시, 또는 estimator 사용법 질문 | ≥ 2 |

## ΔQ 산정 기준

ΔQ는 "현재 질문이 기본 모듈 지식만으로 답하기 어려운 정도"를 0~5로 추정한다.

| ΔQ | 해석 | 예시 |
|----|------|------|
| 0~1 | 모듈 내 지식으로 충분 | "linear vs parallel 뭐가 낫나?" |
| 2~3 | 정확한 스키마/절차 참조 필요 | "출력 JSON에 어떤 필드가 있나?" |
| 4~5 | 복수 참조 + 교차 검증 필요 | "estimator + output contract 연동 전체 설계" |

## 로딩 순서

1. Core + Orchestrator (항상)
2. Phase에 따른 모듈 (routing_rules 참조)
3. ΔQ ≥ 2 시 해당 Pack
4. ΔQ ≥ 4 시 추가 Pack (최대 2개)
