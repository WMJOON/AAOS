---
name: inquisitor-core
description: Swarm Inquisitor 공통 런타임(validator/audit/auto-enforcement/dissolution). 다른 judgment 스킬들이 의존하는 “공유 코어”이며 단독 이식 시 반드시 함께 복사해야 한다.
trigger: on_request
---
# Inquisitor Core (Shared Runtime)

이 폴더는 `permission-judgment`, `blueprint-judgment`가 공통으로 사용하는 코어 런타임이다.
AAOS Immune System 내부에서 **중복을 줄이고**, **판정 로직을 일관되게** 유지하기 위해 공유 모듈을 한 곳에 둔다.

## 포함 모듈

- `yaml_validator.py`: Blueprint/Permission 요청 실제 YAML 파싱 + 빈 값 검증
- `audit.py`: Append-only + 해시체인 기반 Audit Log 무결성
- `auto_inquisitor.py`: 자동 스캔/훅/프리플라이트(집행)
- `dissolution_monitor.py`: Natural Dissolution 모니터링/실행

## 이식(Transplant) 규칙

1. **단일 judgment 스킬만 복사하면 동작하지 않을 수 있다.**
2. 이식 시에는 최소 단위로 아래를 함께 복사한다.
   - `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/blueprint-judgment/`
   - `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/permission-judgment/`
   - `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/` (본 폴더)
3. “공유 파일은 하나의 스킬이어야 한다”는 관점에서, 본 폴더는 **`inquisitor-core` 스킬**로 간주한다.
