# Swarm Skill Registry Index

> 4-Layer Mental Model Orchestrator Architecture를 AAOS 전체 Swarm에 일반화한 토큰 효율성 거버넌스 인덱스.

- Generated at: `2026-02-15T04:20:42+00:00`
- Scanned swarms: `4`
- Source architecture: `agentic-workflow-topology/reference/Four_Layer_Mental_Model_Orchestrator_Architecture.md`

---

## 1. Generalized Principles

원문은 멘탈모델(PM/VC/Marketer 등) 도메인에 특화되어 있다.
아래는 도메인 특수성을 제거하고 **모든 Swarm Skill에 적용 가능한 보편 원리**로 추출한 것이다.

### 1.1 4-Layer 구조

모든 Skill은 토큰 비용 최적화를 위해 4개 레이어로 분리한다.

| Layer | 역할 | 로딩 조건 | Token Budget |
|---|---|---|---|
| **L3** Orchestrator | 목적 감지 + 모듈 라우팅 | 항상 (SKILL.md loader) | ≤ 350 tok (120줄) |
| **L0** Core | 공유 공리, 통일 어휘, 출력 형식 | 항상 | ~150 tok |
| **L1** Modules | 도메인별 고유 질문 축 (시그널) | 선택적 — Orchestrator가 결정 | ~350 tok/개 |
| **L2** References | 상세 체크리스트, 팩 | 온디맨드 — `ΔQ/L₂ > ΔQ/L₁`일 때만 | ~800 tok/개 |

**핵심**: L3+L0은 항상 로딩(~500 tok), L1+L2는 조건부 로딩. 이 분리가 풀로딩 대비 60–80% 토큰 절감의 근거다.

### 1.2 비용 공식

```
단일 Step:  Cᵢ = Ω + L₀ + Dᵢ·L₁ + mᵢ·L₂ + P + O
N Step 총:  T   = Σᵢ₌₁ᴺ [Ω + L₀ + Dᵢ·L₁ + mᵢ·L₂ + P + (i-1)(O+δ)]
```

| 변수 | 의미 |
|---|---|
| Ω | Orchestrator (~200 tok) |
| L₀ | Core (~150 tok) |
| Dᵢ | 활성 도메인(모듈) 수 |
| mᵢ | 로딩되는 Reference 수 |
| P, O | 프롬프트, 출력 |
| δ | 누적 출력 오버헤드 |

### 1.3 직교성 원칙

모듈 간 어휘·질문 축이 중첩되면 간섭 계수 α가 하락하여 품질이 감소한다.

```
효용 함수:  U = α · (Q₁ · Q₂) / T
```

| α 범위 | 의미 | 처방 |
|---|---|---|
| ≥ 0.85 | 직교 — 각 모듈이 고유 축 보유 | 정상 운영 |
| 0.5–0.84 | 간섭 — 어휘/질문 중첩 존재 | Core 리팩터링 필요 |
| < 0.5 | 충돌 — 모듈 병합 또는 재설계 | 구조 변경 필수 |

### 1.4 L2 로딩 Gate

Reference는 항상 로딩하지 않는다. 로딩 조건:

```
ΔQ/L₂ > ΔQ/L₁   (Reference의 품질 한계기여 > Module의 품질 한계기여)
```

실무 기준: **구체적 수치 검증**(체크리스트, 분류표, 스키마 등)이 필요한 경우에만 L2 로딩.

---

## 2. Swarm Health Dashboard

| Swarm | Skills | 4Layer | Overloaded | Warnings | Errors |
|---|---:|---:|---:|---:|---:|
| agentic-workflow-topology | 5 | 5/5 | N | 0 | 0 |
| context-orchestrated-filesystem | 5 | 5/5 | N | 0 | 0 |
| context-orchestrated-workflow-intelligence | 1 | 1/1 | N | 0 | 0 |
| cortex-agora | 2 | 1/2 | N | 0 | 0 |

### Column Definitions

- **4Layer**: `compliant / total` — 필수 레이어 디렉토리(`00.meta`, `10.core`, `20.modules`, `30.references`, `40.orchestrator`, `90.tests`) 보유 여부
- **Overloaded**: Skill 수 > Overload threshold 시 `Y`
- **Warnings**: 4Layer 레이어 부분 누락, SKILL.md 120줄 초과 등 (Phase A: warning)
- **Errors**: context_id 중복, frontmatter 필수 필드 누락 등 (Phase B: error 승격 예정)

---

## 3. Governance Thresholds

| 규칙 | 값 | 근거 |
|---|---|---|
| Swarm당 Skill 상한 | 12 | N ≥ 12에서 Orchestrator 라우팅 정확도 < 90% (비용 모델 § 6 참고) |
| SKILL.md 최대 줄 수 | 120줄 | Loader 토큰 ≤ 350 tok 유지 — L3 예산 초과 방지 |
| 직교성 계수 α 하한 | ≥ 0.85 | α < 0.85 시 효용 U가 비선형 하락 (품질 모델 § 3 참고) |
| L2 Reference 동시 로딩 상한 | 2개 | mᵢ ≤ 2에서 비용-품질 최적 (비용 공식 § 1.2) |

### Enforcement Policy

| Phase | 범위 | 정책 |
|---|---|---|
| **A** (current) | 4Layer 레이어 누락, 로더 초과 | Warning |
| **B** (next release) | 동일 위반 | Error 승격 |

---

## 4. Per-Swarm Skill Index

### 4.1 agentic-workflow-topology (AWT)

| # | Skill | Context ID | Layers | Scripts | Refs |
|---|---|---|---|---|---|
| 00 | mental-model-design | `awt-mental-model-design` | full | Y | Y |
| 01 | topology-design | `awt-topology-design` | full | Y | Y |
| 02 | execution-design | `awt-execution-design` | full | N | Y |
| 03 | observability-evolution | `awt-observability-evolution` | full | Y | Y |
| 04 | skill-governance | `awt-skill-governance` | full | N | Y |

### 4.2 context-orchestrated-filesystem (COF)

| # | Skill | Context ID | Layers | Scripts | Refs |
|---|---|---|---|---|---|
| 00 | pointerical-tooling | `cof-pointerical-tooling` | full | Y | Y |
| 01 | glob-indexing | `cof-glob-indexing` | full | Y | N |
| 02 | task-context-management | `cof-task-context-management` | full | Y | N |
| 03 | ticket-solving | `cof-ticket-solving` | full | Y | N |
| 04 | skill-governance | `cof-skill-governance` | full | Y | N |

### 4.3 context-orchestrated-workflow-intelligence (COWI)

| # | Skill | Context ID | Layers | Scripts | Refs |
|---|---|---|---|---|---|
| 00 | agora-consumption-bridge | `cowi-agora-consumption-bridge` | full | Y | N |

### 4.4 cortex-agora

| # | Skill | Context ID | Layers | Scripts | Refs |
|---|---|---|---|---|---|
| — | structuring-cortex-agora-proposals | `cortex-agora-instruction-nucleus` | legacy | N | N |
| 04 | skill-governance | `cortex-agora-skill-governance` | full | N | Y |

> **Note**: instruction-nucleus는 4-Layer 마이그레이션 미완료 (legacy flat structure).

---

## 5. Companion Documents

| Document | Location | Purpose |
|---|---|---|
| 4-Layer Architecture | `agentic-workflow-topology/reference/Four_Layer_Mental_Model_Orchestrator_Architecture.md` | 원문 — 비용/품질 모델 전체 유도 |
| 4-Layer Contract | `02_Swarm/cortex-agora/registry/SKILL_4LAYER_CONTRACT.md` | 필수 구조 정의 + 검증 체크리스트 |
| Global Registry (JSON) | `02_Swarm/cortex-agora/registry/GLOBAL_SKILL_REGISTRY.json` | 머신리더블 전체 스킬 인벤토리 |
| Skill Rename Map | `02_Swarm/cortex-agora/registry/SKILL_RENAME_MAP.md` | NN.role-slug 마이그레이션 이력 |
| Swarm-level Registries | `{swarm}/registry/SKILL_REGISTRY.md` | Swarm별 상세 스킬 테이블 |
