#!/usr/bin/env python3
"""
Migration Orchestrator: v2.1 → v3.0

Runs all extraction, conversion, and validation steps.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from constitution_parser import ConstitutionParser
from dsl_converter import DSLConverter
from guidelines_extractor import GuidelinesExtractor
from migration_validator import MigrationValidator


class MigrationOrchestrator:
    """Orchestrate complete v2.1 → v3.0 migration"""

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.repo_root = Path(__file__).parent.parent.parent
        self.migration_dir = self.repo_root / "migration"
        self.output_dir = self.migration_dir / "output"
        self.reports_dir = self.migration_dir / "reports"

        # Ensure output directories exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def run_full_migration(self) -> bool:
        """Run complete migration pipeline"""
        print("🚀 SDD v2.1 → v3.0 Migration")
        print("=" * 50)

        try:
            # Phase 1: Parse v2.1 constitution
            print("\n📖 Phase 1: Parsing v2.1 constitution...")
            mandates_data = self._parse_constitution()
            if not mandates_data:
                print("❌ Failed to parse constitution")
                return False
            print(f"✅ Extracted {len(mandates_data['mandates'])} mandates")

            # Phase 2: Extract v2.1 guidelines
            print("\n📋 Phase 2: Extracting guidelines...")
            guidelines_data = self._extract_guidelines()
            if guidelines_data is None:
                print("⚠️  No guidelines found, continuing...")
                guidelines_data = {"guidelines": [], "metadata": {}}
            print(f"✅ Extracted {len(guidelines_data['guidelines'])} guidelines")

            # Phase 3: Convert to v3.0 DSL
            print("\n🔄 Phase 3: Converting to v3.0 DSL...")
            self._convert_to_dsl(mandates_data, guidelines_data)
            print("✅ DSL conversion complete")

            # Phase 4: Validate
            print("\n✔️  Phase 4: Validating...")
            if not self._validate_output(len(mandates_data["mandates"])):
                print("⚠️  Validation found issues (see reports)")
            print("✅ Validation complete")

            # Phase 5: Generate reports
            print("\n📊 Phase 5: Generating reports...")
            self._generate_reports(mandates_data, guidelines_data)
            print("✅ Reports generated")

            print("\n" + "=" * 50)
            print("✅ Migration complete!")
            print(f"Output: {self.output_dir}")
            print(f"Reports: {self.reports_dir}")

            return True

        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            if self.debug:
                import traceback

                traceback.print_exc()
            return False

    def _parse_constitution(self) -> dict:
        """Parse v2.1 constitution"""
        constitution_file = self.repo_root / "EXECUTION/spec/CANONICAL/rules/constitution.md"

        if not constitution_file.exists():
            print(f"⚠️  Constitution file not found at {constitution_file}")
            print("   Creating sample output for testing...")
            return self._create_sample_mandates()

        parser = ConstitutionParser()
        mandates = parser.parse_file(constitution_file)

        return {
            "mandates": [
                {
                    "id": m.id,
                    "title": m.title,
                    "description": m.description,
                    "category": m.category,
                    "rationale": m.rationale,
                    "validation": m.validation,
                }
                for m in mandates
            ],
            "metadata": {"total": len(mandates), "version": "2.1"},
        }

    def _extract_guidelines(self) -> dict:
        """Extract v2.1 guidelines"""
        guides_dir = self.repo_root / "EXECUTION/spec/guides"

        if not guides_dir.exists():
            if self.debug:
                print(f"   Guides directory not found at {guides_dir}")
            return None

        extractor = GuidelinesExtractor()
        guidelines = extractor.extract_from_directory(guides_dir)

        return {
            "guidelines": [
                {"id": g.id, "title": g.title, "description": g.description, "category": g.category, "examples": g.examples}
                for g in guidelines
            ],
            "metadata": {"total": len(guidelines), "version": "2.1"},
        }

    def _convert_to_dsl(self, mandates_data: dict, guidelines_data: dict):
        """Convert to v3.0 DSL format"""
        # Convert mandates
        mandate_spec = DSLConverter.convert_mandates(mandates_data["mandates"])
        mandate_file = self.output_dir / "mandate.spec"
        mandate_file.write_text(mandate_spec, encoding="utf-8")

        # Convert guidelines
        guidelines_dsl = DSLConverter.convert_guidelines(guidelines_data["guidelines"])
        guidelines_file = self.output_dir / "guidelines.dsl"
        guidelines_file.write_text(guidelines_dsl, encoding="utf-8")

    def _validate_output(self, expected_mandates: int) -> bool:
        """Validate migration output"""
        validator = MigrationValidator()

        mandate_file = self.output_dir / "mandate.spec"
        guidelines_file = self.output_dir / "guidelines.dsl"

        validator.validate_mandate_spec(mandate_file, expected_mandates)
        validator.validate_guidelines_dsl(guidelines_file)

        # Save validation report
        report = validator.get_report()
        report_file = self.reports_dir / "validation_report.json"
        report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")

        return all(r["passed"] for r in report["results"])

    def _generate_reports(self, mandates_data: dict, guidelines_data: dict):
        """Generate migration reports"""
        # Extraction report
        extraction_report = {
            "timestamp": datetime.utcnow().isoformat(),
            "mandates": {
                "extracted": len(mandates_data["mandates"]),
                "categories": self._count_categories([m["category"] for m in mandates_data["mandates"]]),
            },
            "guidelines": {
                "extracted": len(guidelines_data["guidelines"]),
                "categories": self._count_categories([g["category"] for g in guidelines_data["guidelines"]]),
            },
            "metadata": {
                "source_version": "2.1",
                "target_version": "3.0",
                "migration_tool": "sdd-migration",
                "migration_date": datetime.utcnow().isoformat(),
            },
        }

        report_file = self.reports_dir / "extraction_report.json"
        report_file.write_text(json.dumps(extraction_report, indent=2), encoding="utf-8")

    def _count_categories(self, categories: list) -> dict:
        """Count categories"""
        counts = {}
        for cat in categories:
            counts[cat] = counts.get(cat, 0) + 1
        return counts

    def _create_sample_mandates(self) -> dict:
        """Create sample mandates for testing"""
        return {
            "mandates": [
                {
                    "id": "M001",
                    "title": "Clean Architecture",
                    "description": "All systems must implement 8-layer Clean Architecture",
                    "category": "architecture",
                    "rationale": "Foundation enables testability and replaceability",
                    "validation": ["pytest tests/architecture/ -v"],
                },
                {
                    "id": "M002",
                    "title": "Test-Driven Development",
                    "description": "All code must be written using TDD (tests first)",
                    "category": "testing",
                    "rationale": "Ensures quality and design clarity",
                    "validation": ["pytest --cov"],
                },
            ],
            "metadata": {"total": 2, "version": "2.1", "note": "sample"},
        }


def main():
    parser = argparse.ArgumentParser(description="SDD v2.1 → v3.0 Migration")
    parser.add_argument("--full", action="store_true", help="Run full migration")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")

    args = parser.parse_args()

    orchestrator = MigrationOrchestrator(debug=args.debug)

    if args.full:
        success = orchestrator.run_full_migration()
        sys.exit(0 if success else 1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
