import json
from pathlib import Path
from typing import Dict, List, Tuple

import msgpack

"""Phase 2: Load and deserialize compiled artifacts from runtime/"""


def _reconstruct_guideline(guide_dict: Dict, string_pool: List[str]) -> Dict:
    """Reconstruct guideline handling None indices gracefully"""
    title = ""
    if "title_idx" in guide_dict and guide_dict["title_idx"] is not None:
        try:
            title = string_pool[guide_dict["title_idx"]]
        except (IndexError, TypeError):
            title = ""

    description = ""
    if "description_idx" in guide_dict and guide_dict["description_idx"] is not None:
        try:
            description = string_pool[guide_dict["description_idx"]]
        except (IndexError, TypeError):
            description = ""

    category = ""
    if isinstance(guide_dict.get("category"), int) and guide_dict["category"] is not None:
        try:
            category = string_pool[guide_dict["category"]]
        except (IndexError, TypeError):
            category = ""

    return {
        "id": guide_dict.get("id", 0),
        "type": guide_dict.get("type", "SOFT"),
        "title": title,
        "description": description,
        "category": category,
        "tags": [],
        "priority": guide_dict.get("priority", 2),
    }


def _reconstruct_guidelines(compiled_data: Dict, string_pool: List[str]) -> Dict:
    """Reconstruct guidelines from indexed format"""
    guidelines = {}
    compiled_guidelines = compiled_data.get("guidelines", [])

    for guide_dict in compiled_guidelines:
        expanded = _reconstruct_guideline(guide_dict, string_pool)
        guide_id = f"G{expanded['id']:02d}"
        guidelines[guide_id] = expanded

    return guidelines


def _reconstruct_mandate(mandate_dict: Dict, string_pool: List[str]) -> Dict:
    """Reconstruct a mandate from indexed format"""
    title = ""
    if "title_idx" in mandate_dict and mandate_dict["title_idx"] is not None:
        try:
            title = string_pool[mandate_dict["title_idx"]]
        except (IndexError, TypeError):
            title = ""

    description = ""
    if "description_idx" in mandate_dict and mandate_dict["description_idx"] is not None:
        try:
            description = string_pool[mandate_dict["description_idx"]]
        except (IndexError, TypeError):
            description = ""

    return {
        "id": mandate_dict.get("id", ""),
        "title": title,
        "description": description,
        "priority": mandate_dict.get("priority", 1),
    }


def _reconstruct_mandates(compiled_data: Dict, string_pool: List[str]) -> Dict:
    """Reconstruct mandates from indexed format"""
    mandates = {}
    compiled_mandates = compiled_data.get("mandates", [])

    for mandate_dict in compiled_mandates:
        expanded = _reconstruct_mandate(mandate_dict, string_pool)
        mandate_id = expanded.get("id", "")
        if mandate_id:
            mandates[mandate_id] = expanded

    return mandates


def phase_2_load_compiled(repo_root: Path | None = None) -> Tuple[bool, Dict]:  # noqa: C901
    """Load and deserialize compiled artifacts from runtime/"""
    repo_root = repo_root or Path.cwd()

    report = {
        "phase": "PHASE_2_LOAD_COMPILED",
        "status": "PENDING",
        "checks": {
            "mandate_bin_exists": False,
            "guidelines_bin_exists": False,
            "metadata_exists": False,
            "artifacts_deserialize": False,
            "data_reconstruction": False,
        },
        "data": {
            "mandate": {},
            "guidelines": {},
        },
        "statistics": {
            "mandate_count": 0,
            "guideline_count": 0,
            "string_pool_size": 0,
        },
        "errors": [],
        "warnings": [],
        "_artifacts": {},
    }

    runtime_compiled = repo_root / "runtime" / "compiled"
    if not runtime_compiled.exists():
        report["errors"].append(f"runtime/compiled directory not found at {runtime_compiled}")
        report["status"] = "FAILED"
        return (False, report)

    # Check for compiled msgpack files
    mandate_msgpack = runtime_compiled / "governance-core.compiled.msgpack"
    guidelines_msgpack = runtime_compiled / "governance-client-template.compiled.msgpack"
    metadata_json = runtime_compiled / "metadata-governance-core.json"

    if not mandate_msgpack.exists():
        report["warnings"].append("governance-core.compiled.msgpack not found (optional)")
    else:
        report["checks"]["mandate_bin_exists"] = True

    if not guidelines_msgpack.exists():
        report["errors"].append("governance-client-template.compiled.msgpack not found")
        report["status"] = "FAILED"
        return (False, report)

    report["checks"]["guidelines_bin_exists"] = True

    if not metadata_json.exists():
        report["warnings"].append("metadata.json not found (optional)")
    else:
        report["checks"]["metadata_exists"] = True

    try:
        mandate_compiled = {}
        if mandate_msgpack.exists():
            with open(mandate_msgpack, "rb") as f:
                mandate_compiled = msgpack.unpackb(f.read(), raw=False)

        with open(guidelines_msgpack, "rb") as f:
            guidelines_compiled = msgpack.unpackb(f.read(), raw=False)

        metadata = {}
        if metadata_json.exists():
            with open(metadata_json, "r", encoding="utf-8") as f:
                metadata = json.load(f)

        report["checks"]["artifacts_deserialize"] = True
        report["_artifacts"]["mandate"] = mandate_compiled
        report["_artifacts"]["guidelines"] = guidelines_compiled
        report["_artifacts"]["metadata"] = metadata

    except Exception as e:
        report["errors"].append(f"Failed to deserialize compiled artifacts: {e}")
        report["status"] = "FAILED"
        return (False, report)

    try:
        mandates = {}
        for item in mandate_compiled.get("items", []):
            if item.get("type") == "MANDATE" and item.get("id"):
                mandates[item["id"]] = {
                    "id": item.get("id", ""),
                    "title": item.get("title", ""),
                    "criticality": item.get("criticality", ""),
                    "category": item.get("category", ""),
                }

        guidelines = {}
        for item in mandate_compiled.get("items", []):
            if item.get("type") == "GUIDELINE" and item.get("id"):
                guidelines[f"core_{item['id']}"] = {
                    "id": item.get("id", ""),
                    "title": item.get("title", ""),
                    "criticality": item.get("criticality", ""),
                    "category": item.get("category", ""),
                    "source": "core",
                }

        for item in guidelines_compiled.get("items", []):
            if item.get("type") == "GUIDELINE" and item.get("id"):
                guidelines[f"client_{item['id']}"] = {
                    "id": item.get("id", ""),
                    "title": item.get("title", ""),
                    "criticality": item.get("criticality", ""),
                    "category": item.get("category", ""),
                    "source": "client",
                }

        report["data"]["mandate"] = mandates
        report["data"]["guidelines"] = guidelines
        report["statistics"]["mandate_count"] = len(mandates)
        report["statistics"]["guideline_count"] = len(guidelines)
        report["statistics"]["string_pool_size"] = 0
        report["checks"]["data_reconstruction"] = True

    except Exception as e:
        report["errors"].append(f"Failed to reconstruct data: {e}")
        report["status"] = "FAILED"
        return (False, report)

    if report["statistics"]["guideline_count"] == 0:
        report["errors"].append("No guidelines loaded")
        report["status"] = "FAILED"
        return (False, report)

    report["status"] = "SUCCESS"
    return (True, report)
