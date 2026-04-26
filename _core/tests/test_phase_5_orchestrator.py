"""
Tests for Phase 5: Orchestrator Workflow

Validates:
1. Orchestrator coordinates all components
2. Complete workflow runs successfully
3. All validations pass
4. Ready for wizard and agent integration
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / ".sdd-wizard"))

from wizard_orchestrator import WizardOrchestrator


class TestPhase5Orchestrator:
    """Test PHASE 5: Orchestrator"""

    @pytest.fixture
    def orchestrator(self):
        """Create orchestrator instance"""
        return WizardOrchestrator()

    def test_orchestrator_runs_full_workflow(self, orchestrator):
        """Test that orchestrator runs complete workflow"""
        result = orchestrator.run_full_workflow()

        assert result.get("success") is True
        assert result.get("loader_status") == "ready"
        assert result.get("integrator_status") == "ready"

    def test_orchestrator_loads_governance(self, orchestrator):
        """Test governance loading"""
        result = orchestrator.run_full_workflow()

        summary = result.get("governance_summary", {})
        assert summary.get("status") == "loaded"
        assert summary.get("core_items") > 0
        assert summary.get("client_items") > 0

    def test_orchestrator_generates_templates(self, orchestrator):
        """Test template generation"""
        result = orchestrator.run_full_workflow()

        assert result.get("templates_generated") > 0
        assert result.get("templates_location") is not None

    def test_orchestrator_validates_workflow(self, orchestrator):
        """Test workflow validation"""
        result = orchestrator.run_full_workflow()

        deploy_summary = result.get("deployment_summary", {})
        assert deploy_summary.get("status") == "ready_for_wizard_and_agents"

    def test_orchestrator_components_initialized(self, orchestrator):
        """Test that all components are initialized"""
        orchestrator.run_full_workflow()

        assert orchestrator.loader is not None
        assert orchestrator.integrator is not None
        assert orchestrator.generator is not None

    def test_orchestrator_workflow_status(self, orchestrator):
        """Test workflow status reporting"""
        orchestrator.run_full_workflow()

        status = orchestrator.get_workflow_status()

        assert status.get("loader") == "initialized"
        assert status.get("integrator") == "initialized"
        assert status.get("generator") == "initialized"
        assert status.get("templates_exist") is True

    def test_orchestrator_fingerprints(self, orchestrator):
        """Test fingerprint handling"""
        result = orchestrator.run_full_workflow()

        fps = result.get("deployment_summary", {}).get("fingerprints", {})

        assert fps.get("core") is not None
        assert fps.get("client") is not None
        assert fps.get("salt") is not None
        assert fps.get("core") != fps.get("client")
        assert fps.get("core") == fps.get("salt")

    def test_orchestrator_governance_items_count(self, orchestrator):
        """Test governance item counts"""
        result = orchestrator.run_full_workflow()

        summary = result.get("deployment_summary", {})

        assert summary.get("total_items") == 155
        assert summary.get("core_items") == 4
        assert summary.get("client_items") == 151
        assert summary.get("customizable_items") == 151
        assert summary.get("immutable_items") == 4

    def test_orchestrator_deployment_summary(self, orchestrator):
        """Test deployment summary generation"""
        result = orchestrator.run_full_workflow()

        summary = result.get("deployment_summary", {})

        assert summary.get("version") == "3.0"
        assert summary.get("status") == "ready_for_wizard_and_agents"
        assert summary.get("templates_generated") > 0

    def test_orchestrator_ready_for_wizard(self, orchestrator):
        """Test that workflow is ready for wizard"""
        result = orchestrator.run_full_workflow()

        # Should have templates for wizard to use
        assert result.get("templates_generated") > 0

        # Should have governance loaded
        summary = result.get("governance_summary", {})
        assert summary.get("core_items") > 0

        # Should show ready status
        deploy_summary = result.get("deployment_summary", {})
        assert "wizard" in deploy_summary.get("status", "").lower()

    def test_orchestrator_idempotent(self, orchestrator):
        """Test that orchestrator can run multiple times"""
        result1 = orchestrator.run_full_workflow()
        assert result1.get("success") is True

        orchestrator2 = WizardOrchestrator()
        result2 = orchestrator2.run_full_workflow()
        assert result2.get("success") is True

        # Should have same counts
        assert result1.get("templates_generated") == result2.get("templates_generated")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
