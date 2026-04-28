import shutil
from pathlib import Path


def run_filesystem_create_structure(inputs: dict, context: dict, spec_dir: Path) -> None:
    working_dir: Path = context.get("working_dir", Path.cwd())
    for directory in inputs.get("directories", []):
        (working_dir / directory).mkdir(parents=True, exist_ok=True)


def run_filesystem_copy(inputs: dict, context: dict, spec_dir: Path) -> None:
    working_dir: Path = context.get("working_dir", Path.cwd())
    src = (spec_dir / inputs["from"]).resolve()
    dst = (working_dir / inputs["to"]).resolve()
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    elif src.is_file():
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
