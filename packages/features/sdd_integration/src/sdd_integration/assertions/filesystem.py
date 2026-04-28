from pathlib import Path

from .base import Assertion
from .result import AssertionResult


class FsExistsAssertion(Assertion):

    def execute(self, context):
        working_dir: Path = context.get("working_dir", Path.cwd())
        rel = self.params["path"]
        exists = (working_dir / rel).exists()

        if exists:
            return AssertionResult(True, f"{rel} exists")
        return AssertionResult(False, f"{rel} NOT found")
