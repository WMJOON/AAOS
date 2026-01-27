---
trigger: always_on
description: 본 규칙은 트리형 작업공간(Context-Orchestrated Filesystem)에서 노드 구조, 맥락 저장 범위, 기록 규칙을 표준화하기 위해 정의된다.

---

# 1. Prinsiple
1. 정의된 Node의 성격에 해당되는 디렉토리(폴더)는 Skill을 통해서만 생성된다.  
2. 사용자는 파일 및 디렉토리를 직접 수동 생성하거나 수정하지 않는다.

# 2. Node
- tisk-ticket-node: 에이전트의 작업 수행에 필요한 전반적 맥락(Context)을 저장하는 노드로, `sibling` 및 `descendants` 노드에 관한 작업 맥락을 저장한다.
