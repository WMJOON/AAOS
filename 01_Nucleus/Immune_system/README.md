---
name: aaos-immune-system
version: "0.3.0"
description: AAOS 구조의 자기보존·정화·정통성(Canonicality) 유지를 담당하는 계층. Doctrine(RULE)에 의해 해석되고 Inquisitor(SKILL)에 의해 집행된다.
canon_reference: "AAOS Canon Section 4, 5, 7"
---
# AAOS Immune System

> AIVarium.Nucleus 구성 요소: “판정/집행/정통성 유지”를 담당한다.

AAOS Immune System은 AAOS가 **Self-Preserving / Self-Limiting** 시스템으로 유지되기 위한 최소 면역 계층이다.
이 폴더는 "무엇이 정통(Canonical)인가"를 판정하고, 오염/과증식/비정상 구조를 **감지·차단·기록**하는 규칙과 스킬을 포함한다.

---

## 구성

```
01_Nucleus/Immune_system/
├── DNA.md                     # Immune System 정식 DNA (승격된 DNA)
├── AAOS_DNA_DOCTRINE_RULE.md  # 핵심 교리 규칙 (v0.2.0)
├── AUDIT_LOG.md               # 일반 판정 감사 로그 (해시 체인)
├── META_AUDIT_LOG.md          # META 수준 변경 감사 로그
├── README.md                  # 본 문서
├── templates/                 # Blueprint, Permission Request 템플릿
│   ├── DNA-BLUEPRINT-TEMPLATE.md
│   └── PERMISSION-REQUEST-TEMPLATE.md
└── SWARM_INQUISITOR_SKILL/    # Inquisitor 스킬 및 자동화 도구
    ├── blueprint-judgment/
    │   ├── SKILL.md
    │   └── scripts/verify_blueprint.py
    ├── permission-judgment/
    │   ├── SKILL.md
    │   └── scripts/judge_permission.py
    ├── skill-governance/
    │   ├── SKILL.md
    │   ├── scripts/verify_skill.py
    │   └── templates/SKILL-TEMPLATE.md
    ├── context-lineage/
    │   └── SKILL.md
    └── _shared/
        ├── SKILL.md              # inquisitor-core (공유 런타임 스킬)
        ├── yaml_validator.py      # YAML 파싱 및 값 검증
        ├── auto_inquisitor.py     # 자동 검증, Hook 생성
        ├── dissolution_monitor.py # Natural Dissolution 모니터링/실행
        ├── audit.py               # 감사 로그, 무결성 검증
        ├── lineage.py             # 파일→DNA 계보 참조 체인 해석
        └── frontmatter.py         # (레거시) 간이 frontmatter 파싱
```

---

## 운용 원칙 (요약)

1. **Blueprint 없는 생성/확장 금지**: DNA Blueprint가 없으면 Non-Canonical.
2. **Natural Dissolution 필수**: "언제/어떻게 사라지는가"가 명시되지 않은 구조는 오염으로 간주.
3. **Permission Principal**: Tool/API 접근, 저장/장기 유지, 구조 생성/확장 같은 행위는 Inquisitor 심판을 전제.
4. **모든 판정은 기록된다**: 최소한의 감사 로그를 남기고, 판정 근거를 재현 가능하게 유지.
5. **자동 강제 (v0.2.0)**: Pre-commit hook, Agent wrapper, 주기적 스캔으로 규칙 위반을 자동 차단.
6. **감사 무결성 (v0.2.0)**: 해시 체인으로 Audit Log 변조를 감지.
7. **다중 합의 (v0.3.0)**: Immune System DNA 변경은 플래그십 Agent 2종 이상 합의 + 인간 승인.

---

## 이식(Transplant) 원칙

- `SWARM_INQUISITOR_SKILL/_shared/`는 여러 judgment 스킬이 공유하는 코어 런타임이며, **`inquisitor-core` 스킬로 취급**한다.
- 따라서 “그대로 이식”하려면 단일 judgment 스킬만 떼어내지 말고 `SWARM_INQUISITOR_SKILL/` 트리(특히 `_shared/`)를 함께 복사하는 것이 안전하다.

---

## Quick Start

### 1. Blueprint 검증

```bash
# 새 구조의 Blueprint 검증
python3 SWARM_INQUISITOR_SKILL/_shared/yaml_validator.py /path/to/DNA.md

# 또는 기존 스크립트 사용
python3 SWARM_INQUISITOR_SKILL/blueprint-judgment/scripts/verify_blueprint.py /path/to/structure
```

### 2. 권한 요청 검증

```bash
python3 SWARM_INQUISITOR_SKILL/_shared/yaml_validator.py /path/to/request.md --type permission
```

### 3. 자동 검증 설정

```bash
# Git pre-commit hook 생성
python3 SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py --gen-hook /path/to/aaos_root > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# 전체 구조 스캔
python3 SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py --scan /path/to/aaos_root
```

### 4. Natural Dissolution 모니터링

```bash
# 해체 후보 스캔
python3 SWARM_INQUISITOR_SKILL/_shared/dissolution_monitor.py --scan /path/to/aaos_root

# 자원 상한 검사
python3 SWARM_INQUISITOR_SKILL/_shared/dissolution_monitor.py --check-limits /path/to/structure

# 해체 실행 (dry-run)
python3 SWARM_INQUISITOR_SKILL/_shared/dissolution_monitor.py --dissolve /path/to/structure --reason "목적 완료" --dry-run
```

### 5. Audit Log 무결성 검증

```bash
python3 SWARM_INQUISITOR_SKILL/_shared/audit.py verify AUDIT_LOG.md
python3 SWARM_INQUISITOR_SKILL/_shared/audit.py stats AUDIT_LOG.md
```

---

## Bootstrap Exception

Immune System은 Canon에 의해 직접 보증되는 META 수준 구조이다.
따라서 일반 Inquisitor 검증 대신 다음 규칙이 적용된다:

- **DNA.md**: 자기 검증 면제(bootstrap), Canon Section 4, 5에 의해 정당성 부여된 정식 DNA
- **변경 시**: META_AUDIT_LOG.md에 기록, Canon 수호자(인간) 승인 필요
- **무결성**: 자체 파일 해시로 변조 감지

변경 제안은 `DNA_BLUEPRINT.md`로 작성하고, 승인/승격 시 `DNA.md`로 rename한다.
자세한 내용은 [DNA.md](./DNA.md)와 [AAOS_DNA_DOCTRINE_RULE.md](./AAOS_DNA_DOCTRINE_RULE.md) Section 6 참조.

---

## Version History

- **v0.1.0**: 최초 Immune System 구성
- **v0.2.0**: Auto-Enforcement, Audit Integrity, Bootstrap Exception, Dissolution Monitor 추가
- **v0.3.0**: Multi-Agent Consensus 교리 반영, Blueprint/validator 정합성 보강
