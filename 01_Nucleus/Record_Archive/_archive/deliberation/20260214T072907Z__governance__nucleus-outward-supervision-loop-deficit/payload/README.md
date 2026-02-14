---
type: plan-index
workflow_id: ISSUE-NUC-20260214-0002
status: in_progress
created: "2026-02-14"
---

# Nucleus 외향적 감독/개선 루프 결손 복구

`supervision-check / supervision-cycle`를 단발성 점검이 아니라 `Deliberation Stage-5` 산출물과 연계되는 주기 운영 루프로 정착시키기 위한 보강 계획입니다.

## 포함 산출물

- `PROBLEM_STATEMENT.md`
- `WORKFLOW_MANIFEST`
- `SUPERVISION_SCOPE.md`
- `DELIBERATION_PACKET.md`
- `CRITIQUE*` (`CRITIQUE.md`, `CRITIQUE-CLAUDE.md`)
- `IMMUNE-CRITIQUE.md`
- `SYNTHESIS.md`
- `DECOMPOSITION_TODO.md`
- `EVIDENCE.md`
- `SEAL_TO_ARCHIVE.md`
- `01_Nucleus/deliberation_chamber/tasks/2026-02-14__nucleus-outward-supervision-loop-deficit.md`

## 진행 단계

| Stage | 상태 | 비고 |
|-------|------|------|
| 1. 문제제기 | done | `PROBLEM_STATEMENT.md` |
| 2. record_archive 기록 | done | `WORKFLOW_MANIFEST` |
| 3. Deliberation 계획 | done | `DELIBERATION_PACKET.md` |
| 4. Immune 비판 | done | `CRITIQUE*`, `IMMUNE-CRITIQUE.md` |
| 5. Deliberation 개선 | done | `DECOMPOSITION_TODO.md`, `SYNTHESIS.md`, `EVIDENCE.md` |
| 6. 실행/봉인 | pending | `SEAL_TO_ARCHIVE.md` 실행 전 |
| 6-b. 계획 정리 | pending | Stage-6 종료 후 `plan_manager.py close` |

## 작업 메모

- 주기: 주간 외향 감시 루프 정착
- 핵심 산출물 1차 연결: `IMPROVEMENT_QUEUE.md -> DECOMPOSITION_TODO.md`
- Stage-5 입력 고정: `IMPROVEMENT_QUEUE.md`의 `required/recommended` 항목
