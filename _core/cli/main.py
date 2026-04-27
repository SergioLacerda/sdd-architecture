"""Main Typer application entry point."""

import typer

from cli.commands import governance

app = typer.Typer(name="sdd", help="SDD (Self-Documented Domain) governance CLI", pretty_exceptions_enable=False)

# Add command groups
app.add_typer(governance.app, name="governance", help="Governance management commands")


@app.command()
def version() -> None:
    """Display CLI version."""
    from cli import __version__

    typer.echo(f"sdd version {__version__}")


if __name__ == "__main__":
    app()
