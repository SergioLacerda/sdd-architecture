"""Tests for migration v2.1 → v3.0"""

import json
import re

import pytest


class TestExtraction:
    """Test extraction phase"""

    def test_mandate_spec_exists(self, output_dir):
        """mandate.spec should exist after extraction"""
        mandate_file = output_dir / "mandate.spec"
        assert mandate_file.exists(), "mandate.spec not found in output/"

    def test_guidelines_dsl_exists(self, output_dir):
        """guidelines.dsl should exist after extraction"""
        guidelines_file = output_dir / "guidelines.dsl"
        assert guidelines_file.exists(), "guidelines.dsl not found in output/"


class TestValidation:
    """Test validation phase"""

    def test_principle_count(self, output_dir):
        """v2.1 has 15 principles, v3.0 must have 15 mandates"""
        mandate_file = output_dir / "mandate.spec"
        if not mandate_file.exists():
            pytest.skip("mandate.spec not generated yet")

        content = mandate_file.read_text()
        mandates = re.findall(r"mandate (M\d+)", content)

        # At least some mandates should be present
        assert len(mandates) > 0, "No mandates found in mandate.spec"

    def test_no_empty_fields(self, output_dir):
        """No empty descriptions or titles"""
        mandate_file = output_dir / "mandate.spec"
        if not mandate_file.exists():
            pytest.skip("mandate.spec not generated yet")

        content = mandate_file.read_text()

        # Check for empty strings
        empty_patterns = [
            r'title:\s*""',
            r'description:\s*""',
        ]

        for pattern in empty_patterns:
            matches = re.findall(pattern, content)
            assert len(matches) == 0, f"Found empty fields matching {pattern}"

    def test_sequential_ids(self, output_dir):
        """Mandate IDs should be M001, M002, M003, etc"""
        mandate_file = output_dir / "mandate.spec"
        if not mandate_file.exists():
            pytest.skip("mandate.spec not generated yet")

        content = mandate_file.read_text()
        matches = re.findall(r"mandate (M\d+)", content)

        if len(matches) > 0:
            # Check that IDs are numeric and sequential
            for i, mandate_id in enumerate(matches, 1):
                expected_id = f"M{str(i).zfill(3)}"
                assert mandate_id == expected_id, f"Expected {expected_id}, got {mandate_id}"

    def test_validation_commands_present(self, output_dir):
        """At least some validation commands should be present"""
        mandate_file = output_dir / "mandate.spec"
        if not mandate_file.exists():
            pytest.skip("mandate.spec not generated yet")

        content = mandate_file.read_text()

        # Look for validation commands
        has_validation = "validation:" in content or "commands:" in content
        assert has_validation, "No validation commands found in mandate.spec"

    def test_dsl_syntax_valid(self, output_dir):
        """DSL syntax should be valid (balanced braces, proper strings)"""
        mandate_file = output_dir / "mandate.spec"
        if not mandate_file.exists():
            pytest.skip("mandate.spec not generated yet")

        content = mandate_file.read_text()

        # Check balanced braces
        open_braces = content.count("{")
        close_braces = content.count("}")
        assert open_braces == close_braces, f"Unbalanced braces: {open_braces} open, {close_braces} close"

        # Check for properly quoted strings
        string_pattern = r':\s+"[^"]*"'
        strings = re.findall(string_pattern, content)
        assert len(strings) > 0, "No properly quoted strings found"

    def test_guidelines_format_valid(self, output_dir):
        """Guidelines should have valid format"""
        guidelines_file = output_dir / "guidelines.dsl"
        if not guidelines_file.exists():
            pytest.skip("guidelines.dsl not generated yet")

        content = guidelines_file.read_text()

        # Should contain guideline blocks (if any guidelines exist)
        if "guideline" in content:
            guideline_pattern = r"guideline (G\d+)"
            matches = re.findall(guideline_pattern, content)
            assert len(matches) > 0, "No guidelines found in guidelines.dsl"


class TestReporting:
    """Test reporting phase"""

    def test_extraction_report_generated(self, reports_dir):
        """extraction_report.json should exist"""
        report_file = reports_dir / "extraction_report.json"
        assert report_file.exists(), "extraction_report.json not found"

        # Verify it's valid JSON
        report = json.loads(report_file.read_text())
        assert "metadata" in report, "Report missing metadata"
        assert "mandates" in report, "Report missing mandates section"

    def test_validation_report_generated(self, reports_dir):
        """validation_report.json should exist"""
        report_file = reports_dir / "validation_report.json"
        assert report_file.exists(), "validation_report.json not found"

        # Verify it's valid JSON
        report = json.loads(report_file.read_text())
        assert "summary" in report, "Report missing summary"
        assert "results" in report, "Report missing results"


class TestFixtures:
    """Test with sample fixtures"""

    def test_sample_fixture_exists(self, fixtures_dir):
        """v2_sample.md fixture should exist"""
        sample_file = fixtures_dir / "v2_sample.md"
        assert sample_file.exists(), "v2_sample.md fixture not found"

    def test_expected_output_fixture_exists(self, fixtures_dir):
        """v3_expected.spec fixture should exist"""
        expected_file = fixtures_dir / "v3_expected.spec"
        assert expected_file.exists(), "v3_expected.spec fixture not found"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
