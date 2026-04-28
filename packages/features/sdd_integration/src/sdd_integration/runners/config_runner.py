import configparser
from pathlib import Path


def run_config_validate(inputs: dict, context: dict, spec_dir: Path) -> None:
    working_dir: Path = context.get("working_dir", Path.cwd())
    config_file = working_dir / inputs.get("file", ".spec.config")

    if not config_file.exists():
        context["config"] = {}
        return

    parser = configparser.ConfigParser()
    parser.read(config_file)

    # Flatten all sections into a single dict
    config: dict = {}
    for section in parser.sections():
        for key, value in parser.items(section):
            config[key] = value

    context["config"] = config
