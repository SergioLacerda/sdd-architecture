from pathlib import Path

import yaml


class ContextOptimizer:
    def __init__(self, rules_path: str):
        self.rules = yaml.safe_load(Path(rules_path).read_text())

    def classify_task(self, task: str) -> str:
        task = task.lower()
        if "bug" in task:
            return "bug_fix"
        if "compare" in task or "analyze" in task:
            return "analysis"
        if "implement" in task:
            return "implementation"
        return "general"

    def select_specs(self, task_type: str):
        mapping = {
            "analysis": ["architecture.md", "contracts.md"],
            "implementation": ["feature-template.md", "conventions.md"],
            "bug_fix": ["known_issues.md", "architecture.md"],
            "general": ["architecture.md"],
        }
        return mapping.get(task_type, ["architecture.md"])

    def load_specs(self, selected_files):
        base = Path("docs/ia")
        content = []

        for file in base.rglob("*.md"):
            if file.name in selected_files:
                content.append(file.read_text())

        return content

    def prune(self, contents):
        pruned = []
        for c in contents:
            lines = c.splitlines()

            # remove verbose sections (heurística simples)
            filtered = [
                l for l in lines
                if len(l.strip()) < 200
                and not l.lower().startswith("example")
            ]

            pruned.append("\n".join(filtered[:200]))  # limite por doc

        return pruned

    def assemble(self, pruned_contents):
        return "\n\n".join(pruned_contents)

    def optimize(self, task: str):
        task_type = self.classify_task(task)
        selected = self.select_specs(task_type)
        raw = self.load_specs(selected)
        pruned = self.prune(raw)
        return self.assemble(pruned)


if __name__ == "__main__":
    optimizer = ContextOptimizer(
        "docs/ia/governance/canonical_rules.yaml"
    )

    task = "analyze retrieval implementation vs spec"
    context = optimizer.optimize(task)

    print("=== OPTIMIZED CONTEXT ===")
    print(context[:2000])
