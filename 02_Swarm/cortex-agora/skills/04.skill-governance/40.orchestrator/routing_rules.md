# Routing Rules -- cortex-agora Skill Governance

## Phase → Module 매핑

| Phase | Module | Check IDs |
|-------|--------|-----------|
| 1 | metadata-validation | FM, SC, 4L |
| 2 | archive-integrity | AE, AF, AD, AB, AI, AM |
| 3 | consumption-contract | BF, CP, XR |

## 의도 분류

| Intent Signal | Routing | Start Phase |
|---------------|---------|-------------|
| "메타데이터 점검", "frontmatter", "sidecar" | Validate | Phase 1 only |
| "아카이브 점검", "JSONL 검증", "이벤트 무결성", "append-only" | Integrity | Phase 2 only |
| "소비 계약", "COWI 인터페이스", "behavior feed", "cross-swarm" | Contract | Phase 3 only |
| "전체 거버넌스 점검", "governance check", "full pipeline" | Full | Phase 1 → 2 → 3 |
| "보고서", "report" | Report | 최근 결과 사용 |
| 모호한 의도 | Default: Full | Phase 1 → 2 → 3 |

## 에스컬레이션 규칙

| 조건 | 행동 |
|------|------|
| Phase 1 FAIL 존재 | Phase 2 진행 전 사용자에게 FAIL 보고 + 진행 여부 확인 |
| CC-01 또는 CC-02 FAIL (HIGH risk, Phase 2) | 즉시 사용자 보고: "proposal 추적 또는 피드백 참조 무결성 깨짐" |
| CC-05 FAIL (HIGH risk, Phase 3) | COWI 소비 중단 가능성 flag: "하류 소비자가 결정을 수신하지 못할 수 있음" |
| 동일 WARN 항목 3회 연속 거버넌스 점검에서 반복 | WARN → FAIL 승격 제안 |
