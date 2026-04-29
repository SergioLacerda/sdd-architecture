import subprocess
from pathlib import Path

import typer

app = typer.Typer(help="Documentation commands")


@app.command("deploy")
def deploy(force: bool = typer.Option(True, help="Force deploy to gh-pages")) -> None:
    """Deploy MkDocs documentation if mkdocs config exists."""
    config_files = [Path("mkdocs.yml"), Path("mkdocs.yaml")]
    if not any(cfg.exists() for cfg in config_files):
        typer.echo("No mkdocs config found (mkdocs.yml/mkdocs.yaml). Skipping docs deploy.")
        return

    cmd = ["mkdocs", "gh-deploy"]
    if force:
        cmd.append("--force")

    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise typer.Exit(result.returncode)
