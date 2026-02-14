---
context_id: mcp-manifest-sa-call-cli-agents
role: MANIFEST
state: active
scope: swarm
lifetime: persistent
manifestation:
  binding_type: tool
  target_system: "sa-call-cli-agents-mcp"
  permission_scope:
    read: true
    write: true
    execute: true
  audit_trail: required
  fallback_behavior: fail-safe
  mcp_config:
    server_id: "call-cli-agents"
    transport: "stdio"
    command: "sa-call-cli-agents-mcp"
    args: []
    env:
      COF_ROOT: "${AAOS_ROOT}/02_Swarm/context-orchestrated-filesystem"
      AAOS_ROOT: "${AAOS_ROOT}"
---

# MANIFEST: Call-CLI-Agents MCP Server

CLI 에이전트 디스패처 MCP 서버를 Manifestation 레이어에 바인딩하는 설정 문서이다.

## Purpose

COF(Context-Orchestrated Filesystem) 스킬들을 MCP 도구로 노출하여, Claude Code 등 MCP 클라이언트가 AAOS 기능을 직접 호출할 수 있게 한다.

## Tools

### cof_index_context

디렉토리 구조를 인덱싱하여 COF 노드 역할을 식별한다.

```json
{
  "target_dir": "/path/to/directory",
  "max_depth": 10
}
```

**Returns**: NODE_INDEX.md, ROLE_EVIDENCE.md 경로

### cof_task_manager

태스크 컨텍스트 노드와 티켓을 관리한다.

```json
{
  "action": "create_ticket",
  "target_dir": "/path/to/NN.agents-task-context",
  "ticket_title": "Implement feature X",
  "ticket_tags": ["architecture", "refactor"],
  "ticket_priority": "P1"
}
```

**Actions**: `create_node`, `create_ticket`, `list_tickets`, `archive`, `verify_node`

### cof_solve_ticket

티켓을 AI CLI 에이전트에 디스패치하여 해결한다.

```json
{
  "ticket_path": "/path/to/ticket.md",
  "provider": "claude",
  "council_mode": false,
  "timeout": 300
}
```

**Agent Selection**: 티켓 태그 기반 자동 선택 (`security` → claude, `performance` → gemini 등)

### cof_start_solve_ticket

티켓 해결을 **백그라운드 Job**으로 시작하고 `job_id`를 반환한다 (권장).

```json
{
  "ticket_path": "/path/to/ticket.md",
  "council_mode": true,
  "timeout": 900,
  "billing_mode": "subscription_only"
}
```

### cof_get_job_status / cof_get_job_logs / cof_cancel_job

`cof_start_solve_ticket`로 시작한 Job을 폴링/로그조회/취소한다.

### cof_get_ticket_status

티켓의 현재 상태를 조회한다 (실행 없이).

## Resources

(없음 - 향후 티켓을 MCP Resource로 노출 예정)

## Constraints

1. **COF 경계 준수**: 모든 작업은 COF 노드 경계 내에서 수행
2. **Status Integrity**: 티켓 상태 전이는 정해진 순서만 허용 (todo → in-progress → done|blocked)
3. **Result Recording**: 에이전트 실행 결과는 반드시 티켓에 기록
4. **Script Dependency**: 실제 스킬 스크립트가 설치되어 있어야 함

## Dependencies

- `@ref(cof-glob-indexing)` - 컨텍스트 인덱싱 스킬
- `@ref(cof-task-manager-node)` - 티켓 관리 스킬
- `@ref(cof-task-solver-agent-group)` - 에이전트 디스패치 스킬
