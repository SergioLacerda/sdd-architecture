import subprocess
import sys
from pathlib import Path

import typer

app = typer.Typer()


def _is_repo_root(path: Path) -> bool:
    required = [
        path / "pyproject.toml",
        path / "packages" / "core" / "sdd_core" / "pyproject.toml",
        path / "packages" / "interfaces" / "sdd_cli" / "pyproject.toml",
    ]
    return all(p.exists() for p in required)


def _detect_repo_root() -> Path:
    cwd = Path.cwd().resolve()
    for candidate in (cwd, *cwd.parents):
        if _is_repo_root(candidate):
            return candidate

    file_path = Path(__file__).resolve()
    for candidate in file_path.parents:
        if _is_repo_root(candidate):
            return candidate

    raise RuntimeError("Could not locate sdd-architecture repository root")


_REPO_ROOT = _detect_repo_root()


def _run(cmd: list[str]) -> None:
    result = subprocess.run(cmd)
    if result.returncode != 0:
        typer.echo(f"❌ Failed: {' '.join(cmd)}")
        raise typer.Exit(1)


@app.command(name="run")
def run_setup() -> None:  # noqa: C901
    """Setup SDD workspace (cross-platform replacement for setup.sh)"""

    typer.echo("🚀 SDD Workspace Setup")
    typer.echo("======================")

    python = sys.executable
    typer.echo(f"✓ Using Python: {python}")

    # Create venv
    venv_dir = _REPO_ROOT / ".venv"
    if not venv_dir.exists():
        typer.echo("✓ Creating virtual environment...")
        _run([python, "-m", "venv", str(venv_dir)])

    # Locate venv python (Linux/Mac or Windows)
    venv_python = venv_dir / "bin" / "python"
    if not venv_python.exists():
        venv_python = venv_dir / "Scripts" / "python.exe"
    if not venv_python.exists():
        typer.echo("❌ Could not find venv python")
        raise typer.Exit(1)

    typer.echo("✓ Virtualenv ready")

    # Upgrade pip (quiet)
    _run([str(venv_python), "-m", "pip", "install", "--upgrade", "pip", "-q"])

    # Install ordered packages
    typer.echo("\n📦 Installing SDD packages...")
    ordered_packages = [
        "packages/core/sdd_core",
        "packages/core/sdd_compiler",
        "packages/features/sdd_integration",
        "packages/interfaces/sdd_wizard",
        "packages/interfaces/sdd_cli",
    ]
    for pkg in ordered_packages:
        pkg_path = _REPO_ROOT / pkg
        if (pkg_path / "pyproject.toml").exists():
            typer.echo(f"  → Installing {pkg}")
            _run([str(venv_python), "-m", "pip", "install", "-e", str(pkg_path)])
        else:
            typer.echo(f"  ⚠ Skipping {pkg} (no pyproject.toml)")

    # Install any extra packages not in the ordered list
    for pkg_path in sorted(_REPO_ROOT.glob("packages/*/*")):
        if not (pkg_path / "pyproject.toml").exists():
            continue
        relative = str(pkg_path.relative_to(_REPO_ROOT))
        if relative not in ordered_packages:
            typer.echo(f"  → Installing (extra) {relative}")
            _run([str(venv_python), "-m", "pip", "install", "-e", str(pkg_path)])

    # Install dev dependencies from root
    if (_REPO_ROOT / "pyproject.toml").exists():
        typer.echo("\n🧪 Installing dev dependencies...")
        _run([str(venv_python), "-m", "pip", "install", "-e", f"{_REPO_ROOT}[dev]", "-q"])

    # Validate imports
    typer.echo("\n🔍 Validating Python imports...")
    for module in ("sdd_core", "sdd_wizard", "sdd_cli"):
        result = subprocess.run(
            [str(venv_python), "-c", f"import {module}"],
            capture_output=True,
        )
        if result.returncode == 0:
            typer.echo(f"  ✓ {module} OK")
        else:
            typer.echo(f"  ❌ {module} FAILED")
            raise typer.Exit(1)

    # Validate CLI
    typer.echo("\n🔍 Validating CLI...")
    venv_sdd = venv_dir / "bin" / "sdd"
    if not venv_sdd.exists():
        venv_sdd = venv_dir / "Scripts" / "sdd.exe"
    if not venv_sdd.exists():
        typer.echo("  ❌ sdd CLI not found in venv")
        raise typer.Exit(1)
    typer.echo("  ✓ sdd command available")

    result = subprocess.run([str(venv_sdd), "--help"], capture_output=True)
    if result.returncode != 0:
        typer.echo("  ❌ CLI not responding")
        raise typer.Exit(1)
    typer.echo("  ✓ CLI responding")

    typer.echo("\n🎉 Setup completed!")
