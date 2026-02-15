# Loading Policy

## 기본 규칙

항상 로딩:
- `10.core/core.md` — 핵심 정의, 입력 인터페이스, when_unsure 정책
- `40.orchestrator/orchestrator.md` — 5-Phase 프로세스, 패턴 감지

온디맨드 로딩:
- `20.modules/module.*.md` — Phase별 필요 모듈만
- `30.references/packs/pack.*.md` — ΔQ 조건 충족 시만

## ΔQ 기반 Reference Pack 로딩

| ΔQ | 허용 | 트리거 예 |
|----|------|----------|
| < 2 | Pack 로딩 금지 | 단순 linear 설계 |
| ≥ 2 | 관련 pack 1개 로딩 고려 | "출력 JSON 스키마 전체 보여줘" → pack.output_contract |
| ≥ 4 | pack 1~2개 로딩 | 복합 설계 + estimator 연동 |

## Pack 목록

| Pack | 파일 | 트리거 |
|------|------|--------|
| output_contract | `packs/pack.output_contract.md` | Phase 5 스키마 검증 시 (ΔQ ≥ 2) |
| estimator | `packs/pack.estimator.md` | Runtime feedback loop 구성 시 (ΔQ ≥ 2) |

## 로딩 순서

```
Core + Orchestrator (항상)
  → Phase 진입 시 해당 모듈 (온디맨드)
  → 상세 필요 시 Pack (ΔQ 조건)
```
