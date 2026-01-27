---
description: Deliberation Chamber 산출물을 Record Archive 패키지로 변환하는 표준 절차
version: "1.0.0"
---
# Deliberation Packet → Archive Package 변환 절차

## 개요

Deliberation Chamber가 합의를 완료하면, 그 산출물은 Record Archive의 `_archive/deliberation/` 버킷에 패키지로 고정되어야 한다.
이 문서는 변환의 표준 절차를 정의한다.

---

## 전제 조건 (Prerequisites)

변환을 시작하기 전 다음을 확인:

- [ ] Deliberation Packet의 `status`가 `submitted` 이상
- [ ] `multi_agent_consensus`에 최소 1개 이상의 verdict 기록 존재
- [ ] Immune System 판정이 필요한 경우, 판정 완료 여부 확인

---

## 변환 절차

### Step 1: 패키지 폴더 생성

```
_archive/deliberation/<YYYY-MM-DDTHHMMSSZ>__deliberation-consensus__<slug>/
├── PACKAGE.md
├── MANIFEST.sha256
└── payload/
    └── DELIBERATION_PACKET.md
```

**폴더명 규칙**:
- `<timestamp>`: UTC ISO 8601 (초 단위까지, 콜론 제거)
- `<slug>`: 합의 대상의 간단한 식별자 (예: `immune-doctrine-v0.3`, `meta-doctrine-update`)

### Step 2: Deliberation Packet 복사

1. 원본 Deliberation Packet을 `payload/DELIBERATION_PACKET.md`로 복사
2. 원본 경로를 `PACKAGE.md`의 `source_refs`에 기록
3. 원본 상태를 `status: archived`로 변경 (optional, Deliberation Chamber 정책에 따름)

### Step 3: 관련 증빙 수집

다음을 `payload/`에 추가:

| 증빙 유형 | 파일명 (권장) | 필수 여부 |
|-----------|---------------|-----------|
| 변경 전 스냅샷 | `BEFORE_<target>.md` | 상위기관 변경 시 필수 |
| 변경 후 스냅샷 | `AFTER_<target>.md` | 상위기관 변경 시 필수 |
| 위험/영향 분석 | `RISK_ANALYSIS.md` | 권장 |
| Agent별 rationale 상세 | `AGENT_RATIONALES.md` | 선택 |

### Step 4: PACKAGE.md 작성

`templates/ARCHIVE_PACKAGE_TEMPLATE.md`를 기반으로 작성:

```yaml
---
timestamp: "<패키지 생성 시각>"
package_id: "<폴더명>"
type: "deliberation-consensus"
status: "sealed"

source_refs:
  - "04_Agentic_AI_OS/01_Nucleus/Deliberation_Chamber/<원본 경로>"

targets:
  - "<합의 대상 경로 또는 ID>"

audit_refs:
  - "04_Agentic_AI_OS/01_Nucleus/Immune_system/AUDIT_LOG.md#<entry>"
  # Immune System 판정이 있는 경우

integrity:
  manifest: "MANIFEST.sha256"
  manifest_sha256: "<Step 5에서 계산>"

created_by:
  actor: "<agent-name 또는 human>"
  method: "manual | tool"

deliberation_summary:
  subject: "<Deliberation Packet의 subject>"
  final_verdict: "approve | reject | request-changes"
  consensus_count: <N>
  dissent_count: <M>
---
# Archive Package: Deliberation Consensus

## Summary

- 합의 대상: <targets>
- 최종 결론: <final_verdict>
- 합의 참여: <N>명 동의, <M>명 반대/수정요청

## Contents

- `payload/DELIBERATION_PACKET.md`: 원본 숙의 패킷
- `payload/BEFORE_*.md`: 변경 전 스냅샷 (해당 시)
- `payload/AFTER_*.md`: 변경 후 스냅샷 (해당 시)
- `MANIFEST.sha256`: 무결성 해시 목록
```

### Step 5: MANIFEST.sha256 생성

```bash
cd _archive/deliberation/<package>/
shasum -a 256 PACKAGE.md payload/* > MANIFEST.sha256
```

### Step 6: 인덱스 업데이트

#### ARCHIVE_INDEX.md에 엔트리 추가

```yaml
---
timestamp: "<패키지 timestamp>"
package_path: "_archive/deliberation/<package>/"
type: "deliberation-consensus"
targets:
  - "<합의 대상>"
summary: "<1-2줄 요약>"
manifest_sha256: "<MANIFEST.sha256 파일의 sha256>"
---
```

#### HASH_LEDGER.md에 체인 엔트리 추가

```yaml
---
timestamp: "<패키지 timestamp>"
package_path: "_archive/deliberation/<package>/"
artifact: "MANIFEST.sha256"
prev_hash: "<직전 엔트리의 hash>"
hash: "<MANIFEST.sha256 파일의 sha256>"
---
```

### Step 7: 검증

`templates/VERIFY_LEDGER_CHECKLIST.md`의 "패키지 추가 시 검증" 수행:

- [ ] prev_hash 연결 확인
- [ ] manifest_sha256 일치 확인
- [ ] timestamp 순서 확인

---

## 특수 케이스

### 상위기관 변경 게이트 통과 시

추가 필수 사항:
- `payload/BEFORE_*.md`, `payload/AFTER_*.md` 스냅샷 필수
- Immune System 판정 참조 (`audit_refs`) 필수
- `_archive/snapshots/`에도 별도 스냅샷 패키지 생성 권장

### 합의 실패 (reject) 시

- 패키지는 동일하게 생성 (기록 보존 목적)
- `final_verdict: reject` 명시
- `dissent_count` 및 반대 rationale 보존

### 분쟁 발생 시

- 패키지를 `_archive/disputed/`에 생성
- `status: disputed` 설정
- Immune System(Inquisitor) 심판 요청

---

## 체크리스트 요약

```
□ Deliberation Packet status 확인
□ 패키지 폴더 생성
□ payload/ 에 증빙 수집
□ PACKAGE.md 작성
□ MANIFEST.sha256 생성
□ ARCHIVE_INDEX.md 엔트리 추가
□ HASH_LEDGER.md 체인 엔트리 추가
□ prev_hash 연결 검증
□ manifest_sha256 일치 검증
```
