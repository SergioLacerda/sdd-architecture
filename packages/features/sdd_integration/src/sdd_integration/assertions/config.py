from sdd_integration.assertions.base import Assertion
from sdd_integration.assertions.result import AssertionResult


class ConfigHasKeyAssertion(Assertion):

    def execute(self, context):
        config = context.get("config", {})
        key = self.params["key"]

        if key in config:
            return AssertionResult(True, f"{key} found")

        return AssertionResult(False, f"{key} missing")


class ConfigIsValidPathAssertion(Assertion):

    def execute(self, context):
        config = context.get("config", {})
        key = self.params["key"]
        value = config.get(key)

        if not value:
            return AssertionResult(False, f"{key} not set")

        return AssertionResult(True, f"{key} is a valid path")
