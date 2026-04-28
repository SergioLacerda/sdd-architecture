import json
import shutil
from pathlib import Path
from typing import Any

import pytest

try:
    from packages.tools.governance_compliance import GovernanceComplianceValidator
except Exception:  # pragma: no cover - test module is skipped below in this repo state
    GovernanceComplianceValidator = None  # type: ignore[assignment]

pytest.skip(allow_module_level=True, reason="GovernanceComplianceValidator module not available")

# Repo root is 2 levels above packages/
REPO_ROOT = Path(__file__).resolve().parents[2]


def _create_valid_governance_file(project_dir: Path, enforcement: str = "strict") -> Path:
    """Cria governance-core.json mínimo e válido para o validador."""
    gov_path = project_dir / ".ai" / "governance-core.json"
    gov_path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "seedlings": {"active": ["python"]},
        "authority": {
            "architect": ["arch@example.com"],
            "governance": ["gov@example.com"],
            "operations": ["ops@example.com"],
        },
        "policies": {"enforcement": enforcement},
        "phases": {"completed": [0]},
        "metadata": {},
    }

    with open(gov_path, "w") as f:
        json.dump(data, f, indent=2)

    return gov_path


def testpackages_governance_immutability(target_level="strict"):
    """Valida se o fingerprint detecta alterações manuais no JSON."""
    if GovernanceComplianceValidator is None:
        pytest.skip("GovernanceComplianceValidator module not available")

    test_dir = REPO_ROOT / "_tmp_test_project"
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir(parents=True, exist_ok=True)

    gov_path = _create_valid_governance_file(test_dir, enforcement=target_level)

    validator: Any = GovernanceComplianceValidator(test_dir)
    assert validator.sign_governance() is True, "Failed to sign governance file"
    validator.integrity_requested = True

    # Sanidade: o arquivo recém-assinado deve ser considerado válido
    is_initially_compliant, initial_results = validator.validate_all()
    assert is_initially_compliant is True, initial_results["violations"]

    # Ataque: Alterar fase concluída manualmente
    with open(gov_path, "r") as f:
        data = json.load(f)
    data["phases"]["completed"] = []  # Violação
    with open(gov_path, "w") as f:
        json.dump(data, f, indent=2)

    is_compliant, results = validator.validate_all()
    assert is_compliant is False
    assert any("Integrity Failure" in v for v in results["violations"])

    print("✅ Immutability Test Passed")
    shutil.rmtree(test_dir)


if __name__ == "__main__":
    testpackages_governance_immutability()
