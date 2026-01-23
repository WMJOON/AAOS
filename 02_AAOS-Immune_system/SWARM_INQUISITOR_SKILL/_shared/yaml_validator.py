#!/usr/bin/env python3
"""
YAML Validator for AAOS Immune System

실제 YAML 파싱을 수행하여 값의 존재와 유효성을 검증한다.
기존 frontmatter.py의 regex 기반 검증을 대체/보완한다.

Dependencies:
  pip install pyyaml (optional, graceful fallback to regex if unavailable)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# PyYAML graceful import
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


class ValidationError:
    """검증 실패 항목"""
    def __init__(self, key: str, reason: str, severity: str = "error"):
        self.key = key
        self.reason = reason
        self.severity = severity  # "error" | "warning"

    def __repr__(self) -> str:
        return f"[{self.severity.upper()}] {self.key}: {self.reason}"


class YAMLValidator:
    """YAML frontmatter 검증기"""

    def __init__(self, text: str):
        self.raw_text = text
        self.frontmatter_raw: Optional[str] = None
        self.data: Optional[Dict[str, Any]] = None
        self.parse_error: Optional[str] = None
        self._parse()

    def _parse(self) -> None:
        """Frontmatter 추출 및 파싱"""
        match = _FRONTMATTER_RE.search(self.raw_text)
        if not match:
            self.parse_error = "Missing YAML frontmatter (--- ... ---)"
            return

        self.frontmatter_raw = match.group(1)

        if YAML_AVAILABLE:
            try:
                self.data = yaml.safe_load(self.frontmatter_raw)
                if not isinstance(self.data, dict):
                    self.parse_error = "Frontmatter must be a YAML mapping (key: value)"
                    self.data = None
            except yaml.YAMLError as e:
                self.parse_error = f"YAML parse error: {e}"
        else:
            # Fallback: regex 기반 간이 파싱 (기존 호환성)
            self.data = self._regex_parse(self.frontmatter_raw)

    def _regex_parse(self, text: str) -> Dict[str, Any]:
        """PyYAML 없을 때 간이 파싱 (nested 지원 제한적)"""
        result: Dict[str, Any] = {}
        current_key: Optional[str] = None
        current_indent = 0

        for line in text.split('\n'):
            if not line.strip() or line.strip().startswith('#'):
                continue

            # 간단한 key: value 추출
            match = re.match(r'^(\s*)([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)?$', line)
            if match:
                indent = len(match.group(1))
                key = match.group(2)
                value = match.group(3).strip() if match.group(3) else ""

                # 빈 값이면 nested dict로 간주
                if not value:
                    result[key] = {}
                    current_key = key
                    current_indent = indent
                else:
                    # 따옴표 제거
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    result[key] = value

        return result

    def is_valid(self) -> bool:
        """파싱 성공 여부"""
        return self.data is not None

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Dot notation으로 nested 값 접근
        예: "natural_dissolution.termination_conditions"
        """
        if self.data is None:
            return default

        keys = key_path.split('.')
        current = self.data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default

        return current

    def has_key(self, key_path: str) -> bool:
        """키 존재 여부 (값이 None이 아닌지도 확인)"""
        value = self.get(key_path)
        return value is not None

    def has_non_empty(self, key_path: str) -> bool:
        """키가 존재하고 비어있지 않은지 확인"""
        value = self.get(key_path)
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
        if isinstance(value, (list, dict)) and len(value) == 0:
            return False
        return True

    def validate_required_keys(
        self,
        required: List[str]
    ) -> List[ValidationError]:
        """필수 키 검증"""
        errors: List[ValidationError] = []

        if self.parse_error:
            errors.append(ValidationError("_parse", self.parse_error))
            return errors

        for key_path in required:
            if not self.has_key(key_path):
                errors.append(ValidationError(key_path, f"Missing required key"))
            elif not self.has_non_empty(key_path):
                errors.append(ValidationError(key_path, f"Key exists but value is empty"))

        return errors

    def validate_type(
        self,
        key_path: str,
        expected_type: type
    ) -> Optional[ValidationError]:
        """타입 검증"""
        value = self.get(key_path)
        if value is None:
            return None  # 존재 여부는 validate_required_keys에서 처리

        if not isinstance(value, expected_type):
            return ValidationError(
                key_path,
                f"Expected {expected_type.__name__}, got {type(value).__name__}"
            )
        return None

    def validate_list_not_empty(self, key_path: str) -> Optional[ValidationError]:
        """리스트가 존재하고 비어있지 않은지 검증"""
        value = self.get(key_path)
        if value is None:
            return ValidationError(key_path, "Missing required list")
        if not isinstance(value, list):
            return ValidationError(key_path, f"Expected list, got {type(value).__name__}")
        if len(value) == 0:
            return ValidationError(key_path, "List is empty")
        # 리스트 내부 빈 문자열 체크
        if all(not item or (isinstance(item, str) and not item.strip()) for item in value):
            return ValidationError(key_path, "List contains only empty values")
        return None


def validate_blueprint(file_path: Path) -> Tuple[str, List[str]]:
    """
    DNA Blueprint 검증 (기존 verify_blueprint.py 대체용)

    Returns:
        (result, reasons) where result is "Canonical" | "Canonical-Conditional" | "Non-Canonical"
    """
    if not file_path.exists():
        return "Non-Canonical", [f"Missing blueprint file: {file_path}"]

    text = file_path.read_text(encoding="utf-8")
    validator = YAMLValidator(text)

    if not validator.is_valid():
        return "Non-Canonical", [validator.parse_error or "Unknown parse error"]

    errors: List[ValidationError] = []
    warnings: List[ValidationError] = []

    # 필수 최상위 키
    required_top = ["name", "version", "scope", "created", "status"]
    errors.extend(validator.validate_required_keys(required_top))

    # 규범 참조(권장): 군체(Swarm) 구조가 Immune System을 계승하도록 참조 경로를 명시
    recommended_refs = [
        "canon_reference",
        "meta_doctrine_reference",
        "immune_doctrine_reference",
        "inquisitor_reference",
        "audit_log_reference",
    ]
    for key in recommended_refs:
        if not validator.has_non_empty(key):
            warnings.append(ValidationError(key, "Missing recommended normative reference", severity="warning"))

    # natural_dissolution 섹션 검증
    nd_errors = []
    nd_errors.append(validator.validate_list_not_empty("natural_dissolution.termination_conditions"))
    nd_errors.append(validator.validate_list_not_empty("natural_dissolution.dissolution_steps"))
    if not validator.has_non_empty("natural_dissolution.purpose"):
        nd_errors.append(ValidationError("natural_dissolution.purpose", "Missing or empty"))
    errors.extend([e for e in nd_errors if e is not None])

    # retention.max_days 예외 처리 (bootstrap 구조만 permanent 허용)
    max_days = validator.get("natural_dissolution.retention.max_days")
    if max_days is not None and not isinstance(max_days, int):
        if isinstance(max_days, str) and max_days.strip().lower() == "permanent":
            if not validator.has_key("meta_exception.granted_by"):
                warnings.append(ValidationError(
                    "natural_dissolution.retention.max_days",
                    "Using 'permanent' without meta_exception.granted_by (bootstrap-only exception)",
                    severity="warning",
                ))
        else:
            warnings.append(ValidationError(
                "natural_dissolution.retention.max_days",
                f"Unexpected value type: {type(max_days).__name__} (expected int; bootstrap may use 'permanent')",
                severity="warning",
            ))

    # resource_limits 섹션 검증
    rl_required = ["resource_limits.max_files", "resource_limits.max_folders"]
    for key in rl_required:
        if not validator.has_key(key):
            errors.append(ValidationError(key, "Missing required key"))
        else:
            val = validator.get(key)
            if not isinstance(val, (int, float)) or val <= 0:
                errors.append(ValidationError(key, f"Must be a positive number, got: {val}"))

    # inquisitor 섹션 검증
    if not validator.has_key("inquisitor.required"):
        errors.append(ValidationError("inquisitor.required", "Missing required key"))
    if not validator.has_non_empty("inquisitor.audit_log"):
        errors.append(ValidationError("inquisitor.audit_log", "Missing or empty"))

    # 결과 판정
    if any(e.severity == "error" for e in errors):
        reasons = [repr(e) for e in errors]
        # Blueprint는 존재하지만 불완전 → Conditional
        return "Canonical-Conditional", reasons

    if warnings:
        return "Canonical-Conditional", [repr(w) for w in warnings]

    return "Canonical", []


def validate_permission_request(file_path: Path) -> Tuple[str, List[str]]:
    """
    Permission Request 검증 (기존 judge_permission.py 대체용)
    """
    if not file_path.exists():
        return "Non-Canonical", [f"Missing request file: {file_path}"]

    text = file_path.read_text(encoding="utf-8")
    validator = YAMLValidator(text)

    if not validator.is_valid():
        return "Non-Canonical", [validator.parse_error or "Unknown parse error"]

    errors: List[ValidationError] = []
    warnings: List[ValidationError] = []

    # 필수 키
    required_top = ["type", "created", "requester", "action", "target", "risk_level", "justification"]
    errors.extend(validator.validate_required_keys(required_top))

    # time_bound 검증
    if not validator.has_non_empty("time_bound.expires"):
        errors.append(ValidationError("time_bound.expires", "Missing or empty expiration date"))

    # natural_dissolution 검증
    nd_errors = []
    nd_errors.append(validator.validate_list_not_empty("natural_dissolution.termination_conditions"))
    nd_errors.append(validator.validate_list_not_empty("natural_dissolution.dissolution_steps"))
    errors.extend([e for e in nd_errors if e is not None])

    # risk_level 값 검증
    risk = validator.get("risk_level")
    if risk and risk not in ["low", "medium", "high"]:
        warnings.append(ValidationError("risk_level", f"Unexpected value: {risk} (expected: low/medium/high)"))

    # constraints는 권장
    if not validator.has_key("constraints"):
        warnings.append(ValidationError("constraints", "Missing recommended key"))

    # 결과 판정
    if errors:
        return "Non-Canonical", [repr(e) for e in errors]

    if warnings:
        return "Canonical-Conditional", [repr(w) for w in warnings]

    return "Canonical", []


# CLI 테스트용
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python yaml_validator.py <file.md> [--type blueprint|permission]")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    validate_type = "blueprint"
    if "--type" in sys.argv:
        idx = sys.argv.index("--type")
        if idx + 1 < len(sys.argv):
            validate_type = sys.argv[idx + 1]

    if validate_type == "permission":
        result, reasons = validate_permission_request(file_path)
    else:
        result, reasons = validate_blueprint(file_path)

    print(f"File: {file_path}")
    print(f"Result: {result}")
    if reasons:
        print("Reasons:")
        for r in reasons:
            print(f"  - {r}")

    sys.exit(0 if result == "Canonical" else (2 if result == "Canonical-Conditional" else 1))
