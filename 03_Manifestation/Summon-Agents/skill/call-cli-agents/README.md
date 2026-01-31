---
name: aaos-manifestation-call-cli-agents
description: Manifestation component that binds Swarm intent to external AI CLIs (Codex/Claude/Gemini) and normalizes results.
---
# Call CLI Agents (Manifestation)

이 폴더는 Swarm의 의도를 외부 AI CLI 실행으로 현현하는 실행 바인딩(Execution Binding) 컴포넌트이다. (별칭: AI Collaborator)

## Canonical

- Current: `call-cli-agents_v0.3/`
  - Skill: `call-cli-agents_v0.3/SKILL.md`
  - Reference: `call-cli-agents_v0.3/REFERENCE.md`
  - Patterns: `call-cli-agents_v0.3/PATTERNS.md`
  - Scripts: `call-cli-agents_v0.3/scripts/`

## Non-Cognition / Hard Boundary

- 이 컴포넌트는 “계획/정책”을 만들지 않고, **Swarm의 의도(프롬프트/작업 정의)** 를 외부 CLI 실행으로만 현현한다.
- 실행 결과는 **요약/정규화**하여 상위 워크플로우로 환류할 뿐, 스스로 규칙을 바꾸지 않는다.
