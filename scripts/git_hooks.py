#!/usr/bin/env python3
"""Cross-platform manager for SDD git hooks."""

from __future__ import annotations

import argparse
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Iterable

HOOKS = ("pre-commit", "pre-push", "post-merge")
MARKER = "SDD Architecture Hook"


def _repo_root_from_cwd() -> Path:
    result = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("Not a git repository")
    return Path(result.stdout.strip()).resolve()


def _repo_root_from_hook_file(hook_file: Path) -> Path:
    return hook_file.resolve().parents[2]


def _git_dir(repo_root: Path) -> Path:
    result = subprocess.run(["git", "rev-parse", "--git-dir"], cwd=repo_root, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError("Could not resolve .git directory")
    git_dir = Path(result.stdout.strip())
    if not git_dir.is_absolute():
        git_dir = (repo_root / git_dir).resolve()
    return git_dir


def _hooks_dir(repo_root: Path) -> Path:
    return _git_dir(repo_root) / "hooks"


def _best_python(repo_root: Path) -> str:
    venv_python_unix = repo_root / ".venv" / "bin" / "python"
    if venv_python_unix.exists():
        return str(venv_python_unix)
    venv_python_win = repo_root / ".venv" / "Scripts" / "python.exe"
    if venv_python_win.exists():
        return str(venv_python_win)
    return sys.executable


def _resolve_sdd(repo_root: Path) -> list[str] | None:
    venv_sdd_unix = repo_root / ".venv" / "bin" / "sdd"
    if venv_sdd_unix.exists():
        return [str(venv_sdd_unix)]
    venv_sdd_win = repo_root / ".venv" / "Scripts" / "sdd.exe"
    if venv_sdd_win.exists():
        return [str(venv_sdd_win)]

    if shutil.which("sdd"):
        return ["sdd"]

    venv_python_unix = repo_root / ".venv" / "bin" / "python"
    if venv_python_unix.exists():
        return [str(venv_python_unix), "-m", "sdd_cli.main"]
    venv_python_win = repo_root / ".venv" / "Scripts" / "python.exe"
    if venv_python_win.exists():
        return [str(venv_python_win), "-m", "sdd_cli.main"]
    return None


def _resolve_health_script(repo_root: Path) -> Path | None:
    candidates = [
        repo_root / "tools" / "health" / "health_check.py",
        repo_root / "packages" / "tools" / "health_check.py",
        repo_root / "packages" / "health_check.py",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _run_command(cmd: list[str], cwd: Path, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, capture_output=capture, text=True)


def _write_hook_file(path: Path, hook_name: str) -> None:
    content = f"""#!/usr/bin/env python3
# {MARKER}
import runpy
import sys
from pathlib import Path

HOOK_FILE = Path(__file__).resolve()
REPO_ROOT = HOOK_FILE.parents[2]
SCRIPT = REPO_ROOT / "scripts" / "git_hooks.py"
if not SCRIPT.exists():
    print("✗ Missing scripts/git_hooks.py")
    raise SystemExit(1)
sys.argv = [str(SCRIPT), "run-hook", "{hook_name}"]
runpy.run_path(str(SCRIPT), run_name="__main__")
"""
    path.write_text(content, encoding="utf-8")
    current_mode = path.stat().st_mode
    path.chmod(current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def install_hooks() -> int:
    repo_root = _repo_root_from_cwd()
    hooks_dir = _hooks_dir(repo_root)
    hooks_dir.mkdir(parents=True, exist_ok=True)

    installed = 0
    for hook_name in HOOKS:
        target = hooks_dir / hook_name
        _write_hook_file(target, hook_name)
        print(f"✓ Installed: {hook_name}")
        installed += 1
    print(f"\nInstalled {installed}/{len(HOOKS)} hooks")
    return 0


def uninstall_hooks() -> int:
    repo_root = _repo_root_from_cwd()
    hooks_dir = _hooks_dir(repo_root)
    removed = 0

    for hook_name in HOOKS:
        target = hooks_dir / hook_name
        if not target.exists():
            continue
        content = target.read_text(encoding="utf-8", errors="ignore")
        if MARKER in content:
            target.unlink()
            print(f"✓ Removed: {hook_name}")
            removed += 1
        else:
            print(f"⚠ Skipped: {hook_name} (not an SDD hook)")
    print(f"\nRemoved {removed} hooks")
    return 0


def _pre_commit(repo_root: Path) -> int:
    branch = _run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_root, capture=True).stdout.strip()
    staged = _run_command(["git", "diff", "--cached", "--name-only"], cwd=repo_root, capture=True).stdout.strip().splitlines()

    print("INFO ADR-008: Code Review Workflow")
    print(f"Current branch: {branch}\n")
    if branch == "main":
        print("WARNING: main branch requires PR review + architect approval\n")

    critical_patterns: Iterable[str] = (
        "_spec/architecture/decisions/ADR-007",
        "_spec/architecture/decisions/ADR-008",
        "spec/architecture/decisions/ADR-007",
        "spec/architecture/decisions/ADR-008",
        "packages/features/migration/phase-archive/DECISIONS.md",
        "packages/features/migration/PHASES.md",
    )
    staged_text = "\n".join(staged)
    for pattern in critical_patterns:
        if pattern in staged_text:
            print(f"CAUTION: Modifying critical file: {pattern}")
            print("  -> Requires explicit review in PR\n")

    if staged:
        print("Staged files:")
        for file_name in staged:
            print(f"  + {file_name}")
    else:
        print("No staged files.")

    print("\nNext steps:")
    print("  1. Commit staged changes")
    print("  2. Push to origin")
    print("  3. Open/update PR when required\n")
    return 0


def _pre_push(repo_root: Path) -> int:
    print("[PRE-PUSH] Starting final validation before push...")
    python_bin = _best_python(repo_root)
    health_script = _resolve_health_script(repo_root)
    if health_script is None:
        print("✗ Health check script not found")
        return 1

    sdd_cmd = _resolve_sdd(repo_root)
    if sdd_cmd is None:
        print("✗ sdd CLI command not found")
        print("  Install and setup first (sdd setup run)")
        return 1

    print("→ Running full health check (fresh, no cache)...")
    health = _run_command([python_bin, str(health_script)], cwd=repo_root, capture=True)
    if health.returncode != 0:
        print("✗ Health check command failed")
        print(health.stdout + health.stderr)
        return 1
    if "FAILED" in (health.stdout + health.stderr):
        print("✗ Health check failed")
        print(health.stdout + health.stderr)
        return 1
    print("✓ Health check passed")

    print("→ Running governance validation...")
    gov = _run_command([*sdd_cmd, "governance", "validate"], cwd=repo_root, capture=True)
    if gov.returncode != 0:
        print("✗ Governance validation failed")
        print(gov.stdout + gov.stderr)
        return 1
    print("✓ Governance validation passed")

    branch = _run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_root, capture=True).stdout.strip()
    upstream = _run_command(["git", "rev-parse", "--abbrev-ref", "@{u}"], cwd=repo_root, capture=True)
    if upstream.returncode == 0:
        commit_count = _run_command(["git", "rev-list", "--count", "@{u}..HEAD"], cwd=repo_root, capture=True).stdout.strip()
    else:
        commit_count = "(no upstream)"

    print(f"→ Summary for branch '{branch}':")
    print(f"  Commits to push: {commit_count}")
    print("  Health: ✓ Healthy")
    print("  Governance: ✓ Validated")
    print("[PRE-PUSH] All checks passed. Push allowed.\n")
    return 0


def _post_merge(repo_root: Path) -> int:
    print("[POST-MERGE] Updating governance cache...")
    cache_file = repo_root / "packages" / ".sdd" / "agent_state.json"
    if cache_file.exists():
        cache_file.unlink()
        print("✓ Cache cleared")

    health_script = _resolve_health_script(repo_root)
    if health_script is not None:
        python_bin = _best_python(repo_root)
        print("→ Warming up cache state...")
        _run_command([python_bin, str(health_script)], cwd=repo_root, capture=True)
        print("✓ Cache warmed")

    print("[POST-MERGE] Cache updated successfully.\n")
    return 0


def run_hook(hook_name: str, repo_root: Path | None = None) -> int:
    root = repo_root or _repo_root_from_cwd()
    if hook_name == "pre-commit":
        return _pre_commit(root)
    if hook_name == "pre-push":
        return _pre_push(root)
    if hook_name == "post-merge":
        return _post_merge(root)
    print(f"Unknown hook: {hook_name}")
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage SDD git hooks")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("install", help="Install SDD hooks")
    subparsers.add_parser("uninstall", help="Uninstall SDD hooks")

    run_hook_parser = subparsers.add_parser("run-hook", help="Run a specific hook")
    run_hook_parser.add_argument("hook_name", choices=HOOKS)

    args = parser.parse_args()
    if args.command == "install":
        return install_hooks()
    if args.command == "uninstall":
        return uninstall_hooks()
    if args.command == "run-hook":
        return run_hook(args.hook_name)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
