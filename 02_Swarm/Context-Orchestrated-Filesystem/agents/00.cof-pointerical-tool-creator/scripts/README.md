# Scripts

본 Agent는 스크립트를 **직접 실행하지 않는다**.

## Design Principle

COF Agent 모델에서 Agent는 **선언적(declarative) 실행 주체**이다.
스크립트 실행은 COF Runtime 또는 외부 실행기에 위임한다.

## Script References

상위 Skill의 스크립트를 참조용으로 사용한다:

| 스크립트 | 경로 | 용도 |
|---------|------|------|
| create_pointerical_doc.py | `../../skills/00.cof-pointerical-tool-creator/scripts/create_pointerical_doc.py` | 문서 생성 CLI |

## Agent의 스크립트 사용 방식

1. **참조 전용**: 스크립트 경로를 산출물에 포함
2. **위임**: 실제 실행은 상위 시스템(Runtime)에 요청
3. **결과 수신**: 실행 결과만 수신하여 처리

## Agent-Specific Scripts

Agent 고유의 스크립트가 필요한 경우:

1. 이 디렉토리에 스크립트 추가
2. AGENT.md의 References 섹션에 등록
3. 실행은 반드시 외부 Runtime에 위임
