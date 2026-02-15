# Core -- cortex-agora Skill Governance

## 고정 문장

이 스킬은 cortex-agora의 관찰/제안 기능을 실행하지 않는다.
스킬 메타데이터, 아카이브 무결성, 소비 계약 정합성을 **점검(Validate)**하고
**보고(Report)**한다. 수정은 사람이 판단한다.

---

## 핵심 정의

| 용어 | 정의 |
|------|------|
| **Governed Skill** | 점검 대상 스킬. 현재 instruction-nucleus 1개. 04(자기 자신) 제외. |
| **Governed Infrastructure** | 점검 대상 인프라. change_archive(3 JSONL + bridge + index) + BEHAVIOR_FEED. |
| **Contract Coupling (CC)** | 스킬/인프라 간 key가 생산-소비 관계로 결합된 지점. |
| **CC Risk Level** | HIGH: 누락 시 downstream 실패. MEDIUM: 기능 저하. LOW: cosmetic. |
| **Governance Check Report** | 점검 결과를 표준 형식으로 구조화한 산출물. |
| **SoT Priority** | `SKILL.meta.yaml` > `SKILL.md frontmatter` > `SKILL_REGISTRY.md` |
| **Append-Only Invariant** | JSONL 파일의 기존 행은 수정/삭제 금지. 새 행만 추가. |
| **Monotonic Timestamp** | 각 JSONL 파일 내 `ts` 필드는 단조 증가해야 한다. |
| **Cross-Swarm Recording** | cortex-agora가 모든 swarm 행동을 기록하는 역할의 완전성. |

---

## 공유 출력 스키마

모든 점검 결과는 다음 형식으로 구조화한다:

```
{판단, 근거, 트레이드오프, 확신도}
```

- **판단**: PASS / WARN / FAIL + 항목 ID
- **근거**: 어떤 파일의 어떤 필드를 검사했는가
- **트레이드오프**: 해당 위반을 허용할 때의 리스크
- **확신도**: high / medium / low

최종 통합 산출물: `30.references/governance_check_report.template.md` 형식 사용.

---

## 점검 대상

| # | Target | Type | Key Files |
|---|--------|------|-----------|
| 00 | instruction-nucleus | Skill | `SKILL.md`, `SKILL.meta.yaml` |
| -- | change_archive | Infrastructure | 3 JSONL + `change_archive_bridge.py` + `CHANGE_INDEX.md` |
| -- | BEHAVIOR_FEED | Data | `behavior/BEHAVIOR_FEED.jsonl` |

---

## Contract Coupling Map

| CC ID | From | From Key | To | To Key | Risk |
|-------|------|----------|----|--------|------|
| CC-01 | instruction-nucleus | `proposal.id` | change_archive | `CHANGE_EVENTS.proposal_id` | HIGH |
| CC-02 | change_archive | `PEER_FEEDBACK.linked_event_id` | change_archive | `CHANGE_EVENTS.event_id` | HIGH |
| CC-03 | change_archive | `IMPROVEMENT_DECISIONS.feedback_refs[]` | change_archive | `PEER_FEEDBACK.feedback_id` | MEDIUM |
| CC-04 | behavior_feed | event schema | instruction-nucleus | observation trigger | MEDIUM |
| CC-05 | change_archive | `IMPROVEMENT_DECISIONS` status | COWI | `pull_agora_feedback.py` | HIGH |

---

## Global Invariants

1. 증거 없는 단정 금지 -- 점검 항목에는 반드시 검사 경로와 기대값을 명시한다.
2. 경로/계약 불일치 시 fail-fast -- 파일 누락이나 schema mismatch는 즉시 FAIL.
3. 불확실성은 `when_unsure` 규칙으로 명시.
4. 자동 수정 금지 -- 점검 결과를 보고할 뿐, 파일을 수정하지 않는다.
5. Append-only JSONL 불변조건 -- 기존 행 수정/삭제 금지.
6. 자기 자신(04) 점검은 manifest + loader 구조만 (계약 결합 해당 없음).
7. DNA 금지사항 계승 -- 실행, 자동반영, 규칙수정, 에이전트호출, record_archive 직접조회 금지.

---

## when_unsure 정책

| 상황 | 행동 |
|------|------|
| frontmatter vs sidecar 값 충돌 | `SKILL.meta.yaml`을 SoT로 우선, frontmatter 수정 권고를 WARN으로 기록 |
| CC 위반 심각도 불명확 | WARN으로 기록 + remediation 항목 + 수동 검토 요청 |
| JSONL 필드 존재하지만 값이 빈 경우 | WARN으로 기록, 빈 값의 의미를 사용자에게 확인 요청 |
| group_id vs trace_id 불일치 | canonical `group_id` 기준 판단 (DNA v0.1.4), `trace_id`는 backward-compat으로 기록 |
| COWI 소비 주기 미확인 | WARN + 수동 검증 요청 |
