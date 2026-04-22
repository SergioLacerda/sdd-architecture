"""
Tests for PHASE 4: Deployment

Validates:
1. Deployment files copied to .sdd-runtime/compiled/
2. All required files present
3. Metadata valid
4. Deployment checklist generated
5. Manifest created
"""

import json
from pathlib import Path
import pytest
import sys

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / ".sdd-core"))

from deployment_manager import DeploymentManager


class TestPhase4Deployment:
    """Test PHASE 4: Deployment"""

    @pytest.fixture
    def manager(self):
        """Create deployment manager instance"""
        return DeploymentManager()

    def test_deployment_succeeds(self, manager):
        """Test that deployment completes successfully"""
        result = manager.deploy()

        assert result.get("success") is True, "Deployment failed"
        assert result.get("deployment_location") is not None
        assert result.get("checklist") is not None

    def test_all_files_deployed(self, manager):
        """Test that all required files are deployed"""
        result = manager.deploy()
        deployed_files = result.get("deployed_files", {})

        assert "governance-core.compiled.msgpack" in deployed_files
        assert "governance-client-template.compiled.msgpack" in deployed_files
        assert "metadata-core.json" in deployed_files
        assert "metadata-client-template.json" in deployed_files

    def test_deployment_location_correct(self, manager):
        """Test that deployment location is correct"""
        result = manager.deploy()

        location = result.get("deployment_location")
        assert ".sdd-runtime/compiled" in location
        assert Path(location).exists()

    def test_checklist_all_passed(self, manager):
        """Test that deployment checklist shows all checks passed"""
        result = manager.deploy()
        checklist = result.get("checklist", {})

        for check_name, status in checklist.items():
            assert status is True, f"Checklist failed: {check_name}"

    def test_manifest_valid(self, manager):
        """Test that deployment manifest is valid JSON"""
        result = manager.deploy()
        manifest = result.get("manifest", {})

        # Check required manifest fields
        assert manifest.get("version") == "3.0"
        assert manifest.get("deployment_date") is not None
        assert manifest.get("artifacts") is not None
        assert manifest.get("status") == "deployed"

    def test_manifest_file_created(self, manager):
        """Test that DEPLOYMENT_MANIFEST.json file is created"""
        manager.deploy()

        manifest_file = manager.runtime_compiled / "DEPLOYMENT_MANIFEST.json"
        assert manifest_file.exists(), "DEPLOYMENT_MANIFEST.json not created"

        # Verify it's valid JSON
        with open(manifest_file) as f:
            manifest = json.load(f)

        assert manifest["version"] == "3.0"
        assert manifest["status"] == "deployed"

    def test_core_msgpack_deployed(self, manager):
        """Test that core msgpack is deployed"""
        result = manager.deploy()

        core_msgpack = manager.runtime_compiled / "governance-core.compiled.msgpack"
        assert core_msgpack.exists(), "Core msgpack not deployed"

        # Should have size > 0
        size = core_msgpack.stat().st_size
        assert size > 0, "Core msgpack is empty"

    def test_client_msgpack_deployed(self, manager):
        """Test that client msgpack is deployed"""
        result = manager.deploy()

        client_msgpack = (
            manager.runtime_compiled / "governance-client-template.compiled.msgpack"
        )
        assert client_msgpack.exists(), "Client msgpack not deployed"

        # Should have size > 0 and larger than core
        size = client_msgpack.stat().st_size
        assert size > 0, "Client msgpack is empty"

    def test_core_metadata_deployed(self, manager):
        """Test that core metadata is deployed"""
        result = manager.deploy()

        metadata_file = manager.runtime_compiled / "metadata-core.json"
        assert metadata_file.exists(), "Core metadata not deployed"

        # Verify valid JSON
        with open(metadata_file) as f:
            metadata = json.load(f)

        assert metadata["type"] == "core"
        assert metadata["readonly"] is True

    def test_client_metadata_deployed(self, manager):
        """Test that client metadata is deployed"""
        result = manager.deploy()

        metadata_file = manager.runtime_compiled / "metadata-client-template.json"
        assert metadata_file.exists(), "Client metadata not deployed"

        # Verify valid JSON
        with open(metadata_file) as f:
            metadata = json.load(f)

        assert metadata["type"] == "client-template"
        assert metadata["customizable"] is True

    def test_backup_directory_created(self, manager):
        """Test that backup directory is created"""
        result = manager.deploy()

        backup_dir = manager.runtime_compiled / "backup"
        assert backup_dir.exists(), "Backup directory not created"
        assert backup_dir.is_dir(), "Backup is not a directory"

    def test_deployment_status(self, manager):
        """Test deployment status check"""
        manager.deploy()

        status = manager.get_deployment_status()

        assert status["deployed"] is True
        assert status["files_present"]["core_msgpack"] is True
        assert status["files_present"]["client_msgpack"] is True
        assert status["files_present"]["core_metadata"] is True
        assert status["files_present"]["client_metadata"] is True

    def test_next_steps_provided(self, manager):
        """Test that next steps are provided"""
        result = manager.deploy()

        next_steps = result.get("next_steps", [])
        assert len(next_steps) > 0, "No next steps provided"

        # Should include git commands
        next_steps_text = "\n".join(next_steps)
        assert "git" in next_steps_text.lower()
        assert "tag" in next_steps_text.lower()

    def test_metadata_fingerprints_preserved(self, manager):
        """Test that metadata fingerprints are preserved in deployment"""
        # Load original metadata
        with open(manager.compiled_dir / "metadata-core.json") as f:
            original_core_meta = json.load(f)

        # Deploy
        manager.deploy()

        # Load deployed metadata
        with open(manager.runtime_compiled / "metadata-core.json") as f:
            deployed_core_meta = json.load(f)

        # Fingerprints should be identical
        assert (
            original_core_meta["fingerprint"] == deployed_core_meta["fingerprint"]
        ), "Core fingerprint changed during deployment"

    def test_files_readable_after_deployment(self, manager):
        """Test that deployed files are readable"""
        manager.deploy()

        # Test core msgpack is readable
        core_file = manager.runtime_compiled / "governance-core.compiled.msgpack"
        data = core_file.read_bytes()
        assert len(data) > 0, "Core msgpack not readable"

        # Test metadata is readable as JSON
        metadata_file = manager.runtime_compiled / "metadata-core.json"
        with open(metadata_file) as f:
            json.load(f)

    def test_deployment_idempotent(self, manager):
        """Test that deployment can be run multiple times"""
        # First deployment
        result1 = manager.deploy()
        size1 = (manager.runtime_compiled / "governance-core.compiled.msgpack").stat().st_size

        # Second deployment
        result2 = manager.deploy()
        size2 = (manager.runtime_compiled / "governance-core.compiled.msgpack").stat().st_size

        # Sizes should be identical
        assert size1 == size2, "File sizes differ on second deployment"

        # Results should show success both times
        assert result1.get("success") is True
        assert result2.get("success") is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
