# COF v0.1.4
**Context-Orchestrated Filesystem**

---

## What is COF?

COF는 단순한 파일 규칙이 아니라, **"AI Agent가 물리적 공간(Filesystem)을 인지하는 철학"**이다.

에이전트가 제한된 Context Window 내에서 효율적으로 작업할 수 있도록, 파일시스템의 구조 자체가 맥락(Context)을 전달하고, 참조(Pointer)를 통해 연결되며, 수명(Lifecycle)을 스스로 관리하는 시스템이다.

---

## Integration Boundary (Agora/COWI)

- COF는 로컬 티켓 운영/실행 맥락 관리를 담당하는 운영 계층이다.
- 관찰/패턴 개선 제안은 `cortex-agora`(관찰)와 `context-orchestrated-workflow-intelligence`(중재) 경유를 따른다.
- `record_archive`는 봉인 대상 SoT이며, COF의 직접 관찰 입력 경로가 아니다.
- Immune reference는 의도적으로 `01_Nucleus/immune_system/rules/cof-environment-set.md`를 사용한다.
  (COF 운영 규칙을 직접 적용하기 위한 분기이며, generic `rules/README.md` 대체가 아니다.)

---

## The Four Pillars

| Pillar | Principle | Action |
|--------|-----------|--------|
| **Context Locality** | 작업이 일어나는 곳에 맥락이 있어야 한다 | 모든 노드는 작업 공간의 Sibling 위치에 배치 |
| **Self-Descriptiveness** | 말하지 않는 노드는 존재하지 않는 것이다 | 모든 핵심 노드에 스킬 기반 규약 참조를 배치 |
| **Agent-First Design** | 에이전트가 읽기 좋아야 한다 | YAML Frontmatter 필수화, 정형화된 네이밍 |
| **Traceable Lifecycle** | 시작과 끝이 없는 데이터는 쓰레기다 | Natural Dissolution 원칙 적용 |

> 상세: [core-docs/COF_DOCTRINE.md](core-docs/COF_DOCTRINE.md)

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
role: RULE | WORKFLOW
state: const | mutable | active | frozen | archived
scope: immune | agora | nucleus | swarm
lifetime: ticket | persistent | archived
---
```

`SKILL.md`는 표준 스킬 frontmatter(`name`, `description`, `allowed-tools`)만 사용하며,
COF 식별 메타는 같은 디렉토리의 `SKILL.meta.yaml`에 저장한다.
우선순위는 `SKILL.md`(실행 인터페이스) → `SKILL.meta.yaml`(COF 식별 SoT)로 분리한다.
또한 active skill은 `SKILL.md`를 **초경량 로더(<=120 lines)** 로 유지하고,
상세 규칙은 `00.meta/10.core/20.modules/30.references/40.orchestrator` 문서로 분리한다.

> 상세: [skills/00.pointerical-tooling/references/cof-environment-set.md](skills/00.pointerical-tooling/references/cof-environment-set.md) § 0. COF Pointer Model Baseline

---

## Directory Structure

```
context-orchestrated-filesystem/
├── README.md                    ← 현재 문서
├── core-docs/COF_DOCTRINE.md              ← 4 Pillars 철학
├── skills/00.pointerical-tooling/references/cof-environment-set.md   ← Skill-based Governance Guide
├── DNA.md                       ← DNA 정의
├── DNA.md                       ← Lifecycle/Resource Limits
│
└── skills/                      ← Skill Genome
    ├── 00.pointerical-tooling/   ← 기초 레이어
    │   ├── SPEC.md              ← 설계 스펙
    │   ├── SKILL.md             ← Quick Reference
    │   ├── references/          ← Normative 해석 문서
    │   └── templates/           ← 문서 타입별 템플릿
    │
    ├── 01.glob-indexing/              ← 인덱싱 스킬
    │   ├── SPEC.md
    │   ├── SKILL.md
    │   └── scripts/
    │
    ├── 02.task-context-management/          ← 작업 관리 스킬
    │   ├── SKILL.md
    │   └── templates/
    │
    └── 03.ticket-solving/    ← 티켓 해결(에이전트 디스패치)
        ├── SPEC.md
        ├── SKILL.md
        └── scripts/
```

---

## Skills

스킬은 **종속성 순서**대로 번호가 부여된다.

| # | Skill | Purpose | Depends On |
|---|-------|---------|------------|
| 00 | `cof-pointerical-tooling` | 포인터 안전한 SKILL/RULE/WORKFLOW/SUB-AGENT 문서 생성 | - |
| 01 | `cof-glob-indexing` | 가장 가까운 `[n].index/` 탐색 및 인덱싱 산출물 생성 | 00 (references) |
| 02 | `cof-task-context-management` | 작업 맥락 생성, 티켓 발행, 아카이브 | 00, 01 |
| 03 | `cof-ticket-solving` | 티켓 → 에이전트 그룹 디스패치 및 결과 통합 | 01, 02 |
| 04 | `cof-skill-governance` | Swarm별 Skill 레지스트리 생성/검증, 과다 Skill 경고 | 00 |

### Skill Usage Mandate

> **"Skill-Mediated Creation Only"**

| Intent | Target Node | Required Skill |
|--------|-------------|----------------|
| 작업 맥락 생성/초기화 | `NN.agents-task-context/` (legacy: `task-manager/`) | `cof-task-context-management` |
| 작업 티켓 발행 | `tickets/` | `cof-task-context-management` |
| 완료 작업 정리 | `archive/` | `cof-task-context-management` |

> **Warning**: `mkdir`나 `touch`로 위 구조를 직접 생성하는 것은 **금지**된다.

---

## Quick Start

### 1. 작업 맥락 생성

```bash
# cof-task-context-management 스킬 사용
python3 skills/02.cof-task-context-management/scripts/create_node.py \
  --path "/target/directory"
```

### 2. 새 Skill/Rule/Workflow 문서 생성

```bash
# cof-pointerical-tooling 스킬 사용
python3 skills/00.pointerical-tooling/scripts/create_pointerical_doc.py \
  --type skill \
  --title "My New Skill" \
  --out "/path/to/SKILL.md" \
  --context-id cof-my-new-skill
```

### 3. 인덱싱

```bash
# cof-glob-indexing 스킬 사용
python3 skills/01.glob-indexing/scripts/cof_glob_indexing.py \
  --target "/path/to/node"
```

### 4. Swarm Skill Registry 갱신

```bash
# cof-skill-governance 스킬 사용
python3 skills/04.cof-skill-governance/scripts/sync_swarms_skill_manager.py \
  --swarm-root "/path/to/04_Agentic_AI_OS/02_Swarm" \
  --max-skills 12
```

---

## Hard Constraints

다음 항목을 위반하는 문서/행위는 **금지**된다:

1. `context_id` 없는 문서 생성 (단, `SKILL.md`는 `SKILL.meta.yaml`로 대체 가능)
2. `history` 컨텍스트를 `active`로 참조
3. 디렉토리 ROLE과 state 불일치
4. 수명 전이가 명시되지 않은 Workflow
5. 숫자 인덱스(`NN`)에 의미 부여

---

## Core Documents

| Document | Role | Description |
|----------|------|-------------|
| [core-docs/COF_DOCTRINE.md](core-docs/COF_DOCTRINE.md) | Doctrine Genome | 4 Pillars 철학 |
| [skills/00.pointerical-tooling/references/cof-environment-set.md](skills/00.pointerical-tooling/references/cof-environment-set.md) | Skill Governance | 실행 지침 (Pointer Model, Skill Mandate) |
| [DNA.md](DNA.md) | DNA Definition | Genome Pointers 정의 |
| [DNA.md](DNA.md) | Lifecycle Genome | Natural Dissolution, Resource Limits |

---

## Inheritance

```
AAOS Canon (04_Agentic_AI_OS/README.md)
    ↓
META Doctrine (DNA.md)
    ↓
Immune System (01_Nucleus/immune_system/)
    ↓
COF v0.1.4 (현재)
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.1.4 | 2026-02-14 | Agora/COWI 연계 경계 및 direct record_archive 관찰 입력 금지 명문화 |
| v0.1.3 | 2026-01-22 | Pointer Model 도입, 스킬 구조 재편 (`[n].[role]/`), SPEC 강화 |
| v0.1.2 | - | 초기 버전, 4 Pillars 정의 |

---

> *"Context-Orchestrated Filesystem: Where structure speaks, and agents listen."*
