"""
PHASE 1: Pipeline Builder
Consolidates governance files from .sdd-core/ into 2 separate JSON structures:
- governance-core.json (customizable=false items)
- governance-client.json (customizable=true items)

Each item includes metadata:
- id, title, type, criticality, customizable, optional, category
- content (parsed body)
"""

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class GovernanceItem:
    """Represents a single governance item (mandate, guideline, decision, rule, guardrail)"""
    id: str
    title: str
    type: str  # MANDATE, GUIDELINE, DECISION, RULE, GUARDRAIL
    criticality: str  # OBRIGATÓRIO, ALERTA, OPCIONAL
    customizable: bool
    optional: bool
    category: str
    content: str
    source_file: str


class PipelineBuilder:
    """Consolidates governance files into 2 JSON structures"""

    def __init__(self, sdd_core_path: str = ".sdd-core"):
        path = Path(sdd_core_path)

        # Compat: when tests run from `_core/`, "_spec" lives in the parent dir.
        if not path.exists() and not path.is_absolute():
            parent_candidate = Path.cwd().parent / path
            if parent_candidate.exists():
                path = parent_candidate

        self.sdd_core_path = path
        self.items: List[GovernanceItem] = []

    def build(self) -> Dict[str, Any]:
        """Main build process"""
        self.items = []

        # Parse all source files
        self._parse_mandate_spec()
        self._parse_guidelines_dsl()
        self._parse_decisions()
        self._parse_rules()
        self._parse_guardrails()

        # Sort by criticality (DESC: OBRIGATÓRIO → OPCIONAL)
        self._sort_by_criticality()

        # Generate core and client items
        core_items = [item for item in self.items if not item.customizable]
        client_items = [item for item in self.items if item.customizable]

        # Generate output structures
        governance_core = self._generate_json_structure(core_items, "CORE")
        governance_client = self._generate_json_structure(client_items, "CLIENT")

        # Calculate fingerprints
        core_fingerprint = self.calculate_fingerprint(governance_core)
        governance_core["fingerprint"] = core_fingerprint

        # Client fingerprint uses core fingerprint as salt
        client_fingerprint = self.calculate_fingerprint(
            {**governance_client, "fingerprint_core_salt": core_fingerprint}
        )
        governance_client["fingerprint"] = client_fingerprint
        governance_client["fingerprint_core_salt"] = core_fingerprint

        return {
            "governance_core": governance_core,
            "governance_client": governance_client,
            "core_items": core_items,
            "client_items": client_items,
        }

    def _parse_mandate_spec(self) -> None:
        """Parse mandate.spec file"""
        mandate_file = self.sdd_core_path / "mandate.spec"
        if not mandate_file.exists():
            return

        content = mandate_file.read_text(encoding="utf-8")
        # Parse mandate blocks: mandate M001 { ... }
        pattern = r'mandate\s+(\w+)\s*\{([^}]+)\}'
        for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
            mandate_id = match.group(1)
            mandate_content = match.group(2)

            # Extract title and description
            title_match = re.search(r'title:\s*"([^"]+)"', mandate_content)
            desc_match = re.search(r'description:\s*"([^"]+)"', mandate_content)
            category_match = re.search(r'category:\s*(\w+)', mandate_content)

            title = title_match.group(1) if title_match else mandate_id
            description = desc_match.group(1) if desc_match else ""
            category = category_match.group(1) if category_match else "general"

            item = GovernanceItem(
                id=mandate_id,
                title=title,
                type="MANDATE",
                criticality="OBRIGATÓRIO",
                customizable=False,  # Mandates are never customizable
                optional=False,
                category=category,
                content=description,
                source_file="mandate.spec",
            )
            self.items.append(item)

    def _parse_guidelines_dsl(self) -> None:
        """Parse guidelines.dsl file"""
        guidelines_file = self.sdd_core_path / "guidelines.dsl"
        if not guidelines_file.exists():
            return

        content = guidelines_file.read_text(encoding="utf-8")
        # Parse guideline blocks: guideline G01 { ... }
        pattern = r'guideline\s+(\w+)\s*\{([^}]+)\}'
        for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
            guideline_id = match.group(1)
            guideline_content = match.group(2)

            # Extract title and description
            title_match = re.search(r'title:\s*"([^"]+)"', guideline_content)
            desc_match = re.search(r'description:\s*"([^"]+)"', guideline_content)
            category_match = re.search(r'category:\s*(\w+)', guideline_content)

            title = title_match.group(1) if title_match else guideline_id
            description = desc_match.group(1) if desc_match else ""
            category = category_match.group(1) if category_match else "general"

            item = GovernanceItem(
                id=guideline_id,
                title=title,
                type="GUIDELINE",
                criticality="OPCIONAL",
                customizable=True,  # Guidelines are customizable by default
                optional=True,
                category=category,
                content=description,
                source_file="guidelines.dsl",
            )
            self.items.append(item)

    def _parse_markdown_with_frontmatter(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Parse markdown file with YAML front-matter"""
        if not file_path.exists():
            return None

        content = file_path.read_text(encoding="utf-8")

        # Extract front-matter (YAML between --- markers)
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not frontmatter_match:
            return None

        frontmatter_text = frontmatter_match.group(1)
        body = content[frontmatter_match.end():]

        try:
            frontmatter = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError:
            return None

        return {
            "frontmatter": frontmatter,
            "body": body,
        }

    def _parse_decisions(self) -> None:
        """Parse decisions/ directory"""
        decisions_dir = self.sdd_core_path / "decisions"
        if not decisions_dir.exists():
            return

        for md_file in sorted(decisions_dir.glob("*.md")):
            parsed = self._parse_markdown_with_frontmatter(md_file)
            if not parsed:
                continue

            fm = parsed["frontmatter"]
            body = parsed["body"]

            item = GovernanceItem(
                id=fm.get("id", md_file.stem),
                title=fm.get("title", md_file.stem),
                type=fm.get("type", "DECISION"),
                criticality=fm.get("criticality", "OBRIGATÓRIO"),
                customizable=fm.get("customizable", False),
                optional=fm.get("optional", False),
                category=fm.get("category", "architecture"),
                content=body,
                source_file=f"decisions/{md_file.name}",
            )
            self.items.append(item)

    def _parse_rules(self) -> None:
        """Parse rules/ directory"""
        rules_dir = self.sdd_core_path / "rules"
        if not rules_dir.exists():
            return

        for md_file in sorted(rules_dir.glob("*.md")):
            parsed = self._parse_markdown_with_frontmatter(md_file)
            if not parsed:
                continue

            fm = parsed["frontmatter"]
            body = parsed["body"]

            item = GovernanceItem(
                id=fm.get("id", md_file.stem),
                title=fm.get("title", md_file.stem),
                type=fm.get("type", "RULE"),
                criticality=fm.get("criticality", "OBRIGATÓRIO"),
                customizable=fm.get("customizable", False),
                optional=fm.get("optional", False),
                category=fm.get("category", "quality"),
                content=body,
                source_file=f"rules/{md_file.name}",
            )
            self.items.append(item)

    def _parse_guardrails(self) -> None:
        """Parse guardrails/ directory"""
        guardrails_dir = self.sdd_core_path / "guardrails"
        if not guardrails_dir.exists():
            return

        for md_file in sorted(guardrails_dir.glob("*.md")):
            parsed = self._parse_markdown_with_frontmatter(md_file)
            if not parsed:
                continue

            fm = parsed["frontmatter"]
            body = parsed["body"]

            item = GovernanceItem(
                id=fm.get("id", md_file.stem),
                title=fm.get("title", md_file.stem),
                type=fm.get("type", "GUARDRAIL"),
                criticality=fm.get("criticality", "OPCIONAL"),
                customizable=fm.get("customizable", False),
                optional=fm.get("optional", False),
                category=fm.get("category", "patterns"),
                content=body,
                source_file=f"guardrails/{md_file.name}",
            )
            self.items.append(item)

    def _sort_by_criticality(self) -> None:
        """Sort items by criticality (DESC: OBRIGATÓRIO → ALERTA → OPCIONAL)"""
        criticality_order = {"OBRIGATÓRIO": 0, "ALERTA": 1, "OPCIONAL": 2}
        self.items.sort(key=lambda x: criticality_order.get(x.criticality, 99))

    def _generate_json_structure(self, items: List[GovernanceItem], category: str) -> Dict[str, Any]:
        """Generate JSON structure for a set of items"""
        return {
            "category": category,
            "version": "3.0",
            "generated_at": None,  # Will be filled by caller if needed
            "items": [
                {
                    "id": item.id,
                    "title": item.title,
                    "type": item.type,
                    "criticality": item.criticality,
                    "customizable": item.customizable,
                    "optional": item.optional,
                    "category": item.category,
                    "source_file": item.source_file,
                    "content": item.content,
                }
                for item in items
            ],
        }

    def calculate_fingerprint(self, data: Dict[str, Any]) -> str:
        """Calculate SHA-256 fingerprint of JSON data"""
        # Serialize in canonical form (sorted keys)
        json_str = json.dumps(data, sort_keys=True, ensure_ascii=True)
        return hashlib.sha256(json_str.encode("utf-8")).hexdigest()

    def save_outputs(self, output_dir: str = ".sdd-compiled") -> Dict[str, str]:
        """Save governance-core.json and governance-client.json"""
        result = self.build()

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Get data from build() - fingerprints already calculated and added
        core_data = result["governance_core"]
        client_data = result["governance_client"]

        # Save governance-core.json
        core_file = output_path / "governance-core.json"
        core_file.write_text(json.dumps(core_data, indent=2, ensure_ascii=True), encoding="utf-8")

        # Save governance-client.json
        client_file = output_path / "governance-client.json"
        client_file.write_text(json.dumps(client_data, indent=2, ensure_ascii=True), encoding="utf-8")

        return {
            "governance_core": str(core_file),
            "governance_client": str(client_file),
            "core_fingerprint": core_data["fingerprint"],
            "client_fingerprint": client_data["fingerprint"],
        }


if __name__ == "__main__":
    # Example usage
    builder = PipelineBuilder(".sdd-core")
    result = builder.save_outputs(".sdd-compiled")

    print("✅ PHASE 1: Pipeline completed")
    print(f"  governance-core.json: {result['governance_core']}")
    print(f"  governance-client.json: {result['governance_client']}")
    print(f"  core_fingerprint: {result['core_fingerprint']}")
    print(f"  client_fingerprint: {result['client_fingerprint']}")
