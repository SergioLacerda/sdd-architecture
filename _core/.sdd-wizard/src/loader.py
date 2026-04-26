"""
SDD v3.0 Wizard - Load and deserialize compiled artifacts
"""

import json
from pathlib import Path
from typing import Any, Dict, Tuple


class ArtifactLoader:
    """Load all artifacts needed for wizard orchestration"""

    def __init__(self, repo_root: Path = Path.cwd()):
        self.repo_root = repo_root
        self.sdd_core = repo_root / ".sdd-core"
        self.sdd_runtime = repo_root / ".sdd-runtime"

    def load_source_mandate(self) -> str:
        """Load SOURCE mandate.spec (text DSL)"""
        mandate_file = self.sdd_core / "mandate.spec"
        if not mandate_file.exists():
            raise FileNotFoundError(f"mandate.spec not found at {mandate_file}")
        return mandate_file.read_text(encoding='utf-8')

    def load_source_guidelines(self) -> str:
        """Load SOURCE guidelines.dsl (text DSL)"""
        guidelines_file = self.sdd_core / "guidelines.dsl"
        if not guidelines_file.exists():
            raise FileNotFoundError(f"guidelines.dsl not found at {guidelines_file}")
        return guidelines_file.read_text(encoding='utf-8')

    def load_compiled_mandate(self) -> Dict[str, Any]:
        """Load COMPILED mandate (JSON or msgpack)"""
        # Try .bin first (may be JSON or msgpack)
        mandate_bin = self.sdd_runtime / "mandate.bin"
        mandate_json = self.sdd_runtime / "mandate.json"

        # Try .bin first
        if mandate_bin.exists():
            try:
                content = mandate_bin.read_text(encoding='utf-8')
                return json.loads(content)
            except (json.JSONDecodeError, UnicodeDecodeError):
                # Might be msgpack - try to parse as binary
                pass

        # Try .json fallback
        if mandate_json.exists():
            return json.loads(mandate_json.read_text(encoding='utf-8'))

        raise FileNotFoundError(
            "Compiled mandate not found.\n"
            "Run: python .sdd-compiler/compiler.py (from repository root)\n"
            "Expected: .sdd-runtime/mandate.bin or .sdd-runtime/mandate.json"
        )

    def load_compiled_guidelines(self) -> Dict[str, Any]:
        """Load COMPILED guidelines (JSON or msgpack)"""
        guidelines_bin = self.sdd_runtime / "guidelines.bin"
        guidelines_json = self.sdd_runtime / "guidelines.json"

        # Try .bin first
        if guidelines_bin.exists():
            try:
                content = guidelines_bin.read_text(encoding='utf-8')
                return json.loads(content)
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass

        # Try .json fallback
        if guidelines_json.exists():
            return json.loads(guidelines_json.read_text(encoding='utf-8'))

        raise FileNotFoundError(
            "Compiled guidelines not found.\n"
            "Run: python .sdd-compiler/compiler.py (from repository root)\n"
            "Expected: .sdd-runtime/guidelines.bin or .sdd-runtime/guidelines.json"
        )

    def load_metadata(self) -> Dict[str, Any]:
        """Load metadata.json with audit trail"""
        metadata_file = self.sdd_runtime / "metadata.json"
        if not metadata_file.exists():
            raise FileNotFoundError(f"metadata.json not found at {metadata_file}")

        return json.loads(metadata_file.read_text(encoding='utf-8'))

    def load_all(self) -> Dict[str, Any]:
        """Load all artifacts (for wizard orchestration)"""
        return {
            'source': {
                'mandate': self.load_source_mandate(),
                'guidelines': self.load_source_guidelines(),
            },
            'compiled': {
                'mandate': self.load_compiled_mandate(),
                'guidelines': self.load_compiled_guidelines(),
            },
            'metadata': self.load_metadata(),
        }


def load_artifacts_safe(repo_root: Path = Path.cwd()) -> Tuple[bool, Dict[str, Any], list]:
    """
    Safely load all artifacts with error handling
    
    Returns:
        (success: bool, data: dict, errors: list)
    """
    loader = ArtifactLoader(repo_root)
    errors = []

    try:
        data = loader.load_all()
        return (True, data, [])
    except FileNotFoundError as e:
        errors.append(f"File not found: {e}")
        return (False, {}, errors)
    except json.JSONDecodeError as e:
        errors.append(f"JSON decode error: {e}")
        return (False, {}, errors)
    except Exception as e:
        errors.append(f"Unexpected error: {e}")
        return (False, {}, errors)
