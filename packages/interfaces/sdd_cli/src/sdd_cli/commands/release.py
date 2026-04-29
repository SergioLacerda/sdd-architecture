import subprocess
import sys
import importlib.util

import typer

app = typer.Typer(help="Release commands")


@app.command("build")
def build() -> None:
    """Build release artifacts into dist/."""
    if importlib.util.find_spec("build") is None:
        typer.echo("❌ Python package 'build' not installed. Install with: pip install build")
        raise typer.Exit(1)

    try:
        subprocess.run([sys.executable, "-m", "build"], check=True)
    except subprocess.CalledProcessError as err:
        raise typer.Exit(err.returncode) from err
