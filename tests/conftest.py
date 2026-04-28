"""
Root conftest.py for packages test suite.

Ensures all project module directories are on sys.path before pytest
collects any test, regardless of CWD (critical for Docker where CWD is /app).
"""

import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
PACKAGES_DIR = REPO_ROOT / "packages"

# All module directories that test files import from without package prefix
_MODULE_PATHS = [
    REPO_ROOT,
    PACKAGES_DIR / "core" / "sdd_core" / "src",
    PACKAGES_DIR / "core" / "sdd_compiler" / "src",
    PACKAGES_DIR / "features" / "sdd_integration" / "src",
    PACKAGES_DIR / "interfaces" / "sdd_wizard" / "src",
    PACKAGES_DIR / "interfaces" / "sdd_cli" / "src",
]

for _p in _MODULE_PATHS:
    _s = str(_p)
    if _p.exists() and _s not in sys.path:
        sys.path.insert(0, _s)
