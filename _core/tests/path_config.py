from pathlib import Path


def get_repo_root() -> Path:
    """Dynamically finds the repository root based on the location of this file."""
    # This file is located in _core/tests/path_config.py
    # Repo root is 2 levels up from _core/
    return Path(__file__).resolve().parents[2]


REPO_ROOT = get_repo_root()
CORE_DIR = REPO_ROOT / "_core"
SPEC_DIR = REPO_ROOT / "_spec"
DOCS_DIR = REPO_ROOT / "docs"
GENERATED_DIR = REPO_ROOT / "sdd-generated"

# Internal Framework Paths
CORE = CORE_DIR / "core"
WIZARD = CORE_DIR / "wizard"
COMPILER = CORE_DIR / "compiler"

# Decision and Spec Paths
CANONICAL_SPEC = SPEC_DIR / "CANONICAL"
ADR_CANONICAL = CANONICAL_SPEC / "decisions"
ADR_ARCH = SPEC_DIR / "architecture" / "decisions"
ADR_DIR = ADR_ARCH  # Default to new architecture path
QUIZ_TRACKING = REPO_ROOT / "docs" / "project-status" / "_quiz_tracking.json"
