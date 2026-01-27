---
type: deliberation-packet
timestamp: "YYYY-MM-DDTHH:MM:SSZ"
subject: "<what change is being deliberated>"
targets:
  - "<path/or/id>"
required_gate: "upper-institution-change-gate"
status: "draft" # draft, submitted, archived

flagship_consensus_requirement:
  required: true
  min_flagship_agents: 2
  distinct_model_families: true
  evidence: "Each flagship agent must record verdict+rationale with model metadata."

multi_agent_consensus:
  - agent_id: "<agent-A>"
    model_id: "<model>"
    model_family: "<provider-or-family>" # e.g., openai-gpt, anthropic-claude, google-gemini
    org: "<org-or-provider>"
    flagship: true
    verdict: "approve | reject | request-changes"
    rationale:
      - "..."
  - agent_id: "<agent-B>"
    model_id: "<model>"
    model_family: "<provider-or-family>"
    org: "<org-or-provider>"
    flagship: true
    verdict: "approve | reject | request-changes"
    rationale:
      - "..."

evidence_links:
  - "record-archive package path"
  - "audit log entry reference"

requested_action:
  - "what to sign / what to promote"
---
# Deliberation Packet

## Risk/Impact

- Risk:
- Blast radius:
- Rollback plan:

## Decision Summary

- Conclusion:
- Conditions (if any):
