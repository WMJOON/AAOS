# Call-CLI-Agents MCP Server

CLI 에이전트(Claude, Codex, Gemini) 디스패처 MCP 서버.

COF 티켓을 AI CLI 에이전트에 자동으로 디스패치하고, 결과를 티켓에 기록한다.

## Quick Start

### Installation

```bash
cd mcp/sa-call-cli-agents-mcp
pip install -e .

# 또는 uvx로 실행 (설치 없이)
uvx --from . sa-call-cli-agents-mcp
```

### Claude Desktop Configuration

`~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "call-cli-agents": {
      "command": "sa-call-cli-agents-mcp",
      "env": {
        "AAOS_ROOT": "/path/to/04_Agentic_AI_OS",
        "COF_ROOT": "/path/to/04_Agentic_AI_OS/02_Swarm/context-orchestrated-filesystem"
      }
    }
  }
}
```

### Claude Code Configuration

`.claude/mcp.json`:

```json
{
  "mcpServers": {
    "call-cli-agents": {
      "command": "sa-call-cli-agents-mcp",
      "env": {
        "AAOS_ROOT": "/path/to/04_Agentic_AI_OS"
      }
    }
  }
}
```

### Docker (위치 독립적)

Docker 이미지에는 모든 CLI 도구가 포함되어 있어 어디서든 동일하게 작동합니다.

> Note: Docker 실행 예시는 기본적으로 **API 키 기반(API 과금 가능)** 환경을 가정합니다.
> 구독 로그인 기반(`billing_mode=subscription_only`)은 로컬 호스트 환경에서 구성하는 것을 권장합니다.

```bash
# 이미지 빌드
docker build -t sa-call-cli-agents-mcp .

# 실행 (모든 API 키 포함)
docker run -i --rm \
  -v /path/to/04_Agentic_AI_OS:/workspace:rw \
  -e AAOS_ROOT=/workspace \
  -e COF_ROOT=/workspace/02_Swarm/context-orchestrated-filesystem \
  -e ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY} \
  -e OPENAI_API_KEY=${OPENAI_API_KEY} \
  -e GOOGLE_API_KEY=${GOOGLE_API_KEY} \
  sa-call-cli-agents-mcp
```

**docker-compose 사용:**

```bash
# .env 파일 생성
cat > .env << 'EOF'
AAOS_ROOT=/path/to/04_Agentic_AI_OS
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
EOF

# 실행
docker-compose up
```

**Claude Desktop에서 Docker 사용:**

```json
{
  "mcpServers": {
    "call-cli-agents": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "/path/to/04_Agentic_AI_OS:/workspace:rw",
        "-e", "AAOS_ROOT=/workspace",
        "-e", "COF_ROOT=/workspace/02_Swarm/context-orchestrated-filesystem",
        "-e", "ANTHROPIC_API_KEY",
        "-e", "OPENAI_API_KEY",
        "-e", "GOOGLE_API_KEY",
        "sa-call-cli-agents-mcp"
      ],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-...",
        "OPENAI_API_KEY": "sk-...",
        "GOOGLE_API_KEY": "..."
      }
    }
  }
}
```

**포함된 CLI 도구:**

| CLI | 패키지 | 용도 |
|-----|--------|------|
| `claude` | @anthropic-ai/claude-code | Security, Audit, 일반 작업 |
| `codex` | @openai/codex | Architecture, Refactor |
| `gemini` | @google/gemini-cli | Performance, Review, Google 생태계 |

## Available Tools

| Tool | Description |
|------|-------------|
| `cof_index_context` | 디렉토리 구조 인덱싱, 노드 역할 식별 |
| `cof_task_manager` | 태스크 컨텍스트 노드/티켓 관리 |
| `cof_solve_ticket` | 티켓을 AI CLI 에이전트에 디스패치 |
| `cof_get_ticket_status` | 티켓 상태 조회 |

## Usage Examples

### 컨텍스트 인덱싱

```
cof_index_context({
  "target_dir": "./01.agents-task-context",
  "max_depth": 5
})
```

### 티켓 생성

```
cof_task_manager({
  "action": "create_ticket",
  "target_dir": "./01.agents-task-context",
  "ticket_title": "Refactor authentication module",
  "ticket_tags": ["architecture", "refactor"],
  "ticket_priority": "P1"
})
```

### 티켓 해결

```
cof_solve_ticket({
  "ticket_path": "./01.agents-task-context/tickets/refactor-auth.md",
  "provider": "codex",
  "timeout": 600,
  "billing_mode": "subscription_only"
})
```

### 티켓 해결 (비동기 Job 모드: 권장)

CLI 호출이 오래 걸리거나 Claude Desktop/클라이언트가 중간에 종료될 수 있으면 Job 모드를 사용하세요.

```
cof_start_solve_ticket({
  "ticket_path": "./01.agents-task-context/tickets/refactor-auth.md",
  "council_mode": true,
  "timeout": 900,
  "billing_mode": "subscription_only"
})
```

이후:

```
cof_get_job_status({ "job_id": "..." })
cof_get_job_logs({ "job_id": "...", "max_bytes": 32000 })
cof_cancel_job({ "job_id": "..." })
```

### Council 모드 (병렬 실행)

```
cof_solve_ticket({
  "ticket_path": "./tickets/security-review.md",
  "council_mode": true
})
```

## Architecture

```
sa-call-cli-agents-mcp/
├── server.py          # MCP 서버 진입점
├── tools/
│   ├── glob_indexing.py   # cof-glob-indexing 래퍼
│   ├── task_manager.py    # cof-task-manager-node 래퍼
│   └── task_solver.py     # cof-task-solver-agent-group 래퍼
└── utils/
    ├── frontmatter.py     # YAML frontmatter 파싱
    └── paths.py           # COF/AAOS 경로 해석
```

## Requirements

- Python 3.10+
- `mcp` >= 1.0.0
- COF skills 설치됨 (scripts/*.py)

## Billing Mode (API 과금 회피)

기본값은 `billing_mode=subscription_only`이며, Job/실행 프로세스의 환경에서
`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY` 등 API 키 환경변수를 제거해서
실수로 pay-per-token API 과금이 발생하는 것을 방지합니다.

의도적으로 API 키 기반 실행이 필요하면 `billing_mode=allow_api`를 사용하세요.

## Indexing Failure Hedge

기본 동작은 **컨텍스트 인덱싱이 실패하거나 COF index anchor를 찾지 못하면 즉시 종료(티켓을 blocked로 전이)** 하며,
티켓 본문에 `## Indexing Failure Evidence` 섹션과 `INDEXING_FAILURE_*.json` 증적 파일을 남깁니다.

최소 컨텍스트 fallback이 필요하면 `allow_minimal_context=true`를 사용하세요.

## Development

```bash
# 테스트 실행
pip install -e ".[dev]"
pytest

# 로컬에서 서버 테스트
python -m aaos_mcp.server
```

## References

- [MANIFEST.md](./MANIFEST.md) - MCP 바인딩 설정
- `@ref(cof-task-solver-agent-group)` - 메인 티켓 해결 스킬
- `@ref(cof-environment-set)` - COF 환경 규칙
