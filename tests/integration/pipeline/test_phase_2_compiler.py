"""
Tests for PHASE 2: Governance Compiler

Validates:
1. msgpack files are generated
2. Metadata files are generated
3. Fingerprints are preserved from pipeline
4. Core fingerprint used as salt for client
5. msgpack files are valid and can be loaded
6. Readonly/customizable flags correct
"""

import json
from pathlib import Path

import msgpack
import pytest
from sdd_compiler.governance_compiler import GovernanceCompiler


class TestPhase2Compiler:
    """Test PHASE 2: Governance Compiler"""

    @pytest.fixture
    def compiler(self):
        """Create a compiler instance"""
        return GovernanceCompiler("compiler/compiled")

    @pytest.fixture
    def output_dir(self, tmp_path):
        """Use temp directory for test output"""
        return str(tmp_path)

    def test_compiler_generates_msgpack_files(self, compiler, output_dir):
        """Test that compiler generates both msgpack files"""
        result = compiler.compile(output_dir)

        assert Path(result["core_msgpack_file"]).exists(), "governance-core.compiled.msgpack not generated"
        assert Path(result["client_msgpack_file"]).exists(), "governance-client-template.compiled.msgpack not generated"

    def test_compiler_generates_metadata_files(self, compiler, output_dir):
        """Test that compiler generates metadata files"""
        result = compiler.compile(output_dir)

        assert Path(result["core_metadata"]).exists(), "metadata-core.json not generated"
        assert Path(result["client_metadata"]).exists(), "metadata-client-template.json not generated"

    def testpackages_metadata_structure(self, compiler, output_dir):
        """Test core metadata has correct structure"""
        result = compiler.compile(output_dir)

        with open(result["core_metadata"]) as f:
            metadata = json.load(f)

        # Check required fields
        assert metadata["version"] == "3.0"
        assert metadata["type"] == "core"
        assert "fingerprint" in metadata
        assert "generated_at" in metadata
        assert metadata["readonly"] is True
        assert metadata["customizable"] is False
        assert "item_count" in metadata
        assert "items_by_type" in metadata
        assert "items_by_criticality" in metadata

    def test_client_metadata_structure(self, compiler, output_dir):
        """Test client metadata has correct structure"""
        result = compiler.compile(output_dir)

        with open(result["client_metadata"]) as f:
            metadata = json.load(f)

        # Check required fields
        assert metadata["version"] == "3.0"
        assert metadata["type"] == "client-template"
        assert "fingerprint" in metadata
        assert "generated_at" in metadata
        assert metadata["readonly"] is False
        assert metadata["customizable"] is True
        assert "fingerprintpackages_salt" in metadata
        assert "item_count" in metadata

    def test_fingerprints_preserved_from_pipeline(self, compiler, output_dir):
        """Test that fingerprints from pipeline are preserved"""
        # Load original JSONs
        with open("compiler/compiled/governance-core.json") as f:
            core_json = json.load(f)
        with open("compiler/compiled/governance-client.json") as f:
            client_json = json.load(f)

        originalpackages_fp = core_json["fingerprint"]
        original_client_fp = client_json["fingerprint"]

        # Compile and check
        result = compiler.compile(output_dir)

        assert result["core_fingerprint"] == originalpackages_fp, "Core fingerprint changed during compilation"
        assert result["client_fingerprint"] == original_client_fp, "Client fingerprint changed during compilation"

    def testpackages_fingerprint_used_as_salt(self, compiler, output_dir):
        """Test that core fingerprint is salt for client"""
        result = compiler.compile(output_dir)

        core_fp = result["core_fingerprint"]
        core_salt = result["core_fingerprint_salt"]

        assert core_fp == core_salt, "Core fingerprint not used as salt for client"

    def test_fingerprints_different(self, compiler, output_dir):
        """Test that core and client fingerprints are different"""
        result = compiler.compile(output_dir)

        assert result["core_fingerprint"] != result["client_fingerprint"], "Core and client fingerprints should be different"

    def test_msgpack_files_valid_format(self, compiler, output_dir):
        """Test that msgpack files are valid and can be loaded"""
        result = compiler.compile(output_dir)

        # Load core msgpack
        core_msgpack_file = result["core_msgpack_file"]
        core_data = msgpack.unpackb(Path(core_msgpack_file).read_bytes(), raw=False)
        assert "items" in core_data, "Core msgpack invalid"
        assert isinstance(core_data["items"], list), "Items not a list in core msgpack"

        # Load client msgpack
        client_msgpack_file = result["client_msgpack_file"]
        client_data = msgpack.unpackb(Path(client_msgpack_file).read_bytes(), raw=False)
        assert "items" in client_data, "Client msgpack invalid"
        assert isinstance(client_data["items"], list), "Items not a list in client msgpack"

    def test_msgpack_contains_fingerprints(self, compiler, output_dir):
        """Test that msgpack files contain fingerprints"""
        result = compiler.compile(output_dir)

        # Load core msgpack
        core_data = msgpack.unpackb(Path(result["core_msgpack_file"]).read_bytes(), raw=False)
        assert "fingerprint" in core_data, "Fingerprint missing from sdd_core msgpack"

        # Load client msgpack
        client_data = msgpack.unpackb(Path(result["client_msgpack_file"]).read_bytes(), raw=False)
        assert "fingerprint" in client_data, "Fingerprint missing from client msgpack"
        assert "fingerprintpackages_salt" in client_data, "Fingerprintpackages_salt missing from client msgpack"

    def test_item_counts_correct(self, compiler, output_dir):
        """Test that item counts in metadata are correct"""
        result = compiler.compile(output_dir)

        assert result["core_item_count"] > 0, "No items in core"
        assert result["client_item_count"] > 0, "No items in client"

        # Verify metadata reflects same counts
        with open(result["core_metadata"]) as f:
            core_meta = json.load(f)
        with open(result["client_metadata"]) as f:
            client_meta = json.load(f)

        assert core_meta["item_count"] == result["core_item_count"]
        assert client_meta["item_count"] == result["client_item_count"]

    def test_items_by_type_counted(self, compiler, output_dir):
        """Test that items_by_type is counted correctly"""
        result = compiler.compile(output_dir)

        with open(result["core_metadata"]) as f:
            core_meta = json.load(f)

        items_by_type = core_meta["items_by_type"]
        assert isinstance(items_by_type, dict), "items_by_type should be dict"
        assert len(items_by_type) > 0, "No types in items_by_type"

    def test_items_by_criticality_counted(self, compiler, output_dir):
        """Test that items_by_criticality is counted correctly"""
        result = compiler.compile(output_dir)

        with open(result["core_metadata"]) as f:
            core_meta = json.load(f)

        items_by_criticality = core_meta["items_by_criticality"]
        assert isinstance(items_by_criticality, dict), "items_by_criticality should be dict"
        assert len(items_by_criticality) > 0, "No criticalities in items_by_criticality"

    def test_validation_passes(self, compiler, output_dir):
        """Test that validation passes after compilation"""
        compiler.compile(output_dir)

        # Create new compiler instance pointing to output_dir
        # For this test, we validate the output_dir
        output_path = Path(output_dir)
        core_metadata = output_path / "metadata-core.json"
        client_metadata = output_path / "metadata-client-template.json"

        # Load metadata to validate
        with open(core_metadata) as f:
            core_meta = json.load(f)
        with open(client_metadata) as f:
            client_meta = json.load(f)

        # All validations
        assert core_meta["readonly"] is True
        assert client_meta["customizable"] is True
        assert core_meta["fingerprint"] == client_meta["fingerprintpackages_salt"]
        assert core_meta["fingerprint"] != client_meta["fingerprint"]

    def test_roundtrip_msgpack_to_json(self, compiler, output_dir):
        """Test that msgpack can be round-tripped to JSON format"""
        result = compiler.compile(output_dir)

        # Load msgpack
        core_msgpack_data = msgpack.unpackb(Path(result["core_msgpack_file"]).read_bytes(), raw=False)

        # Should be serializable back to JSON
        json_str = json.dumps(core_msgpack_data)
        recovered = json.loads(json_str)

        assert recovered["category"] == "CORE"
        assert "items" in recovered
        assert "fingerprint" in recovered

    def test_compilation_idempotence(self, compiler, output_dir):
        """Test that running compilation twice produces identical results"""
        result1 = compiler.compile(output_dir)

        # Compile again
        result2 = compiler.compile(output_dir)

        # Fingerprints should be identical
        assert result1["core_fingerprint"] == result2["core_fingerprint"]
        assert result1["client_fingerprint"] == result2["client_fingerprint"]

        # File sizes should be identical
        size1packages = Path(result1["core_msgpack_file"]).stat().st_size
        size2packages = Path(result2["core_msgpack_file"]).stat().st_size
        assert size1packages == size2packages, "Core msgpack size changed"

        size1_client = Path(result1["client_msgpack_file"]).stat().st_size
        size2_client = Path(result2["client_msgpack_file"]).stat().st_size
        assert size1_client == size2_client, "Client msgpack size changed"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
