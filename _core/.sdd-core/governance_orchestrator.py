"""
PHASE 3: Governance Orchestrator
End-to-end orchestration of PHASE 1 (Pipeline) + PHASE 2 (Compiler)

Coordinates:
1. PHASE 1: Read .sdd-core/ → Generate governance-core.json + governance-client.json
2. PHASE 2: Read JSONs → Generate msgpack files + metadata

This enables end-to-end validation of the complete compilation flow.
"""

import sys
from pathlib import Path
from typing import Any, Dict

# Import pipeline builder
sys.path.insert(0, str(Path(__file__).parent))
from pipeline_builder import PipelineBuilder

# Import compiler
sys.path.insert(0, str(Path(__file__).parent.parent / ".sdd-compiler"))
from governance_compiler import GovernanceCompiler


class GovernanceOrchestrator:
    """Orchestrates complete governance compilation pipeline (PHASE 1 + PHASE 2)"""

    def __init__(self, repo_root: str = None):
        """Initialize orchestrator"""
        if repo_root is None:
            repo_root = Path.cwd()
        else:
            repo_root = Path(repo_root)

        self.repo_root = repo_root
        self.sdd_spec = repo_root / "_spec"
        if not self.sdd_spec.exists():
            parent_spec = repo_root.parent / "_spec"
            if parent_spec.exists():
                self.sdd_spec = parent_spec
        self.compiled_dir = repo_root / ".sdd-compiled"

    def run_full_pipeline(self) -> Dict[str, Any]:
        """
        Run complete end-to-end pipeline

        Returns:
            Dictionary with results from both phases
        """
        print("🚀 Starting governance compilation pipeline...")
        print()

        # PHASE 1: Pipeline
        print("📝 PHASE 1: Building governance pipeline...")
        phase1_result = self._run_phase_1()
        if not phase1_result:
            print("❌ PHASE 1 failed")
            return None

        print("✅ PHASE 1 complete:")
        print(f"   - Core items: {phase1_result['core_item_count']}")
        print(f"   - Client items: {phase1_result['client_item_count']}")
        print(f"   - Core fingerprint: {phase1_result['core_fingerprint'][:16]}...")
        print()

        # PHASE 2: Compiler
        print("🔨 PHASE 2: Compiling to msgpack...")
        phase2_result = self._run_phase_2()
        if not phase2_result:
            print("❌ PHASE 2 failed")
            return None

        print("✅ PHASE 2 complete:")
        print(f"   - Core msgpack: {Path(phase2_result['core_msgpack_file']).name}")
        print(f"   - Client msgpack: {Path(phase2_result['client_msgpack_file']).name}")
        print()

        # Combine results
        combined_result = {
            "phase_1": phase1_result,
            "phase_2": phase2_result,
            "full_pipeline_success": True,
        }

        # Run validations
        print("✔️ Validating complete pipeline...")
        if self._validate_full_pipeline(combined_result):
            print("✅ All validations passed")
            combined_result["validated"] = True
        else:
            print("❌ Validation failed")
            combined_result["validated"] = False

        return combined_result

    def _run_phase_1(self) -> Dict[str, Any]:
        """
        Run PHASE 1: Pipeline

        Returns:
            Result dictionary from pipeline
        """
        try:
            builder = PipelineBuilder(str(self.sdd_spec))
            result = builder.build()

            # Save outputs
            saved = builder.save_outputs(str(self.compiled_dir))

            return {
                "core_fingerprint": result["governance_core"]["fingerprint"],
                "client_fingerprint": result["governance_client"]["fingerprint"],
                "core_item_count": len(result["core_items"]),
                "client_item_count": len(result["client_items"]),
                "core_json": str(self.compiled_dir / "governance-core.json"),
                "client_json": str(self.compiled_dir / "governance-client.json"),
                "success": True,
            }
        except Exception as e:
            print(f"❌ PHASE 1 error: {e}")
            return None

    def _run_phase_2(self) -> Dict[str, Any]:
        """
        Run PHASE 2: Compiler

        Returns:
            Result dictionary from compiler
        """
        try:
            compiler = GovernanceCompiler(str(self.compiled_dir))
            result = compiler.compile(str(self.compiled_dir))

            # Validate
            if not compiler.validate_compilation(str(self.compiled_dir)):
                print("❌ Compilation validation failed")
                return None

            return {**result, "success": True}
        except Exception as e:
            print(f"❌ PHASE 2 error: {e}")
            return None

    def _validate_full_pipeline(self, combined_result: Dict[str, Any]) -> bool:
        """Validate that complete pipeline is working correctly"""
        p1 = combined_result.get("phase_1", {})
        p2 = combined_result.get("phase_2", {})

        checks = [
            ("Phase 1 success", p1.get("success") is True),
            ("Phase 2 success", p2.get("success") is True),
            (
                "Core fingerprint preserved",
                p1.get("core_fingerprint") == p2.get("core_fingerprint"),
            ),
            (
                "Client fingerprint preserved",
                p1.get("client_fingerprint") == p2.get("client_fingerprint"),
            ),
            (
                "Core fingerprint used as salt",
                p1.get("core_fingerprint") == p2.get("core_fingerprint_salt"),
            ),
            (
                "Fingerprints different",
                p1.get("core_fingerprint") != p1.get("client_fingerprint"),
            ),
            ("Core items > 0", p1.get("core_item_count", 0) > 0),
            ("Client items > 0", p1.get("client_item_count", 0) > 0),
        ]

        all_passed = True
        for check_name, result in checks:
            status = "✅" if result else "❌"
            print(f"   {status} {check_name}")
            if not result:
                all_passed = False

        return all_passed

    def get_deployment_summary(self) -> Dict[str, Any]:
        """Get summary ready for deployment"""
        return {
            "status": "ready_for_deployment",
            "artifacts": {
                "core_msgpack": str(self.compiled_dir / "governance-core.compiled.msgpack"),
                "client_msgpack": str(
                    self.compiled_dir / "governance-client-template.compiled.msgpack"
                ),
                "core_metadata": str(self.compiled_dir / "metadata-core.json"),
                "client_metadata": str(self.compiled_dir / "metadata-client-template.json"),
            },
            "deployment_location": ".sdd-compiled/",
            "next_step": "PHASE 4: Deploy to .sdd-runtime/",
        }


if __name__ == "__main__":
    orchestrator = GovernanceOrchestrator()
    result = orchestrator.run_full_pipeline()

    if result and result.get("full_pipeline_success"):
        print()
        print("=" * 60)
        print("🎉 PHASE 1 + PHASE 2 COMPLETE")
        print("=" * 60)
        print()

        summary = orchestrator.get_deployment_summary()
        print("📦 Deployment Summary:")
        for key, value in summary.items():
            if key == "artifacts":
                print(f"  {key}:")
                for artifact_name, artifact_path in value.items():
                    print(f"    - {artifact_name}: {Path(artifact_path).name}")
            elif key != "deployment_location":
                print(f"  {key}: {value}")

        print()
        print(f"✅ Ready for: {summary['next_step']}")
    else:
        print()
        print("❌ Pipeline failed")
        sys.exit(1)
