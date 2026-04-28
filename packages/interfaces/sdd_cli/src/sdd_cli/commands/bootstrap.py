import subprocess
import sys
from pathlib import Path

import typer

app = typer.Typer()


def run(cmd):
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise typer.Exit(result.returncode)


@app.command(name="run")
def run_bootstrap():
    """Bootstrap project (venv + install packages)"""

    typer.echo("🚀 Bootstrapping SDD project...")

    python = sys.executable

    if not Path(".venv").exists():
        typer.echo("Creating virtualenv...")
        run([python, "-m", "venv", ".venv"])

    venv_python = Path(".venv/bin/python")
    if not venv_python.exists():
        venv_python = Path(".venv/Scripts/python.exe")

    typer.echo("Installing packages...")

    packages = [
        "packages/features/sdd_integration",
        "packages/interfaces/sdd_cli",
    ]

    for pkg in packages:
        run([str(venv_python), "-m", "pip", "install", "-e", pkg])

    typer.echo("✅ Bootstrap complete!")
