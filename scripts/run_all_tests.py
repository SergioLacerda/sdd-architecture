#!/usr/bin/env python3
"""Cross-platform entrypoint for the SDD test pipeline."""

import argparse
import subprocess
import sys
from pathlib import Path


def detect_repo_root() -> Path:
    cwd = Path.cwd().resolve()
    for candidate in (cwd, *cwd.parents):
        if (candidate / "pyproject.toml").exists() and (candidate / "packages").exists():
            return candidate
    raise RuntimeError("Project root not found")


def ensure_governance_artifacts(repo_root: Path) -> None:
    """Ensure compiled and deployed governance artifacts exist before tests."""
    compiled_dir = repo_root / "compiler" / "compiled"
    runtime_dir = repo_root / "runtime" / "compiled"
    required = [
        compiled_dir / "governance-core.compiled.msgpack",
        compiled_dir / "governance-client-template.compiled.msgpack",
        runtime_dir / "governance-core.compiled.msgpack",
        runtime_dir / "governance-client-template.compiled.msgpack",
    ]
    if all(path.exists() for path in required):
        return

    print("🔧 Preparing governance compiled artifacts...")
    from sdd_compiler.governance_compiler import GovernanceCompiler
    from sdd_core.deployment_manager import DeploymentManager

    compiler = GovernanceCompiler(str(compiled_dir))
    compiler.compile(str(compiled_dir))
    DeploymentManager(str(repo_root)).deploy()


def run_pytest(repo_root: Path, verbose: bool, fail_fast: bool) -> int:
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "tests",
        "packages",
        "--strict-markers",
        "--tb=short",
        "--import-mode=importlib",
        "--ignore-glob=**/test_phase_5_orchestrator.py",
        "--ignore-glob=**/test_phase_5_wizard.py",
        "--ignore-glob=**/templates/tests/phase_5_examples/test_execution_flow.py",
        "--ignore-glob=**/templates/tests/phase_5_examples/test_integration_flow.py",
        "--ignore-glob=**/templates/tests/phase_5_examples/examples/python/test_execution_flow.py",
        "--ignore-glob=**/templates/tests/phase_5_examples/examples/python/test_integration_flow.py",
    ]
    cmd.append("-v" if verbose else "-q")
    if fail_fast:
        cmd.append("-x")

    result = subprocess.run(cmd, cwd=repo_root)
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Run SDD test pipeline (cross-platform)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose pytest output")
    parser.add_argument("-x", "--fail-fast", action="store_true", help="Stop on first failure")
    args = parser.parse_args()

    repo_root = detect_repo_root()
    ensure_governance_artifacts(repo_root)
    return run_pytest(repo_root, verbose=args.verbose, fail_fast=args.fail_fast)


if __name__ == "__main__":
    raise SystemExit(main())
