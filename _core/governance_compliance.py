#!/usr/bin/env python3
"""Backward-compatible shim for governance compliance tools."""

from _core.tools.governance_compliance import *  # noqa: F403


if __name__ == "__main__":
    import runpy

    runpy.run_module("_core.tools.governance_compliance", run_name="__main__")
