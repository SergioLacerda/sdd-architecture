from __future__ import annotations

import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ExecutionContext:
    """Holds runtime state for an integration flow execution."""

    spec_dir: Path
    working_dir: Path
    isolation_enabled: bool = False
    data: dict[str, Any] = field(default_factory=dict)
    _temp_dir: Path | None = None

    @classmethod
    def from_spec(cls, spec: dict[str, Any], spec_dir: Path) -> "ExecutionContext":
        context_spec = spec.get("context", {})

        isolation = bool(context_spec.get("isolation", False))
        configured_working_dir = context_spec.get("working_dir")
        temp_dir: Path | None = None

        if isolation or configured_working_dir == "temp":
            temp_dir = Path(tempfile.mkdtemp(prefix="sdd-doctor-"))
            working_dir = temp_dir
            isolation = True
        elif configured_working_dir:
            working_dir = Path(configured_working_dir).expanduser().resolve()
            working_dir.mkdir(parents=True, exist_ok=True)
        else:
            working_dir = Path.cwd()

        context = cls(
            spec_dir=spec_dir,
            working_dir=working_dir,
            isolation_enabled=isolation,
            _temp_dir=temp_dir,
        )
        context.data["working_dir"] = working_dir
        return context

    def as_dict(self) -> dict[str, Any]:
        """Return the mutable dictionary expected by runners/assertions."""
        return self.data

    def cleanup(self) -> None:
        if self._temp_dir is not None:
            shutil.rmtree(self._temp_dir, ignore_errors=True)
            self._temp_dir = None
