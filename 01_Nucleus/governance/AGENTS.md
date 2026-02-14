---
name: aaos-nucleus-agents-canonical
scope: "04_Agentic_AI_OS/01_Nucleus"
status: canonical
updated: "2026-02-14"
---

# Nucleus 작업 규칙 (Provider-Agnostic Rule Set)

- 이 폴더에서 수행하는 모든 Nucleus 작업은 다음 규칙을 **필수로 준수**한다.
- 실행 규칙은 provider/모델군에 무관하며 `Claude`, `Gemini`, `Grok`, `Codex` 등 모든 모델군이 동일 적용한다.

## 최상위 원칙 (Human Controllability)

- 최우선 규범: `https://github.com/WMJOON/semantic-atlas-hypothesis`
- 사람의 통제가능성은 정보 엔트로피가 임계치를 넘지 않을 때만 유지된다.
- 따라서 Nucleus 운영 문서는 `통제가능 영역 최소화`와 `메타데이터 최소화`를 기본값으로 한다.
  - 통제가능 영역 최소화: 강제 규칙은 핵심 정본 문서와 `SKILL.md` frontmatter로 한정한다.
  - 메타데이터 최소화: 프론트매터는 최소 필수 키만 유지하고, 과잉 필드는 금지한다.

## 문제제기 게이트 (Issue Framing)

- Nucleus에서 임의 작업을 개시하면 `문제제기`를 먼저 기록해야 한다.
- 기록 항목: `issue_scope`, `success_criteria`, `risk_level`, `context_for_next`.
- 1스텝 체인: 문제제기 산출물 없이 Step-2 기록/Step-3 plans 작성은 즉시 중단한다.
- `issue_proposer`는 사람이거나 승인된 책임자여야 하며, `issue_proposer` 누락은 즉시 중단 사유다.
- 단계 3(Deliberation) 이전에 `issue_*` 데이터가 없으면 작업은 승인 루프 진입 불가다.

## 반드시 준수할 규칙

1) `01_Nucleus/motor_cortex/governance/AGENTIC_WORKFLOW_ORCHESTRATION.md`를 최우선 실행 규약으로 따른다.
2) 1스텝 진입 규칙:
   - 문제제기(Problem Framing) 산출물 작성 없이 2단계·3단계로 진입하지 않는다.
   - `WORKFLOW_TRACE_MANIFEST`에 `record_path`(봉인 예정 경로 포인터)를 남기지 않은 상태에서 Deliberation 계획을 작성하지 않는다.
   - 모든 작업 산출물은 `deliberation_chamber/plans/<plan-id>/`에 보관한다. `record_archive`에 작업 파일을 직접 저장하지 않는다.
   - 실행 단계는 `motor_cortex` 책임으로 수행하며, 실행 결과만 `record_archive`에 봉인한다.
3) 핵심 심사 단계에서 단일 모델군으로 종결하지 않는다.
   - `plan_critic`와 `decomposition_critic`는 서로 다른 `model_family`여야 한다.
4) 증빙 아티팩트(`workflow manifest`)에 다음 필수 항목이 모두 남아야 한다.
   - `goal_statement`, `dq_index`, `rsv_total`
   - `topology_type`, `topology_rationale`, `task_graph_signature`
   - `model_consensus`
   - `criticality_separation_required: "true"`
   - `criticality_model_family_separated: "true"`
   - `plan_critic_model_id/provider/model_family`
   - `decomposition_critic_model_id/provider/model_family`
5) 상위기관 변경(특히 META/Nucleus 규범 변경)은
   `Proposal → Evidence → Judgment → Signature → Feedback` 루프를 통과해야 한다.
6) `cross_ref_validator` 및 `dissolution_monitor` 정합성 검증 없이 정식 종료로 간주하지 않는다.
7) Nucleus 규약 문서는 `01_Nucleus/governance/AGENTS.md` 단일 정본으로 운영한다.
   - `AGENT.md` 재생성/재도입은 금지한다.
8) 모든 `SKILL.md` frontmatter는 Claude Skills 공식 규범을 따른다.
   - 허용 키는 `name`, `description`, `argument-hint`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `model`, `context`, `agent`, `hooks`만 사용한다.
   - 위반 검증 기준: `https://code.claude.com/docs/en/skills`
9) 기관 하위 디렉토리명은 소문자만 허용한다.
   - 예: `SKILLS/` 금지, `skills/` 사용

## 위반 처리

- 위 규칙 위반이 감지되면 즉시 `Request-Changes` 또는 `on_conflict`로 Immune/META 귀속한다.
- “동일 에이전트/동일 모델군 독자 수행”은 자동 무효 처리 대상이다.
