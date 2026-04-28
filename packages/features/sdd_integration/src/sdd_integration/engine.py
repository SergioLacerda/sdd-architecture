"""Compatibility module for legacy imports.

Use the implementation in ``sdd_integration.engine.integration_engine``.
"""

from sdd_integration.engine.integration_engine import IntegrationEngine, Report, StepResult

__all__ = ["IntegrationEngine", "Report", "StepResult"]
