"""
PHASE 4: Deployment Manager
Deploy compiled governance files to runtime/compiled/

Workflow:
1. Validate compiled files exist and are valid
2. Create runtime/compiled/ directory structure
3. Copy msgpack files to runtime location
4. Copy metadata files to runtime location
5. Create deployment checklist
6. Generate deployment manifest
7. Provide git commands for commit + tag
"""

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


class DeploymentManager:
    """Manages deployment of compiled governance files to runtime"""

    def __init__(self, repo_root: str = None):
        """Initialize deployment manager"""
        if repo_root is None:
            repo_root = Path.cwd()
        else:
            repo_root = Path(repo_root)

        self.repo_root = Path(repo_root)
        self.compiled_dir = self.repo_root / "compiler" / "compiled"
        self.runtime_dir = self.repo_root / "runtime"
        self.runtime_compiled = self.runtime_dir / "compiled"

    def deploy(self) -> Dict[str, Any]:
        """
        Execute complete deployment

        Returns:
            Dictionary with deployment results
        """
        print("🚀 Starting PHASE 4: Deployment...")
        print()

        # Step 1: Validate compiled files
        print("📋 Step 1: Validating compiled files...")
        if not self._validate_compiled_files():
            print("❌ Validation failed")
            return {"success": False}
        print("✅ Validation passed")
        print()

        # Step 2: Create runtime directory structure
        print("📁 Step 2: Creating runtime directory structure...")
        self._create_runtime_structure()
        print("✅ Runtime structure created")
        print()

        # Step 3: Copy files
        print("📦 Step 3: Copying compiled files to runtime...")
        copy_result = self._copy_files()
        if not copy_result:
            print("❌ Copy failed")
            return {"success": False}
        print("✅ Files copied successfully")
        print()

        # Step 4: Verify deployment
        print("✔️ Step 4: Verifying deployment...")
        if not self._verify_deployment():
            print("❌ Verification failed")
            return {"success": False}
        print("✅ Deployment verified")
        print()

        # Step 5: Generate checklist and manifest
        checklist = self._generate_checklist()
        manifest = self._generate_manifest()

        return {
            "success": True,
            "deployed_files": copy_result,
            "deployment_location": str(self.runtime_compiled),
            "checklist": checklist,
            "manifest": manifest,
            "next_steps": self._get_next_steps(),
        }

    def _validate_compiled_files(self) -> bool:
        """Validate that all required compiled files exist"""
        required_files = [
            self.compiled_dir / "governance-core.compiled.msgpack",
            self.compiled_dir / "governance-client-template.compiled.msgpack",
            self.compiled_dir / "metadata-core.json",
            self.compiled_dir / "metadata-client-template.json",
        ]

        all_exist = True
        for file in required_files:
            if file.exists():
                size_kb = file.stat().st_size / 1024
                print(f"  ✅ {file.name} ({size_kb:.1f} KB)")
            else:
                print(f"  ❌ {file.name} MISSING")
                all_exist = False

        # Verify metadata is valid JSON
        for metadata_file in [
            self.compiled_dir / "metadata-core.json",
            self.compiled_dir / "metadata-client-template.json",
        ]:
            try:
                with open(metadata_file) as f:
                    json.load(f)
                print(f"  ✅ {metadata_file.name} is valid JSON")
            except Exception as e:
                print(f"  ❌ {metadata_file.name} is not valid JSON: {e}")
                all_exist = False

        return all_exist

    def _create_runtime_structure(self) -> None:
        """Create runtime/compiled/ directory structure"""
        self.runtime_compiled.mkdir(parents=True, exist_ok=True)

        # Create subdirectories if needed
        (self.runtime_compiled / "backup").mkdir(exist_ok=True)

        print(f"  📁 Created: {self.runtime_compiled}")

    def _copy_files(self) -> Dict[str, str]:
        """Copy compiled files to runtime location"""
        files_to_copy = [
            ("governance-core.compiled.msgpack", self.compiled_dir),
            ("governance-client-template.compiled.msgpack", self.compiled_dir),
            ("metadata-core.json", self.compiled_dir),
            ("metadata-client-template.json", self.compiled_dir),
        ]

        copied_files = {}
        for filename, source_dir in files_to_copy:
            src = source_dir / filename
            dst = self.runtime_compiled / filename

            # Backup existing file if it exists
            if dst.exists():
                backup_dst = self.runtime_compiled / "backup" / f"{filename}.backup"
                shutil.copy2(dst, backup_dst)
                print(f"  💾 Backed up: {filename}")

            # Copy file
            shutil.copy2(src, dst)
            copied_files[filename] = str(dst)
            print(f"  📄 Copied: {filename}")

        return copied_files

    def _verify_deployment(self) -> bool:
        """Verify that deployment was successful"""
        required_files = [
            "governance-core.compiled.msgpack",
            "governance-client-template.compiled.msgpack",
            "metadata-core.json",
            "metadata-client-template.json",
        ]

        all_verified = True
        for filename in required_files:
            file_path = self.runtime_compiled / filename
            if file_path.exists():
                size_kb = file_path.stat().st_size / 1024
                print(f"  ✅ {filename} deployed ({size_kb:.1f} KB)")
            else:
                print(f"  ❌ {filename} NOT deployed")
                all_verified = False

        return all_verified

    def _generate_checklist(self) -> Dict[str, bool]:
        """Generate deployment checklist"""
        checklist = {
            "Compiled files validated": True,
            "Runtime directory created": self.runtime_compiled.exists(),
            "Core msgpack copied": (self.runtime_compiled / "governance-core.compiled.msgpack").exists(),
            "Client msgpack copied": (self.runtime_compiled / "governance-client-template.compiled.msgpack").exists(),
            "Core metadata copied": (self.runtime_compiled / "metadata-core.json").exists(),
            "Client metadata copied": (self.runtime_compiled / "metadata-client-template.json").exists(),
            "Backup directory created": (self.runtime_compiled / "backup").exists(),
        }

        return checklist

    def _generate_manifest(self) -> Dict[str, Any]:
        """Generate deployment manifest"""
        manifest = {
            "version": "3.0",
            "deployment_date": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "deployment_location": str(self.runtime_compiled),
            "artifacts": {
                "core_msgpack": "governance-core.compiled.msgpack",
                "client_msgpack": "governance-client-template.compiled.msgpack",
                "core_metadata": "metadata-core.json",
                "client_metadata": "metadata-client-template.json",
            },
            "file_count": 4,
            "status": "deployed",
            "ready_for": "wizard_and_agent_runtime",
        }

        # Save manifest
        manifest_file = self.runtime_compiled / "DEPLOYMENT_MANIFEST.json"
        with open(manifest_file, "w") as f:
            json.dump(manifest, f, indent=2)

        return manifest

    def _get_next_steps(self) -> List[str]:
        """Get next steps after deployment"""
        return [
            "1. Review deployment files in runtime/compiled/",
            "2. Run: git add runtime/compiled/",
            "3. Run: git commit -m 'chore(sdd): PHASE 4 deployment - v3.0 pipeline+compiler'",
            "4. Run: git tag -a v3.0-pipeline-compiler-complete -m 'PHASE 1-4 complete'",
            "5. Update CHANGELOG.md with deployment details",
            "6. Ready for PHASE 5: Wizard integration",
        ]

    def get_deployment_status(self) -> Dict[str, Any]:
        """Get current deployment status"""
        return {
            "deployed": self.runtime_compiled.exists(),
            "files_present": {
                "core_msgpack": (self.runtime_compiled / "governance-core.compiled.msgpack").exists(),
                "client_msgpack": (self.runtime_compiled / "governance-client-template.compiled.msgpack").exists(),
                "core_metadata": (self.runtime_compiled / "metadata-core.json").exists(),
                "client_metadata": (self.runtime_compiled / "metadata-client-template.json").exists(),
            },
            "location": str(self.runtime_compiled),
        }


if __name__ == "__main__":
    manager = DeploymentManager()
    result = manager.deploy()

    if result.get("success"):
        print()
        print("=" * 70)
        print("🎉 PHASE 4: DEPLOYMENT COMPLETE")
        print("=" * 70)
        print()

        print("📋 Deployment Checklist:")
        for check, status in result.get("checklist", {}).items():
            status_icon = "✅" if status else "❌"
            print(f"  {status_icon} {check}")

        print()
        print("📦 Deployment Location:")
        print(f"  {result.get('deployment_location')}")

        print()
        print("📄 Artifacts Deployed:")
        for name, path in result.get("manifest", {}).get("artifacts", {}).items():
            print(f"  - {name}: {path}")

        print()
        print("🔗 Next Steps:")
        for step in result.get("next_steps", []):
            print(f"  {step}")

        print()
        print(f"✅ Status: {result.get('manifest', {}).get('status').upper()}")
    else:
        print()
        print("❌ Deployment failed")
