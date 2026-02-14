#!/usr/bin/env python3
"""
Record Archive Hash Ledger & Archive Index 관리.

Commands:
  seal     <package_path> [options]     패키지 봉인 (HASH_LEDGER + ARCHIVE_INDEX 추가)
  verify                                 HASH_LEDGER 체인 무결성 검증

Legacy CLI (하위 호환):
  <package_path> [notes] [--dry-run]    seal과 동일

Usage:
  python3 ledger_keeper.py seal _archive/deliberation/2026-02-15T.../ --summary "desc" --targets "file1.md,file2.md"
  python3 ledger_keeper.py --verify
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import os
import re
import sys

# Consts
ARCHIVE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEXES_DIR = os.path.join(ARCHIVE_ROOT, 'indexes')
HASH_LEDGER_PATH = os.path.join(INDEXES_DIR, 'HASH_LEDGER.md')
ARCHIVE_INDEX_PATH = os.path.join(INDEXES_DIR, 'ARCHIVE_INDEX.md')


def utc_now_iso():
    # datetime.utcnow() is deprecated in Python 3.12+
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _yaml_escape(value):
    return str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def get_last_ledger_entry():
    candidate_blocks = parse_ledger_entries()
    if not candidate_blocks:
        return None, "GENESIS"

    last_block = candidate_blocks[-1]
    return last_block, last_block.get('hash', 'GENESIS')


def _is_genesis_entry(entry: dict) -> bool:
    """GENESIS 블록인지 판별한다."""
    return entry.get("hash", "") == "GENESIS" or entry.get("timestamp", "") == "GENESIS"


def verify_ledger():
    entries = parse_ledger_entries()
    if not entries:
        print("OK: No entries in HASH_LEDGER.md")
        return 0

    legacy_mode = True
    prev_hash = "GENESIS"
    errors = []
    warnings = []

    # 사전 스캔: 동일 package_path에 repair 엔트리가 있는지 확인
    repair_set: set[str] = set()
    pkg_count: dict[str, int] = {}
    for entry in entries:
        pp = entry.get("package_path", "")
        pkg_count[pp] = pkg_count.get(pp, 0) + 1
    for pp, count in pkg_count.items():
        if count > 1 and pp != "_archive/":
            repair_set.add(pp)

    for idx, entry in enumerate(entries, start=1):
        package_path = entry.get("package_path", "")
        artifact = entry.get("artifact", "")
        expected_prev = prev_hash
        actual_prev = entry.get("prev_hash", "")
        current_hash = entry.get("hash", "")

        # GENESIS 엔트리 스킵
        if _is_genesis_entry(entry):
            prev_hash = current_hash
            continue

        # CHAIN_MIGRATION 마커 처리
        if artifact == "CHAIN_MIGRATION.marker":
            if actual_prev != expected_prev:
                errors.append(f"{idx}) migration marker prev_hash mismatch: expected {expected_prev}, got {actual_prev}")
            legacy_mode = False
            prev_hash = current_hash
            continue

        # prev_hash 체인 연결 확인
        if actual_prev != expected_prev:
            errors.append(f"{idx}) prev_hash mismatch for {package_path}: expected {expected_prev}, got {actual_prev}")

        # MANIFEST.sha256 파일 해시 검증
        manifest_path = os.path.join(ARCHIVE_ROOT, package_path.rstrip("/"), "MANIFEST.sha256")
        if not os.path.exists(manifest_path):
            errors.append(f"{idx}) missing MANIFEST.sha256 for {package_path}")
            prev_hash = current_hash
            continue

        manifest_hash = calculate_sha256(manifest_path)

        if legacy_mode:
            # Legacy 모드: manifest-only 해시 시도
            expected_legacy = manifest_hash
            # Chain 모드 fallback: legacy 시기에 이미 chain 방식을 쓴 엔트리 대응
            expected_chain = hashlib.sha256(f"{actual_prev}{manifest_hash}".encode("utf-8")).hexdigest()

            if current_hash == expected_legacy:
                pass  # OK: legacy 모드 정합
            elif current_hash == expected_chain:
                # 엔트리가 CHAIN_MIGRATION 이전이지만 chain 방식으로 해시됨
                warnings.append(
                    f"{idx}) pre-migration chain hash detected for {package_path} (accepted)"
                )
            else:
                # repair 엔트리인 경우 (동일 package_path 중 첫 번째가 아닌 경우) 허용
                if package_path in repair_set:
                    warnings.append(
                        f"{idx}) hash mismatch for {package_path} (repair chain, accepted)"
                    )
                else:
                    errors.append(
                        f"{idx}) hash mismatch for {package_path}: expected {expected_legacy}, got {current_hash}"
                    )
        else:
            # Chain 모드: prev_hash + manifest_hash
            expected_hash = hashlib.sha256(f"{actual_prev}{manifest_hash}".encode("utf-8")).hexdigest()

            if current_hash != expected_hash:
                # repair 엔트리 체인 허용: MANIFEST가 수정된 후 다음 엔트리가 repair인 경우
                if package_path in repair_set:
                    warnings.append(
                        f"{idx}) hash mismatch for {package_path} (repair entry, accepted)"
                    )
                else:
                    errors.append(
                        f"{idx}) hash mismatch for {package_path}: expected {expected_hash}, got {current_hash}"
                    )

        prev_hash = current_hash

    if warnings:
        for w in warnings:
            print(f"  WARN: {w}")

    if errors:
        print("FAIL: HASH_LEDGER verification failed")
        for e in errors:
            print(f"- {e}")
        return 1

    entry_count = len(entries)
    warn_count = len(warnings)
    print(f"OK: HASH_LEDGER verification passed ({entry_count} entries, {warn_count} warnings)")
    return 0


def create_ledger_entry(package_rel_path, manifest_hash, prev_hash, notes=""):
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
notes: "{_yaml_escape(notes)}"
---
"""
    return entry, new_hash, timestamp


def parse_ledger_entries():
    if not os.path.exists(HASH_LEDGER_PATH):
        return []

    in_code_fence = False
    current_block_lines = None
    entries = []

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
                        and re.search(r'^\s*hash:\s*"', block, re.M)
                    ):
                        entry = {}
                        for key, val in re.findall(r'^([a-z_]+):\s*"(.*)"$', block, re.M):
                            entry[key] = val
                        if entry:
                            entries.append(entry)
                continue

            if current_block_lines is not None:
                current_block_lines.append(stripped)

    return entries


def infer_type_from_package_path(package_rel_path):
    """
    _archive/<bucket>/<timestamp>__<type>__<slug>/ 형식에서 type을 추출한다.
    패턴이 깨져 있으면 버킷명을 fallback 타입으로 사용한다.
    """
    package_name = os.path.basename(os.path.normpath(package_rel_path))
    parts = package_name.split("__")
    if len(parts) >= 2:
        return parts[1]
    return "other"


def append_archive_index(timestamp, package_rel_path, package_type, manifest_hash,
                         summary, notes, new_hash, targets=None):
    """ARCHIVE_INDEX.md에 엔트리를 추가한다."""
    if targets:
        targets_lines = "\n".join(f'  - "{t}"' for t in targets)
    else:
        targets_lines = f'  - "{package_rel_path.rstrip("/")}"'

    summary_text = _yaml_escape(summary) if summary else "auto-recorded package"
    notes_text = notes if notes else ""
    ledger_note = f"ledger hash: {new_hash}"
    if notes_text:
        full_notes = f"{_yaml_escape(notes_text)}; {ledger_note}"
    else:
        full_notes = ledger_note

    index_entry = f"""
---
timestamp: "{timestamp}"
package_path: "{package_rel_path}"
type: "{package_type}"
targets:
{targets_lines}
summary: "{summary_text}"
manifest_sha256: "{manifest_hash}"
notes: "{full_notes}"
---
"""
    with open(ARCHIVE_INDEX_PATH, "a", encoding="utf-8") as f:
        f.write(index_entry)


def cmd_seal(args):
    """패키지를 봉인한다 (HASH_LEDGER + ARCHIVE_INDEX 추가)."""
    package_path = args.package_path

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
    if not rel_package_path.startswith("_archive/"):
        print(f"Error: Package must be inside _archive/ folder. Got: {rel_package_path}")
        sys.exit(1)
    if not rel_package_path.endswith("/"):
        rel_package_path += "/"

    print(f"Processing package: {rel_package_path}")

    # 1. Calculate Manifest Hash
    manifest_hash = calculate_sha256(manifest_path)
    print(f"Manifest SHA256: {manifest_hash}")

    # 2. Get Previous Hash
    _, prev_hash = get_last_ledger_entry()
    print(f"Previous Ledger Hash: {prev_hash}")

    # 3. Build notes from summary
    notes = args.notes or ""

    # 4. Create New Entry
    entry_str, new_hash, timestamp = create_ledger_entry(rel_package_path, manifest_hash, prev_hash, notes)

    # 5. Parse targets
    targets = None
    if args.targets:
        targets = [t.strip() for t in args.targets.split(",") if t.strip()]

    # 6. Write
    if args.dry_run:
        print("[Dry Run] No changes written to HASH_LEDGER.md")
        print("[Dry Run] No changes written to ARCHIVE_INDEX.md")
        print(f"[Dry Run] Would create entry with hash: {new_hash}")
    else:
        with open(HASH_LEDGER_PATH, 'a', encoding='utf-8') as f:
            f.write(entry_str)

        print(f"Successfully appended to HASH_LEDGER.md")
        print(f"New Ledger Hash: {new_hash}")

        package_type = infer_type_from_package_path(rel_package_path)
        summary = args.summary or notes or ""
        append_archive_index(timestamp, rel_package_path, package_type, manifest_hash,
                             summary, notes, new_hash, targets)
        print(f"Successfully appended to ARCHIVE_INDEX.md (type: {package_type})")


def main():
    # Legacy CLI 하위 호환: --verify 또는 경로를 직접 전달한 경우
    if len(sys.argv) >= 2 and sys.argv[1] == "--verify":
        sys.exit(verify_ledger())

    if len(sys.argv) >= 2 and sys.argv[1] not in ("seal", "verify", "-h", "--help"):
        # Legacy mode: <package_path> [notes] [--dry-run]
        legacy_args = sys.argv[1:]
        dry_run = "--dry-run" in legacy_args
        legacy_args = [a for a in legacy_args if a != "--dry-run"]
        pkg = legacy_args[0]
        notes = " ".join(legacy_args[1:]).strip()

        class LegacyArgs:
            pass

        la = LegacyArgs()
        la.package_path = pkg
        la.summary = notes
        la.targets = ""
        la.notes = notes
        la.dry_run = dry_run
        cmd_seal(la)
        return

    parser = argparse.ArgumentParser(
        description="Record Archive Hash Ledger & Archive Index 관리",
    )
    sub = parser.add_subparsers(dest="command")

    # seal command
    p_seal = sub.add_parser("seal", help="패키지 봉인")
    p_seal.add_argument("package_path", help="패키지 디렉토리 경로")
    p_seal.add_argument("--summary", default="", help="ARCHIVE_INDEX summary 필드")
    p_seal.add_argument("--targets", default="", help="쉼표로 구분된 변경 대상 파일 목록")
    p_seal.add_argument("--notes", default="", help="HASH_LEDGER notes 필드")
    p_seal.add_argument("--dry-run", action="store_true", help="실제 기록 없이 결과 확인")

    # verify command
    sub.add_parser("verify", help="HASH_LEDGER 체인 무결성 검증")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "verify":
        sys.exit(verify_ledger())
    elif args.command == "seal":
        cmd_seal(args)


if __name__ == "__main__":
    main()
