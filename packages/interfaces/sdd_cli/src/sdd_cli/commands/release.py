import subprocess
import sys

import typer

app = typer.Typer(help="Release commands")


@app.command("build")
def build() -> None:
    """Build release artifacts into dist/."""
    result = subprocess.run([sys.executable, "-m", "build"])
    if result.returncode != 0:
        raise typer.Exit(result.returncode)
