---
type: improvement-blueprint
target: 04_Agentic_AI_OS/METADoctrine.md
status: draft
version: v0.1.2
created: 2026-01-27
updated: 2026-01-27
time_bound:
  expires: 2026-02-26
  action_on_expiry: archive-to-record
---

# METADoctrine 개선 Blueprint

> METADoctrine.md v0.1.10 Critic 결과 기반 개선안

## Placement / Evidence Note

- 본 문서는 **Draft(비정통/비집행)** 이며, Canonical 문서에서 **normative reference(규범 참조)** 로 사용될 수 없다. (METADoctrine v0.1.7 Draft/Planning Protocol 준수)
- 본 파일은 기존 `META_AUDIT_LOG.md`/`AUDIT_LOG.md`에서 경로로 참조되고 있어 **루트(`04_Agentic_AI_OS/`)에 유지**한다. (향후 이동 시, 리다이렉트 문서 + 참조 갱신 권장)
- 관련(역사/구현): `04_Agentic_AI_OS/00_Planning/METADoctrine-BLUEPRINT.md`는 v0.1.7 반영을 위한 “구현 완료(implemented)” Blueprint이며, 본 문서는 v0.1.10 이후 개선안을 다루는 별도 Blueprint다.
- “현행 구현/CLI” 언급은 **Repo 근거(파일 경로)** 를 함께 적는다. Change Packet에는 필요 시 해당 파일 스냅샷(또는 라인 레퍼런스)을 포함하는 것을 권장한다.

**Repo evidence anchors (as-is)**
- Inquisitor core: `04_Agentic_AI_OS/01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/`
  - `auto_inquisitor.py` (CLI: `--gen-hook`, `--scan`, `--preflight`)
  - `audit.py` (CLI: `verify`, `stats`)

## 0. Critique Summary (v0.1.10)

### 핵심 문제(요약)

- **참조 무결성**: `AAOS_META_CANON/README.md`, `AAOS_META_DNA/METADoctrine.md`, `AAOS_SWARM/AAOS_COF/` 등 *실제 파일시스템에 존재하지 않는* 레거시 경로가 남아 있어, “정본이 무엇인지”가 흔들림.
- **Swarm 레지스트리 불일치**: COF/COO가 현재 `02_Swarm/` 구조(버전 폴더 포함)와 매칭되지 않음. 특히 COO는 `DNA.md`가 아직 없는데 METADoctrine에는 존재하는 것으로 서술됨.
- **Auto-Enforcement 바인딩 약함**: 도구 이름만 나열되어 있고, 실제 구현(`01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/`)과의 연결/호출 규약이 METADoctrine에 고정돼 있지 않음.
- **Change Packet “실무 동선” 누락**: Change Packet minimum은 선언돼 있으나, (1) 템플릿 위치, (2) 제출/보관 위치(`00_Planning/change_packets/`), (3) Record Archive 패키지 링크 규약이 METADoctrine에 명시돼 있지 않음.
- **Manifestation 계약 미완성**: `03_Manifestation/`은 Canon/META에서 중요도가 올라갔지만, METADoctrine 내에서는 “비인지 실행 계층”의 최소 계약(입출력/감사/권한)이 부족.

### 개선 목표(한 줄)

METADoctrine를 “원리 선언”에서 **실제 repo/도구/템플릿과 1:1로 연결되는 집행 규격(spec)** 으로 업그레이드한다.

## 0.1. Gemini Blueprint 반영: META Layer “구조 DNA” [🟡 Priority: High]

Gemini안은 “META 레이어의 물리 구조(3기관/3레이어)가 곧 DNA이며, 그 자체가 Supremacy Clause를 가진다”는 점을 더 강하게 형식화한다.
Claude안에는 해당 형식(구조를 YAML로 고정, 개정 프로토콜을 조항화)이 없으므로 아래를 반영한다.

### 반영 포인트(요약)

- **Supremacy Clause(구조 권위)**: `04_Agentic_AI_OS/`의 최상위 3분 구조(`01_Nucleus/`, `02_Swarm/`, `03_Manifestation/`)를 “머신-리더블 구조 DNA”로 고정
- **Amendment Protocol(개정 규약)**: 변경은 `multi-agent-consensus` + 상위 변경 게이트(서명/감사)로만 가능
- **DNA Lifecycle(지속/해체)**: 이 구조는 Canon 폐기/대체가 아닌 한 해체되지 않는 “기본 기관”으로 취급

### Gemini 원문(보존용; 레거시 경로 포함)

```markdown
# AAOS META Layer DNA Blueprint (Gemini)

- 3기관 구조: Nucleus / Swarm / Manifestation
- Amendment protocol: multi-agent-consensus
- (레거시) Swarm components: AAOS_COF / AAOS_COO
```

### AAOS 정합화 버전(제안; Ready-to-Paste)

> 아래는 Gemini안을 현재 repo/Canon/METADoctrine 규약에 맞춰 “실경로 + 상위 변경 게이트”로 정렬한 버전이다.

```markdown
---
type: meta-layer-structure-blueprint
name: "AAOS-META-Layer-Structure"
status: draft
created: "2026-01-27"

governance:
  voice: constitutional
  amendment_protocol:
    required_gate: "upper-institution-change-gate"
    multi_agent_consensus: true
    canon_guardian_signature: true
    audit_required: true
  supremacy:
    - "AAOS Canon (04_Agentic_AI_OS/README.md)"
    - "META Doctrine (04_Agentic_AI_OS/METADoctrine.md)"
    - "Immune Doctrine (04_Agentic_AI_OS/01_Nucleus/Immune_system/AAOS_DNA_DOCTRINE_RULE.md)"

structure:
  nucleus: "01_Nucleus/"          # Governing Body (Validation Engine)
  swarm: "02_Swarm/"              # Working Body (Cognition; non-execution)
  manifestation: "03_Manifestation/" # Interface Body (execution binding)

references:
  canon: "04_Agentic_AI_OS/README.md"
  meta_doctrine: "04_Agentic_AI_OS/METADoctrine.md"
---

# META Layer Structure DNA (Draft)

## Supremacy Clause

본 구조 정의는 `04_Agentic_AI_OS/`의 최상위 기관 배치를 고정한다.
하위 구조/Agent는 이 구조 정의를 위반할 수 없다(충돌 시 homing_instinct로 상위 판정 요청).

## Structural Definition (Tri-Partite System)

### Nucleus (`01_Nucleus/`)

- Role: memory, immunity, deliberation, audit
- Components:
  - `Record_Archive/`
  - `Immune_system/`
  - `Deliberation_Chamber/`

### Swarm (`02_Swarm/`)

- Role: planning/cognition/pattern/skill (직접 하드웨어 실행은 하지 않음)
- Examples:
  - `Cortex_Agora/` (Swarm 행동(Behavior Trace) 관찰·요약·제안; Record_Archive 직접 조회 금지)
  - `Context-Orchestrated-Filesystem/` (COF)

### Manifestation (`03_Manifestation/`)

- Role: execution binding / I/O / interface (Non-Cognition)

## DNA Lifecycle

- Persistence: 이 구조 정의는 기본 기관으로 취급되며, 변경은 상위 변경 게이트를 통과해야 한다.
- Dissolution: Canon이 폐기/대체되는 경우에만 가능하다.
```

## 1. Manifestation 계층 명세 추가 [🔴 Priority: Critical]

### 현재 문제
- `03_Manifestation/` 계층이 언급만 되고 구체적 정의 없음
- "실행 바인딩; Non-Cognition"의 실체 불명확

### 개선안

```markdown
## 6. Manifestation Layer (현현/접속 계층)

`03_Manifestation/`

Swarm의 사고/행동양식을 외부 시스템에 실행 가능하게 바인딩하는 계층이다.
Manifestation은 인지(Cognition) 권한 없이 순수 실행만 수행한다.

참조(현행 draft):
- `04_Agentic_AI_OS/03_Manifestation/DNA_BLUEPRINT.md` (Execution Contract의 최소 형태)

### 6.1. Manifestation Binding Types

| 유형 | 설명 | 예시 |
|------|------|------|
| **Tool Binding** | 외부 도구/API 호출 인터페이스 | MCP Server, REST API |
| **Environment Binding** | 실행 환경 연결 | Docker, Shell, IDE |
| **Storage Binding** | 영속성 계층 연결 | DB, File System |
| **Communication Binding** | 외부 채널 연결 | Webhook, Message Queue |

### 6.2. Manifestation DNA Schema

```yaml
manifestation:
  binding_type: [tool|environment|storage|communication]
  target_system: string
  permission_scope:
    read: boolean
    write: boolean
    execute: boolean
  audit_trail: required
  fallback_behavior: [fail-safe|fail-open|escalate]
```

### 6.3. Execution Isolation Principle

- Manifestation은 Swarm/Immune System의 결정을 "해석/변경 없이" 실행
- 실행 중 발생한 예외는 Immune System으로 즉시 보고
- 자체 판단에 의한 행동 변경 금지 (Non-Cognition 원칙)
```

---

## 2. Auto-Enforcement 도구 스펙 정의 [🔴 Priority: Critical]

### 현재 문제
- METADoctrine는 “도구 이름”만 나열한다.
- 실제 구현은 이미 `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/` 아래에 존재하지만, 문서 연결이 약해서 “어디를 실행해야 하는지”가 흐려진다.

### 개선안

```markdown
### 1.4. Auto-Enforcement 도구 스펙 [개정 v0.3.0]

다음 도구는 AAOS Immune System의 Inquisitor Core에 포함되며, 실제 파일 위치는 아래와 같다.

| 도구 | 파일 |
|------|------|
| `yaml_validator.py` | `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/yaml_validator.py` |
| `auto_inquisitor.py` | `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py` |
| `dissolution_monitor.py` | `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/dissolution_monitor.py` |
| `audit.py` | `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/audit.py` |

#### yaml_validator.py

**목적**: DNA Blueprint/Permission Request의 YAML frontmatter 파싱 + 빈 값/필수키 검증

**권장 호출 경로**: 직접 실행하지 않고 `auto_inquisitor.py`가 내부적으로 사용한다.

**인터페이스(현행)**:
```python
validate_blueprint(path: Path) -> Tuple[result, reasons]
validate_permission_request(path: Path) -> Tuple[result, reasons]
```

**필수 검증 항목(요약)**:
- YAML 구문 유효성
- `natural_dissolution.*` 비어있지 않음(빈 값 불허)
- `resource_limits.*` 상한 명시

---

#### auto_inquisitor.py

**목적**: Git hook 및 런타임에서 자동 규칙 검증

**인터페이스**:
```python
def check_commit(diff: str) -> InquisitorVerdict:
    """Pre-commit hook용"""

def check_runtime(action: AgentAction) -> InquisitorVerdict:
    """Agent wrapper용"""

class InquisitorVerdict:
    approved: bool
    reason: str
    blocking_rules: List[str]
    audit_entry: AuditLogEntry
```

**Hook 생성(권장)**:
```bash
python3 01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py --gen-hook 04_Agentic_AI_OS
```

**주요 CLI(현행 구현)**:
```bash
python3 01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py --scan 04_Agentic_AI_OS --format md
python3 01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py --preflight 04_Agentic_AI_OS
python3 01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/auto_inquisitor.py --context 04_Agentic_AI_OS/02_Swarm --format md
```

---

#### dissolution_monitor.py

**목적**: TTL 만료 감시 및 Natural Dissolution 실행

**인터페이스**:
```python
def scan_expired() -> List[ExpiredStructure]:
    """만료된 구조 탐색"""

def execute_dissolution(target: str, mode: str) -> DissolutionReport:
    """
    mode: 'archive' | 'delete' | 'escalate'
    """
```

**Cron 설정 (권장)**:
```cron
0 0 * * * python3 01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/dissolution_monitor.py --scan 04_Agentic_AI_OS
```

**주요 CLI(현행 구현)**:
```bash
python3 01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/dissolution_monitor.py --scan 04_Agentic_AI_OS
python3 01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/dissolution_monitor.py --check-limits 04_Agentic_AI_OS/02_Swarm
python3 01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/dissolution_monitor.py --dissolve <structure_path> --reason "TTL expired" --dry-run
```

---

#### audit.py

**목적**: Append-only + 해시 체인으로 Audit Log 변조 감지 및 차단

**구현 포인트(현행)**:
- `safe_append_audit_entry(...)`: append 전 무결성 검증(손상 시 append 자체를 차단)
- `verify_audit_integrity(...)`: 전체 체인 검증
- `hash`: SHA-256 기반 16자리 short-hash(가독성 목적)

**인터페이스**:
```python
def verify_chain(log_path: str) -> ChainVerificationResult:
    """
    Returns:
        ChainVerificationResult:
            valid: bool
            broken_at: Optional[int]  # 무결성 깨진 라인
            hash_algorithm: str
    """

def append_entry(log_path: str, entry: AuditEntry) -> str:
    """Returns: new_hash"""
```

**해시 체인 포맷**:
```
[timestamp] [prev_hash] [action] [actor] [target] [verdict] [current_hash]
```
```

---

## 2.1. 참조 경로/레거시 네이밍 정합화 [🔴 Priority: Critical]

### 현재 문제

- METADoctrine.md에 레거시(개념) 경로가 남아 있어, 실제 repo 구조를 기준으로 집행/감사/링킹하기 어렵다.
  - 예: `AAOS_META_CANON/README.md`, `AAOS_META_DNA/METADoctrine.md`, `AAOS_SWARM/AAOS_COF/`

### 개선안(원칙)

1. **Canonical 문서는 “실재 경로”만 사용한다.** (repo 내 존재하는 파일/폴더)
2. 과거 명칭/개념 경로가 필요하면, METADoctrine에 **Legacy Alias Map(정보성)** 으로만 둔다.

---

## 2.2. Swarm 서브시스템 레지스트리 정합화 [🟡 Priority: High]

### 현재 문제

- METADoctrine의 COF/COO 섹션이 실제 `02_Swarm/` 구조와 다름.
- COO는 현행 `DNA_BLUEPRINT.md`만 존재(draft)인데, METADoctrine에는 `DNA.md`(정식)까지 있는 것으로 적혀 있음.

### 개선안(제안 문구)

```markdown
### 2.1. AAOS-COF (Context Orchestrated Filesystem)

- 컨테이너(버전 보관): `02_Swarm/Context-Orchestrated-Filesystem/`
  - 컨테이너 Blueprint: `02_Swarm/Context-Orchestrated-Filesystem/DNA_BLUEPRINT.md`
- 최신 정식 DNA(예시): `02_Swarm/Context-Orchestrated-Filesystem/DNA.md`

### 2.2. AAOS-COO (Context Orchestrated Ontology)

- 스캐폴드(draft): `02_Swarm/Context-Orchestrated-Ontology/DNA_BLUEPRINT.md`
- `DNA.md`는 아직 미존재(승격 전). 승격 시 Inquisitor 승인 + Audit Log 고정 후 `DNA.md`로 승격한다.
```

---

## 2.3. Change Packet 템플릿/보관 위치 명시 [🟡 Priority: High]

### 현재 문제

- METADoctrine의 Change Packet minimum은 좋지만, “어디에 무엇을 두는지” 실무 지침이 빠져 있다.

### 개선안(제안 문구)

```markdown
#### Change Packet (Where / Templates)

- Draft change packets (planning): `00_Planning/change_packets/`
- Deliberation packet template (Record Archive): `01_Nucleus/Record_Archive/templates/DELIBERATION_PACKET_TEMPLATE.md`
- Immune templates:
  - `01_Nucleus/Immune_system/templates/DNA-BLUEPRINT-TEMPLATE.md`
  - `01_Nucleus/Immune_system/templates/PERMISSION-REQUEST-TEMPLATE.md`
```

---

## 2.4. Proposed Patch (Ready-to-Apply; METADoctrine v0.1.10 → v0.1.11 제안)

> 아래는 “개선 Blueprint”가 아니라, 실제 `04_Agentic_AI_OS/METADoctrine.md`에 적용할 **텍스트 패치 제안**이다.

### P0: 참조 경로 2개 즉시 수정

- `AAOS_META_CANON/README.md` → `04_Agentic_AI_OS/README.md`
- `AAOS_META_DNA/METADoctrine.md`(개념 경로) → `04_Agentic_AI_OS/METADoctrine.md`(실제 경로) 또는 해당 1줄 삭제(중복이므로)

### P0: Auto-Enforcement 도구 경로 명시

- `yaml_validator.py` 등 4개 스크립트를 “이름만” 나열하지 말고, `01_Nucleus/Immune_system/SWARM_INQUISITOR_SKILL/_shared/` 아래 실제 경로로 고정

### P1: COF/COO 참조 정합화

- `AAOS_SWARM/AAOS_COF/` → `04_Agentic_AI_OS/02_Swarm/Context-Orchestrated-Filesystem/`
- COO는 `DNA_BLUEPRINT.md`만 존재(draft)임을 명시하고, `DNA.md` 존재 서술은 제거

### P1: Change Packet “Where/Templates” 추가

- `00_Planning/change_packets/` 및 `01_Nucleus/Record_Archive/templates/DELIBERATION_PACKET_TEMPLATE.md` 링크를 METADoctrine에 포함

---

## 3. 플래그십 Agent 선정 프로토콜 [🟡 Priority: High]

### 현재 문제
- "가장 발전된 능력"의 정량적 기준 없음
- 선정 절차 구체화 필요

### 개선안

```markdown
### 1.2.1. 플래그십 Agent 선정 프로토콜 [신규]

#### 선정 기준 (정량화)

| 기준 | 가중치 | 측정 방법 |
|------|--------|-----------|
| **벤치마크 성능** | 30% | 공인 벤치마크(MMLU, HumanEval 등) 상위 5% |
| **추론 능력** | 25% | 복합 추론 태스크 성공률 |
| **안전성 평가** | 25% | Safety alignment 테스트 통과율 |
| **운영 안정성** | 20% | 6개월 이상 프로덕션 운영 이력 |

#### 선정 절차

1. **후보 식별**: 분기별로 공인 벤치마크 상위 5% Agent 목록 수집
2. **다양성 검증**: 서로 다른 조직/모델 계열 2종 이상 확보
3. **자격 심사**: Canon Guardian이 위 기준표로 점수화
4. **등록**: `META_AUDIT_LOG.md`에 선정 근거와 함께 기록
5. **갱신**: 분기별 재평가, 탈락 시 대체 Agent 선정

#### 플래그십 명단 관리

```yaml
# META_AUDIT_LOG.md 기록 형식
flagship_agents:
  - agent_id: "agent-a"
    organization: "Org A"
    model_family: "Family X"
    qualified_date: 2026-01-27
    qualification_score: 85
    next_review: 2026-04-27
```
```

---

## 4. 긴급 패치 롤백 프로토콜 [🟡 Priority: High]

### 현재 문제
- "사후 합의 실패 시 롤백" 절차 미구체화

### 개선안

```markdown
### 1.2.2. 긴급 패치 롤백 프로토콜 [신규]

#### 롤백 트리거 조건

1. **사후 합의 실패**: 긴급 패치 후 72시간 내 플래그십 Agent 합의 미달성
2. **부작용 발견**: 패치로 인한 새로운 보안 취약점 또는 기능 장애
3. **Canon 위반 판정**: Inquisitor가 Canon 위반으로 판정

#### 롤백 절차

```
[T+0] 긴급 패치 적용
     │
     ▼
[T+72h] 합의 기한 도래
     │
     ├─ 합의 성공 → Canonical 승격
     │
     └─ 합의 실패/부작용/위반
           │
           ▼
     [즉시] 롤백 개시
           │
           ├─ 1. 변경 전 버전 복원 (자동)
           ├─ 2. AUDIT_LOG에 롤백 사유 기록
           ├─ 3. 영향받은 Swarm에 알림 전파
           └─ 4. Non-Canonical 태그 부착
```

#### 롤백 실패 시 Escalation

- **1차**: 인간 관리자 2인 개입
- **2차**: Canon Guardian 직접 개입
- **3차**: 전체 시스템 Freeze + 수동 복구
```

---

## 5. Agent 간 Conflict Resolution 프로토콜 [🟡 Priority: High]

### 현재 문제
- 인간 의존도 과다, Agent 자체 중재 메커니즘 없음

### 개선안

```markdown
### 1.2.3. Agent Conflict Resolution Protocol [신규]

#### 1단계: 자동 중재 (Agent-to-Agent)

```
Agent A Verdict ←→ Agent B Verdict
        │
        ▼
   차이점 분석
        │
        ├─ 핵심 논점 동일 → 표현 차이 병합
        │
        └─ 핵심 논점 상이
              │
              ▼
        제3 Agent 투표 요청 (플래그십 중 1)
              │
              ├─ 2:1 다수결 성립 → 다수 의견 채택
              │
              └─ 3자 모두 상이 → 2단계로 Escalate
```

#### 2단계: 구조화된 논쟁 (Deliberation Chamber)

1. 각 Agent가 `01_Nucleus/Deliberation_Chamber/`에 논점 제출
2. 형식: `{issue_id}_position_{agent_id}.md`
3. 72시간 내 추가 논증 허용
4. Record Archive에 논쟁 기록 보존

#### 3단계: 인간 중재 (최후 수단)

- 2단계에서 120시간 내 합의 불가 시
- Canon Guardian 또는 지정된 인간 중재자 개입
- 결정은 final, AUDIT_LOG에 기록
```

---

## 6. 시스템 건강도 메트릭 [🟠 Priority: Medium]

### 개선안

```markdown
## 7. AAOS Health Metrics [신규]

### 7.1. 핵심 지표 (KPI)

| 지표 | 측정 대상 | 정상 범위 | 경고 임계값 |
|------|-----------|-----------|-------------|
| **Consensus Latency** | 합의 소요 시간 | < 24h | > 72h |
| **Dissolution Rate** | 자연소멸 실행률 | > 90% | < 70% |
| **Audit Chain Integrity** | 해시 체인 유효율 | 100% | < 100% |
| **Inquisitor Approval Rate** | 승인/전체 요청 | 60-90% | < 40% or > 95% |
| **TTL Compliance** | 만료 전 처리율 | > 95% | < 80% |
| **Escalation Frequency** | 인간 개입 빈도 | < 5%/월 | > 15%/월 |

### 7.2. 대시보드 출력 (권장)

```yaml
# health_report.yaml
timestamp: 2026-01-27T00:00:00Z
period: weekly
metrics:
  consensus_latency_avg: 18h
  dissolution_rate: 94%
  audit_integrity: 100%
  inquisitor_approval: 72%
  ttl_compliance: 98%
  escalation_frequency: 2%
status: HEALTHY
```

### 7.3. 자동 경보

- 경고 임계값 초과 시 `Immune System`에 자동 보고
- 2회 연속 초과 시 Canon Guardian에 알림
```

---

## 7. Semantic Versioning 정책 [🟠 Priority: Medium]

### 개선안

```markdown
### META Doctrine Versioning Policy [신규]

#### 버전 형식: `vMAJOR.MINOR.PATCH`

| 변경 유형 | 버전 증가 | 예시 |
|-----------|-----------|------|
| **Canon 정렬 변경** | MAJOR | Canon 조항 추가/삭제에 따른 구조 변경 |
| **새 교리/기관 추가** | MINOR | Multi-Agent Consensus 도입 |
| **기존 교리 세부 조정** | MINOR | 플래그십 선정 기준 추가 |
| **오타/포맷팅/명확화** | PATCH | 문구 수정, 링크 업데이트 |
| **버그 수정** | PATCH | 누락된 참조 추가 |

#### 버전 변경 기록 필수 항목

```markdown
| 버전 | 날짜 | 변경 유형 | 변경 내용 | 승인 근거 |
```
```

---

## 8. Cross-Reference 검증 도구 [🟠 Priority: Medium]

### 개선안

```markdown
### 1.4.5. cross_ref_validator.py [신규]

**목적**: Canon ↔ META Doctrine ↔ DNA 간 참조 무결성 검증

**인터페이스**:
```python
def validate_references(root_path: str) -> CrossRefReport:
    """
    검증 항목:
    - 모든 링크 대상 파일 존재 여부
    - 참조된 버전과 실제 버전 일치 여부
    - 순환 참조 탐지
    - 고아(orphan) 문서 탐지
    """

class CrossRefReport:
    broken_links: List[BrokenLink]
    version_mismatches: List[VersionMismatch]
    circular_refs: List[CircularRef]
    orphan_docs: List[str]
```

**CI 통합 (권장)**:
```yaml
# .github/workflows/doctrine-check.yml
- name: Cross-Reference Validation
  run: python cross_ref_validator.py --root=04_Agentic_AI_OS/
```
```

---

## 9. Homing Instinct 발동 조건 명확화 [🟢 Priority: Low]

### 개선안

```markdown
### 4.1. Homing Instinct 발동 조건 [신규]

Record Archive 및 하위 구조는 다음 조건 중 하나라도 해당 시 Immune System으로 귀속:

| 조건 | 구체적 판단 기준 |
|------|------------------|
| **충돌 (Conflict)** | 동일 리소스에 대해 상반된 verdict가 존재 |
| **불명확 (Ambiguity)** | 48시간 내 자동 해석 불가, 또는 Agent 3종이 서로 다른 해석 제시 |
| **권한 경계 (Boundary)** | 요청 scope가 명시된 permission_scope 초과 |
| **무결성 손상** | 해시 체인 불일치 탐지 |
| **TTL 초과** | time_bound.expires 경과 후 미처리 |
```

---

## 10. TTL 유연성 확보 [🟢 Priority: Low]

### 개선안

```markdown
### Draft Natural Dissolution [개정]

기본 만료(기본값):
- **Planning Notes**: 30일
- **DNA Blueprint**: 30일
- **Experimental Feature**: 14일
- **Hotfix Draft**: 7일

프로젝트 특성별 조정:

```yaml
time_bound:
  expires: 2026-03-27
  base_ttl: 30d
  extension_limit: 2  # 최대 연장 횟수
  extension_requires: inquisitor-approval
```

연장 절차:
1. 만료 7일 전 연장 요청 제출
2. Inquisitor 승인 (사유 필수)
3. `META_AUDIT_LOG.md`에 연장 기록
```

---

## 구현 우선순위 로드맵

```
Phase 1 (즉시) [Critical]
├── #1 Manifestation 계층 명세
└── #2 Auto-Enforcement 도구 스펙

Phase 2 (2주 내) [High]
├── #3 플래그십 선정 프로토콜
├── #4 긴급 패치 롤백 프로토콜
└── #5 Conflict Resolution 프로토콜

Phase 3 (4주 내) [Medium]
├── #6 시스템 건강도 메트릭
├── #7 Semantic Versioning 정책
└── #8 Cross-Reference 검증 도구

Phase 4 (6주 내) [Low]
├── #9 Homing Instinct 조건 명확화
└── #10 TTL 유연성 확보
```

---

## 승인 요청

본 Blueprint는 METADoctrine.md v0.1.10의 개선안으로,
`Upper-Institution Change Gate` 절차에 따라 다음 승인을 요청합니다:

- [ ] Deliberation Chamber 산출물 (multi-agent-consensus)
- [ ] Record Archive 증빙 고정
- [ ] META_AUDIT_LOG 기록
- [ ] Canon Guardian 서명
- [ ] Inquisitor verdict + AUDIT_LOG 기록

---

*Generated by Claude Opus 4.5 | 2026-01-27*
