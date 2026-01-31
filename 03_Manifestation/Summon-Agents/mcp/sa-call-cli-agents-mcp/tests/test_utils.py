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
        (cof_root / "COF_DOCTRINE.md").touch()

        monkeypatch.setenv("COF_ROOT", str(cof_root))

        result = resolve_cof_root()
        assert result == cof_root


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
