"""MCP Tool wrapper for cof-task-manager-node skill."""

import subprocess
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from ..utils.paths import get_script_path
from ..utils.frontmatter import parse_frontmatter


@dataclass
class TicketInfo:
    """Information about a ticket."""

    path: str
    title: str
    status: str
    priority: str
    tags: list[str]
    description: str


@dataclass
class TaskManagerResult:
    """Result of task manager operations."""

    success: bool
    action: str
    message: str
    data: dict | None = None


class TaskManagerTool:
    """MCP Tool for COF task/ticket management.

    Provides operations for:
    - Creating task context nodes (NN.agents-task-context/)
    - Creating tickets
    - Listing tickets
    - Archiving completed tasks
    """

    TOOL_NAME = "cof_task_manager"
    TOOL_DESCRIPTION = """Manage COF task contexts and tickets.

Use this tool when you need to:
- Create a new agents-task-context node for tracking work
- Create a new ticket for a task
- List existing tickets in a task context
- Archive completed tasks

This tool follows the COF pointer model for task management."""

    def __init__(self):
        self._scripts = {
            "create_node": get_script_path('cof-task-manager-node', 'create_node.py'),
            "create_ticket": get_script_path('cof-task-manager-node', 'create_ticket.py'),
            "archive_tasks": get_script_path('cof-task-manager-node', 'archive_tasks.py'),
            "verify_node": get_script_path('cof-task-manager-node', 'verify_node.py'),
        }

    @property
    def input_schema(self) -> dict:
        """JSON Schema for tool input."""
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["create_node", "create_ticket", "list_tickets", "archive", "verify_node"],
                    "description": "Action to perform"
                },
                "target_dir": {
                    "type": "string",
                    "description": "Target directory for the operation"
                },
                "ticket_title": {
                    "type": "string",
                    "description": "Title for new ticket (required for create_ticket)"
                },
                "ticket_description": {
                    "type": "string",
                    "description": "Description for new ticket"
                },
                "ticket_tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tags for new ticket"
                },
                "ticket_priority": {
                    "type": "string",
                    "enum": ["P0", "P1", "P2", "P3"],
                    "description": "Priority for new ticket (default: P2)"
                }
            },
            "required": ["action", "target_dir"]
        }

    async def execute(
        self,
        action: Literal["create_node", "create_ticket", "list_tickets", "archive", "verify_node"],
        target_dir: str,
        ticket_title: str | None = None,
        ticket_description: str | None = None,
        ticket_tags: list[str] | None = None,
        ticket_priority: str = "P2"
    ) -> TaskManagerResult:
        """Execute task manager action."""

        if action == "list_tickets":
            return await self._list_tickets(target_dir)
        elif action == "create_ticket":
            if not ticket_title:
                return TaskManagerResult(
                    success=False,
                    action=action,
                    message="ticket_title is required for create_ticket action"
                )
            return await self._create_ticket(
                target_dir, ticket_title, ticket_description, ticket_tags, ticket_priority
            )
        elif action == "create_node":
            return await self._run_script("create_node", target_dir)
        elif action == "archive":
            return await self._run_script("archive_tasks", target_dir)
        elif action == "verify_node":
            return await self._run_script("verify_node", target_dir)
        else:
            return TaskManagerResult(
                success=False,
                action=action,
                message=f"Unknown action: {action}"
            )

    async def _list_tickets(self, target_dir: str) -> TaskManagerResult:
        """List tickets in a task context."""
        target_path = Path(target_dir).resolve()

        # Find tickets directory
        tickets_dirs = [
            target_path / "tickets",
            target_path  # If already in tickets dir
        ]

        tickets = []
        for tickets_path in tickets_dirs:
            if not tickets_path.exists():
                continue

            for ticket_file in tickets_path.glob("*.md"):
                if ticket_file.name.startswith("_"):
                    continue

                try:
                    content = ticket_file.read_text(encoding="utf-8", errors="replace")
                    fm, body = parse_frontmatter(content)

                    tickets.append(TicketInfo(
                        path=str(ticket_file),
                        title=fm.get("title", ticket_file.stem),
                        status=fm.get("status", "todo"),
                        priority=fm.get("priority", "P2"),
                        tags=fm.get("tags", []),
                        description=body[:200] + "..." if len(body) > 200 else body
                    ))
                except Exception:
                    continue

            if tickets:
                break

        return TaskManagerResult(
            success=True,
            action="list_tickets",
            message=f"Found {len(tickets)} ticket(s)",
            data={
                "tickets": [
                    {
                        "path": t.path,
                        "title": t.title,
                        "status": t.status,
                        "priority": t.priority,
                        "tags": t.tags,
                    }
                    for t in tickets
                ]
            }
        )

    async def _create_ticket(
        self,
        target_dir: str,
        title: str,
        description: str | None,
        tags: list[str] | None,
        priority: str
    ) -> TaskManagerResult:
        """Create a new ticket."""
        script = self._scripts.get("create_ticket")
        if script is None:
            return TaskManagerResult(
                success=False,
                action="create_ticket",
                message="create_ticket script not found"
            )

        args = [
            sys.executable, str(script),
            "--target-dir", target_dir,
            "--title", title,
            "--priority", priority
        ]

        if description:
            args.extend(["--description", description])
        if tags:
            args.extend(["--tags", ",".join(tags)])

        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                return TaskManagerResult(
                    success=True,
                    action="create_ticket",
                    message="Ticket created successfully",
                    data={"output": result.stdout}
                )
            else:
                return TaskManagerResult(
                    success=False,
                    action="create_ticket",
                    message=f"Failed to create ticket: {result.stderr or result.stdout}"
                )
        except Exception as e:
            return TaskManagerResult(
                success=False,
                action="create_ticket",
                message=f"Error creating ticket: {str(e)}"
            )

    async def _run_script(self, script_name: str, target_dir: str) -> TaskManagerResult:
        """Run a task manager script."""
        script = self._scripts.get(script_name)
        if script is None:
            return TaskManagerResult(
                success=False,
                action=script_name,
                message=f"{script_name} script not found"
            )

        try:
            result = subprocess.run(
                [sys.executable, str(script), "--target-dir", target_dir],
                capture_output=True,
                text=True,
                timeout=60
            )

            return TaskManagerResult(
                success=result.returncode == 0,
                action=script_name,
                message=result.stdout if result.returncode == 0 else result.stderr,
                data={"returncode": result.returncode}
            )
        except Exception as e:
            return TaskManagerResult(
                success=False,
                action=script_name,
                message=f"Error running {script_name}: {str(e)}"
            )
