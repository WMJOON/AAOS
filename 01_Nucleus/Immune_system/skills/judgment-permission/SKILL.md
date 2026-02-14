---
name: judging-permission-request
description: "Tool/API 접근, 구조 생성/확장, 장기 저장 등 '권한'이 필요한 요청을 표준 템플릿으로 검증하고 판정 기록을 남긴다. Use when 권한이 필요한 요청(Tool/API 접근, 구조 생성/확장, 장기 저장)을 검증해야 할 때."
allowed-tools: Bash
---

# Swarm Inquisitor: Permission Judgment

Permission Principal Doctrine에 따라, 아래 요청은 "심판(검증)"을 전제로 한다.

- Tool/API 접근
- 구조 생성/확장
- 장기 저장(영구 보관)
- RULE/SKILL 변경으로 인한 계보 영향

## Quick Start

```bash
python3 scripts/judge_permission.py <permission_request.md>
```

## When to Use

- Tool/API 접근, 구조 생성/확장, 장기 저장 등 권한이 필요한 요청을 검증할 때
- RULE/SKILL 변경이 계보에 영향을 미치는지 판정해야 할 때

## Inputs

- `permission_request` (required): Permission Request 문서 경로 (템플릿: `../../templates/PERMISSION-REQUEST-TEMPLATE.md`)
- `--audit` (default: `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md`): 감사 로그 경로

## Outputs

- 판정 결과: `Approved` | `Conditional` | `Denied`
- `Conditional`인 경우: 제약/만료/해체 절차 보완 요구 사항
- `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md`에 판정 기록 append

## Workflow (Checklist)

```
Permission Judgment Progress:
- [ ] Step 1: Create permission request — 템플릿으로 요청서 작성
- [ ] Step 2: Run judge_permission.py — 스크립트 실행
- [ ] Step 3: Apply constraints — Conditional이면 제약/만료/해체 절차 보완 후 재심
- [ ] Step 4: Append audit log — 01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md에 판정 기록 추가
```

## Constraints

- 판정 기록은 반드시 `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md`에 append-only로 남긴다.
- `Conditional` 판정 시 제약/만료/해체 절차가 보완될 때까지 최종 승인하지 않는다.
- Permission Request 없이 권한 행사를 허용하지 않는다.

## References

- Script: `scripts/judge_permission.py`
- Template: `../../templates/PERMISSION-REQUEST-TEMPLATE.md`
- Immune DNA: `../../rules/README.md`
- Audit Log: `../../../record_archive/_archive/audit-log/AUDIT_LOG.md`
