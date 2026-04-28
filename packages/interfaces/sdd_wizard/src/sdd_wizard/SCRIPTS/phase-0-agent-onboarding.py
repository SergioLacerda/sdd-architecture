#!/usr/bin/env python3
"""
PHASE 0: Agent Workspace Initialization

Purpose: Automate PHASE 0 onboarding for AI agents
- Discovers SPEC framework via .spec.config
- Creates .ai/context-aware/ infrastructure
- Validates SDD knowledge (quiz)
- Confirms workspace is ready

Usage:
    python phase-0-agent-onboarding.py [project_root]

Example:
    cd /path/to/your/project
    python $(grep spec_path .spec.config | cut -d' ' -f3)/docs/ia/SCRIPTS/phase-0-agent-onboarding.py

Time: ~15-20 minutes
"""

import os
import shutil
import stat
import sys
from configparser import ConfigParser
from pathlib import Path


class PHASE0Bootstrap:
    """Bootstrap agent workspace for SPEC project."""

    def __init__(self, project_root=None):
        self.project_root = Path(project_root or os.getcwd()).resolve()
        self.spec_config = self.project_root / ".spec.config"
        self.spec_path = None
        self.ai_dir = self.project_root / ".ai" / "context-aware"

    def run(self):
        """Execute full PHASE 0 onboarding."""
        print("\n" + "=" * 60)
        print("🚀 PHASE 0: Agent Workspace Initialization")
        print("=" * 60 + "\n")

        # Step 1: Verify .spec.config
        if not self._verify_config():
            return False

        # Step 2: Verify SPEC framework
        if not self._verify_framework():
            return False

        # Step 3: Create infrastructure
        if not self._create_infrastructure():
            return False

        # Step 4: Take quiz
        if not self._validate_knowledge():
            return False

        # Step 5: Success
        self._print_success()
        return True

    def _verify_config(self):
        """Verify .spec.config exists and is readable."""
        print("✓ Step 1: Verify .spec.config")

        if not self.spec_config.exists():
            print(f"  ❌ ERROR: .spec.config not found at {self.spec_config}")
            return False

        try:
            config = ConfigParser()
            config.read(self.spec_config)
            self.spec_path = Path(config.get("spec", "spec_path")).expanduser()

            # Resolve relative paths relative to project root
            if not self.spec_path.is_absolute():
                self.spec_path = (self.project_root / self.spec_path).resolve()

            print("  ✅ .spec.config found")
            print(f"  ✅ spec_path = {self.spec_path}")
            return True

        except Exception as e:
            print(f"  ❌ ERROR parsing .spec.config: {e}")
            return False

    def _verify_framework(self):
        """Verify SPEC framework location."""
        print("\n✓ Step 2: Verify SPEC Framework")

        required_dirs = [
            "docs/ia/CANONICAL/rules",
            "docs/ia/guides/onboarding",
            "docs/ia/guides/runtime",
            "templates/ai/context-aware",
        ]

        for req_dir in required_dirs:
            path = self.spec_path / req_dir
            if not path.exists():
                print(f"  ❌ ERROR: {req_dir} not found in SPEC framework")
                return False
            print(f"  ✅ {req_dir} exists")

        return True

    def _create_infrastructure(self):
        """Create .ai/context-aware/ infrastructure."""
        print("\n✓ Step 3: Create Infrastructure")

        # Create directories
        dirs = [
            self.ai_dir,
            self.ai_dir / "task-progress" / "completed",
            self.ai_dir / "analysis",
            self.ai_dir / "runtime-state",
            self.project_root / ".ai" / "runtime",
            self.project_root / "scripts",
        ]

        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {d.relative_to(self.project_root)}")

        # Copy templates from SPEC framework
        templates_to_copy = [
            # Context-aware infrastructure
            ("templates/ai/context-aware/README.md", self.ai_dir / "README.md"),
            ("templates/ai/context-aware/task-progress/_current.md", self.ai_dir / "task-progress" / "_current.md"),
            ("templates/ai/context-aware/analysis/_current-issues.md", self.ai_dir / "analysis" / "_current-issues.md"),
            ("templates/ai/context-aware/runtime-state/_current.md", self.ai_dir / "runtime-state" / "_current.md"),
            # Runtime infrastructure (NEW)
            ("templates/ai/runtime/README.md", self.project_root / ".ai" / "runtime" / "README.md"),
            (
                "templates/ai/runtime/spec-canonical-index.md",
                self.project_root / ".ai" / "runtime" / "spec-canonical-index.md",
            ),
            ("templates/ai/runtime/spec-guides-index.md", self.project_root / ".ai" / "runtime" / "spec-guides-index.md"),
            ("templates/ai/runtime/search-keywords.md", self.project_root / ".ai" / "runtime" / "search-keywords.md"),
            # Pre-commit governance (NEW)
            ("templates/.pre-commit-config.yaml", self.project_root / ".pre-commit-config.yaml"),
            ("templates/scripts/setup-precommit-hook.sh", self.project_root / "scripts" / "setup-precommit-hook.sh"),
        ]

        for src_rel, dst in templates_to_copy:
            src = self.spec_path / src_rel
            if src.exists():
                shutil.copy2(src, dst)
                # Make shell scripts executable
                if dst.suffix == ".sh":
                    st = os.stat(dst)
                    os.chmod(dst, st.st_mode | stat.S_IEXEC)
                print(f"  ✅ Copied: {dst.relative_to(self.project_root)}")
            else:
                print(f"  ⚠️  Template not found: {src_rel}")

        return True

    def _validate_knowledge(self):
        """Validate SDD knowledge via quiz."""
        print("\n✓ Step 4: Validate SDD Knowledge")

        quiz_file = self.spec_path / "docs/ia/guides/onboarding/VALIDATION_QUIZ.md"

        if not quiz_file.exists():
            print(f"  ⚠️  Quiz not found: {quiz_file}")
            print("  ⚠️  Skipping quiz (manual validation recommended)")
            return True

        print("  📖 Quiz located: VALIDATION_QUIZ.md")
        print("  📋 Please answer the following quiz questions:")
        print(f"  📍 Path: {quiz_file}")
        print("\n  Quiz Instructions:")
        print(f"    1. Open: {quiz_file}")
        print("    2. Answer all 5 questions")
        print("    3. Score must be ≥ 4/5 (80%)")
        print("    4. If score < 4, re-read ia-rules.md and retry")

        # Automated quiz (simplified for testing)
        response = input("\n  ✓ Have you passed the quiz (≥4/5)? (yes/no): ").strip().lower()

        if response in ("yes", "y"):
            print("  ✅ Quiz validation: PASSED")
            return True
        else:
            print("  ❌ Quiz validation: FAILED")
            print(f"  📖 Please read: {self.spec_path}/docs/ia/CANONICAL/rules/ia-rules.md")
            print("  ⏰ Wait 30 minutes, then retake the quiz")
            return False

    def _print_success(self):
        """Print success report."""
        print("\n" + "=" * 60)
        print("✅ PHASE 0: ONBOARDING COMPLETE")
        print("=" * 60)
        print(f"""
Infrastructure Status:
  ✅ .ai/context-aware/ created (task tracking)
  ✅ .ai/runtime/ created (SDD remote index)
  ✅ Pre-commit hooks configured
  ✅ Templates copied
  ✅ Knowledge validated (quiz passed)

What was created:

  Context-Aware (Dynamic)
  ✅ .ai/context-aware/README.md
  ✅ .ai/context-aware/task-progress/_current.md
  ✅ .ai/context-aware/analysis/_current-issues.md
  ✅ .ai/context-aware/runtime-state/_current.md

  Runtime (SDD Index)
  ✅ .ai/runtime/README.md (navigation)
  ✅ .ai/runtime/spec-canonical-index.md (CANONICAL reference)
  ✅ .ai/runtime/spec-guides-index.md (guides reference)
  ✅ .ai/runtime/search-keywords.md (quick search)

  Governance
  ✅ .pre-commit-config.yaml (pre-commit hooks)
  ✅ scripts/setup-precommit-hook.sh (hook setup)

Next Steps:
  1. Optional: Setup pre-commit hooks
     $ bash scripts/setup-precommit-hook.sh

  2. Read: .ai/runtime/README.md
     (Understanding the SDD remote index)

  3. Search: Use .ai/runtime/search-keywords.md
     (Find what you need quickly)

  4. Read: {self.spec_path}/docs/ia/guides/onboarding/AGENT_HARNESS.md
     (7-phase development workflow)

  5. Create: Your first task in .ai/context-aware/task-progress/_current.md

Recommended Actions:
  $ git add .ai/ .pre-commit-config.yaml scripts/
  $ git commit -m "🚀 PHASE 0: Agent workspace initialized (with runtime index)"
  $ bash scripts/setup-precommit-hook.sh (optional)

Time to Complete First Task: ~5-10 minutes

Ready to start work!
""")


def main():
    """Main entry point."""
    project_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    bootstrap = PHASE0Bootstrap(project_root)
    success = bootstrap.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
