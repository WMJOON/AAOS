#!/usr/bin/env python3
"""
Bootstrap COF Task Manager Node.
Combines creation and verification in one step to reduce friction.
"""

import argparse
import sys
import subprocess
from pathlib import Path

NODE_DIRNAME = "01.agents-task-context"

def bootstrap_node(target_path: str) -> bool:
    path = Path(target_path).resolve()
    script_dir = Path(__file__).parent.resolve()
    create_script = script_dir / "create_node.py"
    verify_script = script_dir / "verify_node.py"

    print(f"Bootstrapping COF node at: {path}")

    # 1. Create Node
    print("\n[Step 1/2] Creating Structure...")
    try:
        subprocess.run(
            [sys.executable, str(create_script), str(path), "--all"],
            check=True
        )
    except subprocess.CalledProcessError:
        print("Creation failed.")
        return False

    # 2. Verify Node
    print("\n[Step 2/2] Verifying Structure...")
    tm_path = path / NODE_DIRNAME
    try:
        subprocess.run(
            [sys.executable, str(verify_script), str(tm_path)],
            check=True
        )
    except subprocess.CalledProcessError:
        print("Verification failed.")
        return False

    print("\nBootstrap complete. COF node is ready.")
    return True

def main():
    parser = argparse.ArgumentParser(description="Bootstrap COF Node (Create + Verify)")
    parser.add_argument("path", help=f"Target directory for {NODE_DIRNAME}/")
    args = parser.parse_args()
    
    if bootstrap_node(args.path):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
