import re
from pathlib import Path

# 🔥 MAPEAMENTO CENTRAL (ajuste conforme seus packages)
IMPORT_MAP = {
    "cli": "sdd_cli",
    "core": "sdd_core",
    "wizard": "sdd_wizard",
    "compiler": "sdd_compiler",
    "build_scripts": "sdd_build",  # ou remova se não existir
}

# Regex para capturar imports
FROM_RE = re.compile(r"^(\s*from\s+)(\w+)(\.[\w\.]*)?\s+import\s+", re.MULTILINE)
IMPORT_RE = re.compile(r"^(\s*import\s+)(\w+)(\.[\w\.]*)?", re.MULTILINE)


def replace_from(match):
    prefix, module, rest = match.groups()
    if module in IMPORT_MAP:
        new_module = IMPORT_MAP[module]
        return f"{prefix}{new_module}{rest or ''} import "
    return match.group(0)


def replace_import(match):
    prefix, module, rest = match.groups()
    if module in IMPORT_MAP:
        new_module = IMPORT_MAP[module]
        return f"{prefix}{new_module}{rest or ''}"
    return match.group(0)


def process_file(path: Path, dry_run: bool = False):
    original = path.read_text(encoding="utf-8")

    updated = FROM_RE.sub(replace_from, original)
    updated = IMPORT_RE.sub(replace_import, updated)

    if original != updated:
        print(f"🔧 {path}")

        if not dry_run:
            path.write_text(updated, encoding="utf-8")


def main():
    base_dirs = ["tests", "packages"]

    for base in base_dirs:
        for file in Path(base).rglob("*.py"):
            process_file(file)


if __name__ == "__main__":
    main()
