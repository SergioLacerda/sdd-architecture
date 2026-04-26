"""Governance configuration loader and integration utilities."""

import sys
from pathlib import Path
from typing import Any, Dict

# Add parent directory to path to import .sdd-wizard modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def load_governance_config(path: str) -> Dict[str, Any]:
    """Load governance configuration from .sdd-wizard."""
    try:
        from sdd_wizard.governance_runtime_loader import GovernanceRuntimeLoader

        loader = GovernanceRuntimeLoader(Path(path))
        config = loader.load_all()

        return {
            "core_fingerprint": config.get("core_fingerprint"),
            "client_fingerprint": config.get("client_fingerprint"),
            "items": config.get("items", []),
            "core_items_count": len([i for i in config.get("items", []) if i.get("is_immutable", False)]),
            "client_items_count": len([i for i in config.get("items", []) if not i.get("is_immutable", False)]),
        }
    except Exception as e:
        raise ValueError(f"Failed to load governance config: {e}")


def validate_governance_path(path: str) -> bool:
    """Validate that governance path contains required files."""
    path_obj = Path(path)

    required_files = [
        path_obj / "compiled" / "governance-core.compiled.msgpack",
        path_obj / "compiled" / "governance-client-template.compiled.msgpack",
        path_obj / "compiled" / "metadata-core.json",
        path_obj / "compiled" / "metadata-client-template.json",
    ]

    return all(f.exists() for f in required_files)


def get_governance_summary(path: str) -> Dict[str, Any]:
    """Get human-readable governance summary."""
    config = load_governance_config(path)

    return {
        "Configuration Path": path,
        "Status": "✓ Ready",
        "Core Items": config.get("core_items_count", 0),
        "Customizable Items": config.get("client_items_count", 0),
        "Total Items": len(config.get("items", [])),
        "Core Fingerprint": config.get("core_fingerprint", "N/A")[:16] + "...",
        "Client Fingerprint": config.get("client_fingerprint", "N/A")[:16] + "...",
    }
