---
name: aaos-manifestation-ai-collaborator
description: Manifestation component that binds Swarm review/workflow intent to external AI CLIs (Codex/Claude/Gemini) and normalizes results.
---
# AI Collaborator (Manifestation)

이 폴더는 `AI Collaborator`를 AAOS `03_Manifestation/` 계층에 정식 편입한 실행 바인딩(Execution Binding) 컴포넌트이다.

## Canonical

- Current: `ai-collaborator_v0.3/`
  - Skill: `ai-collaborator_v0.3/SKILL.md`
  - Reference: `ai-collaborator_v0.3/REFERENCE.md`
  - Patterns: `ai-collaborator_v0.3/PATTERNS.md`
  - Scripts: `ai-collaborator_v0.3/scripts/`

## Non-Cognition / Hard Boundary

- 이 컴포넌트는 “계획/정책”을 만들지 않고, **Swarm의 의도(프롬프트/작업 정의)** 를 외부 CLI 실행으로만 현현한다.
- 실행 결과는 **요약/정규화**하여 상위 워크플로우로 환류할 뿐, 스스로 규칙을 바꾸지 않는다.

