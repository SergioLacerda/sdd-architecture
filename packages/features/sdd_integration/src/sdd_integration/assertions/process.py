from sdd_integration.assertions.base import Assertion
from sdd_integration.assertions.result import AssertionResult


class ProcessExitAssertion(Assertion):

    def execute(self, context):
        expected = self.params["equals"]
        actual = context.get("last_exit_code")

        if actual == expected:
            return AssertionResult(True, "exit code ok")

        return AssertionResult(False, f"expected {expected}, got {actual}")
