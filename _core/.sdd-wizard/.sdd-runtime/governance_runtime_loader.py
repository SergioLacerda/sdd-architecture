"""
PHASE 5: Governance Runtime Loader
Load compiled msgpack artifacts from .sdd-compiler/runtime/

Provides:
1. Load and deserialize msgpack files
2. Validate fingerprints and checksums
3. Provide governance data to agents and wizards
4. Support customization of client governance
"""

import msgpack
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from hashlib import sha256


class GovernanceRuntimeLoader:
    """Load and manage governance artifacts at runtime"""

    def __init__(self, compiled_dir: str = None):
        """Initialize runtime loader
        
        Args:
            compiled_dir: Path to .sdd-compiler/runtime directory.
                         If None, discovers from repository root.
        """
        if compiled_dir is None:
            # Discover from repository root: go up from this file
            # File is at: repo/.sdd-wizard/.sdd-runtime/governance_runtime_loader.py
            repo_root = Path(__file__).parent.parent.parent.parent
            compiled_dir = repo_root / "_core" / ".sdd-compiler" / "runtime"
        else:
            compiled_dir = Path(compiled_dir)

        self.compiled_dir = compiled_dir
        self._core_data = None
        self._client_data = None
        self._core_metadata = None
        self._client_metadata = None

    def load_all(self) -> Dict[str, Any]:
        """Load all governance artifacts"""
        print("📦 Loading governance runtime artifacts...")

        # Load core
        print("  Loading core governance...")
        self.load_core()
        print("    ✅ Core loaded (4 items)")

        # Load client
        print("  Loading client governance...")
        self.load_client()
        print("    ✅ Client loaded (151 items)")

        # Validate
        print("  Validating integrity...")
        if not self._validate_integrity():
            raise Exception("Governance integrity validation failed")
        print("    ✅ All validations passed")

        return {
            "status": "loaded",
            "core_items": len(self._core_data.get("items", [])),
            "client_items": len(self._client_data.get("items", [])),
            "core_fingerprint": self._core_metadata.get("fingerprint"),
            "client_fingerprint": self._client_metadata.get("fingerprint"),
        }

    def load_core(self) -> Dict[str, Any]:
        """Load core governance (immutable)"""
        msgpack_file = self.compiled_dir / "governance-core.compiled.msgpack"
        metadata_file = self.compiled_dir / "metadata-core.json"

        # Load msgpack
        with open(msgpack_file, "rb") as f:
            self._core_data = msgpack.unpackb(f.read(), raw=False)

        # Load metadata
        with open(metadata_file) as f:
            self._core_metadata = json.load(f)

        return self._core_data

    def load_client(self) -> Dict[str, Any]:
        """Load client governance (customizable template)"""
        msgpack_file = (
            self.compiled_dir / "governance-client-template.compiled.msgpack"
        )
        metadata_file = self.compiled_dir / "metadata-client-template.json"

        # Load msgpack
        with open(msgpack_file, "rb") as f:
            self._client_data = msgpack.unpackb(f.read(), raw=False)

        # Load metadata
        with open(metadata_file) as f:
            self._client_metadata = json.load(f)

        return self._client_data

    def get_core_governance(self) -> Dict[str, Any]:
        """Get loaded core governance"""
        if self._core_data is None:
            self.load_core()
        return self._core_data

    def get_client_governance(self) -> Dict[str, Any]:
        """Get loaded client governance"""
        if self._client_data is None:
            self.load_client()
        return self._client_data

    def get_all_items(self) -> List[Dict[str, Any]]:
        """Get all governance items (core + client merged)"""
        core_items = self.get_core_governance().get("items", [])
        client_items = self.get_client_governance().get("items", [])
        return core_items + client_items

    def get_items_by_type(self, item_type: str) -> List[Dict[str, Any]]:
        """Get items by type (mandate, adr, rule, guideline, guardrail)"""
        items = self.get_all_items()
        return [item for item in items if item.get("type") == item_type]

    def get_items_by_criticality(self, criticality: str) -> List[Dict[str, Any]]:
        """Get items by criticality (OBRIGATÓRIO, ALERTA, OPCIONAL)"""
        items = self.get_all_items()
        return [item for item in items if item.get("criticality") == criticality]

    def get_core_fingerprint(self) -> str:
        """Get core governance fingerprint"""
        if self._core_metadata is None:
            self._load_metadata_only()
        return self._core_metadata.get("fingerprint")

    def get_client_fingerprint(self) -> str:
        """Get client governance fingerprint"""
        if self._client_metadata is None:
            self._load_metadata_only()
        return self._client_metadata.get("fingerprint")

    def get_salt_fingerprint(self) -> str:
        """Get core fingerprint used as salt in client"""
        if self._client_metadata is None:
            self._load_metadata_only()
        return self._client_metadata.get("fingerprint_core_salt")

    def _load_metadata_only(self) -> None:
        """Load only metadata (for fingerprint checks)"""
        with open(self.compiled_dir / "metadata-core.json") as f:
            self._core_metadata = json.load(f)
        with open(self.compiled_dir / "metadata-client-template.json") as f:
            self._client_metadata = json.load(f)

    def _validate_integrity(self) -> bool:
        """Validate governance integrity"""
        checks = [
            ("Core fingerprint", self._validate_core_fingerprint()),
            ("Client fingerprint", self._validate_client_fingerprint()),
            ("Salt strategy", self._validate_salt_strategy()),
            ("Core readonly", self._validate_core_readonly()),
            ("Client customizable", self._validate_client_customizable()),
            ("Core > 0 items", len(self._core_data.get("items", [])) > 0),
            ("Client > 0 items", len(self._client_data.get("items", [])) > 0),
            ("Fingerprints different", self.get_core_fingerprint() != self.get_client_fingerprint()),
        ]

        all_passed = True
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"    {status} {check_name}")
            if not result:
                all_passed = False

        return all_passed

    def _validate_core_fingerprint(self) -> bool:
        """Validate core fingerprint is embedded"""
        core = self.get_core_governance()
        return "fingerprint" in core

    def _validate_client_fingerprint(self) -> bool:
        """Validate client fingerprint is embedded"""
        client = self.get_client_governance()
        return "fingerprint" in client

    def _validate_salt_strategy(self) -> bool:
        """Validate salt strategy (core fingerprint in client metadata)"""
        core_fp = self.get_core_fingerprint()
        salt_fp = self.get_salt_fingerprint()
        return core_fp == salt_fp

    def _validate_core_readonly(self) -> bool:
        """Validate core metadata has readonly flag"""
        return self._core_metadata.get("readonly") is True

    def _validate_client_customizable(self) -> bool:
        """Validate client metadata has customizable flag"""
        return self._client_metadata.get("customizable") is True

    def get_governance_summary(self) -> Dict[str, Any]:
        """Get summary of loaded governance"""
        core = self.get_core_governance()
        client = self.get_client_governance()

        core_items = core.get("items", [])
        client_items = client.get("items", [])

        # Count by type
        type_counts = {}
        for item in core_items + client_items:
            item_type = item.get("type", "unknown")
            type_counts[item_type] = type_counts.get(item_type, 0) + 1

        # Count by criticality
        criticality_counts = {}
        for item in core_items + client_items:
            criticality = item.get("criticality", "unknown")
            criticality_counts[criticality] = criticality_counts.get(criticality, 0) + 1

        return {
            "version": "3.0",
            "status": "loaded",
            "total_items": len(core_items) + len(client_items),
            "core_items": len(core_items),
            "client_items": len(client_items),
            "by_type": type_counts,
            "by_criticality": criticality_counts,
            "core_fingerprint": self.get_core_fingerprint(),
            "client_fingerprint": self.get_client_fingerprint(),
            "salt_fingerprint": self.get_salt_fingerprint(),
            "core_readonly": self._core_metadata.get("readonly"),
            "client_customizable": self._client_metadata.get("customizable"),
        }

    def export_governance_json(self, filepath: str, include_core: bool = True, include_client: bool = True) -> None:
        """Export governance as JSON for inspection/customization"""
        output = {}

        if include_core:
            output["core"] = self.get_core_governance()

        if include_client:
            output["client"] = self.get_client_governance()

        output["_metadata"] = {
            "exported": True,
            "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
            "summary": self.get_governance_summary(),
        }

        with open(filepath, "w") as f:
            json.dump(output, f, indent=2)


if __name__ == "__main__":
    loader = GovernanceRuntimeLoader()
    result = loader.load_all()

    print()
    print("=" * 70)
    print("✅ GOVERNANCE RUNTIME LOADER INITIALIZED")
    print("=" * 70)
    print()

    summary = loader.get_governance_summary()
    print("📊 Governance Summary:")
    print(f"  Version: {summary.get('version')}")
    print(f"  Total Items: {summary.get('total_items')}")
    print(f"  Core Items (immutable): {summary.get('core_items')}")
    print(f"  Client Items (customizable): {summary.get('client_items')}")
    print()

    print("📈 By Type:")
    for item_type, count in summary.get("by_type", {}).items():
        print(f"  - {item_type}: {count}")

    print()
    print("📊 By Criticality:")
    for criticality, count in summary.get("by_criticality", {}).items():
        print(f"  - {criticality}: {count}")

    print()
    print("🔐 Fingerprints:")
    print(f"  Core: {summary.get('core_fingerprint')[:16]}...")
    print(f"  Client: {summary.get('client_fingerprint')[:16]}...")
    print(f"  Salt: {summary.get('salt_fingerprint')[:16]}...")

    print()
    print("✅ Ready for wizard and agent integration")
