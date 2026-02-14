---
type: "COF-DOCTRINE"
version: "0.1.0"
date: "2026-01-22"
---

# COF Doctrine: The Four Pillars

> **Inheritance Note**: This doctrine inherits and evolves the principles defined in earlier COF versions (≤ v0.1.2). It retains the core definition of "Context-Orchestrated Filesystem" while expanding the philosophical foundation for Agentic AI.

Context-Orchestrated Filesystem (COF)는 단순한 파일 규칙이 아니라, **"AI Agent가 물리적 공간(Filesystem)을 인지하는 철학"**이다. 본 독트린은 COF의 모든 규칙과 스킬이 지향해야 할 4가지 절대적 기둥(Pillars)을 정의한다.

## Canonical Placement (v0.1.3+)

COF는 버전 폴더(`COF vX.Y.Z/`)로 보관하지 않는다. COF의 canonical 문서는 다음 경로에 **직접 위치**한다.

- `04_Agentic_AI_OS/02_Swarm/context-orchestrated-filesystem/`

버전은 폴더명이 아니라 문서의 YAML Frontmatter(`version`) 및 변경 기록(버전 히스토리/아카이브)으로 표현한다.

## 0. Fundamental Principle (Inherited)

> **"Skill-Mediated Creation Only"**

- **원칙**: 정의된 Node(e.g., `task-manager`)는 반드시 승인된 Skill을 통해서만 생성된다. 사용자와 에이전트는 파일/디렉토리를 수동으로 조작해서는 안 된다.
- **Why**: 구조적 정합성과 메타데이터(Rule, Frontmatter) 누락을 방지하기 위함이다. (v0.1.2 Principle #1, #2 계승)

## 1. Context Locality (맥락의 국소성)

> **"작업이 일어나는 곳에 맥락이 있어야 한다."**

- **원칙**: 작업에 필요한 정보(Rule, History, Context)는 에이전트가 작업하는 디렉토리(Node)의 `sibling` 또는 `descendant` 범위 내에 물리적으로 존재해야 한다.
- **Why**: 에이전트는 제한된 Context Window를 가진다. 중앙집중식 문서(Global Wiki)를 뒤지는 것보다, 발밑(Local Node)에 있는 정보가 가장 관련성이 높고 비용 효율적이다.
- **Action**: 모든 `task-manager` 노드는 해당 작업 공간 바로 옆(Sibling)에 위치시킨다.
- **Exception**: `Immune System` 및 `AAOS Canon`과 같이 시스템 전체에 적용되는 상위 공리(Axiom)는 예외적으로 Ancestor 경로 참조를 허용한다.

## 2. Self-Descriptiveness (자기 서술성)

> **"말하지 않는 노드는 존재하지 않는 것이다."**

- **원칙**: 모든 노드(디렉토리/파일)는 자신이 무엇이며, 어떤 규칙을 따르는지 명시적으로 설명해야 한다.
- **Why**: 인간은 암묵적 합의로 폴더를 쓰지만, 에이전트는 명시적 텍스트(`README.md`, `rules/cof-environment-set.md`) 없이는 폴더의 의도를 추론해야 하므로 오류가 발생한다.
- **Action**: 핵심 노드에는 반드시 `rules/cof-environment-set.md`를 배치하여 에이전트에게 "이 공간의 법칙"을 선언한다.

## 3. Agent-First Design (에이전트 우선 설계)

> **"인간이 보기 좋은 것이 아니라, 에이전트가 읽기 좋아야 한다."**

- **원칙**: 파일명, 구조, 내용은 Agent의 파싱(Parsing)과 탐색(Traversal) 효율성을 최우선으로 고려한다.
- **Why**: 긴 문장보다는 구조화된 YAML Frontmatter가, 모호한 이름보다는 `YYYYMMDD` 같은 정형화된 패턴이 에이전트의 실수를 줄인다.
- **Action**: 모든 Ticket과 Note에 YAML Frontmatter를 필수화하고, 명확한 네이밍 규칙(Sanitized Filename)을 강제한다.

## 4. Traceable Lifecycle (추적 가능한 생명주기)

> **"시작과 끝이 없는 데이터는 쓰레기다."**

- **원칙**: 생성된 근거(Creation Context)와 소멸 조건(Dissolution Condition)이 정의되지 않은 정보는 시스템에 남기지 않는다.
- **Why**: 에이전트는 무한정 데이터를 생성하는 경향이 있다. 언제 지워야 할지 모르는 데이터는 시스템을 오염시키고 미래의 에이전트에게 혼란(Hallucination Trigger)을 준다.
- **Action**: `Natural Dissolution` 원칙에 따라 완료된 작업은 아카이빙하고, 불필요한 노드는 스스로 정리할 수 있도록 설계한다.

## 5. Immutable Record Discipline (Audit / Append-Only)

COF는 추적 가능한 생명주기를 위해 **변경 기록을 불변(append-only) 로그로 남긴다**.

- `AUDIT_LOG.md`는 **수정하지 않는다(편집 금지)**.
- 새로운 사실/판정/마이그레이션은 기존 엔트리를 고치지 말고 **새 엔트리를 append**한다.
