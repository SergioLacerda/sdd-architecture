import subprocess
from pathlib import Path


def run_command_exec(inputs: dict, context: dict, spec_dir: Path) -> None:
    working_dir: Path = context.get("working_dir", Path.cwd())
    command = inputs.get("command", "")
    result = subprocess.run(
        command,
        shell=True,
        cwd=working_dir,
        capture_output=True,
        text=True,
    )
    context["last_exit_code"] = result.returncode
