---
name: judging-blueprint-canonicality
description: "DNA Blueprint 존재/형식/자연소멸/자원상한 명시 여부를 검증하고 Canonicality를 판정한다. Use when 구조 생성/확장 요청이 들어와 Blueprint 검증이 필요할 때."
allowed-tools: Bash
---

# Swarm Inquisitor: Blueprint Judgment

DNA 없는 구조는 Non-Canonical이다.
본 스킬은 `DNA.md`를 검증하고 판정 결과를 `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md`에 기록한다.

## Quick Start

```bash
python3 scripts/verify_blueprint.py <target_path>
```

## When to Use

- 새로운 구조(디렉토리/모듈)를 생성하거나 확장하려는 요청이 들어왔을 때
- 기존 DNA의 정통성(Canonicality)을 검증해야 할 때

## Inputs

- `target_path` (required): 검증 대상 폴더 또는 blueprint 파일 경로
- `--blueprint` (default: `AUTO`): `DNA.md` 자동 선택, 또는 명시 지정
- `--audit` (default: `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md`): 감사 로그 경로

## Outputs

- 판정 결과: `Canonical` | `Canonical-Conditional` | `Non-Canonical`
- `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md`에 판정 기록 append

## Workflow (Checklist)

```
Blueprint Judgment Progress:
- [ ] Step 1: Confirm target path — 검증 대상 폴더/파일 경로 확정
- [ ] Step 2: Run verify_blueprint.py — 스크립트 실행
- [ ] Step 3: Review result — 판정 결과 + 필요 시 보완 사항 확인
- [ ] Step 4: Append audit log — 01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md에 판정 기록 추가
```

### 판정 기준

- `Canonical`: 통과
- `Canonical-Conditional`: 보완 후 재심 권고
- `Non-Canonical`: 차단(생성/확장 금지)

## Constraints

- Blueprint/DNA가 없는 구조는 Non-Canonical로 판정한다.
- 판정 기록은 반드시 `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md`에 append-only로 남긴다.
- `Non-Canonical` 판정 시 구조 생성/확장을 차단한다.
- 자연소멸(Natural Dissolution) 조건 명시 여부를 반드시 검증한다.

## References

- Script: `scripts/verify_blueprint.py`
- Immune DNA: `../../rules/README.md`
- Audit Log: `../../../record_archive/_archive/audit-log/AUDIT_LOG.md`
