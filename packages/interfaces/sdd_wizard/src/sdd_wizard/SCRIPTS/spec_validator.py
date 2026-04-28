from pathlib import Path

import yaml


class SpecValidator:
    def __init__(self, rules_path: str):
        self.rules = yaml.safe_load(Path(rules_path).read_text())

    def validate(self, specs_root: Path):
        errors = []

        for spec_dir in specs_root.iterdir():
            if not spec_dir.is_dir():
                continue

            files = [f.name for f in spec_dir.glob("*.md")]

            # Rule: must have test-cases
            if self.rules["spec_integrity"]["require_test_cases"]:
                if "test-cases.md" not in files:
                    errors.append(f"{spec_dir}: missing test-cases.md")

            # Rule: separation IS vs SHOULD (simplificado)
            if self.rules["spec_integrity"]["require_separation_is_should"]:
                content = "\n".join(f.read_text() for f in spec_dir.glob("*.md"))
                if "current" in content.lower() and "must" in content.lower():
                    errors.append(f"{spec_dir}: possible IS/SHOULD mixing detected")

        return errors


if __name__ == "__main__":
    validator = SpecValidator("docs/ia/governance/canonical_rules.yaml")
    result = validator.validate(Path("specs"))

    if result:
        print("❌ Spec validation errors:")
        for e in result:
            print("-", e)
    else:
        print("✅ Specs are valid")
