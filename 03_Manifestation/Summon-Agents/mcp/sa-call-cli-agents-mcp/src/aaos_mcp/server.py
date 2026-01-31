"""AAOS MCP Server - Unified interface for COF skills.

This server exposes COF (Context-Orchestrated Filesystem) skills as MCP tools:
- cof_index_context: Index directory structure and identify node roles
- cof_task_manager: Create/manage task contexts and tickets
- cof_solve_ticket: Dispatch tickets to AI CLI agents
- cof_get_ticket_status: Query ticket status
"""

import asyncio
import json
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    CallToolResult,
)

from .tools.glob_indexing import GlobIndexingTool
from .tools.task_manager import TaskManagerTool
from .tools.task_solver import TaskSolverTool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aaos-mcp-server")

# Initialize server
server = Server("aaos-mcp-server")

# Initialize tools
glob_indexing = GlobIndexingTool()
task_manager = TaskManagerTool()
task_solver = TaskSolverTool()


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="cof_index_context",
            description=GlobIndexingTool.TOOL_DESCRIPTION,
            inputSchema=glob_indexing.input_schema
        ),
        Tool(
            name="cof_task_manager",
            description=TaskManagerTool.TOOL_DESCRIPTION,
            inputSchema=task_manager.input_schema
        ),
        Tool(
            name="cof_solve_ticket",
            description=TaskSolverTool.TOOL_DESCRIPTION,
            inputSchema=task_solver.input_schema
        ),
        Tool(
            name="cof_start_solve_ticket",
            description="Start solving a ticket in the background and return a job_id for polling.",
            inputSchema=task_solver.input_schema
        ),
        Tool(
            name="cof_get_job_status",
            description="Get status for a previously started background job.",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {"type": "string", "description": "Job id returned by cof_start_solve_ticket"},
                },
                "required": ["job_id"]
            }
        ),
        Tool(
            name="cof_get_job_logs",
            description="Get recent stdout/stderr for a background job (best-effort).",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {"type": "string", "description": "Job id returned by cof_start_solve_ticket"},
                    "max_bytes": {"type": "integer", "default": 32000, "description": "Max bytes to return per stream"},
                },
                "required": ["job_id"]
            }
        ),
        Tool(
            name="cof_cancel_job",
            description="Attempt to cancel a background job by sending SIGTERM to its process group.",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {"type": "string", "description": "Job id returned by cof_start_solve_ticket"},
                },
                "required": ["job_id"]
            }
        ),
        Tool(
            name="cof_get_ticket_status",
            description="Get the current status of a ticket without solving it.",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_path": {
                        "type": "string",
                        "description": "Path to the ticket file"
                    }
                },
                "required": ["ticket_path"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    try:
        if name == "cof_index_context":
            result = await glob_indexing.execute(
                target_dir=arguments["target_dir"],
                max_depth=arguments.get("max_depth", 10)
            )
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({
                        "status": result.status,
                        "node_index_path": result.node_index_path,
                        "role_evidence_path": result.role_evidence_path,
                        "message": result.message
                    }, indent=2)
                )]
            )

        elif name == "cof_task_manager":
            result = await task_manager.execute(
                action=arguments["action"],
                target_dir=arguments["target_dir"],
                ticket_title=arguments.get("ticket_title"),
                ticket_description=arguments.get("ticket_description"),
                ticket_tags=arguments.get("ticket_tags"),
                ticket_priority=arguments.get("ticket_priority", "P2")
            )
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({
                        "success": result.success,
                        "action": result.action,
                        "message": result.message,
                        "data": result.data
                    }, indent=2)
                )]
            )

        elif name == "cof_solve_ticket":
            result = await task_solver.execute(
                ticket_path=arguments["ticket_path"],
                provider=arguments.get("provider"),
                council_mode=arguments.get("council_mode", False),
                timeout=arguments.get("timeout", 300),
                context_depth=arguments.get("context_depth", 10),
                dry_run=arguments.get("dry_run", False),
                allow_minimal_context=arguments.get("allow_minimal_context", False),
                billing_mode=arguments.get("billing_mode", "subscription_only"),
            )
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({
                        "success": result.success,
                        "ticket_path": result.ticket_path,
                        "original_status": result.original_status,
                        "final_status": result.final_status,
                        "agent_group": result.agent_group,
                        "execution_time": result.execution_time,
                        "output": result.output[:2000] if result.output else "",
                        "error": result.error
                    }, indent=2)
                )]
            )

        elif name == "cof_start_solve_ticket":
            result = await task_solver.start_solve_job(
                ticket_path=arguments["ticket_path"],
                provider=arguments.get("provider"),
                council_mode=arguments.get("council_mode", False),
                timeout=arguments.get("timeout", 300),
                context_depth=arguments.get("context_depth", 10),
                dry_run=arguments.get("dry_run", False),
                allow_minimal_context=arguments.get("allow_minimal_context", False),
                billing_mode=arguments.get("billing_mode", "subscription_only"),
            )
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({
                        "success": result.success,
                        "job_id": result.job_id,
                        "message": result.message,
                        "stripped_env_vars": result.stripped_env_vars,
                        "paths": {
                            "job_file": str(result.job_paths.job_file),
                            "stdout_file": str(result.job_paths.stdout_file),
                            "stderr_file": str(result.job_paths.stderr_file),
                            "result_file": str(result.job_paths.result_file),
                        }
                    }, indent=2)
                )]
            )

        elif name == "cof_get_job_status":
            data = await task_solver.get_job_status(job_id=arguments["job_id"])
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(data, indent=2))]
            )

        elif name == "cof_get_job_logs":
            data = await task_solver.get_job_logs(
                job_id=arguments["job_id"],
                max_bytes=arguments.get("max_bytes", 32000),
            )
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(data, indent=2))]
            )

        elif name == "cof_cancel_job":
            data = await task_solver.cancel_job(job_id=arguments["job_id"])
            return CallToolResult(
                content=[TextContent(type="text", text=json.dumps(data, indent=2))]
            )

        elif name == "cof_get_ticket_status":
            result = await task_solver.get_ticket_status(
                ticket_path=arguments["ticket_path"]
            )
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            )

        else:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=json.dumps({"error": f"Unknown tool: {name}"})
                )],
                isError=True
            )

    except Exception as e:
        logger.exception(f"Error executing tool {name}")
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=json.dumps({"error": str(e)})
            )],
            isError=True
        )


def main():
    """Run the AAOS MCP server."""
    logger.info("Starting AAOS MCP Server...")
    asyncio.run(run_server())


async def run_server():
    """Run the server with stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    main()
