---
name: aaos-manifestation-summon-agents-mcp
description: Manifestation bindings for Model Context Protocol (MCP) servers.
---
# MCP (summon-agents)

Model Context Protocol (MCP) 서버를 호출(summon)하기 위한 Manifestation 바인딩들이 위치하는 디렉토리이다.

## Contents

| Directory | Type | Description |
|-----------|------|-------------|
| [sa-call-cli-agents-mcp/](sa-call-cli-agents-mcp/) | **Native Package** | CLI 에이전트 디스패처 MCP 서버 |
| [MCP-MANIFESTATION-TEMPLATE.md](MCP-MANIFESTATION-TEMPLATE.md) | Template | MCP 바인딩 표준 템플릿 |

## Quick Start

```bash
cd sa-call-cli-agents-mcp
pip install -e .
```

Claude Code에서 사용:

```json
// .claude/mcp.json
{
  "mcpServers": {
    "call-cli-agents": {
      "command": "sa-call-cli-agents-mcp"
    }
  }
}
```

### Available Tools

| Tool | Skill | Description |
|------|-------|-------------|
| `cof_index_context` | cof-glob-indexing | 디렉토리 구조 인덱싱 |
| `cof_task_manager` | cof-task-manager-node | 티켓/노드 관리 |
| `cof_solve_ticket` | cof-task-solver-agent-group | AI 에이전트 디스패치 |
| `cof_get_ticket_status` | - | 티켓 상태 조회 |
