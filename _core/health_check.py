#!/usr/bin/env python3
"""
SDD Architecture - Health Check Engine

Validates project health:
- Git status and branches
- Directory structure integrity
- .sdd/ governance structure
- Python dependencies
- Seedling configurations

Usage:
    python _core/health_check.py [--verbose] [--json]
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any


class HealthCheckEngine:
    """Core health check validator for SDD Architecture"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.project_root = self._find_project_root()
        self.checks = {}
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "checks": {},
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0
            },
            "status": "UNKNOWN"
        }
    
    def _find_project_root(self) -> Path:
        """Find project root by looking for _core directory"""
        current = Path.cwd()
        
        # If already in _core, go up one level
        if current.name == "_core":
            return current.parent
        
        # Search up the tree
        for parent in [current] + list(current.parents):
            if (parent / "_core").exists():
                return parent
        
        # Fallback to cwd
        return current
    
    def log(self, message: str, level: str = "info"):
        """Log message if verbose mode enabled"""
        if self.verbose:
            prefix = {
                "info": "ℹ️ ",
                "ok": "✅ ",
                "error": "❌ ",
                "warning": "⚠️ "
            }.get(level, "• ")
            print(f"{prefix} {message}")
    
    # ========== GIT CHECKS ==========
    
    def check_git_status(self) -> Tuple[bool, str]:
        """Check git repository status"""
        try:
            os.chdir(self.project_root)
            
            # Check if git repo exists
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                return False, "Not a git repository"
            
            # Get current branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                timeout=5
            )
            current_branch = branch_result.stdout.strip()
            
            # Get uncommitted changes count
            status_result = subprocess.run(
                ["git", "status", "--short"],
                capture_output=True,
                text=True,
                timeout=5
            )
            changes = len([l for l in status_result.stdout.strip().split('\n') if l])
            
            message = f"On branch '{current_branch}' with {changes} changes"
            self.log(f"Git status: {message}", "ok")
            
            return True, message
        except Exception as e:
            return False, f"Git check failed: {str(e)}"
    
    def check_git_remote(self) -> Tuple[bool, str]:
        """Check git remote connectivity"""
        try:
            result = subprocess.run(
                ["git", "remote", "-v"],
                capture_output=True,
                text=True,
                timeout=5,
                cwd=self.project_root
            )
            
            if result.returncode == 0 and result.stdout.strip():
                remote_lines = result.stdout.strip().split('\n')
                return True, f"Connected to {len(remote_lines)} remote(s)"
            
            return True, "No remotes configured"
        except Exception as e:
            return False, f"Remote check failed: {str(e)}"
    
    # ========== DIRECTORY STRUCTURE CHECKS ==========
    
    def check_core_structure(self) -> Tuple[bool, str]:
        """Check core subsystem structure"""
        required_subsystems = [
            ".sdd-core",
            ".sdd-cli",
            ".sdd-wizard",
            ".sdd-compiler",
            ".sdd-migration"
        ]
        
        core_dir = self.project_root / "_core"
        missing = []
        
        for subsys in required_subsystems:
            if not (core_dir / subsys).exists():
                missing.append(subsys)
        
        if missing:
            msg = f"Missing subsystems: {', '.join(missing)}"
            self.log(msg, "error")
            return False, msg
        
        self.log("All core subsystems present", "ok")
        return True, f"All {len(required_subsystems)} subsystems found"
    
    def check_docs_structure(self) -> Tuple[bool, str]:
        """Check docs directory structure"""
        docs_dir = self.project_root / "docs"
        
        if not docs_dir.exists():
            return False, "docs/ directory not found"
        
        required_subdirs = [
            "project-status",
            "phases",
            "migration",
            "integration",
            "guides",
            "operations"
        ]
        
        missing = []
        for subdir in required_subdirs:
            if not (docs_dir / subdir).exists():
                missing.append(subdir)
        
        found = len(required_subdirs) - len(missing)
        
        if missing:
            msg = f"docs/ has {found}/{len(required_subdirs)} subdirs (missing: {', '.join(missing)})"
            self.log(msg, "warning")
            return True, msg  # Warning, not failure
        
        self.log(f"docs/ structure complete ({found} dirs)", "ok")
        return True, f"All {len(required_subdirs)} doc subdirs found"
    
    def check_sdd_structure(self) -> Tuple[bool, str]:
        """Check .sdd/ governance structure"""
        sdd_dir = self.project_root / ".sdd"
        
        if not sdd_dir.exists():
            return True, ".sdd/ not yet initialized (optional)"
        
        required_dirs = ["source", "runtime"]
        missing = []
        
        for d in required_dirs:
            if not (sdd_dir / d).exists():
                missing.append(d)
        
        if missing:
            msg = f".sdd/ missing: {', '.join(missing)}"
            self.log(msg, "warning")
            return True, msg  # Warning
        
        self.log(".sdd/ structure valid", "ok")
        return True, ".sdd/ governance structure complete"
    
    def check_seedling_structure(self) -> Tuple[bool, str]:
        """Check seedling directories (.vscode, .cursor, .ia, .github)"""
        seedlings = [".vscode", ".cursor", ".ia", ".github"]
        found = []
        
        for seedling in seedlings:
            if (self.project_root / seedling).exists():
                found.append(seedling)
        
        if not found:
            return True, "No seedlings configured (optional)"
        
        msg = f"Seedlings found: {', '.join(found)}"
        self.log(msg, "ok")
        return True, msg
    
    # ========== DEPENDENCIES CHECKS ==========
    
    def check_python_version(self) -> Tuple[bool, str]:
        """Check Python version (3.8+)"""
        version_info = sys.version_info
        version = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
        
        if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 8):
            return False, f"Python {version} (requires 3.8+)"
        
        self.log(f"Python {version} ✓", "ok")
        return True, f"Python {version}"
    
    def check_required_modules(self) -> Tuple[bool, str]:
        """Check required Python modules"""
        required = ["json", "subprocess", "pathlib"]  # stdlib
        optional = ["msgpack", "yaml"]  # optional
        
        missing_optional = []
        for module in optional:
            try:
                __import__(module)
            except ImportError:
                missing_optional.append(module)
        
        msg = f"Required modules available"
        if missing_optional:
            msg += f" (missing optional: {', '.join(missing_optional)})"
        
        self.log(msg, "ok" if not missing_optional else "warning")
        return True, msg
    
    # ========== GOVERNANCE CHECKS ==========
    
    def check_governance_files(self) -> Tuple[bool, str]:
        """Check compiled governance files"""
        compiled_dir = self.project_root / "_core" / ".sdd-compiled"
        
        if not compiled_dir.exists():
            return True, ".sdd-compiled/ not found (optional)"
        
        # List compiled files
        compiled_files = list(compiled_dir.glob("*.json")) + list(compiled_dir.glob("*.msgpack"))
        
        if not compiled_files:
            return True, ".sdd-compiled/ is empty"
        
        self.log(f"Compiled artifacts: {len(compiled_files)} files", "ok")
        return True, f"Found {len(compiled_files)} governance artifacts"
    
    def check_wizard_state(self) -> Tuple[bool, str]:
        """Check wizard phase state"""
        sdd_gen_dir = self.project_root / "sdd-generated"
        
        if not sdd_gen_dir.exists():
            return True, "Wizard not run yet (optional)"
        
        phases = []
        if (sdd_gen_dir / "phase-2-input").exists():
            phases.append("phase-2")
        if (sdd_gen_dir / "final-output").exists():
            phases.append("phase-3")
        
        if phases:
            self.log(f"Wizard phases: {', '.join(phases)}", "ok")
            return True, f"Wizard completed: {', '.join(phases)}"
        
        return True, "Wizard phases not found"
    
    # ========== ORCHESTRATION ==========
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Execute all health checks"""
        checks_to_run = [
            ("Git Repository", self.check_git_status),
            ("Git Remote", self.check_git_remote),
            ("Core Structure", self.check_core_structure),
            ("Docs Structure", self.check_docs_structure),
            ("SDD Structure", self.check_sdd_structure),
            ("Seedlings", self.check_seedling_structure),
            ("Python Version", self.check_python_version),
            ("Python Modules", self.check_required_modules),
            ("Governance Files", self.check_governance_files),
            ("Wizard State", self.check_wizard_state),
        ]
        
        for check_name, check_func in checks_to_run:
            try:
                passed, message = check_func()
                status = "✅" if passed else "❌"
                
                self.results["checks"][check_name] = {
                    "status": "PASS" if passed else "FAIL",
                    "message": message
                }
                
                self.results["summary"]["total"] += 1
                if passed:
                    self.results["summary"]["passed"] += 1
                else:
                    self.results["summary"]["failed"] += 1
                
                if self.verbose:
                    print(f"{status} {check_name}: {message}")
            
            except Exception as e:
                self.results["checks"][check_name] = {
                    "status": "ERROR",
                    "message": str(e)
                }
                self.results["summary"]["total"] += 1
                self.results["summary"]["failed"] += 1
                if self.verbose:
                    print(f"❌ {check_name}: ERROR - {str(e)}")
        
        # Determine overall status
        if self.results["summary"]["failed"] == 0:
            self.results["status"] = "OPERATIONAL ✅"
        elif self.results["summary"]["failed"] < 3:
            self.results["status"] = "DEGRADED ⚠️"
        else:
            self.results["status"] = "FAILED ❌"
        
        return self.results
    
    def print_report(self):
        """Print formatted health check report"""
        print("\n" + "=" * 60)
        print("🟢 SDD Architecture - Health Check Report")
        print("=" * 60 + "\n")
        
        print(f"📂 Project: {self.project_root}")
        print(f"🕐 Time: {self.results['timestamp']}")
        print("")
        
        print("📋 Check Results:")
        for check_name, result in self.results["checks"].items():
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(f"  {status_icon} {check_name}: {result['message']}")
        
        print("")
        print(f"📊 Summary:")
        print(f"  Total: {self.results['summary']['total']}")
        print(f"  Passed: {self.results['summary']['passed']}")
        print(f"  Failed: {self.results['summary']['failed']}")
        
        print("")
        print(f"🎯 Overall Status: {self.results['status']}")
        print("=" * 60 + "\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="SDD Architecture Health Check"
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
    
    engine = HealthCheckEngine(verbose=args.verbose)
    results = engine.run_all_checks()
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        engine.print_report()
    
    # Exit with status code based on results
    return 0 if results["summary"]["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
