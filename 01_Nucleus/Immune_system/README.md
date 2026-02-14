---
name: aaos-immune-system
scope: "04_Agentic_AI_OS/01_Nucleus/immune_system"
version: "0.3.1"
status: canonical
updated: "2026-02-14"
---

# AAOS Immune System

> AIVarium.Nucleus 구성 요소: “판정/집행/정통성 유지”를 담당한다.

Immune System은 AAOS가 **Self-Preserving / Self-Limiting** 시스템으로 유지되기 위한 면역 계층이다.  
이 폴더는 “무엇이 정통(Canonical)인가”를 판정하고, 오염/과증식/비정상 구조를 감지·차단·기록한다.

## 정렬 규칙

- 우선순위: `AAOS Canon > META Doctrine > Immune Doctrine > 이 문서`.
- `decree` 문체를 따른다. 하위구조 충돌/불명확 시 판정/증거를 남기고 즉시 상위 기관으로 귀속한다.
- 스스로를 완전 무비판적으로 검증하지 않는다. 본 구조는 Canon 직접 보증(bootstrap 예외) 대상이다.
- 디렉토리 네이밍 규칙은 `rules/08-naming-patterns.md`를 따른다.

## 구성

``` 
01_Nucleus/immune_system/
├── DNA.md                     # Immune System 정식 DNA
├── rules/                     # 상세 교리 규칙(모듈 분할)
│   └── README.md
├── README.md                  # 본 문서
├── _archive/
│   └── legacy/
│       ├── AAOS_IDENTITY_DNA_BLUEPRINT.md # 레거시 정체성 제안 문서(참고용)
│       └── templates/
│           └── DNA-BLUEPRINT-TEMPLATE.md  # 레거시 템플릿(신규 작성 비권장)
├── templates/
│   └── PERMISSION-REQUEST-TEMPLATE.md
└── skills/
    ├── judgment-dna/   # 변경 제안 판정 모듈
    ├── judgment-permission/
    ├── governance-skill/
    ├── lineage-context/
    └── core/
```

## 핵심 운영 원칙

> Blueprint 제도는 사람의 2차 점검 병목을 제거하기 위해 독립 제도 단계로는 폐지되었고, 동일 목적은 `record`/`audit` 루프의 비동기적 검증으로 수행한다.
1. `DNA.md` 없이 새 구조를 생성/확장할 수 없다.
2. Natural Dissolution은 목적·종료조건·해체절차가 반드시 있어야 한다.
3. Tool/API 접근, 장기 유지, 구조 변경은 Permission 판정 전제로 한다.
4. 모든 판정은 감사 기록으로 고정된다.
5. Pre-Commit/Agent wrapper/주기적 스캔은 Inquisitor 자동강제의 기본 채널이다.
6. Multi-Agent Consensus(최소 2 model family)는 Immune System DNA 변경에 적용한다.
7. `canonical` 결과만 구조 승격 조건을 만족한다.

## 상위 변경 게이트(요약)

다음은 상위기관 변경으로 간주한다.

- `DNA.md` 갱신
- Inquisitor 규칙/도구의 정합성에 영향 주는 변경
- 감사 로그 무결성 정책의 핵심 변경

통과 조건:

1. 변경 사유와 리스크를 `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md`에 기록
2. 다중 모델 합의 또는 예외 규칙(긴급보안/형식적 수정) 이행
3. Canon Guardian 승인 및 META 승인 경로 연결
4. `context_for_next` 제공

## 실행 루틴

### 1. 변경 제안 산출물 검증

```bash
python3 skills/core/yaml_validator.py /path/to/DNA.md
python3 skills/judgment-dna/scripts/verify_blueprint.py /path/to/structure  # 변경 제안 산출물 점검
```

### 2. 권한 요청 검증

```bash
python3 skills/core/yaml_validator.py /path/to/request.md --type permission
```

### 3. 자동 검증 설정

```bash
python3 skills/core/auto_inquisitor.py --gen-hook /path/to/aaos_root > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
python3 skills/core/auto_inquisitor.py --scan /path/to/aaos_root
```

### 4. Natural Dissolution 모니터링

```bash
python3 skills/core/dissolution_monitor.py --scan /path/to/aaos_root
python3 skills/core/dissolution_monitor.py --check-limits /path/to/structure
python3 skills/core/dissolution_monitor.py --dissolve /path/to/structure --reason "목적 완료" --dry-run
```

### 5. 감사 무결성

```bash
python3 skills/core/audit.py verify 01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md
python3 skills/core/audit.py stats 01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md
```

## 아카이브 병합 규약

- `AUDIT_LOG.md`의 정식 보관은 `01_Nucleus/record_archive/_archive/audit-log/AUDIT_LOG.md`에서 수행한다.
- `META_AUDIT_LOG.md`의 정식 보관은 `01_Nucleus/record_archive/_archive/meta-audit-log/META_AUDIT_LOG.md`에서 수행한다.
- 기존 구경로 스냅샷은 과거 증적으로 함께 보존하고, 신규 규약 문서에서 경로 기준은 `record_archive/_archive`를 사용한다.

## Bootstrap Exception

Immune System은 Canon에 의해 직접 보증되는 META 수준 구조이다.
따라서 `Immune System` 자체는 `DNA.md`의 자기검증을 면제한다.  
변경 제안은 `DNA.md` 단일 문서에서 버전/합의 메타데이터로 관리한다.
