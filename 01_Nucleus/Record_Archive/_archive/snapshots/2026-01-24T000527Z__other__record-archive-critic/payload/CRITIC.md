---
type: critic
target: "04_Agentic_AI_OS/01_AAOS-Record_Archive"
scope: record-archive
created: "2026-01-23"
archived: "2026-01-24T00:05:27Z"
---
# Critic: AAOS Record Archive System

## 핵심 결론

현재 `01_AAOS-Record_Archive/`는 “기관 선언(DNA_BLUEPRINT) + 간단 README”까지만 존재하며, META Doctrine이 요구하는 **증빙 고정(스냅샷/해시/인덱스/재현성)** 을 실제 파일 시스템으로 구현하지 못하고 있다.  
Record Archive가 기관 순서상 상위(2순위)로 지정된 것에 비해, 운영 표준(패키징/인덱싱/해시 원장)이 부재하여 “증빙이 흩어지고, 나중에 재현이 불가능해지는” 실패 모드가 발생하기 쉽다.

## 관찰된 결함 (Gap)

1. **실제 아카이브 저장소 부재**
   - `_archive/` 및 버킷 구조가 없어 “무엇을 어디에 어떻게 보존하는지”가 표준화되지 않음.
2. **Append-only 원칙의 실행 장치 부재**
   - “수정 금지”가 문장으로만 존재하고, 인덱스/원장/패키지 단위가 없어 실수로 덮어쓰기 쉬움.
3. **재현성(Reproducibility) 스펙 부재**
   - 스냅샷/해시/인덱스가 필요하다는 선언은 있으나, 최소 필수 필드/파일(매니페스트, 패키지 메타데이터, 참조 관계)이 정의되지 않음.
4. **상위 변경 게이트와의 연결 미흡**
   - Canon/META/기관 DNA/Swarm 루트 DNA 변경 시 “필수로 고정해야 하는 증빙 묶음”이 명시되지 않음.
5. **Homing Instinct의 구체 프로토콜 부재**
   - 충돌/불명확 감지 시 어떤 기록을 남기고 어디로 에스컬레이션하는지(최소 패킷)가 부족함.

## 권장 설계 (Target State)

1. **패키지 중심(Directory-as-Artifact)**
   - 아카이브의 최소 단위를 “폴더 1개(패키지)”로 고정: `PACKAGE.md` + `MANIFEST.sha256` + `payload/`.
2. **인덱스/해시 원장(ledger) 분리**
   - `indexes/ARCHIVE_INDEX.md`: 사람이 찾는 목록(엔트리 추가만).
   - `indexes/HASH_LEDGER.md`: 무결성 체인(엔트리 추가만, `prev_hash`→`hash` 연결).
3. **변경 게이트 표준 패킷**
   - 상위 변경(군체 이상 + META)마다 “스냅샷 + 합의 + 판정 참조 + 매니페스트”를 1패키지로 고정.
4. **실패 모드의 기본 행동**
   - 경로/권한/증빙 불명확 시: 패키지 작성 중단 → Immune System(Inquisitor) 심판 요청 → 결과를 다시 패키지에 추가(기존 내용 수정 금지).

## 구축 결과 (이번 턴 목표)

- `_archive/`, `indexes/`, `templates/`를 도입해 **운영 가능한 파일 시스템 표준**을 제공한다.
- Deliberation/Immune System과 연결되는 **최소 템플릿 3종**(패키지/매니페스트/숙의 패킷)을 제공한다.

