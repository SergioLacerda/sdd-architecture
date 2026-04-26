#!/usr/bin/env python3
"""Backward-compatible shim for governance compliance tools."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from _core.tools.governance_compliance import *  # noqa: F403


if __name__ == "__main__":
    import runpy

    runpy.run_module("_core.tools.governance_compliance", run_name="__main__")
