#!/usr/bin/env python3
"""
ADR VALIDATOR
Verifies all 6 ADRs exist and have required sections.

Usage:
    python docs/ia/scripts/validate_adrs.py

Exit codes:
    0 = All ADRs valid
    1 = ADR violation detected
"""

import importlib
import sys
from pathlib import Path

# Ensure packages is in path for tests.path_config
root = Path(__file__).resolve().parents[3]
if str(root / "packages") not in sys.path:
    sys.path.insert(0, str(root / "packages"))

ADR_CANONICAL = importlib.import_module("tests.path_config").ADR_CANONICAL


class ADRValidator:
    """Validates Architectural Decision Records"""

    REQUIRED_ADRS = {
        "ADR-001-clean-architecture-8-layer.md": "8-Layer Pattern",
        "ADR-002-async-first-no-blocking.md": "Async-First Strategy",
        "ADR-003-ports-adapters-pattern.md": "Ports & Adapters",
        "ADR-004-vector-index-strategy.md": "Vector Index Choice",
        "ADR-005-thread-isolation-mandatory.md": "Thread Isolation",
        "ADR-006-append-only-storage.md": "Storage Strategy",
    }

    REQUIRED_SECTIONS = [
        "## Status",
        "## Context",
        "## Decision",
        "## Consequences",
        "## Alternatives Considered",
        "## Current Implementation Status",
    ]

    def __init__(self):
        self.root = ADR_CANONICAL
        self.violations = []
        self.warnings = []

    def validate(self) -> bool:
        """Run all ADR validations"""
        print("🏗️  ADR VALIDATION")
        print("-" * 60)

        # Check all required ADRs exist
        self._check_adrs_exist()

        # Check each ADR has required sections
        self._check_adr_sections()

        # Check ADR quality
        self._check_adr_quality()

        # Print results
        return self._print_results()

    def _check_adrs_exist(self):
        """Check all 6 required ADRs exist"""
        print("\n📋 Checking required ADRs...")
        for adr_file, _description in self.REQUIRED_ADRS.items():
            full_path = self.root / adr_file
            if full_path.exists():
                size = full_path.stat().st_size
                print(f"  ✅ {adr_file:<45} ({size:,} bytes)")
            else:
                msg = f"  ❌ {adr_file:<45} MISSING!"
                print(msg)
                self.violations.append(msg)

    def _check_adr_sections(self):
        """Check each ADR has required sections"""
        print("\n📝 Checking ADR sections...")
        for adr_file in self.REQUIRED_ADRS.keys():
            full_path = self.root / adr_file
            if not full_path.exists():
                continue

            try:
                content = full_path.read_text()
                missing_sections = []

                for section in self.REQUIRED_SECTIONS:
                    if section not in content:
                        missing_sections.append(section)

                if missing_sections:
                    msg = f"  ⚠️  {adr_file:<40} missing: {', '.join(missing_sections)}"
                    print(msg)
                    self.warnings.append(msg)
                else:
                    print(f"  ✅ {adr_file:<40} all sections present")

            except Exception as e:
                self.violations.append(f"Error reading {adr_file}: {e}")

    def _check_adr_quality(self):
        """Check ADR quality metrics"""
        print("\n📊 Checking ADR quality...")
        for adr_file in self.REQUIRED_ADRS.keys():
            full_path = self.root / adr_file
            if not full_path.exists():
                continue

            try:
                content = full_path.read_text()
                content.split("\n")
                size_bytes = len(content)

                # Check minimum size (at least 500 bytes)
                if size_bytes < 500:
                    msg = f"  ⚠️  {adr_file:<40} ({size_bytes} bytes) — SMALL, consider expanding"
                    print(msg)
                    self.warnings.append(msg)

                # Check for key quality indicators
                has_rationale = "rationale" in content.lower() or "why" in content.lower()
                has_consequences = "consequence" in content.lower()
                has_review_date = "review date" in content.lower() or "2027" in content

                quality_score = sum([has_rationale, has_consequences, has_review_date])

                if quality_score == 3:
                    print(f"  ✅ {adr_file:<40} high quality ✓✓✓")
                elif quality_score >= 2:
                    print(f"  🟡 {adr_file:<40} medium quality ✓✓")
                else:
                    msg = f"  ⚠️  {adr_file:<40} low quality"
                    print(msg)
                    self.warnings.append(msg)

            except Exception as e:
                self.violations.append(f"Error analyzing {adr_file}: {e}")

    def _print_results(self) -> bool:
        """Print validation results"""
        print("\n" + "=" * 60)
        print("VALIDATION RESULTS")
        print("=" * 60)

        expected = len(self.REQUIRED_ADRS)
        existing = sum(1 for adr in self.REQUIRED_ADRS.keys() if (self.root / adr).exists())

        print(f"\n📊 ADR Summary: {existing}/{expected} ADRs exist")

        if self.violations:
            print(f"\n🔴 VIOLATIONS: {len(self.violations)}")
            for v in self.violations:
                print(f"  {v}")

        if self.warnings:
            print(f"\n🟡 WARNINGS: {len(self.warnings)}")
            for w in self.warnings:
                print(f"  {w}")

        if not self.violations:
            print("\n✅ ADR VALIDATION PASSED")
            return True
        else:
            print("\n❌ ADR VALIDATION FAILED")
            return False


if __name__ == "__main__":
    validator = ADRValidator()
    success = validator.validate()
    sys.exit(0 if success else 1)
