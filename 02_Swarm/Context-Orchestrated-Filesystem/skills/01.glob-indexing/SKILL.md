---
name: cof-glob-indexing
description: Resolves the nearest COF /[n].index/ from a target directory, scans within that node boundary, and writes NODE_INDEX.md and ROLE_EVIDENCE.md under the resolved index. Use when the user needs COF context boundary detection, role directory inference, or anchor discovery.
---

# COF Glob Indexing

`target_dir`(절대 경로) 기준으로 가장 가까운 `/[n].index/`를 찾아 **Node Root 경계 내**를 스캔하고, 선택된 인덱스 디렉토리 하위에 인덱싱 산출물(`NODE_INDEX.md`, `ROLE_EVIDENCE.md`)을 생성/갱신한다.

## When to Use

- “현재 위치에서 어떤 COF 노드에 속하는지”를 빠르게 확정해야 할 때
- `/[n].[role]/` 디렉토리 구조를 기반으로 role(포인터 타입)을 추론/기록해야 할 때
- Node Root 내 secondary `/[n].index/`(anchor) 위치를 수집해야 할 때
- 후속 에이전트가 재사용할 **경계/거점/근거**를 인덱스에 남겨야 할 때

## Inputs

- `target_dir` (required): 인덱싱 기준 디렉토리(절대 경로)
- `max_depth` (default: 10): Node Root 기준 하위 탐색 최대 깊이
- `include_hidden` (default: false): 숨김 폴더(`.` prefix) 포함 여부
- `follow_symlinks` (default: false): 심볼릭 링크 추적 여부

## Quick Start (Script)

```bash
python3 scripts/cof_glob_indexing.py \
  --target-dir "/abs/path/to/anywhere/inside/node" \
  --max-depth 10
```

## Outputs (Index Artifacts)

- 산출물은 **반드시** 선택된 `/[n].index/` 하위에 기록한다.
  - `NODE_INDEX.md` (human-first)
  - `ROLE_EVIDENCE.md` (agent-first, JSON 포함)
- 산출물은 append가 아니라 **갱신(overwrite)**을 기본으로 한다.

## Workflow (Checklist)

```
Indexing Progress:
- [ ] Step 1: Resolve nearest /[n].index/ (tie-break: smallest n, then lexicographic)
- [ ] Step 2: Identify Node Root and collect /[n].[role]/ directories
- [ ] Step 3: Discover secondary /[n].index/ anchors within node boundary (max_depth)
- [ ] Step 4: Emit role + anchor evidence (JSON list)
- [ ] Step 5: Write artifacts under the resolved /[n].index/
```

## Guardrails (Hard Constraints)

- 숫자 인덱스(`n`)에 의미를 부여하지 않는다.
- `/[n].index/`를 찾지 못한 상태에서 루트 무제한 스캔을 수행하지 않는다.
- Glob/패턴 매칭은 read-scope 후보를 제공할 뿐, 수정/삭제 권한을 의미하지 않는다.
- `99.history/` 등 정책/아카이브 영역은 기본적으로 read-only 컨텍스트로 취급한다.
- 표준 role token set은 고정: `index`, `reference`, `working`, `ticket`, `runtime`, `history`

## References

- Spec: `SPEC.md`
- Governance Guide: `../00.pointerical-tooling/references/cof-environment-set.md`
- Glob patterns: `../00.pointerical-tooling/references/glob-patterns.md`
- Rule normative: `../00.pointerical-tooling/references/rule-normative-interpretation.md`
