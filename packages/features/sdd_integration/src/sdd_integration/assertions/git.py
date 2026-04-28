import subprocess
from pathlib import Path

from sdd_integration.assertions.base import Assertion
from sdd_integration.assertions.result import AssertionResult


class GitHasCommitAssertion(Assertion):

    def execute(self, context):
        working_dir: Path = context.get("working_dir", Path.cwd())
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                cwd=working_dir,
            )
            if result.returncode == 0:
                return AssertionResult(True, "git has at least one commit")
            return AssertionResult(False, "no commits found in repository")
        except FileNotFoundError:
            return AssertionResult(False, "git not found")
