---
name: providing-inquisitor-runtime
description: "Swarm Inquisitor 공통 런타임(validator/audit/auto-enforcement/dissolution). 다른 judgment 스킬들이 의존하는 '공유 코어'이며 단독 이식 시 반드시 함께 복사해야 한다. Use when judgment 스킬(judgment-permission, judgment-dna)을 실행하거나 이식할 때."
allowed-tools: Bash
---

# Inquisitor Core (Shared Runtime)

이 폴더는 `judgment-permission`, `judgment-dna`가 공통으로 사용하는 코어 런타임이다.
AAOS Immune System 내부에서 **중복을 줄이고**, **판정 로직을 일관되게** 유지하기 위해 공유 모듈을 한 곳에 둔다.

## Quick Start

```python
# 다른 judgment 스킬에서 공유 모듈 임포트
from core.yaml_validator import validate_blueprint
from core.audit import safe_append_audit_entry
```

## When to Use

- `judgment-permission` 또는 `judgment-dna` 스킬을 실행할 때 (자동 의존)
- Inquisitor 스킬을 새로운 환경으로 이식(transplant)할 때
- 판정 로직의 공통 모듈을 확인/수정해야 할 때

## Inputs

- 본 스킬은 라이브러리 성격이므로 직접 실행하지 않는다.
- 의존 스킬(`judgment-permission`, `judgment-dna`)이 내부적으로 임포트한다.

## Outputs

- `yaml_validator.py`: Blueprint/Permission 요청 YAML 파싱 + 빈 값 검증 결과
- `audit.py`: Append-only + 해시체인 기반 Audit Log 무결성 보장
- `auto_inquisitor.py`: 자동 스캔/훅/프리플라이트(집행) 결과
- `dissolution_monitor.py`: Natural Dissolution 모니터링/실행 결과

## Workflow (Checklist)

```
Transplant Progress:
- [ ] Step 1: 의존 폴더(core/) 함께 복사 확인
- [ ] Step 2: 상대경로 import가 새 위치에서 유효한지 검증
- [ ] Step 3: audit log 경로가 새 AAOS 루트 기준으로 올바른지 확인
- [ ] Step 4: strict mode 정책 필요 여부 판단
```

## Constraints

- 단일 judgment 스킬만 복사하면 동작하지 않을 수 있다 — 본 폴더를 반드시 함께 복사한다.
- 공유 모듈의 변경은 의존하는 모든 judgment 스킬에 영향을 미친다.
- `audit.py`의 append-only 속성을 훼손하는 변경은 금지한다.
- Immune System 내부 변경이므로 `record_archive/_archive/meta-audit-log/META_AUDIT_LOG.md` 기록을 권장한다.

## References

- Blueprint Judgment: `../judgment-dna/SKILL.md`
- Permission Judgment: `../judgment-permission/SKILL.md`
- Immune DNA: `../../rules/README.md`
