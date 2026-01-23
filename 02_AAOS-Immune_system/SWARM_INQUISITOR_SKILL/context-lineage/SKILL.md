---
name: context-lineage
description: 파일을 읽기/수정하기 전에, 해당 경로에서 시작하는 DNA 계보(노드 DNA → Immune → META → Canon)를 해석하고 행동 심각도에 따라 읽어야 할 규범 참조를 제시한다.
trigger: on_request
---
# Context Lineage (파일 읽기 → DNA 인지)

AAOS OS Core에서 “파일을 읽는다”는 것은, 그 파일이 속한 **노드의 DNA(blueprint)를 먼저 인지**한다는 뜻이다.
그리고 행동이 파괴적/고위험일수록 자연스럽게 **Immune → META → Canon**까지 참조가 확장되어야 한다.

이 스킬은 그 체인을 자동으로 계산해 출력한다.

## 사용 시점

- 어떤 파일을 열었는데 “이 작업의 규범이 어디서 시작되는가?”가 불명확할 때
- 파일 수정/삭제/구조 생성/정책 변경 등 행동 전에 심각도에 맞는 참조를 자동으로 안내받고 싶을 때

## 심각도(severity) 가이드

- `low`: 읽기/메모/비파괴 편집(로컬 노드 수준)
- `medium`: 파일 생성/일반 수정/구조 확장(면역체계까지)
- `high`: 삭제/대규모 변경/장기 저장/권한 요청(메타/캐논까지)
- `meta`: Immune System/DNA/규범 자체 변경(메타 감사 + 합의/승인 전제)

## 실행

Markdown 출력:

```bash
python3 04_Agentic_AI_OS/02_AAOS-Immune_system/SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py --context "<path>" --severity high --format md
```

Text 출력:

```bash
python3 04_Agentic_AI_OS/02_AAOS-Immune_system/SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py --context "<path>" --severity medium --format text
```

## 기대 결과

- 가장 가까운 `DNA.md`(정식) 또는 `DNA_BLUEPRINT.md`(제안)를 찾아 `node.dna_blueprint`로 제시
- (있다면) 가장 가까운 `RULE.md`를 `node.rule`로 제시
- 심각도에 따라 `AAOS_DNA_DOCTRINE_RULE.md`, `04_Agentic_AI_OS/METADoctrine.md`, `04_Agentic_AI_OS/README.md`까지 확장
- 누락된 참조는 `MISSING`으로 표시하여 Non-Canonical 위험을 즉시 드러냄
