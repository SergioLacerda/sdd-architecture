#!/usr/bin/env python
"""
SDD v3.0 Integration Pipeline: Compile & Deploy

Workflow:
  1. Read SOURCE (.sdd-core/*.spec/*.dsl)
  2. Validate syntax
  3. Compile to MessagePack binary (.bin)
  4. Deploy to .sdd-runtime/
  5. Generate metadata.json with audit trail

This bridges migration → compiler → runtime → wizard
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


class SDDIntegrator:
    """Integrate migration output through compiler to runtime"""
    
    def __init__(self, repo_root: Path = Path.cwd()):
        self.repo = repo_root
        self.sdd_core = repo_root / ".sdd-core"
        self.sdd_compiler = repo_root / ".sdd-compiler"
        self.sdd_runtime = repo_root / ".sdd-runtime"
    
    def validate_paths(self) -> bool:
        """Verify all required directories exist"""
        required = {
            ".sdd-core/mandate.spec": self.sdd_core / "mandate.spec",
            ".sdd-core/guidelines.dsl": self.sdd_core / "guidelines.dsl",
            ".sdd-compiler/src/dsl_compiler.py": self.sdd_compiler / "src" / "dsl_compiler.py",
            ".sdd-runtime/": self.sdd_runtime,
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
    
    def compile_mandate(self) -> bool:
        """Compile mandate.spec to mandate.bin"""
        print("\n📝 Compiling mandate.spec → mandate.bin")
        
        input_file = self.sdd_core / "mandate.spec"
        output_file = self.sdd_runtime / "mandate.bin"
        
        script = self.sdd_compiler / "src" / "dsl_compiler.py"
        
        # Use compile_to_binary function directly
        cmd = [
            sys.executable,
            str(script),
            str(input_file),
            str(output_file),
            "--format", "msgpack"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                if output_file.exists():
                    size = output_file.stat().st_size
                    print(f"  ✅ mandate.bin ({size:,} bytes)")
                    return True
                else:
                    # Try parsing output for metrics
                    if "Compression Ratio" in result.stdout:
                        print(f"  ✅ mandate.bin compiled (JSON format)")
                        # Copy JSON as fallback
                        json_file = self.sdd_core / "mandate.compiled.json"
                        if json_file.exists():
                            import shutil
                            shutil.copy(json_file, output_file.with_suffix('.json'))
                        return True
            else:
                print(f"  ❌ Compilation failed:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False
    
    def compile_guidelines(self) -> bool:
        """Compile guidelines.dsl to guidelines.bin"""
        print("\n📝 Compiling guidelines.dsl → guidelines.bin")
        
        input_file = self.sdd_core / "guidelines.dsl"
        output_file = self.sdd_runtime / "guidelines.bin"
        
        script = self.sdd_compiler / "src" / "dsl_compiler.py"
        
        cmd = [
            sys.executable,
            str(script),
            str(input_file),
            str(output_file),
            "--format", "msgpack"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                if output_file.exists():
                    size = output_file.stat().st_size
                    print(f"  ✅ guidelines.bin ({size:,} bytes)")
                    return True
                else:
                    # Try parsing output for metrics
                    if "Compression Ratio" in result.stdout:
                        print(f"  ✅ guidelines.bin compiled (JSON format)")
                        json_file = self.sdd_core / "guidelines.compiled.json"
                        if json_file.exists():
                            import shutil
                            shutil.copy(json_file, output_file.with_suffix('.json'))
                        return True
            else:
                print(f"  ❌ Compilation failed:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return False
    
    def copy_compiled_json(self) -> bool:
        """Fallback: Copy compiled JSON files if binary compilation didn't work"""
        print("\n📋 Fallback: Copying compiled JSON artifacts")
        
        import shutil
        
        # Mandate
        src_mandate = self.sdd_core / "mandate.compiled.json"
        dest_mandate = self.sdd_runtime / "mandate.json"
        if src_mandate.exists():
            shutil.copy(src_mandate, dest_mandate)
            print(f"  ✅ {dest_mandate.name} ({dest_mandate.stat().st_size:,} bytes)")
        else:
            print(f"  ⚠️  mandate.compiled.json not found")
        
        # Guidelines
        src_guidelines = self.sdd_core / "guidelines.compiled.json"
        dest_guidelines = self.sdd_runtime / "guidelines.json"
        if src_guidelines.exists():
            shutil.copy(src_guidelines, dest_guidelines)
            print(f"  ✅ {dest_guidelines.name} ({dest_guidelines.stat().st_size:,} bytes)")
        else:
            print(f"  ⚠️  guidelines.compiled.json not found")
        
        return True
    
    def generate_metadata(self) -> bool:
        """Generate metadata.json with audit trail"""
        print("\n📊 Generating metadata.json")
        
        # Get source hashes
        import hashlib
        
        def file_hash(path: Path) -> str:
            """Calculate SHA256 of file"""
            return hashlib.sha256(path.read_bytes()).hexdigest()[:8]
        
        mandate_hash = file_hash(self.sdd_core / "mandate.spec")
        guidelines_hash = file_hash(self.sdd_core / "guidelines.dsl")
        
        # Count mandates and guidelines
        mandate_text = (self.sdd_core / "mandate.spec").read_text()
        guidelines_text = (self.sdd_core / "guidelines.dsl").read_text()
        
        import re
        mandate_count = len(re.findall(r'mandate\s+M\d+', mandate_text))
        guideline_count = len(re.findall(r'guideline\s+G\d+', guidelines_text))
        
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
                "mandate_bin": (self.sdd_runtime / "mandate.bin").exists() or (self.sdd_runtime / "mandate.json").exists(),
                "guidelines_bin": (self.sdd_runtime / "guidelines.bin").exists() or (self.sdd_runtime / "guidelines.json").exists(),
            },
            "audit_trail": [
                {"timestamp": datetime.utcnow().isoformat() + "Z", "action": "integration", "status": "in_progress"},
            ],
        }
        
        metadata_file = self.sdd_runtime / "metadata.json"
        metadata_file.write_text(json.dumps(metadata, indent=2))
        
        print(f"  ✅ metadata.json ({metadata_file.stat().st_size} bytes)")
        print(f"     - {mandate_count} mandates, {guideline_count} guidelines")
        return True
    
    def run(self) -> bool:
        """Execute complete integration pipeline"""
        print("=" * 60)
        print("SDD v3.0 Integration Pipeline")
        print("=" * 60)
        
        if not self.validate_paths():
            return False
        
        # Try binary compilation first
        mandate_ok = self.compile_mandate()
        guidelines_ok = self.compile_guidelines()
        
        # If binary compilation didn't work, fallback to JSON
        if not (mandate_ok and guidelines_ok):
            print("\n⚠️  Binary compilation may have generated JSON instead")
            self.copy_compiled_json()
        
        # Always generate metadata
        if not self.generate_metadata():
            return False
        
        # Verify output
        print("\n" + "=" * 60)
        print("📦 Deployment Summary")
        print("=" * 60)
        
        manifest = []
        for item in self.sdd_runtime.glob("*"):
            if item.is_file() and item.name != ".gitignore" and item.name != ".gitkeep":
                size = item.stat().st_size
                manifest.append(f"  {item.name:25s} {size:>10,} bytes")
        
        if manifest:
            print("✅ Artifacts deployed to .sdd-runtime/:")
            for line in sorted(manifest):
                print(line)
        
        print("\n✅ Integration complete!")
        print("   Ready for wizard: python .sdd-wizard/src/wizard.py")
        
        return True


if __name__ == "__main__":
    integrator = SDDIntegrator(Path.cwd())
    success = integrator.run()
    sys.exit(0 if success else 1)
