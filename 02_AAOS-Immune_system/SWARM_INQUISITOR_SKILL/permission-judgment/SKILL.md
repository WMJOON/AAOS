---
name: permission-judgment
description: Tool/API 접근, 구조 생성/확장, 장기 저장 등 “권한”이 필요한 요청을 표준 템플릿으로 검증하고 판정 기록을 남긴다.
---
# Swarm Inquisitor: permission-judgment

Permission Principal Doctrine에 따라, 아래 요청은 “심판(검증)”을 전제로 한다.

- Tool/API 접근
- 구조 생성/확장
- 장기 저장(영구 보관)
- RULE/SKILL 변경으로 인한 계보 영향

## Workflow

```
Task Progress:
- [ ] Step 1: Create a permission request (template)
- [ ] Step 2: Run judge_permission.py
- [ ] Step 3: Apply constraints / time-bound limits
- [ ] Step 4: Append audit log
```

## Step 1: Permission request template

템플릿: `../../templates/PERMISSION-REQUEST-TEMPLATE.md`

## Step 2: Run judge_permission.py

```bash
python3 scripts/judge_permission.py <permission_request.md>
```

Options:
- `--audit <path>`: 감사 로그 경로 지정(기본: `02_AAOS-Immune_system/AUDIT_LOG.md`)

## Step 3: Apply constraints

`Canonical-Conditional`이면 “제약/만료/해체 절차”를 보완하고 재심한다.

