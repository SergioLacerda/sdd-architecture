#!/usr/bin/env python3
"""Governance compliance validator for SDD Architecture."""

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class GovernanceComplianceValidator:
    """Validates governance file integrity and compliance rules."""

    GOVERNANCE_FILE = ".ai/governance-core.json"
    SIGNATURE_FILE = ".ai/.governance-signature.json"
    COMPILED_GOVERNANCE_FILE = "_core/compiler/compiled/governance-core.json"
    COMPILED_GOVERNANCE_FILE_ALT = "compiler/compiled/governance-core.json"

    def __init__(self, project_dir: Path) -> None:
        self.project_dir = Path(project_dir)
        self.integrity_requested: bool = False
        self.governance_file = self._resolve_governance_file()
        self.signature_file = self._resolve_signature_file()

    def _resolve_governance_file(self) -> Path:
        """Resolve the governance file path for project and framework contexts."""
        candidates = [
            self.project_dir / self.GOVERNANCE_FILE,
            self.project_dir / self.COMPILED_GOVERNANCE_FILE,
            self.project_dir / self.COMPILED_GOVERNANCE_FILE_ALT,
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return candidates[0]

    def _resolve_signature_file(self) -> Path:
        """Resolve the signature file path for project-scoped governance."""
        return self.project_dir / self.SIGNATURE_FILE

    def _is_project_governance(self, data: Dict[str, Any]) -> bool:
        """Return True when validating generated project governance under .ai/."""
        required = {"seedlings", "authority", "policies", "phases"}
        return required.issubset(data.keys())

    def _is_compiled_governance(self, data: Dict[str, Any]) -> bool:
        """Return True when validating compiled governance artifacts."""
        required = {"category", "version", "items", "fingerprint"}
        return required.issubset(data.keys())

    # ------------------------------------------------------------------
    # Signing
    # ------------------------------------------------------------------

    def _compute_fingerprint(self, data: Dict[str, Any]) -> str:
        """Compute SHA-256 fingerprint of the governance data (excluding signature field)."""
        clean = {k: v for k, v in data.items() if k not in {"_signature", "fingerprint"}}
        serialized = json.dumps(clean, sort_keys=True, ensure_ascii=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def sign_governance(self) -> bool:
        """Sign the governance file and write a companion signature file."""
        if not self.governance_file.exists():
            return False
        try:
            with open(self.governance_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            fingerprint = self._compute_fingerprint(data)
            signature = {"fingerprint": fingerprint}
            self.signature_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.signature_file, "w", encoding="utf-8") as f:
                json.dump(signature, f, indent=2)
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def _check_integrity(self, data: Dict[str, Any]) -> List[str]:
        """Return list of integrity violation messages (empty = OK)."""
        if not self.integrity_requested:
            return []
        if self._is_compiled_governance(data):
            expected = data.get("fingerprint")
            actual = self._compute_fingerprint(data)
            if expected != actual:
                return [f"Integrity Failure: fingerprint mismatch (expected {expected[:8]}…, got {actual[:8]}…)"]
            return []
        if not self.signature_file.exists():
            return ["Integrity Failure: signature file missing"]
        try:
            with open(self.signature_file, "r", encoding="utf-8") as f:
                sig = json.load(f)
            expected = sig.get("fingerprint")
            actual = self._compute_fingerprint(data)
            if expected != actual:
                return [f"Integrity Failure: fingerprint mismatch (expected {expected[:8]}…, got {actual[:8]}…)"]
        except Exception as e:
            return [f"Integrity Failure: could not read signature — {e}"]
        return []

    def _check_structure(self, data: Dict[str, Any]) -> List[str]:
        """Check required top-level fields."""
        violations = []
        required = ["seedlings", "authority", "policies", "phases"]
        for field in required:
            if field not in data:
                violations.append(f"Missing required field: {field}")
        return violations

    def _check_compiled_structure(self, data: Dict[str, Any]) -> List[str]:
        """Check required fields for compiled governance artifacts."""
        violations = []
        required = ["category", "version", "items", "fingerprint"]
        for field in required:
            if field not in data:
                violations.append(f"Missing required compiled field: {field}")
        if data.get("category") != "CORE":
            violations.append("Compiled governance category must be 'CORE'")
        if not isinstance(data.get("items", []), list):
            violations.append("Compiled governance items must be a list")
        return violations

    def _check_policies(self, data: Dict[str, Any]) -> List[str]:
        """Check policies section."""
        violations = []
        policies = data.get("policies", {})
        enforcement = policies.get("enforcement", "")
        valid_levels = {"strict", "standard", "permissive"}
        if enforcement.lower() not in valid_levels:
            violations.append(f"Invalid enforcement level: '{enforcement}' (must be one of {valid_levels})")
        return violations

    def validate_all(self) -> Tuple[bool, Dict[str, Any]]:
        """Run all validation checks.

        Returns:
            (is_compliant, results_dict) where results_dict has key 'violations'.
        """
        if not self.governance_file.exists():
            return False, {"violations": [f"Governance file not found: {self.governance_file}"]}

        try:
            with open(self.governance_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            return False, {"violations": [f"Invalid JSON in governance file: {e}"]}

        violations: List[str] = []
        if self._is_project_governance(data):
            violations.extend(self._check_structure(data))
            violations.extend(self._check_policies(data))
        elif self._is_compiled_governance(data):
            violations.extend(self._check_compiled_structure(data))
        else:
            violations.append("Unrecognized governance format")
        violations.extend(self._check_integrity(data))

        is_compliant = len(violations) == 0
        return is_compliant, {"violations": violations, "governance_file": str(self.governance_file)}

    def get_mandatory_fix_steps(self, results: Dict[str, Any]) -> List[str]:
        """Return human-readable fix steps for each violation."""
        steps = []
        for v in results.get("violations", []):
            if "Missing required field" in v:
                steps.append(f"Add the missing field to {self.GOVERNANCE_FILE}")
            elif "Missing required compiled field" in v:
                steps.append("Regenerate compiled governance artifacts from the current spec")
            elif "enforcement level" in v:
                steps.append("Set policies.enforcement to 'strict', 'standard', or 'permissive'")
            elif "Integrity Failure" in v:
                if str(self.governance_file).endswith("governance-core.json") and "/compiled/" in str(self.governance_file):
                    steps.append("Regenerate compiled governance artifacts to refresh the embedded fingerprint")
                else:
                    steps.append("Re-sign the governance file: validator.sign_governance()")
            else:
                steps.append(f"Fix violation: {v}")
        return steps

    def get_enforcement_level(self) -> Tuple[str, str]:
        """Return governance enforcement level and context message."""
        valid_levels = {"strict", "standard", "permissive"}

        if not self.governance_file.exists():
            return "UNKNOWN", f"Governance file not found: {self.governance_file}"

        try:
            with open(self.governance_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            return "UNKNOWN", f"Could not read governance file: {e}"

        if self._is_project_governance(data):
            enforcement = str(data.get("policies", {}).get("enforcement", "permissive")).lower()
            if enforcement not in valid_levels:
                return "UNKNOWN", f"Invalid enforcement level in governance file: {enforcement}"
            return enforcement.upper(), f"Source: {self.governance_file}"

        if self._is_compiled_governance(data):
            # Compiled artifacts do not carry full policy metadata.
            # Default to PERMISSIVE for reporting compatibility.
            return "PERMISSIVE", f"Source: {self.governance_file} (compiled artifact default)"

        return "UNKNOWN", f"Unrecognized governance format: {self.governance_file}"


def main(argv: Optional[List[str]] = None) -> int:
    """Run governance validation CLI."""
    parser = argparse.ArgumentParser(description="Validate governance compliance and integrity")
    parser.add_argument("project_dir", nargs="?", default=".", help="Project directory to validate")
    parser.add_argument("--verify", action="store_true", help="Run compliance verification")
    parser.add_argument("--check-integrity", action="store_true", help="Validate governance integrity")
    parser.add_argument("--fix-steps", action="store_true", help="Print recommended fix steps on failure")
    parser.add_argument("--sign", action="store_true", help="Create or refresh governance signature")
    parser.add_argument("--enforcement-check", action="store_true", help="Print current enforcement level")

    args = parser.parse_args(argv)

    validator = GovernanceComplianceValidator(Path(args.project_dir))
    validator.integrity_requested = args.check_integrity

    if args.sign:
        ok = validator.sign_governance()
        if ok:
            print(f"✅ Governance signed: {validator.signature_file}")
            return 0
        print(f"❌ Could not sign governance file: {validator.governance_file}")
        return 1

    if args.enforcement_check:
        level, context = validator.get_enforcement_level()
        print(f"Enforcement level: {level}")
        print(context)
        return 0 if level in {"STRICT", "STANDARD", "PERMISSIVE"} else 1

    ok, results = validator.validate_all()
    if ok:
        print(f"✅ Governance is compliant: {results['governance_file']}")
        return 0

    print("❌ Governance violations found:")
    for v in results["violations"]:
        print(f"  • {v}")
    if args.fix_steps:
        for step in validator.get_mandatory_fix_steps(results):
            print(f"  → {step}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
