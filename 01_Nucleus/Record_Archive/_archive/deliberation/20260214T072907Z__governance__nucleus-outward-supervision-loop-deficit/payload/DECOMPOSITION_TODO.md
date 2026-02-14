---
type: decomposition-revision
auto_generated_from: "01_Nucleus/deliberation_chamber/plans/2026-02-14__nucleus-outward-supervision-loop-deficit/PROBLEM_STATEMENT.md"
workflow_id: ISSUE-NUC-20260214-0002
status: in_progress
owner: Deliberation Chamber
created: "2026-02-14T11:00:00+09:00"
---

# Stage-5 Decomposition TODO (IMPROVEMENT_QUEUE 1:1 반영)

## Mapping Rule (엄수 규칙)

- `IMPROVEMENT_QUEUE.md`의 각 `- [ ] item`은 1개 TODO로 직결한다.
- TODO 식별자는 `IMPQ-####` 형식, Source는 `LOWER_LAYER_SUPERVISION.json` / `IMPROVEMENT_QUEUE.md` 본문 라인으로 역추적 가능해야 한다.
- `required` 항목은 Stage-6 진입 허들, `recommended`는 실행 전 optional backlog으로 분리한다.

## TODO List (Required)

1. `IMPQ-0001` — 감독 대상 Scope 정규화
   - source: `01_Nucleus/motor_cortex/scripts/nucleus_ops.py`가 출력한 scope JSON
   - task: `SUPERVISION_SCOPE.md`에 고정 대상 모듈(3+1) 및 체크 규칙 정식 반영
   - owner: Deliberation Chamber
   - status: [x] 계획 작성 완료
   - evidence: `payload/LOWER_LAYER_SUPERVISION.json`, `SUPERVISION_SCOPE.md`

2. `IMPQ-0002` — 감시 결과 JSON 정렬
   - source: `LOWER_LAYER_SUPERVISION.json`
   - task: `supervision_scope`, `supervision_outputs`, `supervision_stage` 메타 필드 추가 및 `required_issues` 정규화
   - owner: Motor Cortex
   - status: [x] 코드 수정 완료
   - evidence: `01_Nucleus/motor_cortex/scripts/nucleus_ops.py`, `payload/LOWER_LAYER_SUPERVISION.json`

3. `IMPQ-0003` — Stage-5 입력 문서 정렬
   - source: `IMPROVEMENT_QUEUE.md`
   - task: `DECOMPOSITION_TODO.md`, `EVIDENCE.md`, `SEAL_TO_ARCHIVE.md`가 1:1 참조 구조로 동기화
   - owner: Deliberation Chamber
   - status: [x] 진행 중
   - evidence: `payload/IMPROVEMENT_QUEUE.md`, 본 문서

4. `IMPQ-0004` — Stage-5 출력 경로 고정
   - source: `LOWER_LAYER_SUPERVISION.json.supervision_outputs`
   - task: `IMPROVEMENT_QUEUE.md`, `SUMMARY.md`, `PACKAGE.md`, `WORKFLOW_AUDIT.json` 경로를 task bundle에 명시
   - owner: Deliberation Chamber
   - status: [x] 계획 반영
   - evidence: `payload/SUMMARY.md`, `payload/PACKAGE.md`, `payload/WORKFLOW_AUDIT.json`

## TODO List (Recommended)

5. `IMPQ-R001` — 블루프린트 탐지 룰 감사 강화
   - source: `LOWER_LAYER_SUPERVISION.json`
   - task: `blueprint_files` 정책 문구를 감시 대상 표준으로 문서화
   - owner: Motor Cortex
   - status: [ ] 대기
   - evidence: `payload/LOWER_LAYER_SUPERVISION.json`

## Exit Criteria

- `IMPROVEMENT_QUEUE.md`의 required 항목 전부가 상기 `TODO`와 매핑되어야 한다.
- 각 TODO `status` 변경 이력과 `evidence` 경로가 Stage-5 이후 패키지 검증 가능한 형태로 유지되어야 한다.
- Stage-6 실행 전 `context_for_next`로 아래 값을 남긴다.
- `supervision_queue_path`: `01_Nucleus/deliberation_chamber/plans/2026-02-14__nucleus-outward-supervision-loop-deficit/DECOMPOSITION_TODO.md`
  - `task_bundle`: `01_Nucleus/deliberation_chamber/tasks/2026-02-14__nucleus-outward-supervision-loop-deficit.md`
