---
context_id: mcp-manifestation-template
role: SCHEMA
state: const
scope: swarm
lifetime: persistent
---

# MCP Manifestation Template

This template defines the standard for binding Model Context Protocol (MCP) servers within the AAOS Manifestation layer. 

> [!NOTE]
> This template follows the **Manifestation 최소 계약(권장 스키마)** defined in [DNA.md#5.2](file:///Users/wmjoon/Library/Mobile%20Documents/iCloud~md~obsidian/Documents/wmjoon/04_Agentic_AI_OS/00_METADoctrine/DNA.md#L439).

## Manifest Configuration

```yaml
manifestation:
  binding_type: tool # tool | environment | storage | communication
  target_system: "mcp-server-name"
  permission_scope:
    read: true
    write: false
    execute: true
  audit_trail: required # Logging requirement level
  fallback_behavior: fail-safe # fail-safe | fail-open | escalate
  mcp_config:
    server_id: "identifier" # Unique logical ID for the server
    transport: "stdio"  # stdio | http
    command: "executable" # Command to run (or URL if HTTP)
    args: [] # CLI arguments
    env: {} # Environment variables
```

## Documentation

### Purpose
Describe what this MCP server provides to the Swarm.

### Tools
List the available tools provided by this MCP server.

- `tool_name`: Description

### Resources
List the available resources (if any).

### Constraints
Describe any specific usage constraints or safety boundaries (Rate limits, Privacy, Verification).
