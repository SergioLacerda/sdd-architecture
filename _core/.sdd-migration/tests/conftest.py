import pytest
from pathlib import Path


@pytest.fixture
def migration_dir():
    """Path to migration directory"""
    return Path(__file__).parent.parent


@pytest.fixture
def output_dir(migration_dir):
    """Path to output directory"""
    return migration_dir / "output"


@pytest.fixture
def reports_dir(migration_dir):
    """Path to reports directory"""
    return migration_dir / "reports"


@pytest.fixture
def fixtures_dir(migration_dir):
    """Path to fixtures directory"""
    return migration_dir / "tests" / "fixtures"
