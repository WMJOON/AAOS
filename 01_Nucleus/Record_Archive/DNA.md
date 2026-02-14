---
name: aaos-record-archive-dna
scope: "04_Agentic_AI_OS/01_Nucleus/record_archive"
status: canonical
version: "0.2.7"
updated: "2026-02-14"
---

# AAOS Record Archive System (DNA)

## Supremacy Clause

Record Archive는 Canon/META/Immune 규범의 판정 근거를 보존한다.
`homing_instinct`에 따라 충돌·권한 경계 불명확 시 즉시 Immune로 귀속하여 판정 후 진행한다.

## 역할

- `record_archive/_archive/audit-log/AUDIT_LOG.md`, `record_archive/_archive/meta-audit-log/META_AUDIT_LOG.md`의 장기 스냅샷과 패키지 보존
- 다중 에이전트 합의 증빙(근거, 리스크, 모델 메타데이터)
- NATURAL dissolution 실행 요약 및 해체 이력 보존

## 운영 원칙 (MUST)

1. `HASH_LEDGER.md` 업데이트는 `scripts/ledger_keeper.py`로만 수행한다.
2. 수동 문자열 편집은 비정상 조작으로 간주한다.
3. 패키지는 `PACKAGE.md`, `MANIFEST.sha256`, `payload`를 최소 구성으로 가진다.
4. 모든 패키지는 `_archive/<bucket>/<timestamp>__<type>__<slug>/` 형식을 따른다.
5. `package -> MANIFEST -> HASH_LEDGER` 체인은 추적 가능해야 한다.
6. record_archive에 `pending/`, `working/`, `draft/` 등 작업용 디렉토리를 생성해서는 안 된다. 활성 작업 산출물은 `deliberation_chamber`에서 관리하며, 봉인 완료된 증빙만 `_archive/`로 수용한다.

## 상위 변경 게이트

- 대상: Canon/META 변경, 기관 DNA 변경, Swarm 루트 DNA 변경
- 필수 증빙:
  - Deliberation Packet
  - Immune 판단 및 감사 엔트리(`AUDIT_LOG`, 필요 시 `META_AUDIT_LOG`)
  - 변경 전/후 스냅샷
  - `MANIFEST.sha256` 및 체인 엔트리

요건:
- model_id/model_family/provider/verdict/rationale 포함
- 최소 2개 model family 합의
- `context_for_next` 기록

## 역할 정합성 (Workflow 반영)

- 분해 체크리스트/업무 티켓은 Deliberation Chamber가 보유·관리하며,
  실행/변경 작업의 증빙만 record_archive가 최종 수용한다.
- 기록된 실행 결과/증빙은 실행 단계 종료 직후 `ARCHIVE_INDEX`와 `HASH_LEDGER`에 반영되어야 한다.
- record_archive에서 정합성/패턴 이슈를 진단한 경우,
  다음 주기 개선 제안은 Deliberation Chamber를 통해 제기해야 한다.

## 패키지 운영

최소 항목:
- `PACKAGE.md`(source_refs + audit_refs)
- `MANIFEST.sha256`
- `payload/` 증빙

## 무결성 및 인덱스

- `indexes/HASH_LEDGER.md`는 prev_hash/hash 체인
- `indexes/ARCHIVE_INDEX.md`는 인덱스 항목 추가
- `indexes/README.md`는 참조 경로 및 예외 정책 정리

## 예외/분쟁 처리

- 증빙 작성 중 분쟁 감지 시 작업 중단
- `disputed/` 버킷 격리 후 Immune 심판 요청
- 승인 시 정상 버킷 이동, 거부 시 폐기 또는 수정반영

## Version Note

- v0.2.4: 플래그십 합의 조건 강화
- v0.2.5: 상위 변경의 다중 모델 증빙 의무화
- v0.2.6: 상위 변경 게이트 및 context_for_next 표기 강화
