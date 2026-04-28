import subprocess

import typer

app = typer.Typer()


@app.command()
def run():
    subprocess.run(["ruff", "check", "."], check=True)
