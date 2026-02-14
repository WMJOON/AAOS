#!/usr/bin/env python3
"""
Archive completed tasks.

Usage:
    python archive_tasks.py <node_path>
"""

import argparse
import sys
import shutil
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).resolve().parent
SHARED_DIR = SCRIPT_DIR.parent.parent / "_shared"
if str(SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_DIR))

from frontmatter import FrontmatterParseError, split_frontmatter_and_body

def get_ticket_status(content: str) -> str:
    """Extract status from frontmatter."""
    try:
        frontmatter, _ = split_frontmatter_and_body(content)
    except FrontmatterParseError:
        return "unknown"
    status = frontmatter.get("status")
    if status is None:
        return "unknown"
    if isinstance(status, str):
        return status.lower()
    return "unknown"

def archive_tasks(node_path: str) -> bool:
    path = Path(node_path).resolve()
    tickets_dir = path / "tickets"
    archive_dir = path / "archive"
    archive_tickets_dir = archive_dir / "tickets"

    if not tickets_dir.exists():
        print(f"Error: tickets directory not found at {tickets_dir}", file=sys.stderr)
        return False

    # Ensure archive structure
    archive_tickets_dir.mkdir(parents=True, exist_ok=True)
    
    # Init archive README if not exists
    readme_path = archive_dir / "README.md"
    if not readme_path.exists():
        readme_path.write_text("# Archived Tasks\n\n| Date | Ticket | Status |\n|---|---|---|\n", encoding="utf-8")

    archived_count = 0
    
    for ticket_file in tickets_dir.glob("*.md"):
        content = ticket_file.read_text(encoding="utf-8")
        status = get_ticket_status(content)
        
        if status == "done":
            # Move to archive with collision handling
            dest = archive_tickets_dir / ticket_file.name
            if dest.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                new_name = f"{ticket_file.stem}_{timestamp}{ticket_file.suffix}"
                dest = archive_tickets_dir / new_name
                print(f"Collision detected. Renaming to: {new_name}")

            shutil.move(str(ticket_file), str(dest))
            
            # Log to README
            with open(readme_path, "a", encoding="utf-8") as f:
                date_str = datetime.now().strftime("%Y-%m-%d")
                f.write(f"| {date_str} | [{dest.stem}](./tickets/{dest.name}) | {status} |\n")
            
            print(f"Archived: {ticket_file.name}")
            archived_count += 1
            
    if archived_count == 0:
        print("No 'done' tickets found to archive.")
    else:
        print(f"Successfully archived {archived_count} tickets.")
        
    return True

def main():
    parser = argparse.ArgumentParser(description="Archive completed tickets.")
    parser.add_argument("path", help="Path to NN.agents-task-context node (or legacy: task-manager)")
    args = parser.parse_args()
    
    success = archive_tasks(args.path)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
