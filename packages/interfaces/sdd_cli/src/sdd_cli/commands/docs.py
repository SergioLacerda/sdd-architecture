import subprocess
from pathlib import Path
import shutil

import typer

app = typer.Typer(help="Documentation commands")


@app.command("deploy")
def deploy(force: bool = typer.Option(True, help="Force deploy to gh-pages")) -> None:
    """Deploy MkDocs documentation if mkdocs config exists."""
    config_files = [Path("mkdocs.yml"), Path("mkdocs.yaml")]
    if not any(cfg.exists() for cfg in config_files):
        typer.echo("No mkdocs config found (mkdocs.yml/mkdocs.yaml). Skipping docs deploy.")
        return

    if shutil.which("mkdocs") is None:
        typer.echo("❌ mkdocs command not found. Install with: pip install mkdocs mkdocs-material")
        raise typer.Exit(1)

    cmd = ["mkdocs", "gh-deploy"]
    if force:
        cmd.append("--force")

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as err:
        raise typer.Exit(err.returncode) from err
