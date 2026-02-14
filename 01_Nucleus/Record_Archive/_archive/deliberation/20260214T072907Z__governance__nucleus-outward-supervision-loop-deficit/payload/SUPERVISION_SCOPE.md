---
type: supervision-scope
workflow_id: ISSUE-NUC-20260214-0002
owner: Deliberation Chamber
frequency: weekly
handoff_stage: Deliberation Stage-5
created: "2026-02-14"
---

# Outward Supervision Scope (정식 Scope 선언)

## 운영 메타

- 주기: 주간 정기 실행
- 담당 구간: Deliberation Stage-5 (개선안 반영)
- 운영 진입점: `IMPROVEMENT_QUEUE.md` / `LOWER_LAYER_SUPERVISION.json`
- 상태: active

## Scope 대상 (고정)

### 02_Swarm

- `context-orchestrated-filesystem`
- `context-orchestrated-ontology`
- `cortex-agora`

### 03_Manifestation

- `summon-agents`

## 공통 감독 체크리스트 (모든 타깃 모듈)

- `README.md` 존재
- `DNA.md` 존재
- README/DNA 상호 참조 정합성
- 경계 항목: 실행 바인딩 또는 외부 연동 지점이 문서화되어 있는가
- 자원/제한 항목: 동시성·배치·쿼터·운영 임계치가 문서에 기록되어 있는가
- 관측 항목: 행동 관측성(behavior/feed) 또는 동등 증적이 존재하는가
- 상향 제안: 개선안이 Deliberation Stage-5로 역전파 가능한지

## 승인 가이드

- 대상에서 누락이 발생할 경우 `required_issues`에 기록하고, `supervision_stage=needs-improvement`로 판단한다.
- `recommendations`은 권고치로 분류하고 `supervision_stage=needs-improvement`만 허용 여부로 반영하지 않는다.
- Stage-5 시작 시 `DECOMPOSITION_TODO.md`에 다음 항목이 1:1 반영되어야 한다.
  - 모듈명
  - 위반 유형
  - 조치안(요청/제안/임시조치)
  - 근거 경로(`LOWER_LAYER_SUPERVISION.json`/`IMPROVEMENT_QUEUE.md`)

## 모듈별 고정 스키마

| layer | module | 공통 체크 | 상호 연동 |
|---|---|---|---|
| 02_Swarm | context-orchestrated-filesystem | README/DNA, 경계/자원/관측 |  Deliberation Stage-5 TODO로 귀속 |
| 02_Swarm | context-orchestrated-ontology | README/DNA, 경계/자원/관측 |  Deliberation Stage-5 TODO로 귀속 |
| 02_Swarm | cortex-agora | README/DNA, 실행 바인딩/행위 관측 |  Deliberation Stage-5 TODO로 귀속 |
| 03_Manifestation | summon-agents | README/DNA, 행동 관측성, 상향 제안 | Deliberation Stage-5 TODO로 귀속 |
