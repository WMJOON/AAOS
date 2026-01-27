---
name: aaos-record-archive
description: AAOS Record Archive System. 감사/합의/승인/해체 기록을 장기 보존하고 재현 가능한 근거를 제공하는 아카이빙 기관.
---
# AAOS Record Archive System

- DNA Blueprint: `04_Agentic_AI_OS/01_AAOS-Record_Archive/DNA_BLUEPRINT.md`
- 상위 규범: `04_Agentic_AI_OS/README.md` → `04_Agentic_AI_OS/METADoctrine.md` → `04_Agentic_AI_OS/02_AAOS-Immune_system/AAOS_DNA_DOCTRINE_RULE.md`

## 역할

- Immune System의 판정/승인/합의 기록을 “장기 보존 가능한 형태”로 아카이빙
- 정통성 분쟁 시 증빙 재현(근거 스냅샷/인덱스/해시)
- Natural Dissolution 실행 결과의 요약본을 보존

## 원칙

- Append-only (수정 금지, 추가만 허용)
- Homing Instinct (충돌 시 Immune System으로 귀속)

## 디렉토리 구조 (운영 표준)

```
01_AAOS-Record_Archive/
├── README.md
├── DNA_BLUEPRINT.md
├── _archive/                        # 실제 패키지(append-only)
│   ├── README.md
│   ├── audit-log/                   # 5년 보존
│   ├── meta-audit-log/              # 10년 보존
│   ├── deliberation/                # 3년 보존
│   ├── approvals/                   # 10년 보존
│   ├── snapshots/                   # 10년 보존 (필요 시 요약 패키지로 갱신)
│   └── disputed/                    # 분쟁/격리 (해결시까지)
├── indexes/                         # 인덱스/해시 원장(append-only)
│   ├── README.md
│   ├── ARCHIVE_INDEX.md
│   └── HASH_LEDGER.md
└── templates/                       # 패키지/매니페스트 템플릿
    ├── ARCHIVE_PACKAGE_TEMPLATE.md
    ├── MANIFEST_SHA256_TEMPLATE.txt
    ├── DELIBERATION_PACKET_TEMPLATE.md
    ├── DELIBERATION_TO_ARCHIVE_PROCEDURE.md
    └── VERIFY_LEDGER_CHECKLIST.md
```

## 운영 규칙 (요약)

- **아카이브 단위는 “패키지 폴더 1개”** 이다. 패키지는 `_archive/<bucket>/<timestamp>__<type>__<slug>/` 형식으로 생성한다.
- 패키지는 최소한 `PACKAGE.md`(메타데이터) + `MANIFEST.sha256`(무결성 목록) + `payload/`(증빙 파일들)을 포함한다.
- `indexes/HASH_LEDGER.md`는 **반드시 자동화 스크립트(`scripts/ledger_keeper.py`)를 통해서만 업데이트해야 한다.** 수동 편집은 금지된다.
- 충돌/불명확/권한 경계 감지 시: **추가 작업을 중단**하고 `02_AAOS-Immune_system/`에 심판(혹은 보류)을 요청한다.

## Critic 기록 규칙

- Critic(비평/사후 분석)은 루트 파일로 두지 않고 **`_archive/` 패키지로만** 보존한다(append-only).

## 언제 무엇을 아카이빙하나 (최소 요구)

- **상위기관 변경 게이트**(Canon/META/기관 DNA/Swarm 루트 DNA):
  - 변경 전/후 스냅샷(대상 파일)
  - Deliberation 산출물(합의 요약 + 근거 링크)
  - Immune System 판정 기록(AUDIT_LOG/META_AUDIT_LOG 관련 엔트리 참조)
  - 패키지 매니페스트 해시 + 원장(HASH_LEDGER) 체인 업데이트

- **Record Archive DNA 승격/변경**(본 기관 자체의 DNA/스크립트/운영 규칙):
  - 플래그십 Agent 2종 이상 합의(Deliberation Packet)
  - `_archive/` 패키지로 증빙 고정 + `HASH_LEDGER` 체인 연결

## 빠른 절차 (수동)

## 빠른 절차 (수동 + 자동)

1. `_archive/<bucket>/`에 새 패키지 폴더 생성
2. `templates/ARCHIVE_PACKAGE_TEMPLATE.md`를 `PACKAGE.md`로 복사해 메타데이터 작성
3. 증빙 파일을 `payload/`에 넣고, `MANIFEST.sha256`를 생성(템플릿 참고)
4. **Script 실행**: `python3 scripts/ledger_keeper.py <package_path> "<notes>"`
   - 이 스크립트가 `HASH_LEDGER.md`에 해시 체인을 연결하고, `ARCHIVE_INDEX.md` 업데이트용 스니펫을 출력한다.
5. 출력된 스니펫을 `indexes/ARCHIVE_INDEX.md`에 추가한다.
6. `templates/VERIFY_LEDGER_CHECKLIST.md`로 prev_hash 연결 검증 (스크립트가 수행하지만 교차 검증 권장)

## Sibling 기관 간 표준 워크플로우

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        상위기관 변경 게이트 워크플로우                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [1] 변경 제안 발생                                                          │
│       │                                                                     │
│       ▼                                                                     │
│  ┌─────────────────────────────────────────┐                               │
│  │      DELIBERATION CHAMBER               │                               │
│  │  ─────────────────────────────────────  │                               │
│  │  • 변경 제안 수집                         │                               │
│  │  • Multi-Agent 합의 진행                 │                               │
│  │  • 위험/영향 분석                         │                               │
│  │  • verdict/rationale 정리               │                               │
│  │                                         │                               │
│  │  Output: Deliberation Packet            │                               │
│  └─────────────────┬───────────────────────┘                               │
│                    │                                                        │
│                    ▼                                                        │
│  ┌─────────────────────────────────────────┐                               │
│  │         IMMUNE SYSTEM                   │                               │
│  │  ─────────────────────────────────────  │                               │
│  │  • 합의 결과 검토                         │                               │
│  │  • 정통성/권한 판정                       │                               │
│  │  • 승인/거부/수정요청 결정                 │                               │
│  │  • AUDIT_LOG / META_AUDIT_LOG 기록       │                               │
│  │                                         │                               │
│  │  Output: Judgment + Audit Entry         │                               │
│  └─────────────────┬───────────────────────┘                               │
│                    │                                                        │
│          ┌────────┴────────┐                                               │
│          │                 │                                                │
│          ▼                 ▼                                                │
│     [승인됨]           [거부/분쟁]                                           │
│          │                 │                                                │
│          ▼                 ▼                                                │
│  ┌─────────────────────────────────────────┐                               │
│  │         RECORD ARCHIVE                  │                               │
│  │  ─────────────────────────────────────  │                               │
│  │  • 패키지 생성 (PACKAGE.md + payload)    │                               │
│  │  • MANIFEST.sha256 생성                 │                               │
│  │  • ARCHIVE_INDEX 엔트리 추가             │                               │
│  │  • HASH_LEDGER 체인 연결                │                               │
│  │  • prev_hash 검증                       │                               │
│  │                                         │                               │
│  │  승인 → _archive/snapshots/ 또는 해당 버킷│                               │
│  │  분쟁 → _archive/disputed/              │                               │
│  └─────────────────────────────────────────┘                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 책임 경계

| 기관 | 역할 | 하지 않는 것 |
|------|------|-------------|
| **Deliberation Chamber** | 합의 정리, 근거 수집 | 판정, 집행, 보존 |
| **Immune System** | 판정, 승인/거부, 감사 기록 | 합의 진행, 장기 보존 |
| **Record Archive** | 증빙 패키징, 해시 체인, 장기 보존 | 판정, 합의 |

### 상호작용 프로토콜

1. **Deliberation → Immune**: Deliberation Packet 제출 (`multi_agent_consensus` 포함)
2. **Immune → Archive**: 판정 완료 후 `audit_refs` 제공
3. **Deliberation → Archive**: 합의 산출물을 `templates/DELIBERATION_TO_ARCHIVE_PROCEDURE.md` 절차로 이관
4. **Archive → Immune**: 체인 파손/분쟁 시 Inquisitor 심판 요청

### 분쟁 발생 시

```
분쟁 감지 → Archive 작업 중단 → disputed/ 격리 → Immune 심판 요청
                                                    │
                     ┌──────────────────────────────┴──────────────────────────────┐
                     ▼                              ▼                              ▼
                  [승인]                         [거부]                        [수정요청]
                     │                              │                              │
                     ▼                              ▼                              ▼
              원래 버킷 복원                    폐기 (기록 보존)                Deliberation 재회부
```
