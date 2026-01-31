"""MCP Tool wrapper for cof-glob-indexing skill."""

import subprocess
import json
from dataclasses import dataclass
from pathlib import Path

from ..utils.paths import get_script_path


@dataclass
class IndexingResult:
    """Result of context indexing."""

    status: str  # success | partial | error
    node_index_path: str | None
    role_evidence_path: str | None
    message: str
    raw_output: str


class GlobIndexingTool:
    """MCP Tool for COF context indexing.

    Wraps the cof-glob-indexing skill to provide:
    - Node boundary detection
    - Role directory identification
    - Context artifact generation (NODE_INDEX.md, ROLE_EVIDENCE.md)
    """

    TOOL_NAME = "cof_index_context"
    TOOL_DESCRIPTION = """Index a directory to identify its COF node structure and role.

Use this tool when you need to:
- Understand the structure of a directory in the COF filesystem
- Get context about a node before performing operations
- Identify role directories (index, reference, working, ticket, etc.)

Returns NODE_INDEX.md and ROLE_EVIDENCE.md paths if successful."""

    def __init__(self):
        self._script_path = get_script_path(
            'cof-glob-indexing',
            'cof_glob_indexing.py'
        )

    @property
    def input_schema(self) -> dict:
        """JSON Schema for tool input."""
        return {
            "type": "object",
            "properties": {
                "target_dir": {
                    "type": "string",
                    "description": "Path to the directory to index"
                },
                "max_depth": {
                    "type": "integer",
                    "description": "Maximum depth for indexing (default: 10)",
                    "default": 10
                }
            },
            "required": ["target_dir"]
        }

    async def execute(self, target_dir: str, max_depth: int = 10) -> IndexingResult:
        """Execute context indexing on target directory."""
        if self._script_path is None:
            return IndexingResult(
                status="error",
                node_index_path=None,
                role_evidence_path=None,
                message="cof-glob-indexing script not found",
                raw_output=""
            )

        target_path = Path(target_dir).resolve()
        if not target_path.exists():
            return IndexingResult(
                status="error",
                node_index_path=None,
                role_evidence_path=None,
                message=f"Target directory does not exist: {target_dir}",
                raw_output=""
            )

        try:
            result = subprocess.run(
                [
                    "python3",
                    str(self._script_path),
                    "--target-dir", str(target_path),
                    "--max-depth", str(max_depth),
                ],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                try:
                    output = json.loads(result.stdout)
                    return IndexingResult(
                        status=output.get("status", "success"),
                        node_index_path=output.get("artifacts", {}).get("node_index"),
                        role_evidence_path=output.get("artifacts", {}).get("role_evidence"),
                        message="Indexing completed successfully",
                        raw_output=result.stdout
                    )
                except json.JSONDecodeError:
                    return IndexingResult(
                        status="partial",
                        node_index_path=None,
                        role_evidence_path=None,
                        message="Indexing completed but output was not valid JSON",
                        raw_output=result.stdout
                    )
            else:
                return IndexingResult(
                    status="error",
                    node_index_path=None,
                    role_evidence_path=None,
                    message=f"Indexing failed with exit code {result.returncode}",
                    raw_output=result.stderr or result.stdout
                )

        except subprocess.TimeoutExpired:
            return IndexingResult(
                status="error",
                node_index_path=None,
                role_evidence_path=None,
                message="Indexing timed out after 60 seconds",
                raw_output=""
            )
        except Exception as e:
            return IndexingResult(
                status="error",
                node_index_path=None,
                role_evidence_path=None,
                message=f"Unexpected error: {str(e)}",
                raw_output=""
            )
