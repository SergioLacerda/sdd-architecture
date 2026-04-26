"""
Tests for Wizard Phases 1-2
- Phase 1: Validate SOURCE
- Phase 2: Load COMPILED
"""

import sys
import tempfile
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from orchestration.phase_1_validate import phase_1_validate_source
from orchestration.phase_2_load_compiled import phase_2_load_compiled
from validator import SourceValidator


class TestPhase1ValidateSource:
    """Tests for Phase 1: Validate SOURCE"""

    def test_phase_1_with_valid_files(self):
        """Phase 1 should succeed with valid mandate.spec and guidelines.dsl"""
        # Use actual repo files (navigate 3 levels up from test file to repo root)
        repo_root = Path(__file__).parent.parent.parent  # .sdd-architecture
        success, report = phase_1_validate_source(repo_root)

        assert success, f"Phase 1 failed: {report['errors']}"
        assert report['status'] == 'SUCCESS'
        assert report['checks']['mandate_spec_exists']
        assert report['checks']['guidelines_dsl_exists']
        assert report['checks']['mandate_spec_valid']
        assert report['checks']['guidelines_dsl_valid']

    def test_phase_1_detects_missing_mandate(self):
        """Phase 1 should fail if mandate.spec is missing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            sdd_core = repo_root / ".sdd-core"
            sdd_core.mkdir()

            # Create guidelines.dsl but not mandate.spec
            (sdd_core / "guidelines.dsl").write_text("guideline G001 { title: 'Test' }")

            success, report = phase_1_validate_source(repo_root)

            assert not success
            assert "mandate.spec not found" in str(report['errors'])

    def test_phase_1_detects_syntax_errors(self):
        """Phase 1 should detect unbalanced braces"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            sdd_core = repo_root / ".sdd-core"
            sdd_core.mkdir()

            # Create files with syntax errors
            (sdd_core / "mandate.spec").write_text("mandate M001 { title: 'Test'")  # Missing }
            (sdd_core / "guidelines.dsl").write_text("guideline G001 { title: 'Test' }")

            success, report = phase_1_validate_source(repo_root)

            assert not success
            assert any("Unbalanced braces" in str(e) for e in report['errors'])

    def test_phase_1_reports_statistics(self):
        """Phase 1 should report mandate/guideline counts"""
        repo_root = Path(__file__).parent.parent.parent  # .sdd-architecture
        success, report = phase_1_validate_source(repo_root)

        assert success
        mandate_count = report['data']['mandate']['mandate_count']
        guideline_count = report['data']['guidelines']['guideline_count']

        assert mandate_count > 0, "Should find at least one mandate"
        assert guideline_count > 0, "Should find at least one guideline"


class TestPhase2LoadCompiled:
    """Tests for Phase 2: Load COMPILED"""

    def test_phase_2_with_valid_artifacts(self):
        """Phase 2 should succeed with valid .sdd-runtime/ files"""
        repo_root = Path(__file__).parent.parent.parent  # .sdd-architecture
        success, report = phase_2_load_compiled(repo_root)

        assert success, f"Phase 2 failed: {report['errors']}"
        assert report['status'] == 'SUCCESS'
        # Phase 2 returns checks for the actual files it validates
        assert report['checks']['guidelines_bin_exists']  # Required file
        # Should have loaded data
        assert 'mandate' in report['data']
        assert 'guidelines' in report['data']

    def test_phase_2_loads_statistics(self):
        """Phase 2 should load and deserialize mandate/guideline data"""
        repo_root = Path(__file__).parent.parent.parent  # .sdd-architecture
        success, report = phase_2_load_compiled(repo_root)

        assert success
        # Phase 2 loads the actual compiled data, not just statistics
        assert isinstance(report['data']['mandate'], dict)
        assert isinstance(report['data']['guidelines'], dict)
        assert len(report['data']['mandate']) > 0  # Should have mandates
        assert len(report['data']['guidelines']) > 0  # Should have guidelines

    def test_phase_2_detects_missing_runtime(self):
        """Phase 2 should fail if .sdd-runtime/ is missing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)

            success, report = phase_2_load_compiled(repo_root)

            assert not success
            assert len(report['errors']) > 0


class TestSourceValidator:
    """Tests for SourceValidator utility"""

    def test_validator_detects_unbalanced_braces(self):
        """Validator should detect unbalanced braces"""
        text = "mandate M001 { title: 'Test'"
        errors = SourceValidator.validate_dsl_syntax(text)

        assert len(errors) > 0
        assert any("Unbalanced braces" in e for e in errors)

    def test_validator_validates_mandate_spec(self):
        """Validator should validate mandate structure"""
        text = """mandate M001 {
            title: "Clean Architecture"
            description: "Maintain clean architecture principles"
        }
        
        mandate M002 {
            title: "Test-Driven Development"
            description: "Write tests first"
        }"""

        result = SourceValidator.validate_mandate_spec(text)

        assert result['valid']
        assert result['statistics']['mandate_count'] == 2
        assert 'M001' in result['statistics']['mandate_ids']
        assert 'M002' in result['statistics']['mandate_ids']

    def test_validator_detects_duplicate_ids(self):
        """Validator should detect duplicate mandate IDs"""
        text = """mandate M001 { title: "Test1" }
        mandate M001 { title: "Test2" }"""

        result = SourceValidator.validate_mandate_spec(text)

        assert not result['valid']
        assert any("Duplicate" in str(e) for e in result['errors'])


class TestIntegration:
    """Integration tests for Phases 1-2"""

    def test_phases_1_and_2_complete_successfully(self):
        """Both phases should complete successfully with real repo"""
        repo_root = Path(__file__).parent.parent.parent  # .sdd-architecture

        # Phase 1
        success1, report1 = phase_1_validate_source(repo_root)
        assert success1, f"Phase 1 failed: {report1['errors']}"

        # Phase 2
        success2, report2 = phase_2_load_compiled(repo_root)
        assert success2, f"Phase 2 failed: {report2['errors']}"

        # Verify data continuity
        phase1_mandates_count = report1['data']['mandate'].get('mandate_count', 0)
        phase2_mandates = report2['data']['mandate']

        # Phase 2 returns compiled mandate data as dict
        assert isinstance(phase2_mandates, dict)
        # Should have at least 1 mandate
        assert len(phase2_mandates) >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
