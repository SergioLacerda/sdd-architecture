import subprocess
from pathlib import Path


def run_git_commit(inputs: dict, context: dict, spec_dir: Path) -> None:
    working_dir: Path = context.get("working_dir", Path.cwd())
    message = inputs.get("message", "init")

    def git(*args: str) -> None:
        subprocess.run(["git", *args], cwd=working_dir, capture_output=True)

    # Initialise a fresh repo in the isolated workspace if needed
    git_dir = working_dir / ".git"
    if not git_dir.exists():
        git("init")
        git("config", "user.email", "sdd-doctor@local")
        git("config", "user.name", "SDD Doctor")

    git("add", ".")
    git("commit", "-m", message, "--allow-empty")
