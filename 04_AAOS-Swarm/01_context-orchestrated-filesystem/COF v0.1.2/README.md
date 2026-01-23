---
name: context-orchestrated-filesystem
description: 이 스킬은 "Universal Project" 구조에 대한 포괄적인 가이드이자 표준입니다. Context/Product/Communication 레이어를 정의하며, 각 하위 폴더별 규칙을 포함합니다.
---
# COF(Context Orchestrated Filesystem) v0.1.2 개요

본 시스템은 트리 구조의 작업공간(File-based Workspace)을 기반으로, 각 노드에 맥락(Context), 규칙(Rule), 목적(Object)을 저장·연결하여 작업 간 연속성과 참조 가능성을 유지하는 맥락 관리 시스템이다.

v0.1.2 Update:
- **Renamed to Task-Manager Node**: `cof-task-ticket-node`가 `cof-task-manager-node`로 변경됨.
- **Ticket Dependencies**: 티켓 간 의존성(dependencies) 명시 및 순차적 작업 흐름 지원.
- **Structured Metadata**: YAML Frontmatter를 통해 Status, Priority 등 메타데이터 표준화.

---
### Rule
- Rule File: cof-rule.md
- 역할: Context-Orchestrated Filesystem 전반의 노드 구조, 참조 범위, 기록 규칙을 정의한다.
- Rule 위치(Global / Project)는 사용자가 선택한다.
- Skill 실행 시 Rule을 로딩하여 구조를 생성한다.
### Skill
- Skill Name: cof-task-manager-node
- 역할: Rule을 참조하여 task-manager 노드를 표준 구조로 생성·초기화하며, 표준화된 티켓을 발행한다.

---
# 1. COF RULE

#### context-orchestrated-filesystem.md

```markdown
---
trigger: always_on
description: 본 규칙은 트리형 작업공간(Context-Orchestrated Filesystem)에서 노드 구조, 맥락 저장 범위, 기록 규칙을 표준화하기 위해 정의된다.

---

# Prinsiple
1. 정의된 Node의 성격에 해당되는 디렉토리(폴더)는 Skill을 통해서만 생성된다.  
2. 사용자는 파일 및 디렉토리를 직접 수동 생성하거나 수정하지 않는다.

# Node
- task-manager-node: 에이전트의 작업 수행에 필요한 전반적 맥락(Context)을 저장하는 노드로, `sibling` 및 `descendants` 노드에 관한 작업 맥락을 저장한다.
```


---
# 2. COF Nodes SKILL

## 2.1. task-manager-node

```json
{
  "task-manager/": {
    "description": "에이전트의 작업 수행에 필요한 전반적 맥락(Context)을 저장하는 노드",
    "children": {
      "tickets/": {
        "description": "작업 수행을 위한 개별 티켓 관리",
        "rule": [
          "YAML Frontmatter를 사용하여 status, priority, dependencies를 명시한다.",
          "dependencies에 명시된 티켓이 완료되어야 해당 티켓을 진행할 수 있다."
        ],
        "files": [
          "{ticketName}.md"
        ]
      },
      "issue_notes/": {
        "description": "이슈, 의사결정, 논의 사항 기록",
        "required": false
      },
      "release_notes/": {
        "description": "완료 결과 요약",
        "required": false
      }
    }
  }
}
```
