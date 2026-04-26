"""
Tests for PHASE 1: Pipeline Builder

Validates:
1. Both JSON files are generated
2. JSON structure is correct
3. Items are properly separated (customizable=true vs false)
4. Fingerprints are calculated correctly
5. Core fingerprint is used as salt for client
"""

import json
import hashlib
from pathlib import Path
import pytest

from pipeline_builder import PipelineBuilder


class TestPhase1Pipeline:
    """Test PHASE 1: Pipeline Builder"""

    @pytest.fixture
    def pipeline(self):
        """Create a pipeline builder instance"""
        return PipelineBuilder(".sdd-core")

    @pytest.fixture
    def output_dir(self, tmp_path):
        """Use temp directory for test output"""
        return str(tmp_path)

    def test_pipeline_generates_core_and_client_files(self, pipeline, output_dir):
        """Test that pipeline generates both core and client JSON files"""
        result = pipeline.save_outputs(output_dir)

        assert Path(result["governance_core"]).exists(), "governance-core.json not generated"
        assert Path(result["governance_client"]).exists(), "governance-client.json not generated"

    def test_core_json_structure(self, pipeline, output_dir):
        """Test governance-core.json has correct structure"""
        result = pipeline.save_outputs(output_dir)

        with open(result["governance_core"]) as f:
            core_data = json.load(f)

        # Check required fields
        assert core_data["category"] == "CORE"
        assert core_data["version"] == "3.0"
        assert "items" in core_data
        assert "fingerprint" in core_data
        assert len(core_data["fingerprint"]) == 64  # SHA-256 hex

    def test_client_json_structure(self, pipeline, output_dir):
        """Test governance-client.json has correct structure"""
        result = pipeline.save_outputs(output_dir)

        with open(result["governance_client"]) as f:
            client_data = json.load(f)

        # Check required fields
        assert client_data["category"] == "CLIENT"
        assert client_data["version"] == "3.0"
        assert "items" in client_data
        assert "fingerprint" in client_data
        assert "fingerprint_core_salt" in client_data
        assert len(client_data["fingerprint"]) == 64  # SHA-256 hex

    def test_core_items_not_customizable(self, pipeline, output_dir):
        """Test that core items have customizable=false"""
        result = pipeline.save_outputs(output_dir)

        with open(result["governance_core"]) as f:
            core_data = json.load(f)

        for item in core_data["items"]:
            assert item["customizable"] is False, f"Item {item['id']} is customizable in CORE"

    def test_client_items_customizable(self, pipeline, output_dir):
        """Test that client items have customizable=true"""
        result = pipeline.save_outputs(output_dir)

        with open(result["governance_client"]) as f:
            client_data = json.load(f)

        for item in client_data["items"]:
            assert item["customizable"] is True, f"Item {item['id']} is not customizable in CLIENT"

    def test_core_fingerprint_used_as_salt(self, pipeline, output_dir):
        """Test that core fingerprint is salt for client fingerprint"""
        result = pipeline.save_outputs(output_dir)

        with open(result["governance_core"]) as f:
            core_data = json.load(f)
        with open(result["governance_client"]) as f:
            client_data = json.load(f)

        core_fingerprint = core_data["fingerprint"]
        core_fingerprint_salt = client_data["fingerprint_core_salt"]

        assert core_fingerprint == core_fingerprint_salt, \
            "Core fingerprint not used as salt for client"

    def test_fingerprints_are_different(self, pipeline, output_dir):
        """Test that core and client fingerprints are different"""
        result = pipeline.save_outputs(output_dir)

        core_fp = result["core_fingerprint"]
        client_fp = result["client_fingerprint"]

        assert core_fp != client_fp, "Core and client fingerprints should be different"

    def test_items_have_required_fields(self, pipeline, output_dir):
        """Test that each item has all required fields"""
        result = pipeline.save_outputs(output_dir)

        required_fields = [
            "id", "title", "type", "criticality", "customizable",
            "optional", "category", "source_file", "content"
        ]

        with open(result["governance_core"]) as f:
            core_data = json.load(f)

        for item in core_data["items"]:
            for field in required_fields:
                assert field in item, f"Field '{field}' missing from item {item.get('id')}"

    def test_criticality_ordering(self, pipeline, output_dir):
        """Test that items are ordered by criticality"""
        result = pipeline.save_outputs(output_dir)

        with open(result["governance_core"]) as f:
            core_data = json.load(f)

        criticality_order = {"OBRIGATÓRIO": 0, "ALERTA": 1, "OPCIONAL": 2}
        prev_criticality_level = -1

        for item in core_data["items"]:
            current_level = criticality_order.get(item["criticality"], 99)
            assert current_level >= prev_criticality_level, \
                f"Items not properly ordered by criticality: {item['criticality']}"
            prev_criticality_level = current_level

    def test_fingerprint_consistency(self, pipeline, output_dir):
        """Test that running pipeline twice produces same fingerprints"""
        result1 = pipeline.save_outputs(output_dir)

        # Create new pipeline and run again (in same dir)
        pipeline2 = PipelineBuilder(".sdd-core")
        result2 = pipeline2.save_outputs(output_dir)

        assert result1["core_fingerprint"] == result2["core_fingerprint"], \
            "Core fingerprint not consistent between runs"
        assert result1["client_fingerprint"] == result2["client_fingerprint"], \
            "Client fingerprint not consistent between runs"

    def test_at_least_one_core_item_exists(self, pipeline, output_dir):
        """Test that core has at least one item (mandate or decision)"""
        result = pipeline.save_outputs(output_dir)

        with open(result["governance_core"]) as f:
            core_data = json.load(f)

        assert len(core_data["items"]) > 0, "No items in governance-core.json"

    def test_at_least_one_client_item_exists(self, pipeline, output_dir):
        """Test that client has at least one item (guideline or guardrail)"""
        result = pipeline.save_outputs(output_dir)

        with open(result["governance_client"]) as f:
            client_data = json.load(f)

        assert len(client_data["items"]) > 0, "No items in governance-client.json"

    def test_source_files_are_documented(self, pipeline, output_dir):
        """Test that each item has source_file documented"""
        result = pipeline.save_outputs(output_dir)

        with open(result["governance_core"]) as f:
            core_data = json.load(f)

        for item in core_data["items"]:
            assert item["source_file"], f"Item {item['id']} has no source_file"
            assert isinstance(item["source_file"], str), \
                f"Item {item['id']} source_file is not a string"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
