"""
PHASE 5: Customization Template Generator
Generate customization templates for client governance

Provides:
1. Create customization templates from governance
2. Validate customizations against core rules
3. Generate customization guides
4. Support template versioning
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class CustomizationTemplateGenerator:
    """Generate and manage customization templates"""

    def __init__(self, loader=None):
        """Initialize template generator"""
        self.loader = loader
        self.templates = {}

    def initialize_loader(self, runtime_dir: str = None) -> None:
        """Initialize the governance runtime loader"""
        if self.loader is None:
            from governance_runtime_loader import GovernanceRuntimeLoader

            self.loader = GovernanceRuntimeLoader(runtime_dir)

    def generate_basic_template(self) -> Dict[str, Any]:
        """Generate basic customization template"""
        if self.loader is None:
            self.initialize_loader()

        client_items = self.loader.get_client_governance().get("items", [])

        template = {
            "version": "3.0",
            "type": "customization-template",
            "generated": datetime.utcnow().isoformat() + "Z",
            "metadata": {
                "template_name": "basic-customization",
                "description": "Basic customization template for client governance",
                "total_items": len(client_items),
                "customizable_items": len([i for i in client_items if i.get("customizable")]),
            },
            "instructions": [
                "1. Review each customization section below",
                "2. Modify values as needed for your organization",
                "3. Do NOT modify immutable core governance (marked with 🔒)",
                "4. Ensure all OBRIGATÓRIO items are respected",
                "5. Test customizations with validation script",
            ],
            "customizations": self._group_items_for_customization(client_items),
        }

        return template

    def generate_full_template(self) -> Dict[str, Any]:
        """Generate full template with both core and client"""
        if self.loader is None:
            self.initialize_loader()

        core_items = self.loader.get_core_governance().get("items", [])
        client_items = self.loader.get_client_governance().get("items", [])

        template = {
            "version": "3.0",
            "type": "full-customization-template",
            "generated": datetime.utcnow().isoformat() + "Z",
            "metadata": {
                "template_name": "full-customization",
                "description": "Full template showing core (immutable) and client (customizable)",
                "total_items": len(core_items) + len(client_items),
                "core_items": len(core_items),
                "client_items": len(client_items),
            },
            "core_governance": {
                "status": "🔒 IMMUTABLE",
                "description": "These items cannot be customized",
                "items": self._prepare_items_for_display(core_items, customizable=False),
            },
            "client_governance": {
                "status": "✏️ CUSTOMIZABLE",
                "description": "These items can be customized for your organization",
                "items": self._prepare_items_for_display(client_items, customizable=True),
            },
        }

        return template

    def generate_category_template(self, category: str) -> Dict[str, Any]:
        """Generate template for specific category"""
        if self.loader is None:
            self.initialize_loader()

        all_items = self.loader.get_all_items()
        category_items = [item for item in all_items if item.get("category") == category]

        template = {
            "version": "3.0",
            "type": "category-customization-template",
            "generated": datetime.utcnow().isoformat() + "Z",
            "category": category,
            "metadata": {
                "total_items": len(category_items),
                "customizable": len([i for i in category_items if i.get("customizable")]),
                "immutable": len([i for i in category_items if not i.get("customizable")]),
            },
            "items": self._prepare_items_for_display(category_items),
        }

        return template

    def generate_criticality_template(self, criticality: str) -> Dict[str, Any]:
        """Generate template for specific criticality level"""
        if self.loader is None:
            self.initialize_loader()

        items = self.loader.get_items_by_criticality(criticality)

        template = {
            "version": "3.0",
            "type": "criticality-customization-template",
            "generated": datetime.utcnow().isoformat() + "Z",
            "criticality": criticality,
            "metadata": {
                "total_items": len(items),
                "description": self._get_criticality_description(criticality),
            },
            "items": self._prepare_items_for_display(items),
        }

        return template

    def generate_adoption_template(self, adoption_level: str) -> Dict[str, Any]:
        """Generate template for specific adoption level"""
        if self.loader is None:
            self.initialize_loader()

        template = {
            "version": "3.0",
            "type": "adoption-level-template",
            "generated": datetime.utcnow().isoformat() + "Z",
            "adoption_level": adoption_level,
            "metadata": self._get_adoption_metadata(adoption_level),
        }

        # Get items relevant to adoption level
        all_items = self.loader.get_all_items()
        relevant_items = self._filter_by_adoption(all_items, adoption_level)

        template["items"] = self._prepare_items_for_display(relevant_items)
        template["implementation_steps"] = self._get_adoption_steps(adoption_level)

        return template

    def save_template(self, template: Dict[str, Any], output_path: str, format: str = "json") -> None:
        """Save template to file"""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        if format == "json":
            with open(path, "w") as f:
                json.dump(template, f, indent=2)
        elif format == "yaml":
            import yaml

            with open(path, "w") as f:
                yaml.dump(template, f, default_flow_style=False)

        print(f"  ✅ Saved: {path}")

    def generate_all_templates(self, output_dir: str = ".") -> Dict[str, str]:
        """Generate all template types"""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        templates_created = {}

        print("📝 Generating customization templates...")
        print()

        # Basic template
        print("  📋 Generating basic template...")
        basic = self.generate_basic_template()
        basic_path = output_dir / "customization-basic.json"
        self.save_template(basic, str(basic_path))
        templates_created["basic"] = str(basic_path)

        # Full template
        print("  📋 Generating full template...")
        full = self.generate_full_template()
        full_path = output_dir / "customization-full.json"
        self.save_template(full, str(full_path))
        templates_created["full"] = str(full_path)

        # Category templates
        if self.loader is None:
            self.initialize_loader()

        all_items = self.loader.get_all_items()
        categories = set(item.get("category") for item in all_items if item.get("category"))

        print(f"  📋 Generating {len(categories)} category templates...")
        for category in categories:
            category_template = self.generate_category_template(category)
            category_path = output_dir / f"customization-category-{category.lower()}.json"
            self.save_template(category_template, str(category_path))
            templates_created[f"category-{category}"] = str(category_path)

        # Criticality templates
        criticalities = ["OBRIGATÓRIO", "ALERTA", "OPCIONAL"]
        print(f"  📋 Generating {len(criticalities)} criticality templates...")
        for criticality in criticalities:
            criticality_template = self.generate_criticality_template(criticality)
            criticality_path = output_dir / f"customization-criticality-{criticality.lower()}.json"
            self.save_template(criticality_template, str(criticality_path))
            templates_created[f"criticality-{criticality}"] = str(criticality_path)

        # Adoption templates
        adoption_levels = ["ultra-lite", "lite", "full"]
        print(f"  📋 Generating {len(adoption_levels)} adoption templates...")
        for level in adoption_levels:
            adoption_template = self.generate_adoption_template(level)
            adoption_path = output_dir / f"customization-adoption-{level}.json"
            self.save_template(adoption_template, str(adoption_path))
            templates_created[f"adoption-{level}"] = str(adoption_path)

        return templates_created

    def _group_items_for_customization(self, items: List[Dict]) -> Dict[str, List]:
        """Group items by type for customization"""
        grouped = {}
        for item in items:
            if item.get("customizable"):
                item_type = item.get("type", "other")
                if item_type not in grouped:
                    grouped[item_type] = []
                grouped[item_type].append(
                    {
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "original": item,
                        "customized": None,
                    }
                )
        return grouped

    def _prepare_items_for_display(self, items: List[Dict], customizable: bool = None) -> List[Dict]:
        """Prepare items for display in templates"""
        display_items = []
        for item in items:
            display_item = {
                "id": item.get("id"),
                "title": item.get("title"),
                "type": item.get("type"),
                "category": item.get("category"),
                "criticality": item.get("criticality"),
                "customizable": item.get("customizable", False),
                "content": item.get("content"),
            }

            if item.get("customizable"):
                display_item["_status"] = "✏️ Can be customized"
            else:
                display_item["_status"] = "🔒 Immutable (core governance)"

            display_items.append(display_item)

        return display_items

    def _get_criticality_description(self, criticality: str) -> str:
        """Get description for criticality level"""
        descriptions = {
            "OBRIGATÓRIO": "Mandatory items that must be enforced",
            "ALERTA": "Alert-level items that should be reviewed",
            "OPCIONAL": "Optional items that can be customized",
        }
        return descriptions.get(criticality, "Unknown criticality")

    def _get_adoption_metadata(self, level: str) -> Dict[str, Any]:
        """Get metadata for adoption level"""
        metadata = {
            "ultra-lite": {
                "setup_time": "5 minutes",
                "ideal_for": "Solo developers, prototypes, MVPs",
                "items_count": 5,
            },
            "lite": {
                "setup_time": "15 minutes",
                "ideal_for": "Small teams (< 5 people), learning",
                "items_count": 25,
            },
            "full": {
                "setup_time": "40 minutes",
                "ideal_for": "Production, mission-critical systems",
                "items_count": 155,
            },
        }
        return metadata.get(level, {})

    def _filter_by_adoption(self, items: List[Dict], level: str) -> List[Dict]:
        """Filter items by adoption level"""
        if level == "ultra-lite":
            # Only most critical items
            return [i for i in items if i.get("criticality") == "OBRIGATÓRIO"][:5]
        elif level == "lite":
            # Critical + some alert items
            return [i for i in items if i.get("criticality") in ["OBRIGATÓRIO", "ALERTA"]][:25]
        else:  # full
            return items

    def _get_adoption_steps(self, level: str) -> List[str]:
        """Get implementation steps for adoption level"""
        steps = {
            "ultra-lite": [
                "1. Review 5 core principles",
                "2. Understand 3 essential rules",
                "3. Define 5 DoD checkpoints",
                "4. Start with basic customization",
                "5. Upgrade to LITE anytime",
            ],
            "lite": [
                "1. Review all OBRIGATÓRIO items",
                "2. Understand ALERTA items",
                "3. Plan customizations",
                "4. Apply category-specific rules",
                "5. Set up basic enforcement",
                "6. Upgrade to FULL for production",
            ],
            "full": [
                "1. Load full governance (155 items)",
                "2. Review all categories",
                "3. Plan comprehensive customizations",
                "4. Set up all enforcement rules",
                "5. Configure agent integration",
                "6. Deploy to production",
            ],
        }
        return steps.get(level, [])


if __name__ == "__main__":
    generator = CustomizationTemplateGenerator()
    generator.initialize_loader()

    print("=" * 70)
    print("✅ CUSTOMIZATION TEMPLATE GENERATOR")
    print("=" * 70)
    print()

    # Generate all templates
    templates = generator.generate_all_templates("runtime/templates")

    print()
    print("=" * 70)
    print(f"✅ Generated {len(templates)} templates")
    print("=" * 70)
    print()

    for template_type, path in templates.items():
        print(f"  ✅ {template_type}: {path}")

    print()
    print("✅ All templates ready for customization workflow")
