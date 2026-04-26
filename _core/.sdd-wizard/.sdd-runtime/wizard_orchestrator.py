"""
PHASE 5: Wizard Orchestrator
Coordinate runtime loading, wizard integration, and template generation

Provides:
1. Complete wizard initialization workflow
2. Governance loading and validation
3. Template generation and export
4. Ready state for agent runtime
"""

import sys
from pathlib import Path
from typing import Any, Dict

# Add runtime to path
sys.path.insert(0, str(Path(__file__).parent))

from customization_template_generator import CustomizationTemplateGenerator
from governance_runtime_loader import GovernanceRuntimeLoader
from wizard_integrator import WizardIntegrator


class WizardOrchestrator:
    """Orchestrate complete wizard integration workflow"""

    def __init__(self, runtime_dir: str = None):
        """Initialize orchestrator"""
        if runtime_dir is None:
            runtime_dir = Path(__file__).parent
        else:
            runtime_dir = Path(runtime_dir)

        self.runtime_dir = Path(runtime_dir)
        self.templates_dir = self.runtime_dir / "templates"

        self.loader = None
        self.integrator = None
        self.generator = None

    def run_full_workflow(self) -> Dict[str, Any]:
        """
        Execute complete wizard initialization workflow

        Returns:
            Dictionary with workflow results
        """
        print("🔗 Starting PHASE 5: Wizard Integration...")
        print()

        # Step 1: Load governance
        print("📦 Step 1: Loading governance runtime...")
        load_result = self._step_load_governance()
        if not load_result:
            print("❌ Load failed")
            return {"success": False}
        print("✅ Governance loaded")
        print()

        # Step 2: Initialize wizard integration
        print("🔗 Step 2: Initializing wizard integration...")
        integration_result = self._step_initialize_integration()
        if not integration_result:
            print("❌ Integration failed")
            return {"success": False}
        print("✅ Wizard integration initialized")
        print()

        # Step 3: Generate customization templates
        print("📝 Step 3: Generating customization templates...")
        template_result = self._step_generate_templates()
        if not template_result:
            print("❌ Template generation failed")
            return {"success": False}
        print("✅ Templates generated")
        print()

        # Step 4: Validate complete workflow
        print("✔️ Step 4: Validating complete workflow...")
        if not self._validate_workflow():
            print("❌ Validation failed")
            return {"success": False}
        print("✅ All validations passed")
        print()

        # Step 5: Generate deployment summary
        summary = self._generate_deployment_summary()

        return {
            "success": True,
            "loader_status": "ready",
            "integrator_status": "ready",
            "templates_generated": len(template_result.get("templates", {})),
            "templates_location": str(self.templates_dir),
            "governance_summary": load_result,
            "deployment_summary": summary,
        }

    def _step_load_governance(self) -> Dict[str, Any]:
        """Load governance from runtime"""
        self.loader = GovernanceRuntimeLoader()
        result = self.loader.load_all()
        return result

    def _step_initialize_integration(self) -> bool:
        """Initialize wizard integration"""
        self.integrator = WizardIntegrator(self.loader)

        # Verify status
        status = self.integrator.get_integration_status()
        return status.get("status") == "ready"

    def _step_generate_templates(self) -> Dict[str, Any]:
        """Generate customization templates"""
        self.generator = CustomizationTemplateGenerator(self.loader)

        # Generate all templates
        templates = self.generator.generate_all_templates(str(self.templates_dir))

        return {"templates": templates}

    def _validate_workflow(self) -> bool:
        """Validate complete workflow"""
        checks = [
            ("Loader initialized", self.loader is not None),
            ("Governance loaded", self._validate_loader()),
            ("Integrator initialized", self.integrator is not None),
            ("Integration ready", self._validate_integrator()),
            ("Generator initialized", self.generator is not None),
            ("Templates generated", self._validate_templates()),
            ("All fingerprints match", self._validate_fingerprints()),
        ]

        all_passed = True
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"    {status} {check_name}")
            if not result:
                all_passed = False

        return all_passed

    def _validate_loader(self) -> bool:
        """Validate loader state"""
        if self.loader is None:
            return False
        try:
            summary = self.loader.get_governance_summary()
            return summary.get("total_items", 0) > 0
        except:
            return False

    def _validate_integrator(self) -> bool:
        """Validate integrator state"""
        if self.integrator is None:
            return False
        try:
            status = self.integrator.get_integration_status()
            return status.get("status") == "ready"
        except:
            return False

    def _validate_templates(self) -> bool:
        """Validate templates were generated"""
        return self.templates_dir.exists() and any(
            self.templates_dir.glob("*.json")
        )

    def _validate_fingerprints(self) -> bool:
        """Validate fingerprints through workflow"""
        try:
            # Verify fingerprints match in all components
            core_fp = self.loader.get_core_fingerprint()
            client_fp = self.loader.get_client_fingerprint()
            salt_fp = self.loader.get_salt_fingerprint()

            # Core should be used as salt
            if core_fp != salt_fp:
                return False

            # Fingerprints should be different
            if core_fp == client_fp:
                return False

            return True
        except:
            return False

    def _generate_deployment_summary(self) -> Dict[str, Any]:
        """Generate deployment summary"""
        summary = self.loader.get_governance_summary()

        return {
            "status": "ready_for_wizard_and_agents",
            "version": "3.0",
            "total_items": summary.get("total_items"),
            "core_items": summary.get("core_items"),
            "client_items": summary.get("client_items"),
            "customizable_items": len(self.integrator.get_customizable_items()),
            "immutable_items": len(self.integrator.get_immutable_items()),
            "mandatory_items": len(self.integrator.get_mandatory_items()),
            "templates_generated": len(
                list(self.templates_dir.glob("*.json"))
            ),
            "fingerprints": {
                "core": summary.get("core_fingerprint"),
                "client": summary.get("client_fingerprint"),
                "salt": summary.get("salt_fingerprint"),
            },
        }

    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status"""
        return {
            "loader": "initialized" if self.loader else "not-initialized",
            "integrator": "initialized" if self.integrator else "not-initialized",
            "generator": "initialized" if self.generator else "not-initialized",
            "templates_dir": str(self.templates_dir),
            "templates_exist": self.templates_dir.exists(),
        }


if __name__ == "__main__":
    orchestrator = WizardOrchestrator()
    result = orchestrator.run_full_workflow()

    if result.get("success"):
        print()
        print("=" * 70)
        print("🎉 PHASE 5: WIZARD INTEGRATION COMPLETE")
        print("=" * 70)
        print()

        summary = result.get("deployment_summary", {})
        print("📊 Governance Loaded:")
        print(f"  Total Items: {summary.get('total_items')}")
        print(f"  Core (immutable): {summary.get('core_items')}")
        print(f"  Client (customizable): {summary.get('client_items')}")
        print(f"  Customizable: {summary.get('customizable_items')}")
        print(f"  Immutable: {summary.get('immutable_items')}")
        print(f"  Mandatory: {summary.get('mandatory_items')}")

        print()
        print("📝 Templates Generated:")
        print(f"  Location: {result.get('templates_location')}")
        print(f"  Count: {summary.get('templates_generated')}")

        print()
        print("🔐 Fingerprints:")
        fps = summary.get("fingerprints", {})
        print(f"  Core: {fps.get('core', '')[:16]}...")
        print(f"  Client: {fps.get('client', '')[:16]}...")
        print(f"  Salt: {fps.get('salt', '')[:16]}...")

        print()
        print(f"✅ Status: {summary.get('status').upper()}")
        print()
        print("🚀 Ready for:")
        print("  ✅ Wizard initialization")
        print("  ✅ Agent runtime integration")
        print("  ✅ Dynamic customization")
        print("  ✅ Template-based configuration")

    else:
        print()
        print("❌ Workflow failed")
