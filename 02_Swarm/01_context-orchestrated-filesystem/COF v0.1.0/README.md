---
name: context-orchestrated-filesystem
description: 이 스킬은 "Universal Project" 구조에 대한 포괄적인 가이드이자 표준입니다. Context/Product/Communication 레이어를 정의하며, 각 하위 폴더별 규칙을 포함합니다.
---
# COF(Context Orchestrated Filesystem) v0.1 개요

본 시스템은 트리 구조의 작업공간(File-based Workspace)을 기반으로, 각 노드에 맥락(Context), 규칙(Rule), 목적(Object)을 저장·연결하여 작업 간 연속성과 참조 가능성을 유지하는 맥락 관리 시스템이다. 이를 통해 에이전트와 사용자가 동일한 작업 트리 내에서 맥락을 공유하며 협업할 수 있도록 설계된다.

---
### Rule
- Rule File: cof-rule.md
- 역할: Context-Orchestrated Filesystem 전반의 노드 구조, 참조 범위, 기록 규칙을 정의한다.
- Version 1에서는 단일 Rule 파일만 사용한다.
- Rule 위치(Global / Project)는 사용자가 선택한다.
- Skill 실행 시 Rule을 로딩하여 구조를 생성한다.
### Skill
- Skill Name: cof-task-ticket-node
- 역할: Rule을 참조하여 task-ticket 노드를 표준 구조로 생성·초기화한다.
- Skill은 파일 시스템을 직접 조작하는 유일한 생성 메커니즘이다.


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
- tisk-ticket-node: 에이전트의 작업 수행에 필요한 전반적 맥락(Context)을 저장하는 노드로, `sibling` 및 `descendants` 노드에 관한 작업 맥락을 저장한다.

```


---
# 2. COF Nodes SKILL

## 2.1. task-ticket-node

```json
{
  "task-ticket/": {
    "description": "에이전트의 작업 수행에 필요한 전반적 맥락(Context)을 저장하는 노드",
    "object": "에이전트가 관련 노드의 맥락을 지속적으로 참조하며 작업을 이어갈 수 있도록 지원하기 위함",
    "rule": [
      "`sibling` 및 `descendants` 노드에 관한 작업 맥락을 저장한다.",
      "참조 대상 노드가 `repository/`인 경우, 해당 `repository/`의 `children` 범위까지만 맥락을 저장한다.",
      "반복적으로 발생하는 문제와 해결 방안은 `troubleshooting.md`에 누적 기록한다.",
      "모든 맥락 기록은 후속 에이전트가 재사용 가능하도록 명시적이고 구조화된 서술을 유지한다."
    ],
    "files": [
      "RULE.md",
      "troubleshooting.md"
    ],
    "children": {
      "tickets/": {
        "description": "작업 에이전트가 현재 수행해야 할 업무 티켓을 관리하는 공간",
        "rule": [
          "동시에 활성화된 티켓은 최대 3개를 초과하지 않는다.",
          "각 티켓은 단일 명확한 작업 목표를 가져야 한다.",
          "완료된 티켓은 즉시 종료 처리하고, 필요 시 결과를 상위 노드 맥락에 반영한다."
        ],
        "files": [
          "{ticketName}.md"
        ]
      },
      "issue_notes/": {
        "description": "작업 수행 중 발견된 이슈, 의사결정, 논의 사항을 기록하는 노드",
        "required": false,
        "rule": [
          "이슈는 발생 시점 기준으로 즉시 기록한다.",
          "해결된 이슈는 해결 방법과 영향 범위를 명시한다.",
          "동일 유형 이슈가 반복될 경우 상위 `troubleshooting.md`로 승격한다."
        ],
        "files": [
          "RULE.md",
          "{parentName}-issue_note-{timestamp}.md"
        ]
      },
      "release_notes/": {
        "description": "티켓 단위 또는 작업 단위 완료 결과를 요약 기록하는 노드",
        "required": false,
        "rule": [
          "주요 변경 사항과 산출물을 간결히 정리한다.",
          "후속 작업 또는 의존 티켓에 영향을 주는 사항은 반드시 명시한다."
        ],
        "files": [
          "RULE.md",
          "{parentName}-release_note-{timestamp}.md"
        ]
      }
    }
  }
}
```

