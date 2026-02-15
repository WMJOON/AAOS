# Modules Index

## 직교 질문 축

| Module | Question Axis | Phase |
|--------|--------------|-------|
| metadata-validation | cortex-agora 스킬의 메타데이터/사이드카 구조가 정책을 준수하는가? | 1 |
| archive-integrity | change_archive 이벤트 로그의 스키마/무결성/불변조건이 충족되는가? | 2 |
| consumption-contract | BEHAVIOR_FEED + COWI 소비 인터페이스 계약이 정합적인가? | 3 |

## 직교성 매트릭스

| 개념 | metadata-validation | archive-integrity | consumption-contract |
|------|---------------------|-------------------|----------------------|
| frontmatter/sidecar | **소유** | -- | -- |
| 4-Layer 구조 (조건부) | **소유** | -- | -- |
| JSONL 스키마 준수 | -- | **소유** | -- |
| bridge 명령 coverage | -- | **소유** | -- |
| CHANGE_INDEX 일관성 | -- | **소유** | -- |
| append-only/단조증가 | -- | **소유** | -- |
| BEHAVIOR_FEED 스키마 | -- | -- | **소유** |
| COWI pull interface | -- | -- | **소유** |
| cross-swarm recording | -- | -- | **소유** |
| proposal_id 추적 | 참조 (FM) | **소유** (CC-01) | 참조 (CC-05) |

## 파일 레지스트리

| Module | File |
|--------|------|
| module.metadata-validation | `20.modules/module.metadata-validation.md` |
| module.archive-integrity | `20.modules/module.archive-integrity.md` |
| module.consumption-contract | `20.modules/module.consumption-contract.md` |

## 로딩 규칙

- 모듈은 Core를 재정의하지 않는다. 고유 질문 축(delta)만 기술.
- Phase별 순차 로딩 기본. 단, 사용자가 특정 모듈만 요청 시 해당 모듈만 로딩 가능.
- metadata-validation 결과가 archive-integrity의 전제가 되므로 순서 준수 권장.
