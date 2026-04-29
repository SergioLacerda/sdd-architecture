"""Environment and path utilities for cross-platform CLI execution."""

from pathlib import Path


def is_repo_root(path: Path) -> bool:
    required = [
        path / "pyproject.toml",
        path / "packages" / "core" / "sdd_core" / "pyproject.toml",
        path / "packages" / "interfaces" / "sdd_cli" / "pyproject.toml",
    ]
    return all(p.exists() for p in required)


def detect_repo_root() -> Path:
    cwd = Path.cwd().resolve()
    for candidate in (cwd, *cwd.parents):
        if is_repo_root(candidate):
            return candidate

    file_path = Path(__file__).resolve()
    for candidate in file_path.parents:
        if is_repo_root(candidate):
            return candidate

    raise RuntimeError("Could not locate sdd-architecture repository root")


def resolve_venv_python(venv_dir: Path) -> Path:
    linux_python = venv_dir / "bin" / "python"
    if linux_python.exists():
        return linux_python

    windows_python = venv_dir / "Scripts" / "python.exe"
    if windows_python.exists():
        return windows_python

    raise RuntimeError("Could not find virtualenv python executable")


def resolve_venv_sdd(venv_dir: Path) -> Path:
    linux_sdd = venv_dir / "bin" / "sdd"
    if linux_sdd.exists():
        return linux_sdd

    windows_sdd = venv_dir / "Scripts" / "sdd.exe"
    if windows_sdd.exists():
        return windows_sdd

    raise RuntimeError("Could not find sdd executable in virtualenv")
