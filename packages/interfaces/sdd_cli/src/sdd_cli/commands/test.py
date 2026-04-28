import subprocess
from pathlib import Path

import typer

app = typer.Typer()


def find_project_root() -> Path:
    current = Path(__file__).resolve()

    for parent in current.parents:
        if (parent / "scripts" / "run-all-tests.sh").exists():
            return parent

    raise RuntimeError("Project root not found")


class TestCommand:
    def run(self):
        root = find_project_root()

        script = root / "scripts" / "run-all-tests.sh"

        if not script.exists():
            typer.echo(f"❌ Script not found: {script}")
            raise typer.Exit(1)

        typer.echo(f"▶ Running tests from: {script}")

        subprocess.run(["bash", str(script)], check=True)


@app.command()
def run():
    """Run full test pipeline"""
    TestCommand().run()
