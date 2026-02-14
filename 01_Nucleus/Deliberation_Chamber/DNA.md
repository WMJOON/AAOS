---
name: aaos-deliberation-chamber-dna
scope: "04_Agentic_AI_OS/01_Nucleus/deliberation_chamber"
status: canonical
version: "0.1.3"
updated: "2026-02-14"
---

# AAOS Deliberation Chamber (DNA)

## Supremacy Clause

Deliberation Chamber는 판결/집행권이 없고, Canon > META > Immune/DNA 위계 하에서 합의 산출물을 구조화한다.
권한 경계가 불명확하면 즉시 작업을 중단하고 META/Immune로 귀속한다.

## 운영 범위

- 상위기관 변경(Meta / 기관 DNA / Swarm 루트 DNA)에 대한 합의 구조화
- 리스크·대안·판단 질문을 DQ로 분해하여 증빙 패키지화
- Immune 판정용 근거 패키지(`DELIBERATION_PACKET.md`) 작성
- Record Archive 이관 규격화
- 분해 체크리스트/티켓은 Deliberation Chamber가 보유·관리하며, 실행 단계 전 최종 검토한다.
- `plans`/`tasks` 산출물은 작업용 임시본으로 취급되며, 최종 영구 증적은 `01_Nucleus/record_archive/_archive/`로만 이전한다.

## Hard Rules

1. **비권한 원칙**: 집행·차단·최종 승인은 Immune System(Inquisitor) 소유
2. **증빙 보존성**: 산출물은 `record_archive` 패키지 규격으로 작성
3. **합의의 정합성**: 모델 메타데이터(`model_id`, `model_family`, `provider`) 포함
4. **귀속 규칙**: 충돌·불명확은 즉시 상위기관 귀속
5. **종료 선언**: `context_for_next`와 `termination conditions`를 명시
6. **개선 제안 채널**: record_archive 패턴 분석은 Deliberation 개선안으로만 제시한다.
7. **보존 중앙화**: 정식 증적은 `01_Nucleus/record_archive/`의 `_archive`로만 유지한다.

## 산출물 체인

```text
Deliberation Packet
  -> Immune Judgment (AUDIT_LOG)
  -> Record Archive Package (MANIFEST + Hash chain)
```

## 필수 산출물 스키마

- `DELIBERATION_PACKET.md`
- `EVIDENCE.md`
- `VERDICT` 요약
- 참가자 메타데이터(모델/가족/기관/근거)
- 분쟁 이력 및 이행 조건

## 상위 변경 게이트 반영

- 기관/Swarm 상위 변경은 최종적으로 `Record Archive` 패키지로 봉인되어야 하며,
  해당 패키지에는 Immune 판정/승인 참조가 포함되어야 한다.
- `plans`/`tasks` 산출물 자체는 영구 보존본이 아니라 record_archive로의 전이 대상이다.
- 합의는 `Approve | Reject | Request-Changes` 중 하나의 명시된 결론으로 종료되어야 한다.

## Version Note

- v0.1.1: 위계 구조 정합성 조정
- v0.1.2: 합의 메타데이터/귀속 규칙/종료 조건 표시 강화
