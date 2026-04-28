from pathlib import Path

import typer
from sdd_integration.engine.integration_engine import IntegrationEngine

app = typer.Typer()

_DEFAULT_SPEC = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "features"
    / "sdd_integration"
    / "src"
    / "sdd_integration"
    / "protocol"
    / "integration_flow.yaml"
)

_SPEC_OPTION = typer.Option(
    _DEFAULT_SPEC,
    exists=True,
    file_okay=True,
    dir_okay=False,
    readable=True,
    help="Path to integration flow spec",
)


@app.command()
def run(
    spec: Path = _SPEC_OPTION,
):
    """Run SDD diagnostics (integration flow)"""

    typer.echo("🔍 Running SDD Doctor...\n")

    engine = IntegrationEngine(str(spec))
    report = engine.run()

    typer.echo(report.pretty())

    if report.score() < 100:
        raise typer.Exit(1)
