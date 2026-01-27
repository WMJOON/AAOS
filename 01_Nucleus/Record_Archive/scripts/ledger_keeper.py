#!/usr/bin/env python3
import os
import sys
import hashlib
import datetime
import re

# Consts
ARCHIVE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEXES_DIR = os.path.join(ARCHIVE_ROOT, 'indexes')
HASH_LEDGER_PATH = os.path.join(INDEXES_DIR, 'HASH_LEDGER.md')
ARCHIVE_INDEX_PATH = os.path.join(INDEXES_DIR, 'ARCHIVE_INDEX.md')

def utc_now_iso():
    # datetime.utcnow() is deprecated in Python 3.12+
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def get_last_ledger_entry():
    if not os.path.exists(HASH_LEDGER_PATH):
        return None, "GENESIS"

    # Parse YAML frontmatter-like blocks outside code fences.
    # HASH_LEDGER.md contains example YAML in fenced code blocks; those must be ignored.
    in_code_fence = False
    current_block_lines = None
    candidate_blocks = []

    with open(HASH_LEDGER_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.rstrip("\n")

            if stripped.startswith("```"):
                in_code_fence = not in_code_fence
                continue

            if in_code_fence:
                continue

            if stripped == "---":
                if current_block_lines is None:
                    current_block_lines = []
                else:
                    block = "\n".join(current_block_lines)
                    current_block_lines = None

                    if (
                        "package_path:" in block
                        and "artifact:" in block
                        and "prev_hash:" in block
                        and re.search(r'^\s*hash:\s*"', block, re.MULTILINE)
                    ):
                        candidate_blocks.append(block)
                continue

            if current_block_lines is not None:
                current_block_lines.append(stripped)

    if not candidate_blocks:
        return None, "GENESIS"

    last_block = candidate_blocks[-1]
    hash_match = re.search(r'^\s*hash:\s*"([^"]+)"', last_block, re.MULTILINE)
    if hash_match:
        return last_block, hash_match.group(1)

    return last_block, "GENESIS"

def create_ledger_entry(package_rel_path, manifest_hash, prev_hash, notes=""):
    # Ledger definition:
    # - `hash` is the sha256 of (prev_hash + MANIFEST.sha256 content).
    # - `prev_hash` links to the previous entry's `hash` (append-only chain).
    #
    # The chain integrity comes from hashing the previous hash into the current one.
    chain_input = f"{prev_hash}{manifest_hash}".encode('utf-8')
    new_hash = hashlib.sha256(chain_input).hexdigest()

    timestamp = utc_now_iso()
    
    entry = f"""
---
timestamp: "{timestamp}"
package_path: "{package_rel_path}"
artifact: "MANIFEST.sha256"
prev_hash: "{prev_hash}"
hash: "{new_hash}"
notes: "{notes}"
---
"""
    return entry, new_hash

def main():
    if len(sys.argv) < 2:
        print("Usage: python ledger_keeper.py <path_to_package_folder> [notes] [--dry-run]")
        sys.exit(1)
        
    package_path = sys.argv[1]
    args = sys.argv[2:]
    dry_run = False
    if "--dry-run" in args:
        dry_run = True
        args = [a for a in args if a != "--dry-run"]
    notes = " ".join(args).strip()
    
    if not os.path.isdir(package_path):
        print(f"Error: {package_path} is not a directory")
        sys.exit(1)
        
    manifest_path = os.path.join(package_path, "MANIFEST.sha256")
    if not os.path.exists(manifest_path):
        print(f"Error: MANIFEST.sha256 not found in {package_path}")
        sys.exit(1)
        
    # Get relative path for recording
    abs_package_path = os.path.abspath(package_path)
    rel_package_path = os.path.relpath(abs_package_path, ARCHIVE_ROOT)
    # Ensure it starts with _archive/
    if not rel_package_path.startswith("_archive/"):
         print(f"Error: Package must be inside _archive/ folder. Got: {rel_package_path}")
         sys.exit(1)
    # Normalize to a directory-like path.
    if not rel_package_path.endswith("/"):
        rel_package_path += "/"

    print(f"Processing package: {rel_package_path}")
    
    # 1. Calculate Manifest Hash
    manifest_hash = calculate_sha256(manifest_path)
    print(f"Manifest SHA256: {manifest_hash}")
    
    # 2. Get Previous Hash
    _, prev_hash = get_last_ledger_entry()
    print(f"Previous Ledger Hash: {prev_hash}")
    
    # 3. Create New Entry
    entry_str, new_hash = create_ledger_entry(rel_package_path, manifest_hash, prev_hash, notes)
    
    # 4. Append to Ledger
    if dry_run:
        print("[Dry Run] No changes written to HASH_LEDGER.md")
    else:
        with open(HASH_LEDGER_PATH, 'a', encoding='utf-8') as f:
            f.write(entry_str)

        print(f"Successfully appended to HASH_LEDGER.md")
        print(f"New Ledger Hash: {new_hash}")
    
    # 5. Suggest ARCHIVE_INDEX update (or automate it if we had robust parsing, but for now just print)
    print("\n[Action Required] Please ensure ARCHIVE_INDEX.md is updated. Here is a snippet:")
    print(f"""
---
timestamp: "{utc_now_iso()}"
package_path: "{rel_package_path}"
type: "auto-recorded"
targets: []
summary: "{notes}"
manifest_sha256: "{manifest_hash}"
---
""")

if __name__ == "__main__":
    main()
