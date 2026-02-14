---
type: task-bundle
workflow_id: ISSUE-NUC-20260214-0001
status: done
owner: agent-hub
created: "2026-02-14T15:50:00+09:00"
---

# Deliberation Task Bundle (Stage-5 Execution Prep)

## Task Ownership

- 담당: Deliberation Chamber
- Stage: 5 (Deliberation Revision)
- Input: `01_Nucleus/deliberation_chamber/plans/_closed/2026-02-14__nucleus-provider-agnostic-workflow-enforcement/ISSUE-NUC-20260214-0001-WORKFLOW_MANIFEST.md`

## TODO Items

1. Manifest 정합성
   - `record_path`가 pending manifest 경로와 일치하도록 정규화
   - `plan_critic`/`decomposition_critic`의 모델 패밀리 분리 증거 보존
2. 증빙 정합성
   - DELIBERATION_PACKET의 증빙 링크를 실제 경로로 정리
3. 운영 문서 정렬
   - WORKFLOW 템플릿 샘플 상태값 상태표기 정합성 반영
4. Stage-6 준비
   - Stage-6에서 사용할 검증 포인트(artifact audit, manifest-audit) 정리
   - 실행 종료 시 `01_Nucleus/record_archive/_archive` 이관 경로 정의

## Exit Criteria

- `DECOMPOSITION_TODO.md`와 `EVIDENCE.md`가 최신 상태로 유지
- 수정 대상 문서에 대해 실행 전 self-check가 완료
- 다음 단계 진입 전 Stage-6 `context_for_next` 가 존재
- Stage-6 봉인 완료: `01_Nucleus/record_archive/_archive/deliberation/2026-02-14T160700Z__governance__nucleus-provider-agnostic-workflow-enforcement/`
