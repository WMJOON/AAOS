# Deliberation Chamber Plans

이 디렉토리는 Deliberation Chamber의 **활성 계획 단위(Plan)**를 보관한다.

## 스캔 규칙

- `plans/` 직하 디렉토리 = 활성 계획 (에이전트 스캔 대상)
- `plans/_closed/` = 봉인 완료 계획 (스캔 대상 제외)

## 운영 규칙

- plans는 상위 변경 이슈의 구조화된 합의안/근거 패키지 계획입니다.
- 승인 완료 후 최종 영구 증적은 `01_Nucleus/record_archive/_archive/`로 이관됩니다.
- 봉인 완료 후 계획 README `status`를 `closed`로 전환하고 `_closed/`로 이동합니다.
- Task 실행 산출물은 `tasks/`에서 관리할 수 있습니다.
