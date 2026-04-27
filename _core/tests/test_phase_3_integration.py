"""
Tests for PHASE 3: End-to-End Integration

Validates complete governance compilation pipeline (PHASE 1 + PHASE 2):
1. Source files → JSON consolidation (PHASE 1)
2. JSON → msgpack serialization (PHASE 2)
3. Fingerprint preservation and salt strategy
4. Idempotence
5. Round-trip deserialization
6. Complete data flow
"""

import json
from pathlib import Path

import msgpack
import pytest
from governance_compiler import GovernanceCompiler
from governance_orchestrator import GovernanceOrchestrator
from pipeline_builder import PipelineBuilder


class TestPhase3Integration:
    """Integration tests for complete pipeline"""

    @pytest.fixture
    def temp_compiled_dir(self, tmp_path):
        """Create temporary compiled directory for testing"""
        return str(tmp_path / "compiled")

    def test_orchestrator_runs_full_pipeline(self):
        """Test that orchestrator runs both phases successfully"""
        orchestrator = GovernanceOrchestrator()
        result = orchestrator.run_full_pipeline()

        assert result is not None, "Orchestrator returned None"
        assert result.get("full_pipeline_success") is True
        assert result.get("validated") is True

    def test_end_to_end_fingerprints_consistent(self):
        """Test fingerprints remain consistent through pipeline and compiler"""
        # Run PHASE 1
        builder = PipelineBuilder("_spec")
        phase1_result = builder.build()
        phase1_core_fp = phase1_result["governance_core"]["fingerprint"]
        phase1_client_fp = phase1_result["governance_client"]["fingerprint"]

        # Save outputs
        builder.save_outputs("compiler/compiled")

        # Run PHASE 2
        compiler = GovernanceCompiler("compiler/compiled")
        phase2_result = compiler.compile("compiler/compiled")

        # Verify fingerprints preserved
        assert phase1_core_fp == phase2_result["core_fingerprint"], "Core fingerprint changed in compiler"
        assert phase1_client_fp == phase2_result["client_fingerprint"], "Client fingerprint changed in compiler"

    def test_core_fingerprint_salt_strategy(self):
        """Test that core fingerprint is properly used as salt for client"""
        # Build and compile
        builder = PipelineBuilder("_spec")
        builder.save_outputs("compiler/compiled")

        compiler = GovernanceCompiler("compiler/compiled")
        result = compiler.compile("compiler/compiled")

        core_fp = result["core_fingerprint"]
        core_salt = result["core_fingerprint_salt"]

        assert core_fp == core_salt, "Core fingerprint not used as salt"

    def test_msgpack_deserializes_correctly(self):
        """Test that msgpack files deserialize to valid data"""
        # Build and compile
        builder = PipelineBuilder("_spec")
        builder.save_outputs("compiler/compiled")

        compiler = GovernanceCompiler("compiler/compiled")
        result = compiler.compile("compiler/compiled")

        # Deserialize core msgpack
        core_msgpack_file = result["core_msgpack_file"]
        core_data = msgpack.unpackb(Path(core_msgpack_file).read_bytes(), raw=False)

        assert core_data["category"] == "CORE"
        assert "items" in core_data
        assert "fingerprint" in core_data
        assert len(core_data["items"]) > 0

        # Deserialize client msgpack
        client_msgpack_file = result["client_msgpack_file"]
        client_data = msgpack.unpackb(Path(client_msgpack_file).read_bytes(), raw=False)

        assert client_data["category"] == "CLIENT"
        assert "items" in client_data
        assert "fingerprint" in client_data
        assert len(client_data["items"]) > 0

    def test_round_trip_msgpack_to_json(self):
        """Test msgpack can be deserialized and converted back to JSON"""
        # Build and compile
        builder = PipelineBuilder("_spec")
        builder.save_outputs("compiler/compiled")

        compiler = GovernanceCompiler("compiler/compiled")
        result = compiler.compile("compiler/compiled")

        # Load msgpack
        core_msgpack_data = msgpack.unpackb(Path(result["core_msgpack_file"]).read_bytes(), raw=False)

        # Convert to JSON and back
        json_str = json.dumps(core_msgpack_data)
        recovered = json.loads(json_str)

        # Verify structure preserved
        assert recovered["category"] == "CORE"
        assert recovered["fingerprint"] == core_msgpack_data["fingerprint"]
        assert len(recovered["items"]) == len(core_msgpack_data["items"])

    def test_pipeline_idempotence(self):
        """Test pipeline produces same output when run twice"""
        # First run
        builder1 = PipelineBuilder("_spec")
        result1 = builder1.build()
        core_fp1 = result1["governance_core"]["fingerprint"]
        client_fp1 = result1["governance_client"]["fingerprint"]

        # Second run
        builder2 = PipelineBuilder("_spec")
        result2 = builder2.build()
        core_fp2 = result2["governance_core"]["fingerprint"]
        client_fp2 = result2["governance_client"]["fingerprint"]

        # Should be identical
        assert core_fp1 == core_fp2, "Pipeline not idempotent (core)"
        assert client_fp1 == client_fp2, "Pipeline not idempotent (client)"

    def test_compiler_idempotence(self):
        """Test compiler produces same output when run twice"""
        # Prepare
        builder = PipelineBuilder("_spec")
        builder.save_outputs("compiler/compiled")

        # First compile
        compiler1 = GovernanceCompiler("compiler/compiled")
        result1 = compiler1.compile("compiler/compiled")
        size1_core = Path(result1["core_msgpack_file"]).stat().st_size

        # Second compile
        compiler2 = GovernanceCompiler("compiler/compiled")
        result2 = compiler2.compile("compiler/compiled")
        size2_core = Path(result2["core_msgpack_file"]).stat().st_size

        # Should be identical
        assert size1_core == size2_core, "Compiler not idempotent (size differs)"
        assert result1["core_fingerprint"] == result2["core_fingerprint"]

    def test_all_items_categorized_correctly(self):
        """Test that items are correctly categorized by customizable flag"""
        # Build
        builder = PipelineBuilder("_spec")
        builder.save_outputs("compiler/compiled")

        # Load JSONs
        with open("compiler/compiled/governance-core.json") as f:
            core_data = json.load(f)
        with open("compiler/compiled/governance-client.json") as f:
            client_data = json.load(f)

        # All core items should have customizable=false
        for item in core_data["items"]:
            assert item["customizable"] is False, f"Item {item['id']} in CORE with customizable=true"

        # All client items should have customizable=true
        for item in client_data["items"]:
            assert item["customizable"] is True, f"Item {item['id']} in CLIENT with customizable=false"

    def test_metadata_reflects_content(self):
        """Test that metadata accurately reflects msgpack content"""
        # Build and compile
        builder = PipelineBuilder("_spec")
        builder.save_outputs("compiler/compiled")

        compiler = GovernanceCompiler("compiler/compiled")
        result = compiler.compile("compiler/compiled")

        # Load metadata
        with open(result["core_metadata"]) as f:
            core_meta = json.load(f)

        # Load msgpack
        core_msgpack_data = msgpack.unpackb(Path(result["core_msgpack_file"]).read_bytes(), raw=False)

        # Verify counts match
        assert core_meta["item_count"] == len(core_msgpack_data["items"])

        # Verify fingerprint matches
        assert core_meta["fingerprint"] == core_msgpack_data["fingerprint"]

    def test_separation_preserved_through_compilation(self):
        """Test that CORE/CLIENT separation is preserved through both phases"""
        # Build and compile
        builder = PipelineBuilder("_spec")
        phase1_result = builder.build()
        builder.save_outputs("compiler/compiled")

        compiler = GovernanceCompiler("compiler/compiled")
        phase2_result = compiler.compile("compiler/compiled")

        # Verify separation
        phase1_core_count = len(phase1_result["core_items"])
        phase1_client_count = len(phase1_result["client_items"])
        phase2_core_count = phase2_result["core_item_count"]
        phase2_client_count = phase2_result["client_item_count"]

        assert phase1_core_count == phase2_core_count, "Core item count changed"
        assert phase1_client_count == phase2_client_count, "Client item count changed"

    def test_criticality_ordering_preserved(self):
        """Test that criticality ordering is preserved through compilation"""
        criticality_order = {"OBRIGATÓRIO": 0, "ALERTA": 1, "OPCIONAL": 2}

        # Build
        builder = PipelineBuilder("_spec")
        builder.save_outputs("compiler/compiled")

        # Load JSON
        with open("compiler/compiled/governance-core.json") as f:
            core_data = json.load(f)

        # Check ordering
        prev_level = -1
        for item in core_data["items"]:
            current_level = criticality_order.get(item["criticality"], 99)
            assert current_level >= prev_level, f"Items not ordered by criticality: {item['criticality']}"
            prev_level = current_level

    def test_no_data_loss_through_pipeline(self):
        """Test that no data is lost when processing through pipeline+compiler"""
        # Build
        builder = PipelineBuilder("_spec")
        phase1_result = builder.build()
        total_items_phase1 = len(phase1_result["core_items"]) + len(phase1_result["client_items"])

        # Compile
        builder.save_outputs("compiler/compiled")
        compiler = GovernanceCompiler("compiler/compiled")
        phase2_result = compiler.compile("compiler/compiled")
        total_items_phase2 = phase2_result["core_item_count"] + phase2_result["client_item_count"]

        # Should be same count
        assert total_items_phase1 == total_items_phase2, f"Data lost: {total_items_phase1} → {total_items_phase2}"

    def test_orchestrator_summary_is_valid(self):
        """Test that orchestrator provides valid deployment summary"""
        orchestrator = GovernanceOrchestrator()
        orchestrator.run_full_pipeline()

        summary = orchestrator.get_deployment_summary()

        assert summary["status"] == "ready_for_deployment"
        assert "artifacts" in summary
        assert "core_msgpack" in summary["artifacts"]
        assert "client_msgpack" in summary["artifacts"]
        assert "core_metadata" in summary["artifacts"]
        assert "client_metadata" in summary["artifacts"]

    def test_msgpack_files_smaller_than_json(self):
        """Test that msgpack is more compact than JSON"""
        # Build and save JSONs
        builder = PipelineBuilder("_spec")
        builder.save_outputs("compiler/compiled")

        # Get JSON sizes
        core_json_size = Path("compiler/compiled/governance-core.json").stat().st_size
        client_json_size = Path("compiler/compiled/governance-client.json").stat().st_size
        total_json_size = core_json_size + client_json_size

        # Compile to msgpack
        compiler = GovernanceCompiler("compiler/compiled")
        result = compiler.compile("compiler/compiled")

        # Get msgpack sizes
        core_msgpack_size = Path(result["core_msgpack_file"]).stat().st_size
        client_msgpack_size = Path(result["client_msgpack_file"]).stat().st_size
        total_msgpack_size = core_msgpack_size + client_msgpack_size

        # msgpack should be more compact (at least for large files)
        assert total_msgpack_size < total_json_size, "msgpack not more compact than JSON"

    def test_complete_workflow_summary(self):
        """Test complete workflow with all validations"""
        orchestrator = GovernanceOrchestrator()
        result = orchestrator.run_full_pipeline()

        # Verify complete workflow
        assert result["full_pipeline_success"] is True
        assert result["validated"] is True
        assert result["phase_1"]["success"] is True
        assert result["phase_2"]["success"] is True

        # Verify fingerprint strategy
        p1 = result["phase_1"]
        p2 = result["phase_2"]
        assert p1["core_fingerprint"] == p2["core_fingerprint"]
        assert p1["client_fingerprint"] == p2["client_fingerprint"]
        assert p1["core_fingerprint"] == p2["core_fingerprint_salt"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
