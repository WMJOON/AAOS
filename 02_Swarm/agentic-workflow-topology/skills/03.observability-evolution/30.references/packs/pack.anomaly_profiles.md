# pack.anomaly_profiles

> **로딩 조건**: ΔQ >= 2 (이상 신호 상세 프로파일 참조 필요 시)

각 Anomaly Signal 유형의 상세 프로파일, 임계값, 판단 가이드.

---

## AS-1: performance_drift

| 속성 | 값 |
|------|-----|
| **정의** | 실행 시간이 히스토리컬 평균에서 2σ 초과 이탈 |
| **데이터 소스** | SQLite `audit_logs` (created_at - date 기반) |
| **임계값** | notice: >2σ, warning: >3σ, critical: >4σ 또는 타임아웃 |
| **오탐 가능성** | 일회성 외부 요인(네트워크, API 지연). 2+ OW 연속 시 확정 |
| **전형적 근본 원인** | θ_GT band 부적합, 모델 성능 저하, 입력 복잡도 증가 |
| **연관 제안** | θ_GT 재보정, mode/model 전환 |

## AS-2: failure_cluster

| 속성 | 값 |
|------|-----|
| **정의** | 동일 task_name에서 OW 내 3건 이상 실패 |
| **데이터 소스** | SQLite `audit_logs` WHERE status='fail' |
| **임계값** | warning: 3-4건, critical: 5건+ |
| **오탐 가능성** | 낮음. 3건 연속 실패는 체계적 문제 |
| **전형적 근본 원인** | 노드 설계 결함, 입력 스키마 불일치, 외부 의존성 장애 |
| **연관 제안** | topology 재구성, 노드 재설계, fallback 규칙 추가 |

## AS-3: retry_spike

| 속성 | 값 |
|------|-----|
| **정의** | OW 내 재시도(transition_repeated=1) 비율 > 20% |
| **데이터 소스** | SQLite `audit_logs` transition_repeated 필드 |
| **임계값** | notice: 20-30%, warning: 30-50%, critical: 50%+ |
| **오탐 가능성** | 중간. 정상적 convergence loop와 구분 필요 |
| **구분 기준** | convergence loop = 재시도마다 θ_GT 감소. 병리적 = θ_GT 정체 또는 증가 |
| **전형적 근본 원인** | max_iterations 부족, 종료 조건 부적합, redundancy accumulation |
| **연관 제안** | max_iterations 조정, 루프 위험 mitigation |

## AS-4: bottleneck

| 속성 | 값 |
|------|-----|
| **정의** | 단일 노드가 전체 실행 시간의 60%+ 소비 |
| **데이터 소스** | SQLite `audit_logs` task_name별 이벤트 비율 |
| **임계값** | warning: 60-80%, critical: 80%+ |
| **오탐 가능성** | 중간. 의도적으로 무거운 노드(합성 노드)는 정상일 수 있음 |
| **구분 기준** | workflow_spec에서 해당 노드의 설계 의도 확인. 합성 노드의 높은 비중은 정상 |
| **전형적 근본 원인** | 노드 미분할, 과도한 scope, 직렬 처리 가능 구간 |
| **연관 제안** | 노드 분할, parallel topology 검토 |

## AS-5: human_deferral_loop

| 속성 | 값 |
|------|-----|
| **정의** | human_intervention=true 이벤트가 OW 내 40%+ |
| **데이터 소스** | Behavior feed JSONL outcome.human_intervention, SQLite notes/continuation_hint |
| **임계값** | notice: 40-50%, warning: 50-70%, critical: 70%+ |
| **오탐 가능성** | 중간. strategy/high-risk 워크플로우는 높은 HITL 비율이 정상 |
| **구분 기준** | DNA의 PF1/H1/H2 gate 설정 확인. gate에 의한 의도적 HITL은 제외 |
| **전형적 근본 원인** | gate 판단 기준 부재, auto-approve 조건 미설정 |
| **연관 제안** | auto-approve 조건 제안, gate 기준 정교화 |

## AS-6: rsv_inflation

| 속성 | 값 |
|------|-----|
| **정의** | 실제 RSV 소비가 설계 RSV 타깃의 130%+ 초과 |
| **데이터 소스** | Workflow spec rsv_target vs 실행 결과 (근사 지표) |
| **임계값** | warning: 130-150%, critical: 150%+ |
| **오탐 가능성** | 중간. Goal 자체가 예상보다 넓었을 수 있음 |
| **전형적 근본 원인** | Goal 과대 설정, DQ 불완전, 노드 간 중복 작업 |
| **연관 제안** | Goal reframe, 워크플로우 분할, DQ 재정의 |
