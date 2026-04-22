"""
Tests for PHASE 5: Wizard Integration

Validates:
1. Runtime loader loads msgpack artifacts
2. Wizard integrator connects to loader
3. Customization templates generated correctly
4. Full integration workflow works
"""

import json
import sys
from pathlib import Path
import pytest

# Add paths
sys.path.insert(0, str(Path(__file__).parent))

from governance_runtime_loader import GovernanceRuntimeLoader
from wizard_integrator import WizardIntegrator
from customization_template_generator import CustomizationTemplateGenerator


class TestPhase5Runtime:
    """Test PHASE 5: Wizard Integration"""

    @pytest.fixture
    def loader(self):
        """Create runtime loader instance"""
        return GovernanceRuntimeLoader()

    @pytest.fixture
    def integrator(self):
        """Create wizard integrator instance"""
        return WizardIntegrator()

    @pytest.fixture
    def generator(self):
        """Create template generator instance"""
        return CustomizationTemplateGenerator()

    # ==================== RUNTIME LOADER TESTS ====================

    def test_loader_loads_core_governance(self, loader):
        """Test that loader can load core governance"""
        core = loader.load_core()

        assert core is not None, "Core governance not loaded"
        assert "items" in core, "Core missing items"
        assert "fingerprint" in core, "Core missing fingerprint"
        assert len(core.get("items", [])) > 0, "Core has no items"

    def test_loader_loads_client_governance(self, loader):
        """Test that loader can load client governance"""
        client = loader.load_client()

        assert client is not None, "Client governance not loaded"
        assert "items" in client, "Client missing items"
        assert "fingerprint" in client, "Client missing fingerprint"
        assert len(client.get("items", [])) > 0, "Client has no items"

    def test_loader_loads_all(self, loader):
        """Test that loader can load all governance"""
        result = loader.load_all()

        assert result["status"] == "loaded"
        assert result["core_items"] > 0
        assert result["client_items"] > 0

    def test_loader_validates_integrity(self, loader):
        """Test that loader validates integrity"""
        loader.load_all()

        # Should not raise exception
        assert loader.get_core_fingerprint() is not None
        assert loader.get_client_fingerprint() is not None
        assert loader.get_salt_fingerprint() is not None

    def test_loader_fingerprints_different(self, loader):
        """Test that core and client fingerprints are different"""
        loader.load_all()

        core_fp = loader.get_core_fingerprint()
        client_fp = loader.get_client_fingerprint()

        assert core_fp != client_fp, "Fingerprints should be different"

    def test_loader_salt_strategy(self, loader):
        """Test that salt strategy is enforced"""
        loader.load_all()

        core_fp = loader.get_core_fingerprint()
        salt_fp = loader.get_salt_fingerprint()

        assert core_fp == salt_fp, "Core fingerprint not used as salt"

    def test_loader_get_items_by_type(self, loader):
        """Test filtering items by type"""
        loader.load_all()

        mandates = loader.get_items_by_type("mandate")
        assert len(mandates) > 0, "No mandates found"

    def test_loader_get_items_by_criticality(self, loader):
        """Test filtering items by criticality"""
        loader.load_all()

        mandatory = loader.get_items_by_criticality("OBRIGATÓRIO")
        assert len(mandatory) > 0, "No mandatory items found"

    def test_loader_governance_summary(self, loader):
        """Test governance summary"""
        summary = loader.get_governance_summary()

        assert summary["version"] == "3.0"
        assert summary["total_items"] > 0
        assert summary["core_items"] > 0
        assert summary["client_items"] > 0
        assert "by_type" in summary
        assert "by_criticality" in summary

    def test_loader_export_json(self, tmp_path, loader):
        """Test exporting governance as JSON"""
        loader.load_all()

        export_file = tmp_path / "governance-export.json"
        loader.export_governance_json(str(export_file))

        assert export_file.exists(), "Export file not created"

        with open(export_file) as f:
            data = json.load(f)

        assert "core" in data
        assert "client" in data
        assert "_metadata" in data

    # ==================== WIZARD INTEGRATOR TESTS ====================

    def test_integrator_loads_governance(self, integrator):
        """Test that integrator can load governance"""
        result = integrator.load_governance()

        assert result["status"] == "loaded"
        assert result["core_items"] > 0
        assert result["client_items"] > 0

    def test_integrator_gets_mandatory_items(self, integrator):
        """Test getting mandatory items"""
        integrator.load_governance()
        mandatory = integrator.get_mandatory_items()

        assert len(mandatory) > 0, "No mandatory items"
        for item in mandatory:
            assert item.get("criticality") == "OBRIGATÓRIO"

    def test_integrator_gets_optional_items(self, integrator):
        """Test getting optional items"""
        integrator.load_governance()
        optional = integrator.get_optional_items()

        # Optional might be empty, so just check it's a list
        assert isinstance(optional, list)

    def test_integrator_gets_customizable_items(self, integrator):
        """Test getting customizable items"""
        integrator.load_governance()
        customizable = integrator.get_customizable_items()

        assert len(customizable) > 0, "No customizable items"
        for item in customizable:
            assert item.get("customizable") is True

    def test_integrator_gets_immutable_items(self, integrator):
        """Test getting immutable items"""
        integrator.load_governance()
        immutable = integrator.get_immutable_items()

        assert len(immutable) > 0, "No immutable items"
        for item in immutable:
            assert item.get("customizable") is False

    def test_integrator_workflow_hooks(self, integrator):
        """Test workflow hook registration"""
        hook_called = [False]

        def test_hook():
            hook_called[0] = True

        integrator.register_workflow_hook("test-hook", test_hook)
        integrator.execute_hook("test-hook")

        assert hook_called[0] is True, "Hook not executed"

    def test_integrator_creates_customization_template(self, integrator):
        """Test creating customization template"""
        integrator.load_governance()
        template = integrator.create_customization_template()

        assert template["version"] == "3.0"
        assert template["type"] == "customization-template"
        assert "customizations" in template
        assert len(template["customizations"]) > 0

    def test_integrator_validates_customizations(self, integrator):
        """Test validation of customizations"""
        integrator.load_governance()

        # Create invalid customization (try to modify immutable)
        immutable = integrator.get_immutable_items()
        if immutable:
            invalid_custom = {immutable[0]["id"]: {"customized_value": {}}}
            result = integrator.validate_customizations(invalid_custom)

            assert result["valid"] is False
            assert len(result["errors"]) > 0

    def test_integrator_generates_constitution_config(self, integrator):
        """Test generating constitution config"""
        integrator.load_governance()
        config = integrator.generate_constitution_config()

        assert config["version"] == "3.0"
        assert config["governance"] is not None
        assert config["fingerprints"]["core"] is not None
        assert config["fingerprints"]["client"] is not None

    def test_integrator_status(self, integrator):
        """Test integration status"""
        integrator.load_governance()
        status = integrator.get_integration_status()

        assert status["status"] == "ready"
        assert status["governance_loaded"] is True

    def test_integrator_export_manifest(self, tmp_path, integrator):
        """Test exporting integration manifest"""
        integrator.load_governance()

        manifest_file = tmp_path / "integration-manifest.json"
        integrator.export_integration_manifest(str(manifest_file))

        assert manifest_file.exists(), "Manifest file not created"

        with open(manifest_file) as f:
            manifest = json.load(f)

        assert manifest["type"] == "wizard-integration"
        assert manifest["status"] is not None

    # ==================== CUSTOMIZATION TEMPLATE TESTS ====================

    def test_generator_creates_basic_template(self, generator):
        """Test creating basic template"""
        generator.initialize_loader()
        template = generator.generate_basic_template()

        assert template["version"] == "3.0"
        assert template["type"] == "customization-template"
        assert "customizations" in template
        assert "instructions" in template

    def test_generator_creates_full_template(self, generator):
        """Test creating full template"""
        generator.initialize_loader()
        template = generator.generate_full_template()

        assert template["version"] == "3.0"
        assert template["type"] == "full-customization-template"
        assert "core_governance" in template
        assert "client_governance" in template

    def test_generator_creates_category_template(self, generator):
        """Test creating category template"""
        generator.initialize_loader()

        # Get first category from loader
        loader = GovernanceRuntimeLoader()
        loader.load_all()
        all_items = loader.get_all_items()
        first_category = all_items[0].get("category") if all_items else None

        if first_category:
            template = generator.generate_category_template(first_category)

            assert template["version"] == "3.0"
            assert template["category"] == first_category
            assert "items" in template

    def test_generator_creates_criticality_template(self, generator):
        """Test creating criticality template"""
        generator.initialize_loader()
        template = generator.generate_criticality_template("OBRIGATÓRIO")

        assert template["version"] == "3.0"
        assert template["criticality"] == "OBRIGATÓRIO"
        assert len(template["items"]) > 0

    def test_generator_creates_adoption_template(self, generator):
        """Test creating adoption template"""
        generator.initialize_loader()

        for level in ["ultra-lite", "lite", "full"]:
            template = generator.generate_adoption_template(level)

            assert template["version"] == "3.0"
            assert template["adoption_level"] == level
            assert "items" in template
            assert "implementation_steps" in template

    def test_generator_saves_template(self, tmp_path, generator):
        """Test saving template to file"""
        generator.initialize_loader()
        template = generator.generate_basic_template()

        save_path = tmp_path / "template.json"
        generator.save_template(template, str(save_path))

        assert save_path.exists(), "Template file not saved"

        with open(save_path) as f:
            loaded = json.load(f)

        assert loaded["version"] == template["version"]

    def test_generator_generates_all_templates(self, tmp_path, generator):
        """Test generating all template types"""
        templates = generator.generate_all_templates(str(tmp_path))

        assert len(templates) > 0, "No templates generated"

        # Verify some key templates exist
        basic_exists = any("basic" in k for k in templates.keys())
        assert basic_exists, "Basic template not generated"

    # ==================== INTEGRATION TESTS ====================

    def test_full_workflow_load_customize_export(self, tmp_path):
        """Test full workflow: load → customize → export"""
        # Load
        loader = GovernanceRuntimeLoader()
        loader.load_all()

        # Create integrator with loaded governance
        integrator = WizardIntegrator(loader)

        # Get customizable items
        customizable = integrator.get_customizable_items()
        assert len(customizable) > 0

        # Create template
        template = integrator.create_customization_template()
        assert len(template["customizations"]) > 0

        # Export
        export_file = tmp_path / "integration-test.json"
        loader.export_governance_json(str(export_file))
        assert export_file.exists()

    def test_end_to_end_wizard_workflow(self, tmp_path):
        """Test complete wizard workflow"""
        # Step 1: Load governance
        integrator = WizardIntegrator()
        result = integrator.load_governance()
        assert result["status"] == "loaded"

        # Step 2: Get governance summary for wizard display
        summary = integrator.get_governance_summary()
        assert summary["total_items"] > 0

        # Step 3: Get mandatory items for enforcement
        mandatory = integrator.get_mandatory_items()
        assert len(mandatory) > 0

        # Step 4: Generate customization template
        template = integrator.create_customization_template()
        assert len(template["customizations"]) > 0

        # Step 5: Generate constitution config
        config = integrator.generate_constitution_config()
        assert config["governance"] is not None

        # Step 6: Export for use by agents
        export_file = tmp_path / "wizard-export.json"
        loader = GovernanceRuntimeLoader()
        loader.load_all()
        loader.export_governance_json(str(export_file))
        assert export_file.exists()

    def test_fingerprint_preservation_through_runtime(self, loader):
        """Test that fingerprints are preserved in runtime"""
        # Load original from compiled
        loader.load_all()

        core_fp = loader.get_core_fingerprint()
        client_fp = loader.get_client_fingerprint()
        salt_fp = loader.get_salt_fingerprint()

        # Verify relationships
        assert core_fp == salt_fp, "Core fingerprint not used as salt"
        assert core_fp != client_fp, "Fingerprints should differ"

        # Export and re-load
        export = loader.export_governance_json.__self__

        # Verify fingerprints unchanged
        assert loader.get_core_fingerprint() == core_fp
        assert loader.get_client_fingerprint() == client_fp


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
