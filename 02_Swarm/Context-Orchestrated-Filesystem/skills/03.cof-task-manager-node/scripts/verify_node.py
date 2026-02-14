#!/usr/bin/env python3
"""
agents-task-context 노드 구조 검증 스크립트 (legacy: task-manager/)

Usage:
    python verify_node.py <node_path>
"""

import argparse
import sys
import re
from pathlib import Path

NODE_NAME_PATTERN = re.compile(r"^\d{2}\.agents-task-context$")
LEGACY_NODE_NAME = "task-manager"

REQUIRED_STRUCTURE = {
    "dirs": ["tickets"],
    "files": ["RULE.md", "troubleshooting.md"]
}

OPTIONAL_STRUCTURE = {
    "issue_notes": {
        "files": ["RULE.md"]
    },
    "release_notes": {
        "files": ["RULE.md"]
    }
}


def verify_task_manager_node(node_path: str) -> dict:
    """
    agents-task-context 노드 구조 검증

    Returns:
        dict: {"valid": bool, "missing": list, "warnings": list, "found": list}
    """
    result = {
        "valid": False,
        "missing": [],
        "warnings": [],
        "found": []
    }

    path = Path(node_path).resolve()

    # 경로 존재 확인
    if not path.exists():
        result["missing"].append(f"Node path does not exist: {path}")
        return result

    if not path.is_dir():
        result["missing"].append(f"Node path is not a directory: {path}")
        return result

    # 이름 확인 (권장: NN.agents-task-context/)
    if path.name == LEGACY_NODE_NAME:
        result["warnings"].append(
            f"Legacy node name detected: '{LEGACY_NODE_NAME}/' (recommended: 'NN.agents-task-context/')."
        )
    elif not NODE_NAME_PATTERN.match(path.name):
        result["warnings"].append(
            f"Expected 'NN.agents-task-context/', found '{path.name}/'."
        )

    # 필수 디렉토리 확인
    for dir_name in REQUIRED_STRUCTURE["dirs"]:
        dir_path = path / dir_name
        if dir_path.exists() and dir_path.is_dir():
            result["found"].append(f"{dir_name}/")
        else:
            result["missing"].append(f"{dir_name}/")

    # 필수 파일 확인
    for file_name in REQUIRED_STRUCTURE["files"]:
        file_path = path / file_name
        if file_path.exists() and file_path.is_file():
            result["found"].append(file_name)
        else:
            result["missing"].append(file_name)

    # 선택적 구조 확인
    for opt_dir, spec in OPTIONAL_STRUCTURE.items():
        opt_path = path / opt_dir
        if opt_path.exists():
            result["found"].append(f"{opt_dir}/ (optional)")
            for file_name in spec.get("files", []):
                file_path = opt_path / file_name
                if file_path.exists():
                    result["found"].append(f"{opt_dir}/{file_name}")
                else:
                    result["warnings"].append(f"{opt_dir}/{file_name} missing")

    # 유효성 판단
    result["valid"] = len(result["missing"]) == 0

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Verify agents-task-context node structure (NN.agents-task-context/)"
    )
    parser.add_argument(
        "node_path",
        help="Path to NN.agents-task-context/ (or legacy: task-manager/) directory"
    )

    args = parser.parse_args()
    result = verify_task_manager_node(args.node_path)

    if result["valid"]:
        print("OK: Valid node")
    else:
        print("INVALID: Missing required items", file=sys.stderr)

    if result["found"]:
        print("\nFound:")
        for item in result["found"]:
            print(f"  [+] {item}")

    if result["missing"]:
        print("\nMissing:")
        for item in result["missing"]:
            print(f"  [-] {item}")

    if result["warnings"]:
        print("\nWarnings:")
        for item in result["warnings"]:
            print(f"  [!] {item}")

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
