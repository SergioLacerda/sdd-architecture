"""
PHASE 5: Wizard Integrator
Connect governance runtime with setup wizard

Provides:
1. Integration hooks for wizard to load governance
2. Governance-aware configuration generation
3. Agent integration points
4. Customization workflow support
"""

import json
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


class WizardIntegrator:
    """Integrate governance with setup wizard"""

    def __init__(self, loader=None):
        """Initialize wizard integrator"""
        self.loader = loader
        self._workflow_hooks = {}
        self._customizations = {}

    def initialize_loader(self, runtime_dir: str = None) -> None:
        """Initialize the governance runtime loader"""
        if self.loader is None:
            # Import here to avoid circular dependency
            from governance_runtime_loader import GovernanceRuntimeLoader

            self.loader = GovernanceRuntimeLoader(runtime_dir)

    def load_governance(self) -> Dict[str, Any]:
        """Load governance data for wizard"""
        if self.loader is None:
            self.initialize_loader()

        print("🔗 Integrating governance with wizard...")
        return self.loader.load_all()

    def get_governance_summary(self) -> Dict[str, Any]:
        """Get governance summary for wizard display"""
        if self.loader is None:
            self.initialize_loader()

        return self.loader.get_governance_summary()

    def get_mandatory_items(self) -> List[Dict[str, Any]]:
        """Get mandatory governance items for wizard enforcement"""
        if self.loader is None:
            self.initialize_loader()

        return self.loader.get_items_by_criticality("OBRIGATÓRIO")

    def get_optional_items(self) -> List[Dict[str, Any]]:
        """Get optional governance items for customization"""
        if self.loader is None:
            self.initialize_loader()

        return self.loader.get_items_by_criticality("OPCIONAL")

    def get_alert_items(self) -> List[Dict[str, Any]]:
        """Get alert-level governance items for warning"""
        if self.loader is None:
            self.initialize_loader()

        return self.loader.get_items_by_criticality("ALERTA")

    def get_customizable_items(self) -> List[Dict[str, Any]]:
        """Get items that can be customized"""
        if self.loader is None:
            self.initialize_loader()

        client_items = self.loader.get_client_governance().get("items", [])
        return [item for item in client_items if item.get("customizable") is True]

    def get_immutable_items(self) -> List[Dict[str, Any]]:
        """Get items that cannot be customized"""
        if self.loader is None:
            self.initialize_loader()

        core_items = self.loader.get_core_governance().get("items", [])
        return [item for item in core_items if item.get("customizable") is False]

    def register_workflow_hook(self, hook_name: str, callback: Callable) -> None:
        """Register a workflow hook for custom behavior"""
        self._workflow_hooks[hook_name] = callback
        print(f"  📌 Hook registered: {hook_name}")

    def execute_hook(self, hook_name: str, *args, **kwargs) -> Any:
        """Execute a registered workflow hook"""
        if hook_name not in self._workflow_hooks:
            return None

        hook = self._workflow_hooks[hook_name]
        return hook(*args, **kwargs)

    def create_customization_template(self) -> Dict[str, Any]:
        """Create a customization template for client governance"""
        if self.loader is None:
            self.initialize_loader()

        customizable = self.get_customizable_items()

        template = {
            "version": "3.0",
            "type": "customization-template",
            "created": datetime.utcnow().isoformat() + "Z",
            "customizations": {},
        }

        for item in customizable:
            item_id = item.get("id")
            template["customizations"][item_id] = {
                "id": item_id,
                "title": item.get("title"),
                "original_value": item,
                "customized_value": None,  # To be filled by user
                "criticality": item.get("criticality"),
                "category": item.get("category"),
            }

        return template

    def apply_customizations(self, customizations: Dict[str, Any]) -> Dict[str, Any]:
        """Apply customizations to client governance"""
        if self.loader is None:
            self.initialize_loader()

        self._customizations = customizations

        client_items = self.loader.get_client_governance().get("items", [])

        # Create customized version
        customized = {
            "category": self.loader.get_client_governance().get("category"),
            "version": self.loader.get_client_governance().get("version"),
            "items": [],
            "fingerprint": self.loader.get_client_governance().get("fingerprint"),
            "_customizations_applied": customizations,
        }

        for item in client_items:
            item_id = item.get("id")
            if item_id in customizations:
                # Use customized value
                customized_item = customizations[item_id].get("customized_value")
                if customized_item:
                    customized["items"].append(customized_item)
                    continue

            # Use original
            customized["items"].append(item)

        return customized

    def validate_customizations(self, customizations: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that customizations don't violate immutable core"""
        errors = []
        warnings = []

        if self.loader is None:
            self.initialize_loader()

        # Get immutable items
        immutable = self.get_immutable_items()
        immutable_ids = {item.get("id") for item in immutable}

        for custom_id, custom_item in customizations.items():
            # Check if trying to customize immutable item
            if custom_id in immutable_ids:
                errors.append(f"Cannot customize immutable item: {custom_id} (core governance)")

            # Check criticality
            criticality = custom_item.get("criticality")
            if criticality == "OBRIGATÓRIO":
                warnings.append(f"Customizing mandatory item: {custom_id} (may have consequences)")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    def generate_constitution_config(self, customizations: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate constitution configuration for agent setup"""
        if self.loader is None:
            self.initialize_loader()

        config = {
            "version": "3.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "governance": self.get_governance_summary(),
            "mandatory_rules": [
                {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "category": item.get("category"),
                }
                for item in self.get_mandatory_items()
            ],
            "customizations_applied": customizations is not None,
            "fingerprints": {
                "core": self.loader.get_core_fingerprint(),
                "client": self.loader.get_client_fingerprint(),
                "salt": self.loader.get_salt_fingerprint(),
            },
        }

        if customizations:
            config["customizations"] = customizations

        return config

    def get_integration_status(self) -> Dict[str, Any]:
        """Get status of wizard integration"""
        if self.loader is None:
            return {
                "status": "not-initialized",
                "loader": None,
                "governance_loaded": False,
            }

        try:
            summary = self.get_governance_summary()
            return {
                "status": "ready",
                "loader": "initialized",
                "governance_loaded": True,
                "total_items": summary.get("total_items"),
                "hooks_registered": len(self._workflow_hooks),
                "customizations_applied": len(self._customizations) > 0,
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "governance_loaded": False,
            }

    def export_integration_manifest(self, filepath: str) -> None:
        """Export integration manifest for documentation"""
        manifest = {
            "version": "3.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "type": "wizard-integration",
            "status": self.get_integration_status(),
            "governance_summary": self.get_governance_summary() if self.loader else None,
            "workflow_hooks": list(self._workflow_hooks.keys()),
            "customizations_count": len(self._customizations),
        }

        with open(filepath, "w") as f:
            json.dump(manifest, f, indent=2)


if __name__ == "__main__":
    integrator = WizardIntegrator()
    result = integrator.load_governance()

    print()
    print("=" * 70)
    print("✅ WIZARD INTEGRATION INITIALIZED")
    print("=" * 70)
    print()

    summary = integrator.get_governance_summary()
    print(f"📦 Governance Loaded: {summary.get('total_items')} items")
    print(f"  Mandatory: {len(integrator.get_mandatory_items())}")
    print(f"  Alert: {len(integrator.get_alert_items())}")
    print(f"  Optional: {len(integrator.get_optional_items())}")
    print()

    print(f"🔧 Customizable Items: {len(integrator.get_customizable_items())}")
    print(f"🔒 Immutable Items: {len(integrator.get_immutable_items())}")
    print()

    print("✅ Ready for wizard workflow")
