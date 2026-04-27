import json
import shutil
import subprocess
import sys
from pathlib import Path

from _core.tools.governance_compliance import GovernanceComplianceValidator


def test_core_governance_immutability(target_level="strict"):
    """
    Test: Ensure that modifying a 'HARD' mandate after project generation
    is detected as an integrity failure.
    """
    test_dir = Path("./_tmp_test_project")
    if test_dir.exists():
        shutil.rmtree(test_dir)

    # 1. Run Wizard to generate a clean project using sys.executable for cross-platform safety
    wizard_script = Path("_core/wizard/src/interactive_mode.py")
    subprocess.run(
        [
            sys.executable,
            str(wizard_script),
            "--headless",
            "--output",
            str(test_dir),
            "--lang",
            "python",
            "--enforcement",
            target_level,
            "--all-mandates",
        ],
        check=True,
    )

    # 2. Verify it's initially compliant and signed
    validator = GovernanceComplianceValidator(test_dir)
    validator.integrity_requested = True
    is_compliant, results = validator.validate_all()

    assert is_compliant is True, f"Generated project should be compliant. Violations: {results['violations']}"

    # 3. Simulate an "Attack" (Tamper with the Core Mandates)
    # We modify the governance-core.json directly, bypassing the framework
    gov_path = test_dir / ".ai" / "governance-core.json"
    with open(gov_path, "r") as f:
        data = json.load(f)

    # Attack: Manually flip a value in the locked metadata or mandates
    if "phases" in data:
        # Trying to "uncomplete" Phase 0 manually
        data["phases"]["completed"] = []

    with open(gov_path, "w") as f:
        json.dump(data, f, indent=2)

    # 4. Run Validator again
    is_compliant_after_attack, results_after_attack = validator.validate_all()

    # 5. Assertions
    assert is_compliant_after_attack is False
    assert any(
        "Integrity Failure" in v for v in results_after_attack["violations"]
    ), "Validator should have caught the fingerprint mismatch!"

    print("\n✅ Immutability Test Passed: Tampering detected successfully.")

    # Cleanup
    shutil.rmtree(test_dir)


if __name__ == "__main__":
    level = sys.argv[1] if len(sys.argv) > 1 else "strict"
    test_core_governance_immutability(level)
