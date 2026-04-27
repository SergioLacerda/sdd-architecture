"""
PHASE 2: Governance Compiler
Converts governance-core.json and governance-client.json to msgpack format

Input:  governance-core.json + governance-client.json (from PHASE 1 pipeline)
Output: governance-core.compiled.msgpack + governance-client-template.compiled.msgpack

Process:
1. Load JSON files (with fingerprints already calculated)
2. Serialize to msgpack binary format
3. Generate metadata with fingerprints and item counts
4. Save msgpack files for runtime use

Note: This is a SIMPLE compiler - no complex logic, just serialization and fingerprints.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import msgpack


class GovernanceCompiler:
    """Compiles governance JSON files to msgpack format"""

    def __init__(self, compiled_dir: str = "compiled"):
        """
        Initialize compiler with path to compiled JSONs

        Args:
            compiled_dir: Directory containing governance-core.json and governance-client.json
        """
        self.compiled_dir = Path(compiled_dir)
        self.core_json_file = self.compiled_dir / "governance-core.json"
        self.client_json_file = self.compiled_dir / "governance-client.json"

    def compile(self, output_dir: str = "compiled") -> Dict[str, Any]:
        """
        Main compilation process

        Returns:
            Dictionary with compilation results (file paths, fingerprints, etc)
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Load JSON files
        core_data = self._load_json(self.core_json_file)
        client_data = self._load_json(self.client_json_file)

        if not core_data or not client_data:
            raise ValueError("Could not load governance JSON files")

        # Serialize to msgpack
        core_msgpack = self._serialize_to_msgpack(core_data)
        client_msgpack = self._serialize_to_msgpack(client_data)

        # Save msgpack files
        core_msgpack_file = output_path / "governance-core.compiled.msgpack"
        client_msgpack_file = output_path / "governance-client-template.compiled.msgpack"

        core_msgpack_file.write_bytes(core_msgpack)
        client_msgpack_file.write_bytes(client_msgpack)

        # Extract fingerprints from JSON (already calculated by pipeline)
        core_fingerprint = core_data.get("fingerprint")
        client_fingerprint = client_data.get("fingerprint")
        core_fingerprint_salt = client_data.get("fingerprint_core_salt")

        # Generate metadata files
        self._generate_metadata(
            output_path,
            "core",
            core_data,
            core_fingerprint,
        )
        self._generate_metadata(
            output_path,
            "client-template",
            client_data,
            client_fingerprint,
        )

        return {
            "core_msgpack_file": str(core_msgpack_file),
            "client_msgpack_file": str(client_msgpack_file),
            "core_metadata": str(output_path / "metadata-core.json"),
            "client_metadata": str(output_path / "metadata-client-template.json"),
            "core_fingerprint": core_fingerprint,
            "client_fingerprint": client_fingerprint,
            "core_fingerprint_salt": core_fingerprint_salt,
            "core_item_count": len(core_data.get("items", [])),
            "client_item_count": len(client_data.get("items", [])),
        }

    def _load_json(self, file_path: Path) -> Dict[str, Any]:
        """Load JSON file"""
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")
            return None

    def _serialize_to_msgpack(self, data: Dict[str, Any]) -> bytes:
        """
        Serialize dictionary to msgpack binary format

        Args:
            data: Dictionary to serialize

        Returns:
            msgpack binary data
        """
        return msgpack.packb(data, use_bin_type=True)

    def _generate_metadata(
        self,
        output_dir: Path,
        file_type: str,
        data: Dict[str, Any],
        fingerprint: str,
    ) -> None:
        """
        Generate metadata JSON file for compiled file

        Args:
            output_dir: Directory to save metadata
            file_type: "core" or "client-template"
            data: Original JSON data
            fingerprint: SHA-256 fingerprint
        """
        metadata = {
            "version": "3.0",
            "type": file_type,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "fingerprint": fingerprint,
            "item_count": len(data.get("items", [])),
            "items_by_type": self._count_items_by_type(data),
            "items_by_criticality": self._count_items_by_criticality(data),
            "readonly": file_type == "core",  # Core is immutable, client is customizable
            "customizable": file_type == "client-template",
        }

        # Add core salt for client metadata
        if file_type == "client-template":
            metadata["fingerprint_core_salt"] = data.get("fingerprint_core_salt")

        metadata_file = output_dir / f"metadata-{file_type}.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=True)

    def _count_items_by_type(self, data: Dict[str, Any]) -> Dict[str, int]:
        """Count items by type"""
        counts = {}
        for item in data.get("items", []):
            item_type = item.get("type", "UNKNOWN")
            counts[item_type] = counts.get(item_type, 0) + 1
        return counts

    def _count_items_by_criticality(self, data: Dict[str, Any]) -> Dict[str, int]:
        """Count items by criticality level"""
        counts = {}
        for item in data.get("items", []):
            criticality = item.get("criticality", "UNKNOWN")
            counts[criticality] = counts.get(criticality, 0) + 1
        return counts

    def validate_compilation(self, output_dir: str = "compiled") -> bool:  # noqa: C901
        """
        Validate that compilation was successful

        Checks:
        - Both msgpack files exist
        - Both metadata files exist
        - Fingerprints are present and valid (hex string, 64 chars)
        - Core and client fingerprints are different

        Returns:
            True if all validations pass
        """
        output_path = Path(output_dir)

        # Check files exist
        core_msgpack = output_path / "governance-core.compiled.msgpack"
        client_msgpack = output_path / "governance-client-template.compiled.msgpack"
        core_metadata = output_path / "metadata-core.json"
        client_metadata = output_path / "metadata-client-template.json"

        if not core_msgpack.exists():
            print(f"❌ Core msgpack file not found: {core_msgpack}")
            return False
        if not client_msgpack.exists():
            print(f"❌ Client msgpack file not found: {client_msgpack}")
            return False
        if not core_metadata.exists():
            print(f"❌ Core metadata file not found: {core_metadata}")
            return False
        if not client_metadata.exists():
            print(f"❌ Client metadata file not found: {client_metadata}")
            return False

        # Load and validate metadata
        with open(core_metadata) as f:
            core_meta = json.load(f)
        with open(client_metadata) as f:
            client_meta = json.load(f)

        core_fp = core_meta.get("fingerprint")
        client_fp = client_meta.get("fingerprint")

        # Validate fingerprints
        if not core_fp or len(core_fp) != 64:
            print(f"❌ Invalid core fingerprint: {core_fp}")
            return False
        if not client_fp or len(client_fp) != 64:
            print(f"❌ Invalid client fingerprint: {client_fp}")
            return False

        # Fingerprints should be different
        if core_fp == client_fp:
            print("❌ Core and client fingerprints are identical (should be different)")
            return False

        # Check core fingerprint is used as salt for client
        core_salt = client_meta.get("fingerprint_core_salt")
        if core_salt != core_fp:
            print("❌ Core fingerprint not used as salt for client")
            return False

        # Check readonly flags
        if core_meta.get("readonly") is not True:
            print("❌ Core metadata readonly flag not True")
            return False
        if client_meta.get("customizable") is not True:
            print("❌ Client metadata customizable flag not True")
            return False

        print("✅ Compilation validation passed")
        return True


if __name__ == "__main__":
    # Example usage
    compiler = GovernanceCompiler("compiled")
    result = compiler.compile("compiled")

    print("✅ PHASE 2: Compilation completed")
    print(f"  Core msgpack: {result['core_msgpack_file']}")
    print(f"  Client msgpack: {result['client_msgpack_file']}")
    print(f"  Core fingerprint: {result['core_fingerprint']}")
    print(f"  Client fingerprint: {result['client_fingerprint']}")
    print(f"  Core items: {result['core_item_count']}")
    print(f"  Client items: {result['client_item_count']}")

    # Validate
    if compiler.validate_compilation("compiled"):
        print("✅ All validations passed")
    else:
        print("❌ Validation failed")
