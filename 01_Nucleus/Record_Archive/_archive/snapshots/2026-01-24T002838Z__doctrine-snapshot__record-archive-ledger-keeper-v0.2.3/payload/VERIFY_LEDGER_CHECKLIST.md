---
description: Hash Ledger 무결성 검증 체크리스트. 패키지 추가 시 또는 정기 감사 시 사용.
---
# Hash Ledger 검증 체크리스트

## 목적

`indexes/HASH_LEDGER.md`의 체인 무결성을 수동/반자동으로 검증한다.
Append-only 원칙이 실제로 지켜지고 있는지 확인한다.

---

## 패키지 추가 시 검증 (MUST)

새 패키지를 `_archive/`에 추가할 때 반드시 수행:

### Step 1: 최신 엔트리의 hash 확인

```bash
# HASH_LEDGER.md의 마지막 엔트리에서 hash 값 추출
tail -20 indexes/HASH_LEDGER.md | grep "^hash:"
```

**체크**: 이 값이 새 엔트리의 `prev_hash`가 되어야 함

### Step 2: MANIFEST.sha256 해시 계산

```bash
# 새 패키지의 MANIFEST.sha256 파일 해시 계산
shasum -a 256 _archive/<bucket>/<package>/MANIFEST.sha256
```

**체크**: 이 값이 새 엔트리의 `hash`가 되어야 함

### Step 3: prev_hash 연결 확인

- [ ] 새 엔트리의 `prev_hash` == 직전 엔트리의 `hash`
- [ ] 새 엔트리의 `hash` == 방금 계산한 MANIFEST.sha256 해시
- [ ] (권장) 새 엔트리의 `timestamp` >= 직전 엔트리의 `timestamp` (다중 에이전트/클럭 차이를 고려해 불일치 시 “분쟁”으로 분류)

---

## 정기 감사 검증 (SHOULD)

월 1회 또는 상위기관 변경 게이트 통과 후 권장:

### Full Chain Verification

```bash
#!/bin/bash
# verify_hash_chain.sh (pseudo-code)

LEDGER="indexes/HASH_LEDGER.md"
PREV="GENESIS"
ERROR=0

# 각 엔트리를 순회하며 체인 검증
while read -r entry; do
  ENTRY_PREV=$(echo "$entry" | grep "prev_hash:" | cut -d'"' -f2)
  ENTRY_HASH=$(echo "$entry" | grep "^hash:" | cut -d'"' -f2)
  PKG_PATH=$(echo "$entry" | grep "package_path:" | cut -d'"' -f2)

  # prev_hash 연결 확인
  if [ "$ENTRY_PREV" != "$PREV" ]; then
    echo "ERROR: Chain break at $PKG_PATH"
    echo "  Expected prev_hash: $PREV"
    echo "  Actual prev_hash: $ENTRY_PREV"
    ERROR=1
  fi

  # MANIFEST.sha256 실제 해시 확인 (GENESIS 제외)
  if [ "$ENTRY_HASH" != "GENESIS" ]; then
    ACTUAL=$(shasum -a 256 "$PKG_PATH/MANIFEST.sha256" | cut -d' ' -f1)
    if [ "$ACTUAL" != "$ENTRY_HASH" ]; then
      echo "ERROR: Hash mismatch at $PKG_PATH"
      echo "  Ledger hash: $ENTRY_HASH"
      echo "  Actual hash: $ACTUAL"
      ERROR=1
    fi
  fi

  PREV="$ENTRY_HASH"
done < <(parse_yaml_entries "$LEDGER")

if [ $ERROR -eq 0 ]; then
  echo "OK: Hash chain verified"
fi
```

### 검증 결과 기록

감사 결과는 `_archive/audit-log/`에 패키지로 보존:

```yaml
type: "audit-snapshot"
subject: "hash-ledger-verification"
result: "pass | fail"
entries_checked: <N>
chain_breaks: <list or empty>
hash_mismatches: <list or empty>
```

---

## 체인 파손 시 대응 (on_conflict)

1. **즉시 중단**: 추가 패키지 생성 금지
2. **Immune System 보고**: `02_AAOS-Immune_system/AUDIT_LOG.md`에 incident 기록
3. **분쟁 패키지 격리**: 문제 패키지를 `_archive/disputed/`로 이동 (신규 버킷)
4. **META Doctrine 귀속**: 판정 요청

---

## 자동화 권장 사항

| 도구 | 용도 | 우선순위 |
|------|------|----------|
| pre-commit hook | 패키지 추가 시 prev_hash 자동 검증 | 높음 |
| CI/CD script | 정기 full chain verification | 중간 |
| Obsidian plugin | Vault 내 해시 계산 보조 | 낮음 |
