# COF v0.1.3
**Context-Orchestrated Filesystem**

---

## What is COF?

COF는 단순한 파일 규칙이 아니라, **"AI Agent가 물리적 공간(Filesystem)을 인지하는 철학"**이다.

에이전트가 제한된 Context Window 내에서 효율적으로 작업할 수 있도록, 파일시스템의 구조 자체가 맥락(Context)을 전달하고, 참조(Pointer)를 통해 연결되며, 수명(Lifecycle)을 스스로 관리하는 시스템이다.

---

## The Four Pillars

| Pillar | Principle | Action |
|--------|-----------|--------|
| **Context Locality** | 작업이 일어나는 곳에 맥락이 있어야 한다 | 모든 노드는 작업 공간의 Sibling 위치에 배치 |
| **Self-Descriptiveness** | 말하지 않는 노드는 존재하지 않는 것이다 | 모든 핵심 노드에 `rules/cof-environment-set.md` 배치 |
| **Agent-First Design** | 에이전트가 읽기 좋아야 한다 | YAML Frontmatter 필수화, 정형화된 네이밍 |
| **Traceable Lifecycle** | 시작과 끝이 없는 데이터는 쓰레기다 | Natural Dissolution 원칙 적용 |

> 상세: [COF_DOCTRINE.md](COF_DOCTRINE.md)

---

## Pointer Model

COF의 핵심은 **포인터 모델**이다. 모든 문서는 Context Pointer로 취급되며, 디렉토리는 포인터 타입을 정의한다.

### Directory Naming Convention

```
[NN].[ROLE]/
```

- `NN`: 사람을 위한 시각적 인덱스 (ordering only, **의미 없음**)
- `ROLE`: 시스템이 해석하는 포인터 타입

### Standard Directory Set

| Directory | Pointer Semantics | Description |
|-----------|-------------------|-------------|
| `00.index/` | Context Pointer Table | 노드의 인덱스/메타 정보 |
| `01.reference/` | const pointer | 불변 참조 문서 |
| `02.working/` | mutable pointer | 작업 중인 문서 |
| `03.ticket/` | stack pointer | 작업 티켓 |
| `04.runtime/` | execution context | 실행 컨텍스트 |
| `99.history/` | freed/archived pointer | 아카이브된 문서 |

### Context Identity

모든 문서는 YAML Frontmatter에 포함:

```yaml
---
context_id: cof-xxxx          # 전역 유일, 불변
role: SKILL | RULE | WORKFLOW
state: const | mutable | active | frozen | archived
scope: immune | agora | nucleus | swarm
lifetime: ticket | persistent | archived
---
```

> 상세: [rules/cof-environment-set.md](rules/cof-environment-set.md) § 0. COF Pointer Model Baseline

---

## Directory Structure

```
Context-Orchestrated-Filesystem/
├── README.md                    ← 현재 문서
├── COF_DOCTRINE.md              ← 4 Pillars 철학
├── rules/cof-environment-set.md                      ← Rule Genome (실행 지침)
├── DNA.md                       ← DNA 정의
├── DNA_BLUEPRINT.md             ← Lifecycle/Resource Limits
│
└── skills/                      ← Skill Genome
    ├── 00.cof-pointerical-tool-creator/   ← 기초 레이어
    │   ├── SPEC.md              ← 설계 스펙
    │   ├── SKILL.md             ← Quick Reference
    │   ├── references/          ← Normative 해석 문서
    │   └── templates/           ← 문서 타입별 템플릿
    │
    ├── 01.cof-glob-indexing/              ← 인덱싱 스킬
    │   ├── SPEC.md
    │   ├── SKILL.md
    │   └── scripts/
    │
    ├── 02.cof-task-manager-node/          ← 작업 관리 스킬
    │   ├── SKILL.md
    │   └── templates/
    │
    └── 03.cof-task-solver-agent-group/    ← 티켓 해결(에이전트 디스패치)
        ├── SPEC.md
        ├── SKILL.md
        └── scripts/
```

---

## Skills

스킬은 **종속성 순서**대로 번호가 부여된다.

| # | Skill | Purpose | Depends On |
|---|-------|---------|------------|
| 00 | `cof-pointerical-tool-creator` | 포인터 안전한 SKILL/RULE/WORKFLOW/SUB-AGENT 문서 생성 | - |
| 01 | `cof-glob-indexing` | 가장 가까운 `[n].index/` 탐색 및 인덱싱 산출물 생성 | 00 (references) |
| 02 | `cof-task-manager-node` | 작업 맥락 생성, 티켓 발행, 아카이브 | 00, 01 |
| 03 | `solving-tickets` | 티켓 → 에이전트 그룹 디스패치 및 결과 통합 | 01, 02 |

### Skill Usage Mandate

> **"Skill-Mediated Creation Only"**

| Intent | Target Node | Required Skill |
|--------|-------------|----------------|
| 작업 맥락 생성/초기화 | `NN.agents-task-context/` (legacy: `task-manager/`) | `cof-task-manager-node` |
| 작업 티켓 발행 | `tickets/` | `cof-task-manager-node` |
| 완료 작업 정리 | `archive/` | `cof-task-manager-node` |

> **Warning**: `mkdir`나 `touch`로 위 구조를 직접 생성하는 것은 **금지**된다.

---

## Quick Start

### 1. 작업 맥락 생성

```bash
# cof-task-manager-node 스킬 사용
python3 skills/02.cof-task-manager-node/scripts/create_node.py \
  --path "/target/directory"
```

### 2. 새 Skill/Rule/Workflow 문서 생성

```bash
# cof-pointerical-tool-creator 스킬 사용
python3 skills/00.cof-pointerical-tool-creator/scripts/create_pointerical_doc.py \
  --type skill \
  --title "My New Skill" \
  --out "/path/to/SKILL.md" \
  --context-id cof-my-new-skill
```

### 3. 인덱싱

```bash
# cof-glob-indexing 스킬 사용
python3 skills/01.cof-glob-indexing/scripts/cof_glob_indexing.py \
  --target "/path/to/node"
```

---

## Hard Constraints

다음 항목을 위반하는 문서/행위는 **금지**된다:

1. `context_id` 없는 문서 생성
2. `history` 컨텍스트를 `active`로 참조
3. 디렉토리 ROLE과 state 불일치
4. 수명 전이가 명시되지 않은 Workflow
5. 숫자 인덱스(`NN`)에 의미 부여

---

## Core Documents

| Document | Role | Description |
|----------|------|-------------|
| [COF_DOCTRINE.md](COF_DOCTRINE.md) | Doctrine Genome | 4 Pillars 철학 |
| [rules/cof-environment-set.md](rules/cof-environment-set.md) | Rule Genome | 실행 지침 (Pointer Model, Skill Mandate) |
| [DNA.md](DNA.md) | DNA Definition | Genome Pointers 정의 |
| [DNA_BLUEPRINT.md](DNA_BLUEPRINT.md) | Lifecycle Genome | Natural Dissolution, Resource Limits |

---

## Inheritance

```
AAOS Canon (04_Agentic_AI_OS/README.md)
    ↓
META Doctrine (METADoctrine.md)
    ↓
Immune System (01_Nucleus/Immune_system/)
    ↓
COF v0.1.3 (현재)
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.1.3 | 2026-01-22 | Pointer Model 도입, 스킬 구조 재편 (`[n].[role]/`), SPEC 강화 |
| v0.1.2 | - | 초기 버전, 4 Pillars 정의 |

---

> *"Context-Orchestrated Filesystem: Where structure speaks, and agents listen."*
