"""YAML frontmatter parsing utilities."""

import re
from typing import Any


def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from markdown content.

    Returns:
        Tuple of (frontmatter_dict, body_content)
    """
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return {}, content

    yaml_str, body = match.groups()
    frontmatter = _parse_simple_yaml(yaml_str)
    return frontmatter, body


def _parse_simple_yaml(yaml_str: str) -> dict[str, Any]:
    """Simple YAML parser for frontmatter (no external dependencies)."""
    result = {}
    current_key = None
    current_indent = 0

    for line in yaml_str.split('\n'):
        if not line.strip() or line.strip().startswith('#'):
            continue

        # Check indentation
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if ':' in stripped:
            key, _, value = stripped.partition(':')
            key = key.strip()
            value = value.strip()

            if value:
                # Remove quotes
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                # Handle lists in single line [a, b, c]
                elif value.startswith('[') and value.endswith(']'):
                    items = value[1:-1].split(',')
                    value = [item.strip().strip('"').strip("'") for item in items if item.strip()]
                # Handle booleans
                elif value.lower() in ('true', 'yes'):
                    value = True
                elif value.lower() in ('false', 'no'):
                    value = False
                # Handle numbers
                elif value.isdigit():
                    value = int(value)
                elif re.match(r'^-?\d+\.?\d*$', value):
                    value = float(value)

                result[key] = value
            else:
                result[key] = {}
                current_key = key
                current_indent = indent

    return result


def update_frontmatter(content: str, updates: dict[str, Any]) -> str:
    """Update frontmatter fields in markdown content."""
    frontmatter, body = parse_frontmatter(content)
    frontmatter.update(updates)

    # Rebuild YAML
    yaml_lines = ['---']
    for key, value in frontmatter.items():
        if isinstance(value, list):
            yaml_lines.append(f'{key}: [{", ".join(str(v) for v in value)}]')
        elif isinstance(value, bool):
            yaml_lines.append(f'{key}: {"true" if value else "false"}')
        elif isinstance(value, dict):
            yaml_lines.append(f'{key}:')
            for k, v in value.items():
                yaml_lines.append(f'  {k}: {v}')
        else:
            yaml_lines.append(f'{key}: {value}')
    yaml_lines.append('---')

    return '\n'.join(yaml_lines) + '\n' + body
