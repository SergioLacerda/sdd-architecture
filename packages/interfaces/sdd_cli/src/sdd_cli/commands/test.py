import subprocess
import sys

import typer
from sdd_cli.utils.environment import detect_repo_root

app = typer.Typer()


class TestCommand:
    def run(self, verbose: bool, fail_fast: bool) -> None:
        root = detect_repo_root()
        script = root / "scripts" / "run_all_tests.py"

        if not script.exists():
            typer.echo(f"❌ Script not found: {script}")
            raise typer.Exit(1)

        cmd = [sys.executable, str(script)]

        if verbose:
            cmd.append("--verbose")
        if fail_fast:
            cmd.append("--fail-fast")

        typer.echo(f"▶ Running tests from: {script}")

        result = subprocess.run(cmd, cwd=root)
        if result.returncode != 0:
            raise typer.Exit(result.returncode)


@app.command()
def run(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose pytest output"),
    fail_fast: bool = typer.Option(False, "--fail-fast", "-x", help="Stop on first failure"),
) -> None:
    """Run full test pipeline"""
    TestCommand().run(verbose=verbose, fail_fast=fail_fast)
