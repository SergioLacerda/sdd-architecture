#!/usr/bin/env python
"""
SDD v3.0 Wizard - Interactive CLI for project generation

Transforms architect specs (.sdd-core/) into client-ready projects
via 7-phase orchestration pipeline.

Usage:
  Interactive mode:
    python wizard.py
  
  Non-interactive mode:
    python wizard.py --language java --output ~/my-project/
  
  Dry-run (preview without creating files):
    python wizard.py --language python --dry-run --verbose
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import phase implementations
# Import interactive mode
from orchestration.phase_1_validate import phase_1_validate_source
from orchestration.phase_2_load_compiled_v3 import phase_2_load_compiled_v3 as phase_2_load_compiled
from orchestration.phase_3_filter_mandates import phase_3_filter_mandates
from orchestration.phase_4_filter_guidelines import phase_4_filter_guidelines
from orchestration.phase_5_apply_template import phase_5_apply_template
from orchestration.phase_6_generate_project import phase_6_generate_project
from orchestration.phase_7_validate_output import phase_7_validate_output


class WizardOrchestrator:
    """Main orchestrator for 7-phase wizard pipeline"""

    def __init__(self, repo_root: Optional[Path] = None, verbose: bool = False):
        self.repo_root = repo_root or Path.cwd()
        self.verbose = verbose
        self.phases_results = {}
        self.artifacts = {}

    def log(self, level: str, message: str):
        """Print log message with level indicator"""
        if level == "INFO" or self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {level:8s} {message}")

    def print_phase_header(self, phase_num: int, phase_name: str):
        """Print phase execution header"""
        print()
        print("=" * 60)
        print(f"Phase {phase_num}: {phase_name}")
        print("=" * 60)

    def print_phase_result(self, success: bool, report: Dict[str, Any]):
        """Print phase result summary"""
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"\n{status} - {report.get('phase', 'UNKNOWN')}")

        if report.get('data'):
            print(f"  Data: {report['data']}")

        if report.get('warnings'):
            for warning in report['warnings']:
                print(f"  ⚠️  Warning: {warning}")

        if report.get('errors') and self.verbose:
            for error in report['errors']:
                print(f"  ❌ Error: {error}")

    def run_phase_1(self):
        """Execute Phase 1: Validate SOURCE"""
        self.print_phase_header(1, "Validate SOURCE (.sdd-core/)")
        self.log("INFO", "Checking mandate.spec and guidelines.dsl...")

        success, report = phase_1_validate_source(self.repo_root)
        self.phases_results['phase_1'] = report
        self.print_phase_result(success, report)

        return success

    def run_phase_2(self):
        """Execute Phase 2: Load COMPILED"""
        self.print_phase_header(2, "Load COMPILED (.sdd-runtime/)")
        self.log("INFO", "Deserializing compiled artifacts...")

        success, report = phase_2_load_compiled(self.repo_root)
        self.phases_results['phase_2'] = report

        # Store artifacts for next phases
        if '_artifacts' in report:
            self.artifacts = report['_artifacts']

        self.print_phase_result(success, report)
        return success

    def run_phase_3(self, mandates=None):
        """Execute Phase 3: Filter mandates"""
        self.print_phase_header(3, "Filter Mandates")
        self.log("INFO", "Filtering mandates by user selection...")

        # Get mandates from Phase 2
        phase_2_report = self.phases_results.get('phase_2', {})
        compiled_mandates = phase_2_report.get('data', {}).get('mandate', {})

        if not compiled_mandates:
            self.log("ERROR", "No mandates from Phase 2")
            return False

        success, report = phase_3_filter_mandates(
            compiled_mandates,
            selected_mandate_ids=mandates,
            repo_root=self.repo_root
        )
        self.phases_results['phase_3'] = report
        self.print_phase_result(success, report)
        return success

    def run_phase_4(self, language='python'):
        """Execute Phase 4: Filter guidelines"""
        self.print_phase_header(4, "Filter Guidelines")
        self.log("INFO", f"Filtering guidelines by language={language}...")

        # Get guidelines from Phase 2
        phase_2_report = self.phases_results.get('phase_2', {})
        compiled_guidelines = phase_2_report.get('data', {}).get('guidelines', {})

        if not compiled_guidelines:
            self.log("ERROR", "No guidelines from Phase 2")
            return False

        success, report = phase_4_filter_guidelines(
            compiled_guidelines,
            language=language,
            repo_root=self.repo_root
        )
        self.phases_results['phase_4'] = report
        self.print_phase_result(success, report)
        return success

    def run_phase_5(self, language='python', output_dir: Path = None):
        """Execute Phase 5: Apply template"""
        self.print_phase_header(5, "Apply Template Scaffold")
        self.log("INFO", "Copying and customizing template files...")

        if output_dir is None:
            output_dir = self.repo_root / "sdd-generated" / "scaffold"

        success, report = phase_5_apply_template(
            scaffolding_dir=output_dir,
            language=language,
            repo_root=self.repo_root
        )
        self.phases_results['phase_5'] = report
        self.print_phase_result(success, report)
        return success

    def run_phase_6(self, output_dir: Path = None, language='python'):
        """Execute Phase 6: Generate project"""
        self.print_phase_header(6, "Generate Project Structure")
        self.log("INFO", "Generating complete project structure...")

        # Get data from previous phases
        phase_1_report = self.phases_results.get('phase_1', {})
        phase_2_report = self.phases_results.get('phase_2', {})
        phase_3_report = self.phases_results.get('phase_3', {})
        phase_4_report = self.phases_results.get('phase_4', {})

        # Extract mandate and guideline text from Phase 1
        mandate_text = phase_1_report.get('data', {}).get('mandate_text', '')
        guidelines_text = phase_1_report.get('data', {}).get('guidelines_text', '')

        # Extract metadata from Phase 2
        metadata = phase_2_report.get('data', {}).get('metadata', {})

        # Extract filtered mandates and guidelines from Phases 3-4
        filtered_mandates = phase_3_report.get('data', {}).get('filtered_mandates', {})
        filtered_guidelines = phase_4_report.get('data', {}).get('filtered_guidelines', {})

        if output_dir is None:
            output_dir = self.repo_root / "sdd-generated" / "project"

        success, report = phase_6_generate_project(
            filtered_mandates=filtered_mandates,
            filtered_guidelines=filtered_guidelines,
            mandate_text=mandate_text,
            guidelines_text=guidelines_text,
            metadata=metadata,
            output_dir=output_dir,
            language=language,
            repo_root=self.repo_root
        )
        self.phases_results['phase_6'] = report
        self.print_phase_result(success, report)
        return success

    def run_phase_7(self, project_dir: Path = None):
        """Execute Phase 7: Validate output"""
        self.print_phase_header(7, "Validate Output")
        self.log("INFO", "Validating generated project...")

        if project_dir is None:
            project_dir = self.repo_root / "sdd-generated" / "project"

        success, report = phase_7_validate_output(
            project_dir=project_dir,
            repo_root=self.repo_root
        )
        self.phases_results['phase_7'] = report
        self.print_phase_result(success, report)
        return success

    def run_full_pipeline(self, language='python', mandates=None, output_dir: Path = None) -> bool:
        """Execute complete pipeline (phases 1-7)"""
        print()
        print("🔮 SDD v3.0 Wizard - Project Generator")
        print("=" * 60)
        print(f"Started: {datetime.now().isoformat()}")
        print(f"Language: {language}")
        print()

        # Phase 1: Validate SOURCE
        if not self.run_phase_1():
            print("\n❌ Pipeline stopped at Phase 1 (Validation failed)")
            return False

        # Phase 2: Load COMPILED
        if not self.run_phase_2():
            print("\n❌ Pipeline stopped at Phase 2 (Failed to load compiled artifacts)")
            return False

        # Phase 3: Filter Mandates
        if not self.run_phase_3(mandates):
            print("\n❌ Pipeline stopped at Phase 3 (Mandate filtering failed)")
            return False

        # Phase 4: Filter Guidelines
        if not self.run_phase_4(language):
            print("\n❌ Pipeline stopped at Phase 4 (Guideline filtering failed)")
            return False

        # Phase 5: Apply Template
        scaffold_dir = (output_dir or (self.repo_root / "sdd-generated")) / "scaffold"
        if not self.run_phase_5(language, scaffold_dir):
            print("\n⚠️  Phase 5 warning (template not critical)")

        # Phase 6: Generate Project
        project_dir = (output_dir or (self.repo_root / "sdd-generated")) / "project"
        if not self.run_phase_6(project_dir, language):
            print("\n❌ Pipeline stopped at Phase 6 (Project generation failed)")
            return False

        # Phase 7: Validate Output
        if not self.run_phase_7(project_dir):
            print("\n⚠️  Phase 7 warning (validation issues)")

        print()
        print("=" * 60)
        print("✅ Phases 1-7 Complete!")
        print("=" * 60)
        print()
        print("📋 Pipeline Status:")
        for phase_name, report in self.phases_results.items():
            status = "✅" if report['status'] == 'SUCCESS' else "❌"
            print(f"  {status} {report['phase']}")

        print()
        if output_dir or not (self.repo_root / "sdd-generated").exists():
            print(f"📁 Generated project: {project_dir}")
        else:
            print(f"📁 Generated project: {project_dir}")
        print()

        return True


def create_argument_parser():
    """Create and configure CLI argument parser"""
    parser = argparse.ArgumentParser(
        description="SDD v3.0 Wizard - Generate project from compiled specifications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Interactive mode:
    python wizard.py
  
  Non-interactive mode:
    python wizard.py --language java --output ~/my-project/
  
  Dry-run (preview without creating files):
    python wizard.py --language python --dry-run --verbose
  
  Test phases 1-2:
    python wizard.py --test-phases 1-2
        """
    )

    # Optional: Language selection
    parser.add_argument(
        "--language",
        choices=["java", "python", "js"],
        help="Target programming language (interactive if not specified)"
    )

    # Optional: Mandate selection
    parser.add_argument(
        "--mandates",
        help="Comma-separated mandate IDs (e.g., M001,M002)"
    )

    # Optional: Output directory
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory for generated project"
    )

    # Optional: Dry-run mode
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without creating files"
    )

    # Optional: Verbose output
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output"
    )

    # Optional: Test specific phases
    parser.add_argument(
        "--test-phases",
        help="Test specific phases (e.g., 1-2, 1-7, just 1)"
    )

    # Optional: Interactive mode
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive guided mode (default if no arguments provided)"
    )

    return parser


def main():
    """Main entry point"""
    parser = create_argument_parser()
    args = parser.parse_args()

    # Create orchestrator
    orchestrator = WizardOrchestrator(verbose=args.verbose)

    # Determine if running in interactive mode
    # Interactive by default if: no required args provided (language, mandates, output)
    # And not in test mode
    should_run_interactive = args.interactive or (
        not args.language
        and not args.mandates
        and not args.output
        and not args.test_phases
    )

    # Test mode
    if args.test_phases:
        print(f"\n🧪 Testing phases: {args.test_phases}")
        # For now, run full pipeline in test mode
        mandates = None
        if args.mandates:
            mandates = args.mandates.split(',')

        orchestrator.run_full_pipeline(
            language=args.language or 'python',
            mandates=mandates,
            output_dir=args.output
        )
        return 0

    # Interactive mode (v3 new flow: 3-phase template generation)
    if should_run_interactive:
        from interactive_mode import run_interactive_wizard
        success = run_interactive_wizard(orchestrator.repo_root)
        return 0 if success else 1

    # Non-interactive mode
    mandates = None
    if args.mandates:
        mandates = args.mandates.split(',')

    success = orchestrator.run_full_pipeline(
        language=args.language or 'python',
        mandates=mandates,
        output_dir=args.output
    )

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
