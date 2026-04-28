#!/usr/bin/env python3
"""
SDD Architecture - Health Check Engine (Relocated to tools/)
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Tuple


class HealthCheckEngine:
    """Core health check validator for SDD Architecture"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.project_root = self._find_project_root()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "checks": {},
            "summary": {"total": 0, "passed": 0, "failed": 0, "warnings": 0},
            "status": "UNKNOWN",
        }

    def _find_project_root(self) -> Path:
        """Find project root by looking for packages directory"""
        current = Path(__file__).resolve().parent
        # Search up the tree from tools/ location
        for parent in [current] + list(current.parents):
            if (parent / "packages").exists() and (parent / "_spec").exists():
                return parent
        return current.parent.parent  # Fallback

    def log(self, message: str, level: str = "info"):
        if self.verbose:
            prefix = {"info": "ℹ️ ", "ok": "✅ ", "error": "❌ ", "warning": "⚠️ "}.get(level, "• ")
            print(f"{prefix} {message}")

    def check_git_status(self) -> Tuple[bool, str]:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"], cwd=self.project_root, capture_output=True, text=True, timeout=5
            )
            if result.returncode != 0:
                return False, "Not a git repository"
            return True, "Git repository is healthy"
        except Exception as e:
            return False, f"Git check failed: {str(e)}"

    def checkpackages_structure(self) -> Tuple[bool, str]:
        required = ["core", "wizard", "compiler"]
        core_dir = self.project_root / "packages"
        missing = [s for s in required if not (core_dir / s).exists()]
        if missing:
            return False, f"Missing subsystems: {', '.join(missing)}"
        return True, "Core structure is valid"

    def check_python_version(self) -> Tuple[bool, str]:
        v = sys.version_info
        if v.major < 3 or (v.major == 3 and v.minor < 10):
            return False, f"Python {v.major}.{v.minor} (requires 3.10+)"
        return True, f"Python {v.major}.{v.minor}.{v.micro}"

    def run_all_checks(self) -> Dict[str, Any]:
        checks = [
            ("Git Status", self.check_git_status),
            ("Core Structure", self.checkpackages_structure),
            ("Python Version", self.check_python_version),
        ]
        for name, func in checks:
            passed, msg = func()
            self.results["checks"][name] = {"status": "PASS" if passed else "FAIL", "message": msg}
            self.results["summary"]["total"] += 1
            if passed:
                self.results["summary"]["passed"] += 1
            else:
                self.results["summary"]["failed"] += 1

        self.results["status"] = "OPERATIONAL ✅" if self.results["summary"]["failed"] == 0 else "FAILED ❌"
        return self.results


if __name__ == "__main__":
    engine = HealthCheckEngine(verbose="--verbose" in sys.argv)
    res = engine.run_all_checks()
    if "--json" in sys.argv:
        print(json.dumps(res, indent=2))
    else:
        print(f"\n🎯 Overall Status: {res['status']}\n")
        for k, v in res["checks"].items():
            print(f"  {'✅' if v['status'] == 'PASS' else '❌'} {k}: {v['message']}")
    sys.exit(0 if res["summary"]["failed"] == 0 else 1)
