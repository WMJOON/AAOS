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
    
    with open(HASH_LEDGER_PATH, 'r') as f:
        content = f.read()
    
    # Find all yaml blocks
    blocks = re.findall(r'---\n(.*?)\n---', content, re.DOTALL)
    if not blocks:
        return None, "GENESIS"
    
    last_block = blocks[-1]
    hash_match = re.search(r'hash:\s*"([^"]+)"', last_block)
    if hash_match:
        return last_block, hash_match.group(1)
    
    return last_block, "GENESIS"

def create_ledger_entry(package_rel_path, manifest_hash, prev_hash, notes=""):
    # Ledger definition:
    # - `hash` is the sha256 of the MANIFEST.sha256 file itself.
    # - `prev_hash` links to the previous entry's `hash` (append-only chain).
    #
    # The chain integrity comes from (prev_hash -> hash) linkage and periodic
    # full verification (re-hashing MANIFEST.sha256 per entry), not from hashing
    # prev_hash into a derived chain hash.
    new_hash = manifest_hash

    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
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
        print("Usage: python ledger_keeper.py <path_to_package_folder> [notes]")
        sys.exit(1)
        
    package_path = sys.argv[1]
    notes = sys.argv[2] if len(sys.argv) > 2 else ""
    
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
    with open(HASH_LEDGER_PATH, 'a') as f:
        f.write(entry_str)
    
    print(f"Successfully appended to HASH_LEDGER.md")
    print(f"New Ledger Hash: {new_hash}")
    
    # 5. Suggest ARCHIVE_INDEX update (or automate it if we had robust parsing, but for now just print)
    print("\n[Action Required] Please ensure ARCHIVE_INDEX.md is updated. Here is a snippet:")
    print(f"""
---
timestamp: "{datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}"
package_path: "{rel_package_path}"
type: "auto-recorded"
targets: []
summary: "{notes}"
manifest_sha256: "{manifest_hash}"
---
""")

if __name__ == "__main__":
    main()
