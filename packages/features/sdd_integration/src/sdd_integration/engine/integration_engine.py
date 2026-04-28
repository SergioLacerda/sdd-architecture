from pathlib import Path

import yaml

from sdd_integration.engine.context import ExecutionContext
from sdd_integration.engine.step_executor import StepExecutor, StepResult


class Report:
    def __init__(self, steps):
        self.steps = steps

    def score(self):
        total = len(self.steps)
        ok = sum(1 for s in self.steps if s.success)
        return int((ok / total) * 100) if total else 0

    def pretty(self):
        lines = ["\n🔍 SDD Doctor Report\n"]

        for s in self.steps:
            icon = "✅" if s.success else "❌"
            lines.append(f"{s.name} {icon} {s.details}")

        lines.append(f"\nScore: {self.score()}/100")
        return "\n".join(lines)


class IntegrationEngine:

    def __init__(self, spec_path: str):
        self.spec = yaml.safe_load(Path(spec_path).read_text())
        self.spec_dir = Path(spec_path).parent
        self.executor = StepExecutor()

    def run(self):
        context = ExecutionContext.from_spec(self.spec, self.spec_dir)

        try:
            results = [
                self.executor.execute(step, context)
                for step in self.spec.get("steps", [])
            ]

        finally:
            context.cleanup()

        return Report(results)
