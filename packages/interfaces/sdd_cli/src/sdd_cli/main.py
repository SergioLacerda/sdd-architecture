import typer

from sdd_cli.commands import bootstrap, doctor, governance, lint, setup, test, wizard

app = typer.Typer(help="SDD CLI - Spec Driven Development Toolkit")

# 🔥 Subcommands (cada um já é um Typer app)
app.add_typer(setup.app, name="setup", help="Setup environment")
app.add_typer(test.app, name="test", help="Run test pipeline")
app.add_typer(lint.app, name="lint", help="Run lint checks")
app.add_typer(wizard.app, name="wizard", help="Run wizard")
app.add_typer(governance.app, name="governance", help="Governance operations")
app.add_typer(doctor.app, name="doctor")
app.add_typer(bootstrap.app, name="bootstrap")


@app.command()
def version():
    """Show SDD version."""
    typer.echo("SDD Version: 3.0.0")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
