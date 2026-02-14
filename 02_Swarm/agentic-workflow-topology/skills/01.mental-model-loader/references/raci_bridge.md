# RACI Bridge: Skillpack ↔ Workflow Planner 연결 규약

## 개요

`01.mental-model-loader`로 생성된 4-Layer 스킬팩은 `raci-workflow-planner` 스킬과 자연스럽게 연동된다.
이 문서는 두 스킬 사이의 인터페이스를 정의한다.

## RACI ↔ 4-Layer 매핑

| RACI 역할 | 4-Layer 대응 | 로딩 규칙 | 워크플로우 역할 |
|-----------|-------------|----------|----------------|
| **A** (Accountable) | Layer 0 (Core) + Layer 3 (Orchestrator) | 항상 로딩 | 품질 보증 + 최종 승인 |
| **R** (Responsible) | Layer 1 (Primary Module) | 패턴 기반 선택 | 직접 수행 + 산출물 생성 |
| **C** (Consulted) | Layer 1 (Secondary Modules) | 다중 모듈 패턴 시 | 전문 의견 제공 |
| **I** (Informed) | Layer 2 (Reference Packs) | ΔQ ≥ 2 트리거 시 | 데이터/근거 제공 |

## 연결 프로토콜

### 1. Skillpack → Workflow Planner 전달 데이터

`modules_index.md`의 등록 테이블이 RACI 매핑의 입력이 된다:

```yaml
raci_input:
  modules:
    - id: module.<name>
      unique_axis: "(고유 질문)"
      reference_triggers: ["키워드A", "키워드B"]
  patterns: [Evaluate, Critique, Translate, Prioritize, Arbitrate, Simulate]
  output_schema: "{판단, 근거, 트레이드오프, 확신도}"
```

### 2. Workflow Planner → Skillpack 요청 형식

RACI 매핑 결과가 Orchestrator의 라우팅 입력이 된다:

```yaml
raci_routing:
  pattern: Evaluate
  responsible: [module.a]        # R: 직접 수행
  consulted: [module.b]          # C: 자문
  informed: [pack.x]             # I: 참조 (ΔQ 충족 시)
  accountable: [core, orchestrator]  # A: 항상 활성
```

### 3. 패턴별 기본 RACI 템플릿

| 패턴 | R (Responsible) | C (Consulted) | I (Informed) |
|------|----------------|---------------|--------------|
| Evaluate | 관련 모듈 1~2개 | (선택) 보조 모듈 | ΔQ ≥ 2 시 pack |
| Critique | 타겟 모듈 1개 | 공격 모듈 1개 | 근거 부족 시 pack |
| Translate | 원본 프레임 모듈 | 대상 프레임 모듈 | - |
| Prioritize | 핵심 모듈 1개 | - | 수치 필요 시 pack |
| Arbitrate | 상충 모듈 A | 상충 모듈 B | 근거 보강 시 pack |
| Simulate | 페르소나 모듈 2~3개 | - | 시나리오 데이터 시 pack |

> **A (Accountable)는 모든 패턴에서 Core + Orchestrator로 고정**이므로 테이블에서 생략.
