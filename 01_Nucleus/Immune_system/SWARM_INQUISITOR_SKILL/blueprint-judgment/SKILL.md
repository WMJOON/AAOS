---
name: blueprint-judgment
description: DNA Blueprint 존재/형식/자연소멸/자원상한 명시 여부를 검증하고 Canonicality를 판정한다. 구조 생성/확장 요청이 들어오면 사용한다.
---
# Swarm Inquisitor: blueprint-judgment

Blueprint/DNA 없는 구조는 Non-Canonical이다.
본 스킬은 `DNA.md`(정식) 또는 `DNA_BLUEPRINT.md`(변경 제안)를 검증하고 판정 결과를 `AUDIT_LOG.md`에 기록한다.

## Workflow

Copy this checklist and track your progress:

```
Task Progress:
- [ ] Step 1: Confirm target path
- [ ] Step 2: Run verify_blueprint.py
- [ ] Step 3: Review result + required fixes (if any)
- [ ] Step 4: Append audit log
```

## Step 1: Confirm target path

검증 대상 폴더(또는 blueprint 파일 경로)를 확정한다.

## Step 2: Run verify_blueprint.py

```bash
python3 scripts/verify_blueprint.py <target_path>
```

Options:
- `--blueprint AUTO`: `DNA.md` → `DNA_BLUEPRINT.md` 순으로 자동 선택 (기본)
- `--blueprint DNA_BLUEPRINT.md`: 변경 제안 파일을 명시 검증
- `--audit <path>`: 감사 로그 경로 지정(기본: `01_Nucleus/Immune_system/AUDIT_LOG.md`)

## Step 3: Review result

- `Canonical`: 통과
- `Canonical-Conditional`: 보완 후 재심 권고
- `Non-Canonical`: 차단(생성/확장 금지)

## Step 4: Audit

본 스크립트는 기본적으로 `AUDIT_LOG.md`에 판정 기록을 추가한다.
