#!/usr/bin/env python
"""
SDD v3.0 Integration Pipeline: Compile & Deploy

Workflow:
  1. Read SOURCE (core/*.spec/*.dsl)
  2. Validate syntax
  3. Compile to MessagePack binary (.bin)
  4. Deploy to runtime/
  5. Generate metadata.json with audit trail

This bridges migration → compiler → runtime → wizard

Location: compiler/src/integrate.py (orchestration logic)
Entry point: python compiler/compiler.py (from repository root)
Usage: from compiler.src.integrate import SDDIntegrator
"""

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class SDDIntegrator:
    """Orchestrate complete SDD v3.0 integration pipeline"""

    def __init__(self, repo_root: Path = None):
        """Initialize integrator with repository root"""
        if repo_root is None:
            # Detect repo root: go up from compiler/src/ to find _core
            current = Path(__file__).parent.parent.parent  # compiler/src/ → _core
            if (current / "core").exists():
                repo_root = current.parent  # go up one more to repo root
            else:
                repo_root = Path.cwd()

        self.repo = repo_root
        self.core = repo_root / "_core" / "core"
        self.spec = repo_root / "_spec"
        self.compiler = repo_root / "_core" / "compiler"
        self.runtime = repo_root / "_core" / "runtime"
        self.compiler_src = self.compiler / "src"

        # Metrics
        self.metrics: Dict[str, Any] = {
            "source": {},
            "compilation": {},
            "deployment": {},
        }

    def validate_paths(self) -> bool:
        """Verify all required directories and files exist"""
        required = {
            "_spec/": self.spec,
            "_spec/mandate.spec": self.spec / "mandate.spec",
            "_spec/guidelines.dsl": self.spec / "guidelines.dsl",
            "compiler/src/dsl_compiler.py": self.compiler_src / "dsl_compiler.py",
            "runtime/": self.runtime,
        }

        missing = []
        for name, path in required.items():
            if not path.exists():
                missing.append(f"  ❌ {name}")

        if missing:
            print("❌ Missing required files:")
            print("\n".join(missing))
            return False

        print("✅ All paths validated")
        return True

    @staticmethod
    def _file_hash(path: Path, truncate: int = 8) -> str:
        """Calculate SHA256 hash of file (truncated)"""
        return hashlib.sha256(path.read_bytes()).hexdigest()[:truncate]

    @staticmethod
    def _count_items(text: str, pattern: str) -> int:
        """Count regex matches in text"""
        return len(re.findall(pattern, text))

    def analyze_sources(self) -> bool:
        """Analyze and validate source files"""
        print("\n📊 Analyzing source files")

        try:
            mandate_file = self.core / "mandate.spec"
            guidelines_file = self.core / "guidelines.dsl"

            mandate_text = mandate_file.read_text(encoding="utf-8")
            guidelines_text = guidelines_file.read_text(encoding="utf-8")

            # Count items
            mandate_count = self._count_items(mandate_text, r"mandate\s+M\d+")
            guideline_count = self._count_items(guidelines_text, r"guideline\s+G\d+")

            # Calculate hashes
            mandate_hash = self._file_hash(mandate_file)
            guidelines_hash = self._file_hash(guidelines_file)

            # Store metrics
            self.metrics["source"] = {
                "mandate_spec": {
                    "size": len(mandate_text),
                    "hash": mandate_hash,
                    "items": mandate_count,
                },
                "guidelines_dsl": {
                    "size": len(guidelines_text),
                    "hash": guidelines_hash,
                    "items": guideline_count,
                },
            }

            print(f"  ✅ mandate.spec: {mandate_count} mandates ({len(mandate_text):,} bytes)")
            print(f"  ✅ guidelines.dsl: {guideline_count} guidelines ({len(guidelines_text):,} bytes)")

            return True

        except Exception as e:
            print(f"  ❌ Error analyzing sources: {e}")
            return False

    def compile_mandate(self) -> bool:
        """Compile mandate.spec to binary"""
        print("\n📝 Compiling mandate.spec")

        input_file = self.core / "mandate.spec"
        output_file = self.runtime / "mandate.bin"

        script = self.compiler_src / "dsl_compiler.py"

        cmd = [sys.executable, str(script), str(input_file), str(output_file), "--format", "msgpack"]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)

            if result.returncode == 0:
                if output_file.exists():
                    size = output_file.stat().st_size
                    self.metrics["compilation"]["mandate"] = {
                        "status": "success",
                        "output_size": size,
                        "format": "binary",
                    }
                    print(f"  ✅ mandate.bin ({size:,} bytes)")
                    return True
                else:
                    print("  ⚠️  Binary not found, trying JSON fallback...")
                    return False
            else:
                print("  ❌ Compilation failed:")
                print(result.stderr)
                self.metrics["compilation"]["mandate"] = {"status": "failed", "error": result.stderr}
                return False

        except Exception as e:
            print(f"  ❌ Error: {e}")
            self.metrics["compilation"]["mandate"] = {"status": "error", "error": str(e)}
            return False

    def compile_guidelines(self) -> bool:
        """Compile guidelines.dsl to binary"""
        print("\n📝 Compiling guidelines.dsl")

        input_file = self.core / "guidelines.dsl"
        output_file = self.runtime / "guidelines.bin"

        script = self.compiler_src / "dsl_compiler.py"

        cmd = [sys.executable, str(script), str(input_file), str(output_file), "--format", "msgpack"]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)

            if result.returncode == 0:
                if output_file.exists():
                    size = output_file.stat().st_size
                    self.metrics["compilation"]["guidelines"] = {
                        "status": "success",
                        "output_size": size,
                        "format": "binary",
                    }
                    print(f"  ✅ guidelines.bin ({size:,} bytes)")
                    return True
                else:
                    print("  ⚠️  Binary not found, trying JSON fallback...")
                    return False
            else:
                print("  ❌ Compilation failed:")
                print(result.stderr)
                self.metrics["compilation"]["guidelines"] = {"status": "failed", "error": result.stderr}
                return False

        except Exception as e:
            print(f"  ❌ Error: {e}")
            self.metrics["compilation"]["guidelines"] = {"status": "error", "error": str(e)}
            return False

    def generate_metadata(self) -> bool:
        """Generate metadata.json with audit trail and metrics"""
        print("\n📊 Generating metadata.json")

        try:
            mandate_hash = self._file_hash(self.core / "mandate.spec")
            guidelines_hash = self._file_hash(self.core / "guidelines.dsl")

            # Count items from cached metrics
            source_metrics = self.metrics.get("source", {})
            mandate_count = source_metrics.get("mandate_spec", {}).get("items", 0)
            guideline_count = source_metrics.get("guidelines_dsl", {}).get("items", 0)

            # Check for artifacts
            mandate_exists = (self.runtime / "mandate.bin").exists()
            guidelines_exists = (self.runtime / "guidelines.bin").exists()

            metadata = {
                "version": "3.0.0",
                "compiled_at": datetime.utcnow().isoformat() + "Z",
                "source": {
                    "mandate_spec_hash": mandate_hash,
                    "guidelines_dsl_hash": guidelines_hash,
                },
                "statistics": {
                    "mandates": mandate_count,
                    "guidelines": guideline_count,
                },
                "artifacts": {
                    "mandate_bin": mandate_exists,
                    "guidelines_bin": guidelines_exists,
                },
                "audit_trail": [
                    {
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "action": "integration",
                        "status": "completed",
                    },
                ],
            }

            metadata_file = self.runtime / "metadata.json"
            metadata_file.write_text(json.dumps(metadata, indent=2))

            self.metrics["deployment"]["metadata"] = {
                "status": "created",
                "size": metadata_file.stat().st_size,
            }

            print(f"  ✅ metadata.json ({metadata_file.stat().st_size} bytes)")
            print(f"     • {mandate_count} mandates, {guideline_count} guidelines")

            return True

        except Exception as e:
            print(f"  ❌ Error generating metadata: {e}")
            return False

    def verify_deployment(self) -> Dict[str, Any]:
        """Verify all artifacts deployed successfully"""
        print("\n" + "=" * 60)
        print("📦 Deployment Verification")
        print("=" * 60)

        artifacts = {
            "mandate.bin": self.runtime / "mandate.bin",
            "guidelines.bin": self.runtime / "guidelines.bin",
            "metadata.json": self.runtime / "metadata.json",
        }

        manifest = []
        for name, path in artifacts.items():
            if path.exists():
                size = path.stat().st_size
                manifest.append(f"  ✅ {name:25s} {size:>10,} bytes")
            else:
                manifest.append(f"  ❌ {name:25s} NOT FOUND")

        print("\nArtifacts in runtime/:")
        for line in manifest:
            print(line)

        # Check if any critical files are missing
        critical = [
            self.runtime / "mandate.bin",
            self.runtime / "guidelines.bin",
        ]

        all_present = all(p.exists() for p in critical)

        return {
            "all_present": all_present,
            "manifest": manifest,
            "critical_count": sum(1 for p in critical if p.exists()),
            "critical_required": len(critical),
        }

    def run(self) -> bool:
        """Execute complete compilation pipeline"""
        print("=" * 60)
        print("🚀 SDD v3.0 Compiler - Integration Pipeline")
        print("=" * 60)

        # Validate
        if not self.validate_paths():
            return False

        # Analyze sources
        if not self.analyze_sources():
            return False

        # Compile
        mandate_ok = self.compile_mandate()
        guidelines_ok = self.compile_guidelines()

        if not (mandate_ok and guidelines_ok):
            print("\n⚠️  One or more compilations failed!")
            return False

        # Generate metadata
        if not self.generate_metadata():
            return False

        # Verify deployment
        verification = self.verify_deployment()

        if not verification["all_present"]:
            print("\n❌ Critical artifacts missing!")
            return False

        # Success
        print("✅ Compilation complete!")
        print("   Ready for wizard: python wizard/src/wizard.py")
        print("   Or import: from compiler.src.integrate import SDDIntegrator")

        return True


if __name__ == "__main__":
    # Allow running as main module
    integrator = SDDIntegrator(Path.cwd())
    success = integrator.run()
    sys.exit(0 if success else 1)
