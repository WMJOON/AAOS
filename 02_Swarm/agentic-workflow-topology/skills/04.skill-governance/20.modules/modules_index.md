# Modules Index

## 직교 질문 축

| Module | Question Axis | Phase |
|--------|--------------|-------|
| metadata-validation | 각 AWT 스킬의 메타데이터/사이드카/4-Layer 구조가 정책을 준수하는가? | 1 |
| contract-sync | AWT 스킬 간 계약 결합점(CC-01~CC-05)이 정합적인가? | 2 |
| registry-runbook | AWT 레지스트리가 실제 디렉토리 상태와 일치하는가? | 3 |

## 직교성 매트릭스

| 개념 | metadata-validation | contract-sync | registry-runbook |
|------|---------------------|---------------|------------------|
| frontmatter/sidecar | **소유** | -- | -- |
| 4-Layer 디렉토리 구조 | **소유** | -- | -- |
| schema key 결합 | -- | **소유** | -- |
| feedback loop closure | -- | **소유** | -- |
| 레지스트리 <-> 디렉토리 일치 | -- | -- | **소유** |
| context_id 중복 | 식별 소유 | 참조 (결합 검증 시) | 참조 (레지스트리 항목) |

## 파일 레지스트리

| Module | File |
|--------|------|
| module.metadata-validation | `20.modules/module.metadata-validation.md` |
| module.contract-sync | `20.modules/module.contract-sync.md` |
| module.registry-runbook | `20.modules/module.registry-runbook.md` |

## 로딩 규칙

- 모듈은 Core를 재정의하지 않는다. 고유 질문 축(delta)만 기술.
- Phase별 순차 로딩 기본. 단, 사용자가 특정 모듈만 요청 시 해당 모듈만 로딩 가능.
- metadata-validation 결과가 contract-sync의 전제가 되므로 순서 준수 권장.
