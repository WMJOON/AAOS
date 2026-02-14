---
name: tracing-lineage-context
description: "파일을 읽기/수정하기 전에, 해당 경로에서 시작하는 DNA 계보(노드 DNA → Immune → META → Canon)를 해석하고 행동 심각도에 따라 읽어야 할 규범 참조를 제시한다. Use when 파일의 규범 계보를 확인하거나 수정/삭제 전 심각도에 맞는 참조를 안내받아야 할 때."
allowed-tools: Bash
---

# Context Lineage (파일 읽기 → DNA 인지)

AAOS OS Core에서 "파일을 읽는다"는 것은, 그 파일이 속한 **노드의 DNA(blueprint)를 먼저 인지**한다는 뜻이다.
그리고 행동이 파괴적/고위험일수록 자연스럽게 **Immune → META → Canon**까지 참조가 확장되어야 한다.

이 스킬은 그 체인을 자동으로 계산해 출력한다.

## Quick Start

```bash
python3 01_Nucleus/immune_system/skills/core/auto_inquisitor.py \
  --context "<target_path>" --severity medium --format md
```

## When to Use

- 어떤 파일을 열었는데 "이 작업의 규범이 어디서 시작되는가?"가 불명확할 때
- 파일 수정/삭제/구조 생성/정책 변경 등 행동 전에 심각도에 맞는 참조를 자동으로 안내받고 싶을 때

## Inputs

- `target_path` (required): 계보를 추적할 대상 파일 또는 디렉토리 경로
- `severity` (required): 행동 심각도 — `low` | `medium` | `high` | `meta`
- `format` (default: `md`): 출력 형식 — `md` | `text`

## Outputs

- 가장 가까운 `DNA.md`를 `node.dna_blueprint`로 제시
- (있다면) 가장 가까운 `RULE.md`를 `node.rule`로 제시
- 심각도에 따라 `rules/README.md`, `00_METADoctrine/DNA.md`, `README.md`까지 확장
- 누락된 참조는 `MISSING`으로 표시하여 Non-Canonical 위험을 즉시 드러냄

## Workflow (Checklist)

```
Lineage Tracing Progress:
- [ ] Step 1: target_path에서 가장 가까운 DNA.md 탐색
- [ ] Step 2: 가장 가까운 RULE.md 탐색
- [ ] Step 3: severity에 따라 참조 확장 범위 결정
- [ ] Step 4: 누락된 참조를 MISSING으로 표시
- [ ] Step 5: 지정 format으로 계보 결과 출력
```

### 심각도(severity) 가이드

- `low`: 읽기/메모/비파괴 편집(로컬 노드 수준)
- `medium`: 파일 생성/일반 수정/구조 확장(면역체계까지)
- `high`: 삭제/대규모 변경/장기 저장/권한 요청(메타/캐논까지)
- `meta`: Immune System/DNA/규범 자체 변경(메타 감사 + 합의/승인 전제)

## Constraints

- DNA 계보는 항상 가장 가까운 노드에서 시작하여 상위로 확장한다.
- `severity`가 명시되지 않으면 기본값 `medium`을 적용한다.
- 계보 추적 결과를 수정하거나 파일을 변경하지 않는다(read-only).
- `MISSING` 참조가 발견되면 Non-Canonical 경고를 반드시 포함한다.

## References

- Script: `core/auto_inquisitor.py`
- Lineage resolver: `core/lineage.py`
- Immune DNA: `../../rules/README.md`
