"""Phase 2: Load and deserialize compiled artifacts from runtime/"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from loader import ArtifactLoader


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

    runtime = repo_root / "runtime"
    if not runtime.exists():
        report["errors"].append(f"runtime directory not found at {runtime}")
        report["status"] = "FAILED"
        return (False, report)

    mandate_bin = runtime / "mandate.bin"
    guidelines_bin = runtime / "guidelines.bin"
    metadata_json = runtime / "metadata.json"

    if not mandate_bin.exists():
        report["warnings"].append("mandate.bin not found (optional)")
    else:
        report["checks"]["mandate_bin_exists"] = True

    if not guidelines_bin.exists():
        report["errors"].append("guidelines.bin not found")
        report["status"] = "FAILED"
        return (False, report)

    report["checks"]["guidelines_bin_exists"] = True

    if not metadata_json.exists():
        report["warnings"].append("metadata.json not found (optional)")
    else:
        report["checks"]["metadata_exists"] = True

    try:
        loader = ArtifactLoader(repo_root)

        mandate_compiled = {}
        try:
            mandate_compiled = loader.load_compiled_mandate()
        except FileNotFoundError:
            report["warnings"].append("Mandate compiled artifacts not found")

        guidelines_compiled = loader.load_compiled_guidelines()

        metadata = {}
        try:
            metadata = loader.load_metadata()
        except FileNotFoundError:
            pass

        report["checks"]["artifacts_deserialize"] = True
        report["_artifacts"]["mandate"] = mandate_compiled
        report["_artifacts"]["guidelines"] = guidelines_compiled
        report["_artifacts"]["metadata"] = metadata

    except Exception as e:
        report["errors"].append(f"Failed to deserialize compiled artifacts: {e}")
        report["status"] = "FAILED"
        return (False, report)

    try:
        string_pool = guidelines_compiled.get("string_pool", [])
        report["statistics"]["string_pool_size"] = len(string_pool)

        if mandate_compiled:
            reconstructed_mandates = _reconstruct_mandates(mandate_compiled, string_pool)
            report["data"]["mandate"] = reconstructed_mandates
            report["statistics"]["mandate_count"] = len(reconstructed_mandates)
        else:
            report["data"]["mandate"] = {}
            report["statistics"]["mandate_count"] = 0

        reconstructed_guidelines = _reconstruct_guidelines(guidelines_compiled, string_pool)
        report["data"]["guidelines"] = reconstructed_guidelines
        report["statistics"]["guideline_count"] = len(reconstructed_guidelines)

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
