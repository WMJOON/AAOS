#!/usr/bin/env python3
"""
Skillpack Factory — 4-Layer Skill-Pack Scaffolding Generator

Usage:
    scaffold.py --domain <domain> --output <path> [--modules m1,m2] [--packs p1,p2]

Examples:
    scaffold.py --domain startup-advisor --output ./skill-pack --modules "pm,vc,marketer" --packs "tam_sam,unit_econ"
    scaffold.py --domain security-audit --output ./skill-pack
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import date


def create_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def write_file(path, content):
    Path(path).write_text(content, encoding="utf-8")
    print(f"  ✅ {path}")


def scaffold(domain, output, modules, packs):
    base = Path(output)
    today = date.today().isoformat()

    if base.exists():
        print(f"⚠️  디렉토리가 이미 존재합니다: {base}")
        print("   기존 파일은 덮어쓰지 않습니다. 새 파일만 생성합니다.")

    # ── 디렉토리 구조 ──
    dirs = [
        "00_meta",
        "10_core",
        "20_modules",
        "20_modules/examples",
        "30_references",
        "30_references/packs",
        "30_references/sources",
        "30_references/sources/snapshots",
        "40_orchestrator",
        "90_tests",
        "90_tests/golden_outputs",
        "99_archive",
        "99_archive/deprecated",
    ]
    for d in dirs:
        create_dir(base / d)

    print(f"\n📁 디렉토리 구조 생성 완료: {base}\n")

    # ── 00_meta/manifest.yaml ──
    modules_yaml = ""
    if modules:
        lines = []
        for m in modules:
            lines.append(f'  - id: module.{m}\n    file: "20_modules/module.{m}.md"\n    unique_axis: "(고유 질문 축 작성)"')
        modules_yaml = "\n".join(lines)
    else:
        modules_yaml = "[]"

    packs_yaml = ""
    if packs:
        lines = []
        for p in packs:
            lines.append(f'  - id: pack.{p}\n    file: "30_references/packs/pack.{p}.md"\n    triggers: ["키워드"]')
        packs_yaml = "\n".join(lines)
    else:
        packs_yaml = "[]"

    mod_block = f"modules:\n{modules_yaml}" if modules else "modules: []"
    pack_block = f"reference_packs:\n{packs_yaml}" if packs else "reference_packs: []"

    write_file(base / "00_meta/manifest.yaml", f"""\
id: skillpack.{domain}.orchestrator
version: 0.1.0
owner: (작성자)
created_at: {today}
status: scaffolding

layers:
  l0_core: "10_core/core.md"
  l1_modules_dir: "20_modules/"
  l2_references_dir: "30_references/"
  l3_orchestrator: "40_orchestrator/orchestrator.md"

io_contract:
  output_schema: "{{판단, 근거, 트레이드오프, 확신도}}"
  language: ko-KR

token_budget:
  always_load_max: 1500
  module_max: 1200
  reference_max: 2000

{mod_block}

{pack_block}
""")

    # ── 00_meta/changelog.md ──
    write_file(base / "00_meta/changelog.md", f"""\
# Changelog

## v0.1.0 ({today})
### Added
- 초기 스캐폴딩 생성 (01.mental-model-loader)
- 도메인: {domain}
""")

    # ── 00_meta/token_budget.md ──
    write_file(base / "00_meta/token_budget.md", """\
# Token Budget

## 원칙
- 아래 수치는 **soft limit(기본값)**이며, 실측 후 보정한다.

## 기본값

| 구분 | 대상 | 상한 (tok) | 로딩 조건 |
|------|------|------------|-----------|
| 상시 로딩 | Core | ~700 | 항상 |
| 상시 로딩 | Orchestrator | ~800 | 항상 |
| **상시 합계** | | **~1,500** | |
| 선택 로딩 | Module 1개 | ~1,200 | 패턴 라우팅 시 |
| 온디맨드 | Reference Pack 1개 | ~2,000 | ΔQ ≥ 2 |

## 비용 모델
```
Cᵢ = Ω + L₀ + Dᵢ·L₁ + mᵢ·L₂ + P + O
```
""")

    # ── 00_meta/glossary.md ──
    write_file(base / "00_meta/glossary.md", """\
# Glossary

## 도메인 공통 용어

| 용어 | 정의 | 사용 모듈 |
|------|------|-----------|
| (도메인에 맞게 작성) | | |

## 출력 스키마 용어 (고정)

| 용어 | 정의 |
|------|------|
| 판단 | 분석 결과의 핵심 결론 (1~2문장) |
| 근거 | 판단을 뒷받침하는 데이터/논리/사례 |
| 트레이드오프 | 반대편 리스크/비용/기회비용 |
| 확신도 | 높음/중간/낮음 + 불확실 요인 |

## 패턴 용어 (고정)

| 패턴 | 정의 |
|------|------|
| Evaluate | 평가하고 점수·근거·리스크를 구조화 |
| Critique | 반박·취약점을 찾아 보완 제안 |
| Translate | 프레임 간 번역/재서술 |
| Prioritize | 우선순위화 |
| Arbitrate | 충돌 조정·중재 |
| Simulate | 시나리오 시뮬레이션 |

## 구조 용어 (고정)

| 용어 | 정의 |
|------|------|
| Layer 0 (Core) | 공유 공리/어휘/출력 형식. 항상 로딩 |
| Layer 1 (Module) | 고유 질문 축. 패턴에 따라 선택 로딩 |
| Layer 2 (Reference) | ΔQ ≥ 2일 때만 온디맨드 로딩 |
| Layer 3 (Orchestrator) | 패턴 감지 + 라우팅. 항상 로딩 |
| ΔQ | Reference 로딩 필요도 점수 |
| α (직교성 계수) | 모듈 간 간섭도 (0.5~0.9) |
""")

    # ── 10_core/core.md ──
    write_file(base / "10_core/core.md", """\
<core>
  <purpose>
    모든 모듈에서 공유하는 공리, 어휘, 출력 형식, 운영 정책을 정의한다.
    모듈은 이 파일의 정의를 재정의하지 않고, 고유 질문 축(delta)만 추가한다.
  </purpose>

  <shared_vocabulary>
    <!-- 도메인에 맞는 공유 용어를 여기에 정의한다 -->
    - 용어A: 정의...
    - 용어B: 정의...
  </shared_vocabulary>

  <output_format>
    출력은 항상 다음 스키마를 따라야 한다:

    ## 판단
    [핵심 결론 1~2문장]

    ## 근거
    [데이터/논리/사례 기반 뒷받침]

    ## 트레이드오프
    [반대편 리스크/비용/기회비용]

    ## 확신도
    [높음/중간/낮음] + 불확실 요인: [목록]
  </output_format>

  <when_unsure_policy>
    - 정보 부족 시, 부족한 항목과 필요 입력을 명시한다.
    - 추정 포함 시, 추정임을 표시하고 가정을 나열한다.
    - 수치 제시 시 출처 또는 추정 근거를 병기한다.
  </when_unsure_policy>

  <orthogonality_principle>
    각 모듈은 자신만의 고유 질문 축을 가진다.
    겹침 발견 시 공통 부분을 이 Core 파일로 올려야 한다.
  </orthogonality_principle>
</core>
""")

    # ── 20_modules/examples/module.example.md ──
    write_file(base / "20_modules/examples/module.example.md", """\
<module id="module.example">
  <!-- 이 파일은 모듈 작성 예시입니다. 실전에서는 module.<name>.md로 생성하세요. -->

  <meta>
    name: (모듈 이름)
    unique_axis: "(고유 질문)"
    migration_status: template
  </meta>

  <unique_axis>
    이 모듈만의 고유 질문 축 정의 (1~2문장)
  </unique_axis>

  <decision_rubric>
    1. 기준 1: (검증 가능한 판단 기준)
    2. 기준 2: ...
    3. 기준 3: ...
  </decision_rubric>

  <reference_triggers>
    - "키워드A", "키워드B" → pack.<name>
  </reference_triggers>
</module>
""")

    # ── 각 모듈 파일 생성 ──
    for m in (modules or []):
        write_file(base / f"20_modules/module.{m}.md", f"""\
<module id="module.{m}">
  <meta>
    name: {m}
    unique_axis: "(이 모듈만의 고유 질문 — 작성 필요)"
    migration_status: scaffold
  </meta>

  <unique_axis>
    <!-- TODO: 이 모듈만의 고유 질문 축을 1~2문장으로 정의 -->
  </unique_axis>

  <decision_rubric>
    <!-- TODO: 고유 축에서 파생되는 판단 기준 3~7개 -->
    1. 기준 1:
    2. 기준 2:
    3. 기준 3:
  </decision_rubric>

  <situation_guide>
    <!-- (선택) 상황별 접근법 -->
  </situation_guide>

  <reference_triggers>
    <!-- TODO: Reference Pack 로딩 키워드 매핑 -->
  </reference_triggers>
</module>
""")

    # ── modules_index.md ──
    mod_rows = ""
    for m in (modules or []):
        mod_rows += f"| module.{m} | (고유 질문 축) | | | | |\n"
    if not mod_rows:
        mod_rows = "| (모듈 등록 필요) | | | | | |\n"

    write_file(base / "20_modules/modules_index.md", f"""\
# Modules Index

> 등록된 모듈의 메타 정보. Orchestrator가 라우팅 시 참조한다.

## 등록된 모듈

| Module ID | 고유 질문 축 | 입력 | 출력 | 토큰 예산 | 주요 Reference Trigger |
|-----------|-------------|------|------|-----------|----------------------|
{mod_rows}
## 패턴-모듈 조합 참고

| 패턴 | 조합 방식 | 모드 |
|------|----------|------|
| Evaluate | 관련 모듈 2개 병렬 | 각 렌즈 독립 판단 |
| Critique | 모듈 A 생성 → 모듈 B 공격 | 적대적 검증 |
| Translate | 원본 → 대상 프레임 모듈 | 프레임 변환 |
| Prioritize | 단일 모듈 심층 | 깊이 분석 |
| Arbitrate | 상충하는 2개 모듈 | 상충점 추출 |
| Simulate | 2~3개 모듈 페르소나 | 병렬 시뮬레이션 |
""")

    # ── 40_orchestrator/orchestrator.md ──
    write_file(base / "40_orchestrator/orchestrator.md", """\
<orchestrator>
  <purpose_detection>
    사용자 입력에서 목적 신호를 감지하고 패턴을 판정한다.
  </purpose_detection>

  <patterns>
    | 패턴 | 의도 | 트리거 키워드 |
    |------|------|-------------|
    | Evaluate | 평가·점수·리스크 구조화 | "평가", "기대효과", "점수" |
    | Critique | 반박·취약점·보완 제안 | "비판", "허점", "반박" |
    | Translate | 프레임 간 번역·재서술 | "관점으로 바꿔줘", "쉽게 설명" |
    | Prioritize | 우선순위화 | "우선순위", "중요도", "로드맵" |
    | Arbitrate | 충돌 조정·중재 | "A vs B", "상충", "트레이드오프" |
    | Simulate | 시나리오 시뮬레이션 | "가정하고", "시나리오" |
  </patterns>

  <routing>
    1. Layer 0(Core)는 항상 로드한다.
    2. Layer 1(Module)은 modules_index.md를 참조하여 1~3개 선택 로드한다.
    3. Layer 2(References)는 loading_policy.md 트리거 충족 시에만 로드한다.
  </routing>

  <reference_loading>
    ΔQ 계산 후 loading_policy.md 규칙에 따라 로딩을 결정한다.
  </reference_loading>

  <execution>
    선택된 모듈은 동일한 출력 스키마로 실행한다.
    모듈 간 상충 발생 시 Arbitrate 패턴으로 구조화한다.
  </execution>
</orchestrator>
""")

    # ── 40_orchestrator/routing_rules.md ──
    write_file(base / "40_orchestrator/routing_rules.md", """\
# Routing Rules

## 패턴 우선순위 규칙
- 명시적 키워드가 있으면 해당 패턴을 우선한다.
- 키워드가 모호하면 Evaluate를 기본값으로 사용한다.
- 복합 요청은 주 패턴 + 부 패턴으로 분리한다.

## 모듈 선택 규칙
- modules_index.md의 "고유 질문 축"과 사용자 입력을 매칭한다.
- 최대 3개 모듈까지 병렬 활성화 가능.

## 충돌 처리
- 2개 이상 모듈이 상충하는 결론을 내면 Arbitrate 패턴으로 전환.
- 종합 판단 섹션에서 조건부 결론을 제시한다.
""")

    # ── 30_references/loading_policy.md ──
    write_file(base / "30_references/loading_policy.md", """\
<loading_policy>
  <principle>
    Reference는 항상 로드하지 않는다.
    수치 검증, 분류 판정, 체크리스트 적용이 필요한 경우에만 로드한다.
  </principle>

  <delta_q_definition>
    ΔQ 점수 규칙:
    - +2: 수치/정량 추정 요청
    - +2: 등급/분류 판정
    - +1: "최신/근거/출처/레퍼런스" 요구
    - +1: Critique에서 근거 부족
    - +1: 모듈의 <reference_triggers> 키워드 매칭
  </delta_q_definition>

  <loading_rules>
    | ΔQ 범위 | 로딩 판단 |
    |---------|----------|
    | ΔQ < 2 | 로딩 금지 |
    | ΔQ ≥ 2 | 관련 pack 1개 로딩 고려 |
    | ΔQ ≥ 4 | pack 1~2개 + sources.bib 확인 |
  </loading_rules>

  <trigger_examples>
    (도메인별 참조팩 등록 후 실제 예시로 교체한다.)
  </trigger_examples>
</loading_policy>
""")

    # ── 각 참조팩 파일 생성 ──
    for p in (packs or []):
        write_file(base / f"30_references/packs/pack.{p}.md", f"""\
# Reference Pack: {p}

> **로딩 조건**: ΔQ ≥ 2 이고, 관련 키워드 매칭 시
> **출처**: (출처 기재)
> **토큰 예산**: ~2,000 tok 이내

---

## 정의

<!-- TODO: 이 참조팩의 핵심 개념/지표/분류 정의 -->

## 검증 체크리스트

- [ ] (검증 항목 1)
- [ ] (검증 항목 2)
- [ ] (검증 항목 3)
""")

    # ── 30_references/sources/sources.bib.md ──
    write_file(base / "30_references/sources/sources.bib.md", f"""\
# Sources Bibliography

| ID | 유형 | 제목 | 출처 | 날짜 |
|----|------|------|------|------|
| SPEC-001 | architecture | 4-Layer Orchestrator SPEC | (내부 문서) | {today} |
""")

    # ── 90_tests ──
    tc_modules = modules[:2] if modules and len(modules) >= 2 else ["example_a", "example_b"]
    tc_pack = packs[0] if packs else "example"

    write_file(base / "90_tests/test_cases.yaml", f"""\
# Test Cases for {domain}
# 최소 10개 이상의 케이스를 포함할 것.

- id: tc.evaluate.basic
  input: "이것을 평가해줘"
  expected_pattern: Evaluate
  expected_modules: [module.{tc_modules[0]}]
  must_include_fields: [판단, 근거, 트레이드오프, 확신도]

- id: tc.critique.basic
  input: "이 주장의 허점을 찾아줘"
  expected_pattern: Critique
  expected_modules: [module.{tc_modules[0]}]
  must_include_fields: [판단, 근거, 트레이드오프, 확신도]

- id: tc.translate.frame
  input: "이것을 다른 관점으로 바꿔줘"
  expected_pattern: Translate
  expected_modules: [module.{tc_modules[0]}, module.{tc_modules[1]}]
  must_include_fields: [판단, 근거]

- id: tc.prioritize.basic
  input: "우선순위를 정해줘"
  expected_pattern: Prioritize
  expected_modules: [module.{tc_modules[0]}]
  must_include_fields: [판단, 근거]

- id: tc.arbitrate.conflict
  input: "A와 B 중 어떤 것이 더 나은지 분석해줘"
  expected_pattern: Arbitrate
  expected_modules: [module.{tc_modules[0]}, module.{tc_modules[1]}]
  must_include_fields: [판단, 근거, 트레이드오프]

- id: tc.simulate.scenario
  input: "이 시나리오를 시뮬레이션해줘"
  expected_pattern: Simulate
  expected_modules: [module.{tc_modules[0]}]
  must_include_fields: [판단, 근거]

- id: tc.ref_load.quantitative
  input: "수치를 추정해줘"
  expected_pattern: Evaluate
  expected_modules: [module.{tc_modules[0]}]
  expected_reference: pack.{tc_pack}
  delta_q: 3

- id: tc.ref_skip.general
  input: "일반적으로 분석해줘"
  expected_pattern: Evaluate
  expected_modules: [module.{tc_modules[0]}]
  expected_reference: null
  delta_q: 0

- id: tc.multi_module.evaluate
  input: "여러 관점에서 평가해줘"
  expected_pattern: Evaluate
  expected_modules: [module.{tc_modules[0]}, module.{tc_modules[1]}]
  must_include_fields: [판단, 근거, 트레이드오프, 확신도]

- id: tc.schema.compliance
  input: "이 안건에 대해 의견을 줘"
  expected_pattern: Evaluate
  expected_modules: [module.{tc_modules[0]}]
  must_include_fields: [판단, 근거, 트레이드오프, 확신도]
""")

    write_file(base / "90_tests/eval_rubric.md", """\
# Evaluation Rubric

## 1. 패턴 감지 정확도 (목표: ≥ 90%)
## 2. 모듈 라우팅 정확도 (목표: ≥ 80%)
## 3. 출력 스키마 준수 (필수: 판단/근거/트레이드오프/확신도)
## 4. Reference 로딩 적절성 (ΔQ 규칙 준수)
## 5. 직교성 계수 α (목표: ≥ 0.85)

```
종합 점수 = (패턴 × 0.3) + (모듈 × 0.3) + (스키마 × 0.2) + (Reference × 0.1) + (직교성 × 0.1)
```
목표: ≥ 0.85
""")

    write_file(base / "90_tests/judge_prompt.md", """\
# Judge Prompt (Self-Evaluation)

아래 기준으로 출력 품질을 자체 평가한다.

1. **패턴 감지**: 입력에서 올바른 패턴을 감지했는가?
2. **모듈 선택**: 적절한 모듈이 활성화되었는가?
3. **출력 스키마**: {판단, 근거, 트레이드오프, 확신도}를 모두 포함하는가?
4. **Reference 로딩**: ΔQ 규칙에 따라 적절히 로딩/스킵했는가?
5. **직교성**: 모듈 간 결론이 서로 다른 질문 축에서 도출되었는가?

각 항목을 Pass/Partial/Fail로 판정한다.
""")

    # ── .gitkeep for empty dirs ──
    write_file(base / "90_tests/golden_outputs/.gitkeep", "")
    write_file(base / "30_references/sources/snapshots/.gitkeep", "")
    write_file(base / "99_archive/deprecated/.gitkeep", "")

    print(f"\n🎉 스킬팩 스캐폴딩 완료: {base}")
    print(f"   도메인: {domain}")
    print(f"   모듈: {modules or '(없음 — 수동 추가 필요)'}")
    print(f"   참조팩: {packs or '(없음 — 수동 추가 필요)'}")
    print(f"\n📋 다음 단계: Core → Modules → Orchestrator → References 순으로 콘텐츠를 채우세요.")


def main():
    parser = argparse.ArgumentParser(description="4-Layer Skill-Pack Scaffolding Generator")
    parser.add_argument("--domain", required=True, help="스킬팩 도메인명 (예: startup-advisor)")
    parser.add_argument("--output", required=True, help="출력 디렉토리 경로")
    parser.add_argument("--modules", default="", help="모듈 목록 (쉼표 구분, 예: pm,vc,marketer)")
    parser.add_argument("--packs", default="", help="참조팩 목록 (쉼표 구분, 예: tam_sam,unit_econ)")

    args = parser.parse_args()

    modules = [m.strip() for m in args.modules.split(",") if m.strip()] if args.modules else []
    packs = [p.strip() for p in args.packs.split(",") if p.strip()] if args.packs else []

    print(f"🏗️  Skillpack Factory — 4-Layer 스캐폴딩 생성")
    print(f"   도메인: {args.domain}")
    print(f"   출력: {args.output}")
    scaffold(args.domain, args.output, modules, packs)


if __name__ == "__main__":
    main()
