# Templates

본 Agent는 상위 Skill의 templates를 **상속**받아 사용한다.

## Inherited Templates

상위 Skill `cof-pointerical-tool-creator`의 templates를 참조한다.

| 템플릿 | 용도 |
|--------|------|
| `SKILL_TEMPLATE.md` | Skill 문서 생성 |
| `RULE_TEMPLATE.md` | Rule 문서 생성 |
| `WORKFLOW_TEMPLATE.md` | Workflow 문서 생성 |
| `SUB_AGENT_TEMPLATE.md` | Sub-Agent 문서 생성 |

> 실제 파일 경로는 사용자 설정에 따라 다를 수 있다.
> COF Runtime이 `cof-pointerical-tool-creator` 스킬의 위치를 resolve한다.

## Template Resolution Protocol

Renderer Sub-Agent는 문서 생성 시 다음 순서로 템플릿을 검색한다:

1. **Agent 로컬** (`./templates/`) - 오버라이드용
2. **상위 Skill** (`cof-pointerical-tool-creator/templates/`)

## Agent-Specific Templates

Agent 고유의 템플릿이 필요한 경우 이 디렉토리에 추가한다.
동일 이름의 템플릿은 상위 Skill 템플릿을 오버라이드한다.

### Override 예시

```
# 로컬에 SKILL_TEMPLATE.md가 있으면 상위 Skill 템플릿 대신 사용
templates/
└── SKILL_TEMPLATE.md  ← 오버라이드
```
