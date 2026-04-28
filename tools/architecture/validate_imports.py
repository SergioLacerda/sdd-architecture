import ast
import sys
from pathlib import Path

RULES = {
    "core": ["cli", "wizard"],
    "cli": [],
    "wizard": [],
}

ROOT = Path(".")


def get_layer(path: Path):
    parts = path.parts
    for p in parts:
        if p.startswith("sdd-"):
            return p.replace("sdd-", "")
    return None


def validate():
    violations = []

    for file in ROOT.rglob("*.py"):
        if "site-packages" in str(file):
            continue

        layer = get_layer(file)
        if not layer:
            continue

        tree = ast.parse(file.read_text())

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                if node.module.startswith("sdd."):
                    target = node.module.split(".")[1]

                    if target in RULES.get(layer, []):
                        violations.append(f"{file}: {layer} → {target}")

    if violations:
        print("\n❌ Architecture violations:\n")
        for v in violations:
            print(v)
        sys.exit(1)

    print("✅ Architecture OK")


if __name__ == "__main__":
    validate()
