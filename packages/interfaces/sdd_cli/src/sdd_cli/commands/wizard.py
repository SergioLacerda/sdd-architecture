import typer

app = typer.Typer()


@app.command()
def run():
    """Run SDD wizard"""

    try:
        from sdd_wizard.main import run_wizard
    except ImportError as err:
        typer.echo("❌ sdd-wizard not installed")
        typer.echo("👉 Run: sdd setup run")
        raise typer.Exit(1) from err

    run_wizard()
