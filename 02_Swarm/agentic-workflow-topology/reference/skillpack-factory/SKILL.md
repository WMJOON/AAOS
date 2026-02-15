---
name: skillpack-factory
description: |
  4-Layer Mental Model Orchestrator 아키텍처 기반의 스킬 패키지(skill-pack)를 자동 생성하는 Skill Factory.
  사용자가 도메인·모듈 후보·참조팩 정보를 제공하면, 표준화된 디렉토리 구조와 템플릿 파일을 일괄 생성한다.

  트리거 상황:
  - "스킬팩 만들어줘", "skill-pack 생성", "4-Layer 스킬 패키지 생성" 요청 시
  - "멘탈모델 스킬 구조 세팅", "새 도메인 스킬 스캐폴딩" 요청 시
  - "Skill Factory", "스킬 공장" 관련 요청 시
  - 기존 2-Layer 스킬(SKILL.md + references/)을 4-Layer로 마이그레이션할 때
---

# Skillpack Factory

4-Layer Mental Model Orchestrator 아키텍처에 기반한 스킬 패키지를 자동 생성한다.

## 생성 워크플로우

### Phase 1: 입력 수집

사용자에게 다음 정보를 확인한다.

1. **domain**: 스킬팩의 도메인명 (예: `startup-advisor`, `security-audit`)
2. **modules**: 모듈 후보 목록 (각각의 고유 질문 축 포함)
3. **reference_packs**: 참조팩 후보 (선택)
4. **token_budget**: 커스텀 토큰 예산 (선택, 기본값 사용 가능)

### Phase 2: 골격 생성

`scripts/scaffold.py`를 실행하여 디렉토리 구조를 생성한다.

```bash
python3 scripts/scaffold.py \
  --domain <domain> \
  --output <output_path> \
  --modules "module_a,module_b" \
  --packs "pack_x,pack_y"
```

스크립트가 생성하는 구조:

```
skill-pack/
  00_meta/          manifest.yaml, changelog.md, token_budget.md, glossary.md
  10_core/          core.md
  20_modules/       modules_index.md, module.<name>.md (각 모듈별)
    examples/       module.example.md
  30_references/    loading_policy.md
    packs/          pack.<name>.md (각 참조팩별)
    sources/        sources.bib.md, snapshots/
  40_orchestrator/  orchestrator.md, routing_rules.md
  90_tests/         test_cases.yaml, eval_rubric.md, judge_prompt.md, golden_outputs/
  99_archive/       deprecated/
```

### Phase 3: 콘텐츠 채우기 순서

**반드시 이 순서를 따른다** (Core가 늦으면 중복 정의가 발생):

1. `00_meta/manifest.yaml` — 패키지 계약서 (도메인, 모듈 목록, 토큰 예산)
2. `10_core/core.md` — 공유 어휘 + 출력 스키마 + when_unsure 정책
3. `20_modules/module.<name>.md` — 각 모듈의 고유 질문 축 + 판단 루브릭 (delta만)
4. `20_modules/modules_index.md` — 모듈 메타 등록 테이블
5. `40_orchestrator/orchestrator.md` — 패턴 감지 + 라우팅 규칙
6. `30_references/packs/pack.<name>.md` — 참조팩 콘텐츠
7. `30_references/loading_policy.md` — ΔQ 트리거 연결
8. `90_tests/test_cases.yaml` — 최소 10개 테스트 케이스

### Phase 4: 검증

생성된 파일들을 검증한다:

- [ ] 모듈 간 직교성 확인 (α ≥ 0.85)
- [ ] Core와 모듈 간 중복 어휘 없음
- [ ] 모든 모듈이 modules_index.md에 등록됨
- [ ] reference_triggers가 loading_policy와 연결됨
- [ ] test_cases.yaml이 최소 10개 케이스 포함

## 핵심 규칙

### 모듈 작성 규칙
- **delta만 담기**: 공유 어휘/출력 스키마는 Core에. 모듈은 고유 질문 축만.
- **직교성 원칙**: 모듈 간 질문이 겹치면 공통 부분을 Core로 올린다.
- **출력 통일**: 모든 모듈은 `{판단, 근거, 트레이드오프, 확신도}` 스키마를 따른다.

### 6가지 패턴 (라우팅 최상위 키)
Evaluate, Critique, Translate, Prioritize, Arbitrate, Simulate

### ΔQ 로딩 규칙
- ΔQ < 2: Reference Pack 로딩 금지
- ΔQ ≥ 2: 관련 pack 1개 로딩 고려
- ΔQ ≥ 4: pack 1~2개 + sources.bib 확인

### 토큰 예산 (soft limit 기본값)
- always_load_max: 1500 (Core + Orchestrator)
- module_max: 1200 (모듈 1개)
- reference_max: 2000 (참조팩 1개)

## 2-Layer → 4-Layer 마이그레이션

기존 `SKILL.md + references/` 구조를 변환할 때:

| 기존 위치 | 이동 대상 | 기준 |
|-----------|----------|------|
| 공통 용어/출력 스키마 | `10_core/core.md` | 여러 모듈에서 반복되는 것 |
| 라우팅 규칙 | `40_orchestrator/orchestrator.md` | 패턴 감지, 모듈 선택 |
| 도메인별 고유 판단축 | `20_modules/module.*.md` | 고유 질문 축만 남기기 |
| 참고자료/체크리스트 | `30_references/packs/*.md` | 온디맨드 로딩 대상 |
| 출처/버전/날짜 | `30_references/sources/sources.bib.md` | 링크 + 스냅샷 |

## RACI 워크플로우 연결

생성된 스킬팩은 `raci-workflow-planner` 스킬과 연동된다.
모듈이 RACI 역할로 매핑되어 워크플로우 플래닝에 사용된다.
상세는 [references/raci_bridge.md](references/raci_bridge.md) 참조.
