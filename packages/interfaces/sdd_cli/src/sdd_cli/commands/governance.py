"""Governance management commands."""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from sdd_cli.generators.agent_seeds import generate_agent_seeds
from sdd_cli.utils.loader import get_governance_summary, load_governance_config, validate_governance_path

app = typer.Typer(help="Governance management commands")
console = Console()


@app.command()
def load(path: str = typer.Option("runtime", help="Path to governance configuration (runtime or runtime/compiled)")) -> None:
    """Load and display governance configuration summary."""
    try:
        # Validate path exists
        if not validate_governance_path(path):
            console.print(f"[red]✗ Invalid governance path: {path}[/red]")
            raise typer.Exit(1)

        # Load configuration
        config = load_governance_config(path)
        summary = get_governance_summary(path, config=config)

        # Display configuration
        console.print(Panel(f"[bold cyan]Governance Configuration Loaded[/bold cyan]\n{path}", border_style="cyan"))

        # Display summary table
        table = Table(title="Governance Summary", show_header=True, header_style="bold")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        for key, value in summary.items():
            table.add_row(str(key), str(value))

        console.print(table)

    except typer.Exit:
        raise
    except FileNotFoundError as e:
        console.print(f"[red]✗ File not found: {e}[/red]")
        raise typer.Exit(1) from e
    except Exception as e:
        console.print(f"[red]✗ Error loading governance: {e}[/red]")
        raise typer.Exit(1) from e


@app.command()
def validate(
    path: str = typer.Option("runtime", help="Path to governance configuration (runtime or runtime/compiled)")
) -> None:
    """Validate governance integrity."""
    try:
        console.print(Panel(f"[bold cyan]Validating Governance[/bold cyan]\n{path}", border_style="cyan"))

        structure_ok = validate_governance_path(path)
        config = None
        if structure_ok:
            try:
                config = load_governance_config(path)
            except Exception:
                config = None

        checks = [
            ("Structure validation", structure_ok),
            ("Files accessible", _check_files_accessible(path)),
            ("Fingerprints valid", _check_fingerprints_valid(config)),
            ("No conflicts", _check_no_conflicts(config)),
        ]

        table = Table(title="Validation Results", show_header=True, header_style="bold")
        table.add_column("Check", style="cyan")
        table.add_column("Status", style="green")

        all_passed = True
        for check_name, passed in checks:
            status = "[green]✓ PASS[/green]" if passed else "[red]✗ FAIL[/red]"
            table.add_row(check_name, status)
            if not passed:
                all_passed = False

        console.print(table)

        if all_passed:
            console.print("[green]✓ All validation checks passed[/green]")
        else:
            console.print("[red]✗ Some validation checks failed[/red]")
            raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]✗ Validation error: {e}[/red]")
        raise typer.Exit(1) from e


@app.command()
def generate(
    output_dir: str = typer.Option(".", help="Output directory for generated files"),
    path: str = typer.Option("runtime", help="Path to governance configuration (runtime or runtime/compiled)"),
) -> None:
    """Generate templates and agent seeds."""
    try:
        # Validate governance path
        if not validate_governance_path(path):
            console.print(f"[red]✗ Invalid governance path: {path}[/red]")
            raise typer.Exit(1)

        console.print(Panel("[bold cyan]Generating Agent Seeds[/bold cyan]", border_style="cyan"))

        # Load governance
        config = load_governance_config(path)

        # Generate agent seeds
        seeds_dir = Path(output_dir) / ".vscode" / "agents"
        seeds_info = generate_agent_seeds(seeds_dir, config)

        # Display generated files
        table = Table(title="Generated Files", show_header=True, header_style="bold")
        table.add_column("Agent Template", style="cyan")
        table.add_column("Location", style="green")
        table.add_column("Status", style="green")

        for agent, file_path, status in seeds_info:
            table.add_row(agent, str(file_path), status)

        console.print(table)
        console.print(Panel(f"[green]✓ Agent seeds generated to {seeds_dir}[/green]", border_style="green"))

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]✗ Generation error: {e}[/red]")
        raise typer.Exit(1) from e


def _check_files_accessible(path: str) -> bool:
    """Check if all required governance files are accessible."""
    return validate_governance_path(path)


def _check_fingerprints_valid(config: dict | None) -> bool:
    """Check if governance fingerprints are valid."""
    try:
        if config is None:
            return False
        return config.get("core_fingerprint") is not None and config.get("client_fingerprint") is not None
    except Exception:
        return False


def _check_no_conflicts(config: dict | None) -> bool:
    """Check for conflicts in governance configuration."""
    try:
        if config is None:
            return False
        # Check that core and client fingerprints are different
        return config.get("core_fingerprint") != config.get("client_fingerprint")
    except Exception:
        return False
