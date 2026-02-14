"""
AAOS Audit Log - 무결성 보장 버전

기능:
1. Append-only 로깅
2. 해시 체인으로 변조 감지
3. 무결성 검증 함수 제공

각 엔트리는 이전 엔트리의 해시를 포함하여 간이 블록체인 구조를 형성한다.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def utc_now_iso() -> str:
    """현재 UTC 시간을 ISO 형식으로 반환"""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def compute_entry_hash(entry: Dict[str, Any], prev_hash: str = "") -> str:
    """
    엔트리의 해시 계산

    Args:
        entry: 해시할 엔트리 데이터
        prev_hash: 이전 엔트리의 해시 (체인 연결용)

    Returns:
        SHA-256 해시 (16진수 문자열, 앞 16자리만)
    """
    # 결정적 직렬화를 위해 키 정렬
    canonical = json.dumps(entry, sort_keys=True, ensure_ascii=False)
    combined = f"{prev_hash}|{canonical}"
    full_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    return full_hash[:16]  # 짧은 해시 사용 (가독성)


def get_last_entry_hash(audit_path: Path) -> str:
    """
    마지막 엔트리의 해시 추출

    Returns:
        마지막 해시, 없으면 "GENESIS"
    """
    if not audit_path.exists():
        return "GENESIS"

    text = audit_path.read_text(encoding="utf-8")

    # 모든 hash 필드 추출
    hash_pattern = re.compile(r'^hash:\s*"?([a-f0-9]+)"?\s*$', re.MULTILINE)
    matches = list(hash_pattern.finditer(text))

    if matches:
        return matches[-1].group(1)

    return "GENESIS"


def append_audit_entry(audit_path: Path, entry: Dict[str, Any]) -> str:
    """
    Audit Log에 새 엔트리 추가 (해시 체인 포함)

    Args:
        audit_path: Audit Log 파일 경로
        entry: 추가할 엔트리 데이터

    Returns:
        생성된 엔트리의 해시
    """
    audit_path.parent.mkdir(parents=True, exist_ok=True)

    # 이전 해시 가져오기
    prev_hash = get_last_entry_hash(audit_path)

    # 엔트리 데이터 정규화
    timestamp = entry.get("timestamp", utc_now_iso())
    entry_type = entry.get("type", "unknown")
    target = entry.get("target", "")
    result = entry.get("result", "unknown")
    reasons: List[str] = entry.get("reasons", [])
    notes = entry.get("notes", "")

    # 해시 계산용 정규화된 엔트리
    hash_entry = {
        "timestamp": timestamp,
        "type": entry_type,
        "target": target,
        "result": result,
        "reasons": reasons,
        "notes": notes,
        "prev_hash": prev_hash
    }
    current_hash = compute_entry_hash(hash_entry, prev_hash)

    # YAML frontmatter 형식으로 작성
    frontmatter_lines = [
        "---",
        f'timestamp: "{timestamp}"',
        f"type: {entry_type}",
        f'target: "{target}"',
        f"result: {result}",
        "reasons:",
    ]
    for r in reasons:
        # 따옴표 이스케이프
        escaped = r.replace('"', '\\"')
        frontmatter_lines.append(f'  - "{escaped}"')
    if notes:
        escaped_notes = notes.replace('"', '\\"')
        frontmatter_lines.append(f'notes: "{escaped_notes}"')

    # 해시 체인 정보 추가
    frontmatter_lines.append(f'prev_hash: "{prev_hash}"')
    frontmatter_lines.append(f'hash: "{current_hash}"')
    frontmatter_lines.append("---")

    block = "\n".join(frontmatter_lines) + "\n\n"

    with audit_path.open("a", encoding="utf-8") as f:
        f.write(block)

    return current_hash


def safe_append_audit_entry(
    audit_path: Path,
    entry: Dict[str, Any],
    *,
    require_integrity: bool = True
) -> str:
    """
    Audit log 무결성 검증 후 append.

    - require_integrity=True 이고 기존 로그가 손상된 경우, append를 거부한다.
    - require_integrity=False 이면 기존 로그 상태와 무관하게 append한다(복구/포렌식 용도).
    """
    if require_integrity and audit_path.exists():
        ok, errors = verify_audit_integrity(audit_path)
        if not ok:
            error_text = "; ".join(errors[:5]) + (" ..." if len(errors) > 5 else "")
            raise RuntimeError(f"Audit integrity violation: {error_text}")

    return append_audit_entry(audit_path, entry)


def parse_audit_entries(audit_path: Path) -> List[Dict[str, Any]]:
    """
    Audit Log의 모든 엔트리 파싱

    Returns:
        엔트리 리스트
    """
    if not audit_path.exists():
        return []

    text = audit_path.read_text(encoding="utf-8")
    entries: List[Dict[str, Any]] = []

    # YAML frontmatter 블록 찾기
    pattern = re.compile(r'^---\s*\n(.*?)\n---\s*$', re.MULTILINE | re.DOTALL)

    for match in pattern.finditer(text):
        block = match.group(1)
        entry: Dict[str, Any] = {}

        # 간단한 YAML 파싱
        for line in block.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # key: value 형식
            if ':' in line and not line.startswith('-'):
                key, _, value = line.partition(':')
                key = key.strip()
                value = value.strip().strip('"')

                if key == "reasons":
                    entry["reasons"] = []
                else:
                    entry[key] = value

            # - "item" 형식 (reasons 리스트)
            elif line.startswith('-') and "reasons" in entry:
                item = line[1:].strip().strip('"')
                entry["reasons"].append(item)

        # 문서 frontmatter(예: description) 및 예시 코드블록(frontmatter sample)과 audit entry를 구분한다.
        # 실제 audit entry는 해시체인을 포함해야 한다.
        is_audit_entry = (
            "timestamp" in entry
            and "type" in entry
            and ("hash" in entry or "prev_hash" in entry)
        )
        if entry and is_audit_entry:
            entries.append(entry)

    return entries


def verify_audit_integrity(audit_path: Path) -> Tuple[bool, List[str]]:
    """
    Audit Log의 무결성 검증

    Returns:
        (is_valid, errors)
    """
    entries = parse_audit_entries(audit_path)

    if not entries:
        return True, []

    errors: List[str] = []
    prev_hash = "GENESIS"

    for i, entry in enumerate(entries):
        stored_hash = entry.get("hash", "")
        stored_prev = entry.get("prev_hash", "")

        # prev_hash 체인 검증
        if stored_prev != prev_hash:
            errors.append(
                f"Entry {i+1}: prev_hash mismatch. Expected '{prev_hash}', got '{stored_prev}'"
            )

        # 현재 해시 재계산 및 검증
        hash_entry = {
            "timestamp": entry.get("timestamp", ""),
            "type": entry.get("type", ""),
            "target": entry.get("target", ""),
            "result": entry.get("result", ""),
            "reasons": entry.get("reasons", []),
            "notes": entry.get("notes", ""),
            "prev_hash": stored_prev
        }
        computed = compute_entry_hash(hash_entry, stored_prev)

        if stored_hash and stored_hash != computed:
            errors.append(
                f"Entry {i+1}: hash mismatch. Stored '{stored_hash}', computed '{computed}'"
            )

        # 다음 검증을 위해 현재 해시 저장
        prev_hash = stored_hash or computed

    return len(errors) == 0, errors


def get_audit_statistics(audit_path: Path) -> Dict[str, Any]:
    """
    Audit Log 통계 정보 반환
    """
    entries = parse_audit_entries(audit_path)

    if not entries:
        return {
            "total_entries": 0,
            "types": {},
            "results": {},
            "first_entry": None,
            "last_entry": None,
            "integrity_valid": True
        }

    types: Dict[str, int] = {}
    results: Dict[str, int] = {}

    for entry in entries:
        entry_type = entry.get("type", "unknown")
        types[entry_type] = types.get(entry_type, 0) + 1

        result = entry.get("result", "unknown")
        results[result] = results.get(result, 0) + 1

    is_valid, _ = verify_audit_integrity(audit_path)

    return {
        "total_entries": len(entries),
        "types": types,
        "results": results,
        "first_entry": entries[0].get("timestamp") if entries else None,
        "last_entry": entries[-1].get("timestamp") if entries else None,
        "integrity_valid": is_valid
    }


# CLI 인터페이스
if __name__ == "__main__":
    import sys

    default_audit_path = (
        Path(__file__).resolve().parents[3]
        / "record_archive"
        / "_archive"
        / "audit-log"
        / "AUDIT_LOG.md"
    )

    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  python audit.py verify [audit_log.md]  - Verify integrity (default: {default_audit_path})")
        print(f"  python audit.py stats [audit_log.md]   - Show statistics (default: {default_audit_path})")
        sys.exit(1)

    command = sys.argv[1]
    audit_path = Path(sys.argv[2]) if len(sys.argv) > 2 else default_audit_path

    if command == "verify":
        print(f"🔍 Verifying: {audit_path}")
        is_valid, errors = verify_audit_integrity(audit_path)

        if is_valid:
            print("✅ Audit log integrity verified. No tampering detected.")
        else:
            print("❌ INTEGRITY VIOLATION DETECTED:")
            for error in errors:
                print(f"  - {error}")
        sys.exit(0 if is_valid else 1)

    elif command == "stats":
        print(f"📊 Statistics for: {audit_path}")
        stats = get_audit_statistics(audit_path)

        print(f"\nTotal Entries: {stats['total_entries']}")
        print(f"First Entry: {stats['first_entry']}")
        print(f"Last Entry: {stats['last_entry']}")
        print(f"Integrity Valid: {'✅' if stats['integrity_valid'] else '❌'}")

        print("\nBy Type:")
        for t, count in stats['types'].items():
            print(f"  - {t}: {count}")

        print("\nBy Result:")
        for r, count in stats['results'].items():
            print(f"  - {r}: {count}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
