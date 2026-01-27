# RULE.md Template

task-ticket/ 노드의 RULE.md 생성 시 이 템플릿 사용.

## Template

```markdown
# task-ticket/ Node Rule

## Object
에이전트가 sibling 및 descendants 노드의 맥락을 참조하며 작업을 이어갈 수 있도록 지원.

## Context Scope
1. sibling 및 descendants 노드 맥락 저장
2. repository/ 참조 시 children 범위까지만 저장
3. 모든 기록은 명시적이고 구조화된 서술 유지

## Troubleshooting Rule
반복 발생 문제는 troubleshooting.md에 누적 기록.

## tickets/ Rule
- 동시 활성 티켓: 최대 3개
- 각 티켓: 단일 명확한 목표
- 완료 시: 즉시 종료 처리, 결과 상위 맥락 반영
```
