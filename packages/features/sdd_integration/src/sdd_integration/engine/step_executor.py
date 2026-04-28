from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sdd_integration.assertions.registry import REGISTRY
from sdd_integration.engine.context import ExecutionContext
from sdd_integration.runners import RUNNER_REGISTRY


@dataclass
class StepResult:
    name: str
    success: bool
    details: str


class StepExecutor:
    """Executes a single protocol step with runners and assertions."""

    def __init__(
        self,
        runner_registry: dict[str, Any] | None = None,
        assertion_registry: dict[str, Any] | None = None,
    ):
        self.runner_registry = runner_registry or RUNNER_REGISTRY
        self.assertion_registry = assertion_registry or REGISTRY

    def execute(self, step: dict[str, Any], context: ExecutionContext) -> StepResult:
        step_name = step.get("id", "unnamed_step")
        step_type = step.get("type", "")
        inputs = step.get("inputs", {})

        step_success = True
        messages: list[str] = []

        runner = self.runner_registry.get(step_type)
        if runner is None:
            step_success = False
            messages.append(f"runner not found: {step_type}")
        else:
            try:
                runner(inputs, context.as_dict(), context.spec_dir)
            except Exception as exc:
                step_success = False
                messages.append(f"runner error: {exc}")

        for assertion_config in step.get("asserts", []):
            assertion_type = assertion_config.get("type", "")
            assertion_cls = self.assertion_registry.get(assertion_type)
            if assertion_cls is None:
                step_success = False
                messages.append(f"assertion not found: {assertion_type}")
                continue

            try:
                assertion = assertion_cls(**assertion_config)
                result = assertion.execute(context.as_dict())
            except Exception as exc:
                step_success = False
                messages.append(f"assertion error ({assertion_type}): {exc}")
                continue

            if not result.success:
                step_success = False
            messages.append(result.message)

        return StepResult(step_name, step_success, " | ".join(messages) or "step executed")
