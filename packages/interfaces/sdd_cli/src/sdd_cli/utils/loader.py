"""Governance configuration loader and integration utilities."""

from pathlib import Path
from typing import Any, Dict, Optional


def _resolve_compiled_dir(path: str) -> Optional[Path]:
    """Resolve governance compiled directory from a user path.

    Accepts either:
    - a path that already points to `.../compiled`
    - a path that contains a `compiled/` child (e.g. `runtime`)
    """
    path_obj = Path(path)

    direct_required = [
        path_obj / "governance-core.compiled.msgpack",
        path_obj / "governance-client-template.compiled.msgpack",
        path_obj / "metadata-core.json",
        path_obj / "metadata-client-template.json",
    ]
    if all(f.exists() for f in direct_required):
        return path_obj

    compiled_dir = path_obj / "compiled"
    nested_required = [
        compiled_dir / "governance-core.compiled.msgpack",
        compiled_dir / "governance-client-template.compiled.msgpack",
        compiled_dir / "metadata-core.json",
        compiled_dir / "metadata-client-template.json",
    ]
    if all(f.exists() for f in nested_required):
        return compiled_dir

    return None


def load_governance_config(path: str) -> Dict[str, Any]:
    """Load governance configuration from sdd_wizard."""
    try:
        from sdd_wizard.sdd_runtime.governance_runtime_loader import GovernanceRuntimeLoader

        compiled_dir = _resolve_compiled_dir(path)
        if compiled_dir is None:
            raise ValueError(f"Invalid governance path: {path}")

        loader = GovernanceRuntimeLoader(compiled_dir)
        runtime_status = loader.load_all()
        core_items = loader.getpackages_governance().get("items", [])
        client_items = loader.get_client_governance().get("items", [])
        all_items = core_items + client_items

        return {
            "core_fingerprint": runtime_status.get("core_fingerprint"),
            "client_fingerprint": runtime_status.get("client_fingerprint"),
            "items": all_items,
            "core_items_count": len(core_items),
            "client_items_count": len(client_items),
        }
    except Exception as e:
        raise ValueError(f"Failed to load governance config: {e}") from e


def validate_governance_path(path: str) -> bool:
    """Validate that governance path contains required files."""
    return _resolve_compiled_dir(path) is not None


def get_governance_summary(path: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get human-readable governance summary."""
    if config is None:
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
