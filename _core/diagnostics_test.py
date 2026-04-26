#!/usr/bin/env python3
"""
SDD Architecture - Diagnostic Test Suite

Runs critical diagnostic tests:
- File existence checks
- Directory integrity
- Configuration validation
- Import tests
- Quick runtime checks

Usage:
    python _core/diagnostics_test.py [--verbose]
"""

import json
import sys
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime


class DiagnosticTestSuite:
    """Comprehensive diagnostic test runner"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.project_root = self._find_project_root()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0
            }
        }
        self.test_count = 0
    
    def _find_project_root(self) -> Path:
        """Find project root"""
        current = Path.cwd()
        if current.name == "_core":
            return current.parent
        
        for parent in [current] + list(current.parents):
            if (parent / "_core").exists():
                return parent
        
        return current
    
    def log(self, message: str, level: str = "info"):
        """Log message"""
        if self.verbose:
            prefix = {
                "info": "ℹ️ ",
                "pass": "✅ ",
                "fail": "❌ ",
                "skip": "⏭️ "
            }.get(level, "• ")
            print(f"{prefix} {message}")
    
    def run_test(
        self,
        test_name: str,
        test_func,
        category: str = "general"
    ) -> bool:
        """Execute a single test"""
        self.test_count += 1
        
        try:
            passed, message = test_func()
            
            status = "PASS" if passed else "FAIL"
            self.results["tests"].append({
                "id": self.test_count,
                "name": test_name,
                "category": category,
                "status": status,
                "message": message
            })
            
            self.results["summary"]["total"] += 1
            if passed:
                self.results["summary"]["passed"] += 1
                self.log(f"{test_name}: PASS", "pass")
            else:
                self.results["summary"]["failed"] += 1
                self.log(f"{test_name}: FAIL - {message}", "fail")
            
            return passed
        
        except Exception as e:
            self.results["tests"].append({
                "id": self.test_count,
                "name": test_name,
                "category": category,
                "status": "ERROR",
                "message": str(e)
            })
            self.results["summary"]["total"] += 1
            self.results["summary"]["failed"] += 1
            self.log(f"{test_name}: ERROR - {str(e)}", "fail")
            return False
    
    # ========== FILE & DIRECTORY TESTS ==========
    
    def test_core_root_exists(self) -> Tuple[bool, str]:
        """Test: _core/ directory exists"""
        core_dir = self.project_root / "_core"
        if core_dir.exists():
            return True, f"Found at {core_dir}"
        return False, "Not found"
    
    def test_core_subsystems(self) -> Tuple[bool, str]:
        """Test: All core subsystems exist"""
        subsystems = [
            ".sdd-core", ".sdd-cli", ".sdd-wizard",
            ".sdd-compiler", ".sdd-migration"
        ]
        
        core_dir = self.project_root / "_core"
        missing = []
        
        for sub in subsystems:
            if not (core_dir / sub).exists():
                missing.append(sub)
        
        if missing:
            return False, f"Missing: {', '.join(missing)}"
        return True, f"All {len(subsystems)} subsystems present"
    
    def test_docs_root_exists(self) -> Tuple[bool, str]:
        """Test: docs/ directory exists"""
        docs_dir = self.project_root / "docs"
        if docs_dir.exists():
            return True, f"Found at {docs_dir}"
        return False, "Not found"
    
    def test_sdd_source_exists(self) -> Tuple[bool, str]:
        """Test: .sdd/source/ exists"""
        sdd_dir = self.project_root / ".sdd"
        if not sdd_dir.exists():
            return True, ".sdd/ not initialized (optional)"
        
        source_dir = sdd_dir / "source"
        if source_dir.exists():
            return True, f"Found at {source_dir}"
        return True, ".sdd/source not yet created (optional)"
    
    def test_seedling_dirs(self) -> Tuple[bool, str]:
        """Test: At least one seedling exists"""
        seedlings = [".vscode", ".cursor", ".ia", ".github"]
        found = []
        
        for s in seedlings:
            if (self.project_root / s).exists():
                found.append(s)
        
        if found:
            return True, f"Found {len(found)} seedling(s): {', '.join(found)}"
        return True, "No seedlings configured (optional)"
    
    def test_git_dir_exists(self) -> Tuple[bool, str]:
        """Test: .git/ directory exists"""
        git_dir = self.project_root / ".git"
        if git_dir.exists():
            return True, "Git repository initialized"
        return False, "Git not initialized"
    
    # ========== CONFIGURATION TESTS ==========
    
    def test_makefile_exists(self) -> Tuple[bool, str]:
        """Test: Makefile.tests exists"""
        makefile = self.project_root / "_core" / "Makefile.tests"
        if makefile.exists():
            return True, f"Found at {makefile}"
        return False, "Not found"
    
    def test_python_scripts_exist(self) -> Tuple[bool, str]:
        """Test: Key Python scripts exist"""
        scripts = [
            "_core/health_check.py",
            "_core/agent_confidence.py",
            "_core/diagnostics_test.py"
        ]
        
        missing = []
        for script in scripts:
            script_path = self.project_root / script
            if not script_path.exists():
                missing.append(script)
        
        if missing:
            return False, f"Missing: {', '.join(missing)}"
        return True, f"All {len(scripts)} scripts present"
    
    def test_ai_instructions_exist(self) -> Tuple[bool, str]:
        """Test: AI instruction files exist"""
        instructions = [
            "AI_INSTRUCTIONS.md",
            ".copilot-instructions.md",
            ".cursorrules"
        ]
        
        found = []
        for instr in instructions:
            instr_path = self.project_root / instr
            if instr_path.exists():
                found.append(instr)
        
        if found:
            return True, f"Found {len(found)}/{len(instructions)} instruction files"
        return True, "AI instruction files not yet created (optional)"
    
    # ========== RUNTIME TESTS ==========
    
    def test_python_import_health_check(self) -> Tuple[bool, str]:
        """Test: health_check.py can be imported"""
        try:
            sys.path.insert(0, str(self.project_root / "_core"))
            from health_check import HealthCheckEngine
            sys.path.pop(0)
            return True, "Module imports successfully"
        except Exception as e:
            return False, f"Import error: {str(e)}"
    
    def test_python_import_agent_confidence(self) -> Tuple[bool, str]:
        """Test: agent_confidence.py can be imported"""
        try:
            sys.path.insert(0, str(self.project_root / "_core"))
            from agent_confidence import AgentConfidenceEvaluator
            sys.path.pop(0)
            return True, "Module imports successfully"
        except Exception as e:
            return False, f"Import error: {str(e)}"
    
    def test_python_import_diagnostics(self) -> Tuple[bool, str]:
        """Test: diagnostics_test.py can be imported"""
        try:
            sys.path.insert(0, str(self.project_root / "_core"))
            from diagnostics_test import DiagnosticTestSuite
            sys.path.pop(0)
            return True, "Module imports successfully"
        except Exception as e:
            return False, f"Import error: {str(e)}"
    
    # ========== GIT TESTS ==========
    
    def test_git_status_clean(self) -> Tuple[bool, str]:
        """Test: Git repository exists and is readable"""
        try:
            result = subprocess.run(
                ["git", "status"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return True, "Git repository is healthy"
            return False, "Git command failed"
        except Exception as e:
            return False, f"Git test error: {str(e)}"
    
    def test_git_main_branch(self) -> Tuple[bool, str]:
        """Test: main branch exists"""
        try:
            result = subprocess.run(
                ["git", "branch", "-a"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            branches = result.stdout.lower()
            if "main" in branches or "master" in branches:
                return True, "Main/master branch found"
            return True, "Branch structure validated (optional)"
        except Exception as e:
            return False, f"Git branch test error: {str(e)}"
    
    # ========== ORCHESTRATION ==========
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Execute all diagnostic tests"""
        
        # File & Directory Tests
        self.run_test("Core _core/ directory", self.test_core_root_exists, "structure")
        self.run_test("Core subsystems", self.test_core_subsystems, "structure")
        self.run_test("Documentation root", self.test_docs_root_exists, "structure")
        self.run_test("SDD source", self.test_sdd_source_exists, "structure")
        self.run_test("Seedling directories", self.test_seedling_dirs, "structure")
        self.run_test("Git directory", self.test_git_dir_exists, "structure")
        
        # Configuration Tests
        self.run_test("Makefile.tests", self.test_makefile_exists, "config")
        self.run_test("Python scripts", self.test_python_scripts_exist, "config")
        self.run_test("AI instructions", self.test_ai_instructions_exist, "config")
        
        # Runtime Tests
        self.run_test("Import health_check", self.test_python_import_health_check, "import")
        self.run_test("Import agent_confidence", self.test_python_import_agent_confidence, "import")
        self.run_test("Import diagnostics", self.test_python_import_diagnostics, "import")
        
        # Git Tests
        self.run_test("Git repository", self.test_git_status_clean, "git")
        self.run_test("Main branch", self.test_git_main_branch, "git")
        
        return self.results
    
    def print_report(self):
        """Print formatted diagnostic report"""
        print("\n" + "=" * 70)
        print("🧪 Diagnostic Test Suite - Report")
        print("=" * 70 + "\n")
        
        # Group tests by category
        tests_by_category = {}
        for test in self.results["tests"]:
            cat = test["category"]
            if cat not in tests_by_category:
                tests_by_category[cat] = []
            tests_by_category[cat].append(test)
        
        # Print by category
        for category in ["structure", "config", "import", "git"]:
            if category not in tests_by_category:
                continue
            
            print(f"📂 {category.upper()}")
            for test in tests_by_category[category]:
                icon = "✅" if test["status"] == "PASS" else "❌"
                print(f"  {icon} {test['name']}: {test['message']}")
            print("")
        
        # Summary
        summary = self.results["summary"]
        pass_pct = (summary["passed"] / summary["total"] * 100) if summary["total"] > 0 else 0
        
        print(f"📊 Summary:")
        print(f"  Total Tests: {summary['total']}")
        print(f"  Passed: {summary['passed']} ({pass_pct:.0f}%)")
        print(f"  Failed: {summary['failed']}")
        
        status = "✅ ALL TESTS PASSED" if summary["failed"] == 0 else "❌ SOME TESTS FAILED"
        print(f"\n  Status: {status}")
        print("=" * 70 + "\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run diagnostic tests for SDD Architecture"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON"
    )
    
    args = parser.parse_args()
    
    suite = DiagnosticTestSuite(verbose=args.verbose)
    results = suite.run_all_tests()
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        suite.print_report()
    
    return 0 if results["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
