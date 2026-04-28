"""Version command for SDD CLI."""

import typer

__version__ = "3.0.0"

app = typer.Typer()


@app.command()
def show():
    """Show SDD version."""
    typer.echo(f"SDD Version: {__version__}")
