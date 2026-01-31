# References

본 Agent는 상위 Skill의 references를 **상속**받아 사용한다.

## Inherited References

상위 Skill `cof-pointerical-tool-creator`의 references를 참조한다.

| 문서 | 설명 |
|------|------|
| `skill-normative-interpretation.md` | Skill 작성 규범 |
| `rule-normative-interpretation.md` | Rule 작성 규범 |
| `workflow-normative-interpretation.md` | Workflow 작성 규범 |
| `subagent-normative-interpretation.md` | Sub-Agent 작성 규범 |
| `glob-patterns.md` | Glob 패턴 문법 |

> 실제 파일 경로는 사용자 설정에 따라 다를 수 있다.
> COF Runtime이 `cof-pointerical-tool-creator` 스킬의 위치를 resolve한다.

## Agent-Specific References

| 문서 | 설명 |
|------|------|
| [agent-normative-interpretation.md](agent-normative-interpretation.md) | Agent 작성 규범 (본 Agent 고유) |
| [skill-authoring-best-practices.md](skill-authoring-best-practices.md) | Skill 작성 모범 사례 (Anthropic + COF 통합) |

## Design Decision

references를 복사하지 않고 상위 Skill을 참조하는 이유:

1. **Single Source of Truth**: Normative 문서의 유일한 소스 유지
2. **유지보수 용이성**: 한 곳에서 수정하면 모든 곳에 반영
3. **COF 포인터 모델 준수**: 값 복사가 아닌 포인터 참조
4. **경로 독립성**: 스킬 이름으로 참조하여 설치 위치에 무관
