#!/usr/bin/env python3
"""
PHASE 2: Compile governance from source/ → governance-core.json + governance-client.json

Reads:
  - .sdd-core/source/{mandates,guidelines,decisions,rules,guardrails}/*.md
  - user_selections.json (which items go to CORE vs CLIENT)

Outputs:
  - governance-core.json (immutable items)
  - governance-client.json (customizable items)
  - metadata-core.json (with fingerprint)
  - metadata-client.json (with fingerprint and core_salt)

Fingerprinting strategy:
  - fingerprint_core = SHA256(governance-core.json)
  - fingerprint_client = SHA256(fingerprint_core + governance-client.json)  ← SALT!
"""

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


class GovernanceCompiler:
    def __init__(self, sdd_core_path: str = ".sdd-core"):
        self.sdd_core_path = Path(sdd_core_path)
        self.source_path = self.sdd_core_path / "source"
        self.selections: Dict[str, Any] = {}
        self.all_items: List[Dict[str, Any]] = []
        self.core_items: List[Dict[str, Any]] = []
        self.client_items: List[Dict[str, Any]] = []

    def load_selections(self, selections_file: str = "user_selections_sample.json") -> None:
        """Load user selections (CORE vs CLIENT)"""
        print("📋 Loading user selections...")

        selections_path = Path(selections_file)
        if not selections_path.exists():
            print(f"   ⚠️  {selections_file} not found, using all as CORE")
            return

        data = json.loads(selections_path.read_text())
        self.selections = data.get("selections", {})

        print(f"   ✓ Loaded {len(self.selections)} item selections")
        print(f"     • CORE items: {sum(1 for s in self.selections.values() if s['choice'] == 'CORE')}")
        print(f"     • CLIENT items: {sum(1 for s in self.selections.values() if s['choice'] == 'CLIENT')}")
        print()

    def extract_markdown_items(self) -> None:
        """Extract all markdown items from source/"""
        print("📝 Extracting markdown items from source/...")
        print()

        for item_type in ["mandates", "guidelines", "decisions", "rules", "guardrails"]:
            type_dir = self.source_path / item_type
            if not type_dir.exists():
                print(f"   ⚠️  source/{item_type}/ not found")
                continue

            md_files = sorted(type_dir.glob("*.md"))
            print(f"   Reading source/{item_type}/ ({len(md_files)} items)")

            for md_file in md_files:
                item = self._parse_markdown_item(md_file, item_type.rstrip('s').upper())
                if item:
                    self.all_items.append(item)

        print(f"\n   ✓ Extracted {len(self.all_items)} total items")
        print()

    def _parse_markdown_item(self, md_file: Path, item_type: str) -> Optional[Dict[str, Any]]:
        """Parse YAML frontmatter from markdown file"""
        content = md_file.read_text(encoding="utf-8")

        # Extract YAML frontmatter
        yaml_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not yaml_match:
            print(f"      ⚠️  No YAML in {md_file.name}")
            return None

        try:
            frontmatter = yaml.safe_load(yaml_match.group(1))
        except yaml.YAMLError as e:
            print(f"      ⚠️  YAML error in {md_file.name}: {e}")
            return None

        item = {
            "id": frontmatter.get("id", md_file.stem),
            "title": frontmatter.get("title", ""),
            "type": frontmatter.get("type", item_type),
            "criticality": frontmatter.get("criticality", "OPCIONAL"),
            "customizable": frontmatter.get("customizable", False),
            "optional": frontmatter.get("optional", True),
            "category": frontmatter.get("category", "general"),
            "source_file": str(md_file.relative_to(self.sdd_core_path)),
        }

        return item

    def separate_core_client(self) -> None:
        """Separate items into CORE vs CLIENT based on user selections"""
        print("🔀 Separating CORE vs CLIENT items...")
        print()

        for item in self.all_items:
            item_id = item["id"]

            # Check if in selections
            if item_id in self.selections:
                choice = self.selections[item_id]["choice"]
                if choice == "CORE":
                    self.core_items.append(item)
                else:
                    self.client_items.append(item)
            else:
                # Default: if not in selections, follow criticality
                if item["criticality"] == "OBRIGATÓRIO":
                    self.core_items.append(item)
                elif item["customizable"]:
                    self.client_items.append(item)
                else:
                    self.core_items.append(item)

        print(f"   ✓ CORE items:   {len(self.core_items)}")
        print(f"   ✓ CLIENT items: {len(self.client_items)}")
        print()

    def calculate_fingerprint(self, data: Dict[str, Any]) -> str:
        """Calculate SHA256 fingerprint"""
        # Create copy without fingerprint fields
        data_copy = {k: v for k, v in data.items()
                    if k not in ["fingerprint", "fingerprint_core_salt"]}

        # Hash as sorted JSON
        hash_input = json.dumps(data_copy, sort_keys=True).encode('utf-8')
        return hashlib.sha256(hash_input).hexdigest()

    def generate_governance_files(self) -> None:
        """Generate governance-core.json and governance-client.json"""
        print("📝 Generating governance files...")
        print()

        # Create core structure
        governance_core = {
            "version": "3.0",
            "type": "GOVERNANCE_CORE",
            "readonly": True,
            "compiled_at": datetime.now().isoformat(),
            "items": self.core_items,
            "metadata": {
                "total_items": len(self.core_items),
                "customizable": False
            }
        }

        # Create client structure
        governance_client = {
            "version": "3.0",
            "type": "GOVERNANCE_CLIENT",
            "readonly": False,
            "compiled_at": datetime.now().isoformat(),
            "items": self.client_items,
            "metadata": {
                "total_items": len(self.client_items),
                "customizable": True
            }
        }

        # Calculate fingerprints
        fingerprint_core = self.calculate_fingerprint(governance_core)
        governance_core["fingerprint"] = fingerprint_core

        # Client fingerprint uses core fingerprint as salt
        combined_for_client = {
            **governance_client,
            "fingerprint_core_salt": fingerprint_core
        }
        fingerprint_client = self.calculate_fingerprint(combined_for_client)
        governance_client["fingerprint"] = fingerprint_client
        governance_client["fingerprint_core_salt"] = fingerprint_core

        # Save files
        output_dir = self.sdd_core_path.parent / ".sdd-compiled"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save core JSON
        core_path = output_dir / "governance-core.json"
        core_path.write_text(json.dumps(governance_core, indent=2, ensure_ascii=False))
        print(f"   ✓ {core_path.relative_to(self.sdd_core_path.parent)}")

        # Save client JSON
        client_path = output_dir / "governance-client.json"
        client_path.write_text(json.dumps(governance_client, indent=2, ensure_ascii=False))
        print(f"   ✓ {client_path.relative_to(self.sdd_core_path.parent)}")

        # Save metadata files
        metadata_core = {
            "version": "3.0",
            "type": "GOVERNANCE_CORE",
            "readonly": True,
            "compiled_at": governance_core["compiled_at"],
            "fingerprint": fingerprint_core,
            "items_count": len(self.core_items),
        }

        metadata_core_path = output_dir / "metadata-core.json"
        metadata_core_path.write_text(json.dumps(metadata_core, indent=2))
        print(f"   ✓ {metadata_core_path.relative_to(self.sdd_core_path.parent)}")

        metadata_client = {
            "version": "3.0",
            "type": "GOVERNANCE_CLIENT",
            "readonly": False,
            "compiled_at": governance_client["compiled_at"],
            "fingerprint": fingerprint_client,
            "fingerprint_core_salt": fingerprint_core,
            "items_count": len(self.client_items),
        }

        metadata_client_path = output_dir / "metadata-client.json"
        metadata_client_path.write_text(json.dumps(metadata_client, indent=2))
        print(f"   ✓ {metadata_client_path.relative_to(self.sdd_core_path.parent)}")

        print()
        print("=" * 100)
        print("🔐 FINGERPRINTING STRATEGY")
        print("=" * 100)
        print()
        print("Core fingerprint (SALT):")
        print(f"  SHA256(governance-core.json) = {fingerprint_core}")
        print()
        print("Client fingerprint (DERIVED from core):")
        print(f"  SHA256(fingerprint_core + governance-client.json) = {fingerprint_client}")
        print()
        print(f"Client includes: fingerprint_core_salt = {fingerprint_core}")
        print()

    def print_summary(self) -> None:
        """Print compilation summary"""
        print("=" * 100)
        print("✅ PHASE 2: GOVERNANCE COMPILATION COMPLETE")
        print("=" * 100)
        print()

        print("📊 ITEMS COMPILED")
        print("-" * 100)
        print(f"  Total items extracted: {len(self.all_items)}")
        print(f"  → CORE (immutable):    {len(self.core_items)} items")
        print(f"  → CLIENT (customizable): {len(self.client_items)} items")
        print()

        print("📁 FILES GENERATED")
        print("-" * 100)
        output_dir = self.sdd_core_path.parent / ".sdd-compiled"
        print(f"  {output_dir}/")
        print("  ├── governance-core.json")
        print("  ├── governance-client.json")
        print("  ├── metadata-core.json")
        print("  └── metadata-client.json")
        print()

        # Show sample items
        print("📋 SAMPLE CORE ITEMS")
        print("-" * 100)
        for item in self.core_items[:3]:
            print(f"  • {item['id']}: {item['title'][:50]}")
        if len(self.core_items) > 3:
            print(f"  ... and {len(self.core_items) - 3} more")
        print()

        print("📋 SAMPLE CLIENT ITEMS")
        print("-" * 100)
        for item in self.client_items[:3]:
            print(f"  • {item['id']}: {item['title'][:50]}")
        if len(self.client_items) > 3:
            print(f"  ... and {len(self.client_items) - 3} more")
        print()

    def run(self, selections_file: str = "user_selections_sample.json") -> None:
        """Execute full compilation"""
        print()
        print("=" * 100)
        print("🔧 PHASE 2: COMPILE GOVERNANCE (source → JSON)")
        print("=" * 100)
        print()

        self.load_selections(selections_file)
        self.extract_markdown_items()
        self.separate_core_client()
        self.generate_governance_files()
        self.print_summary()


if __name__ == "__main__":
    import sys

    # Determine correct path
    from pathlib import Path
    current_dir = Path.cwd()
    if current_dir.name == ".sdd-core":
        sdd_core_path = current_dir
    else:
        sdd_core_path = current_dir / ".sdd-core"

    compiler = GovernanceCompiler(str(sdd_core_path))

    # Allow custom selections file as argument
    selections_file = sys.argv[1] if len(sys.argv) > 1 else "user_selections_sample.json"
    compiler.run(selections_file)
