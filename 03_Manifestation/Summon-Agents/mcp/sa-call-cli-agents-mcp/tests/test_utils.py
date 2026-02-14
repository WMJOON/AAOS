"""Tests for utility functions."""

import pytest
from aaos_mcp.utils.frontmatter import parse_frontmatter, update_frontmatter


class TestFrontmatter:
    """Tests for frontmatter parsing."""

    def test_parse_simple_frontmatter(self):
        """Test parsing simple YAML frontmatter."""
        content = """---
title: Test Ticket
status: todo
priority: P1
---

# Description

This is a test ticket.
"""
        fm, body = parse_frontmatter(content)

        assert fm["title"] == "Test Ticket"
        assert fm["status"] == "todo"
        assert fm["priority"] == "P1"
        assert "# Description" in body

    def test_parse_frontmatter_with_list(self):
        """Test parsing frontmatter with list values."""
        content = """---
title: Test
tags: [security, audit, review]
---

Body content.
"""
        fm, body = parse_frontmatter(content)

        assert fm["tags"] == ["security", "audit", "review"]

    def test_parse_frontmatter_with_boolean(self):
        """Test parsing frontmatter with boolean values."""
        content = """---
active: true
archived: false
---

Body.
"""
        fm, _ = parse_frontmatter(content)

        assert fm["active"] is True
        assert fm["archived"] is False

    def test_parse_no_frontmatter(self):
        """Test parsing content without frontmatter."""
        content = "# Just a header\n\nSome content."
        fm, body = parse_frontmatter(content)

        assert fm == {}
        assert body == content

    def test_update_frontmatter(self):
        """Test updating frontmatter fields."""
        content = """---
status: todo
priority: P2
---

Body content.
"""
        updated = update_frontmatter(content, {"status": "done", "new_field": "value"})

        fm, _ = parse_frontmatter(updated)
        assert fm["status"] == "done"
        assert fm["priority"] == "P2"
        assert fm["new_field"] == "value"


class TestPaths:
    """Tests for path resolution (requires actual COF structure)."""

    def test_resolve_cof_root_from_env(self, monkeypatch, tmp_path):
        """Test COF root resolution from environment variable."""
        from aaos_mcp.utils.paths import resolve_cof_root

        # Create a marker file
        cof_root = tmp_path / "cof"
        cof_root.mkdir()
        (cof_root / "core-docs" / "COF_DOCTRINE.md").parent.mkdir(parents=True, exist_ok=True)
        (cof_root / "core-docs" / "COF_DOCTRINE.md").touch()

        monkeypatch.setenv("COF_ROOT", str(cof_root))

        result = resolve_cof_root()
        assert result == cof_root

    def test_resolve_cof_root_prefers_canonical_under_aaos(self, monkeypatch, tmp_path):
        from aaos_mcp.utils.paths import resolve_cof_root

        aaos_root = tmp_path / "04_Agentic_AI_OS"
        canonical = aaos_root / "02_Swarm" / "context-orchestrated-filesystem"
        canonical.mkdir(parents=True)
        (canonical / "core-docs" / "COF_DOCTRINE.md").parent.mkdir(parents=True, exist_ok=True)
        (canonical / "core-docs" / "COF_DOCTRINE.md").touch()

        start = aaos_root / "03_Manifestation" / "summon-agents"
        start.mkdir(parents=True)

        monkeypatch.delenv("COF_ROOT", raising=False)
        monkeypatch.setenv("AAOS_ROOT", str(aaos_root))

        result = resolve_cof_root(str(start))
        assert result == canonical.resolve()

    def test_resolve_skills_path_falls_back_to_canonical(self, monkeypatch, tmp_path):
        from aaos_mcp.utils.paths import resolve_skills_path

        aaos_root = tmp_path / "04_Agentic_AI_OS"
        canonical = aaos_root / "02_Swarm" / "context-orchestrated-filesystem"
        skills = canonical / "skills"
        skills.mkdir(parents=True)

        wrong_cof = tmp_path / "wrong-cof"
        wrong_cof.mkdir()

        monkeypatch.setenv("AAOS_ROOT", str(aaos_root))
        monkeypatch.delenv("COF_ROOT", raising=False)

        result = resolve_skills_path(wrong_cof)
        assert result == skills.resolve()


def test_strip_api_billing_env():
    from aaos_mcp.jobs import strip_api_billing_env

    env = {
        "OPENAI_API_KEY": "sk-test",
        "ANTHROPIC_API_KEY": "sk-ant-test",
        "KEEP": "1",
    }
    new_env, stripped = strip_api_billing_env(env)
    assert "OPENAI_API_KEY" not in new_env
    assert "ANTHROPIC_API_KEY" not in new_env
    assert new_env["KEEP"] == "1"
    assert set(stripped) == {"OPENAI_API_KEY", "ANTHROPIC_API_KEY"}


def test_job_id_validation_is_hex32():
    import re
    from aaos_mcp.jobs import new_job_id

    jid = new_job_id()
    assert re.fullmatch(r"[0-9a-f]{32}", jid)


def test_task_solver_input_validation():
    from aaos_mcp.tools.task_solver import TaskSolverTool

    assert TaskSolverTool._validate_inputs("codex", 300, 10, "subscription_only") is None
    assert "Invalid provider" in TaskSolverTool._validate_inputs("bad", 300, 10, "subscription_only")
    assert "timeout must be between" in TaskSolverTool._validate_inputs("codex", 0, 10, "subscription_only")
    assert "context_depth must be between" in TaskSolverTool._validate_inputs("codex", 300, 0, "subscription_only")
    assert "Invalid billing_mode" in TaskSolverTool._validate_inputs("codex", 300, 10, "bad")
