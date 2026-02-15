# Core

## Purpose
- 공통 용어, 출력 형식, 실패 처리 원칙을 정의한다.
- 모듈 문서는 고유 판단 축(delta)만 기술하고 Core를 재정의하지 않는다.

## Output Format
- 판단
- 근거
- 트레이드오프
- 확신도

## Global Invariants
- 증거 없는 단정 금지
- 경로/계약 불일치 시 fail-fast
- 불확실성은 `when_unsure` 규칙으로 명시
