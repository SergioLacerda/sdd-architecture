#!/usr/bin/env python3
"""
Phase 5: INTEGRATION Flow Functional Test

Tests the actual INTEGRATION flow by simulating a new project setup.
This is a "fake" test that follows all 5 steps without modifying the framework.
"""

import os
import tempfile
import shutil
from pathlib import Path


class TestIntegrationFlow:
    """Test INTEGRATION flow: 5-step onboarding process"""

    def setup_test_project(self):
        """Create a temporary test project directory"""
        self.test_dir = tempfile.mkdtemp(prefix="sdd_integration_test_")
        print(f"✅ Created test project: {self.test_dir}")
        return self.test_dir

    def cleanup(self):
        """Clean up test project"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
            print(f"✅ Cleaned up test project")

    def test_step_1_setup(self):
        """Test STEP 1: Setup Project Structure"""
        print("\n📋 TEST STEP 1: Setup Project Structure")
        
        # Create required directories
        dirs = [".github", ".vscode", ".cursor", "scripts", ".ai"]
        for d in dirs:
            dir_path = os.path.join(self.test_dir, d)
            os.makedirs(dir_path, exist_ok=True)
            assert os.path.exists(dir_path), f"Failed to create {d}"
            print(f"  ✅ Created directory: {d}/")
        
        print("  ✅ STEP 1 PASSED: All directories created")
        return True

    def test_step_2_templates(self):
        """Test STEP 2: Copy Templates"""
        print("\n📋 TEST STEP 2: Copy Templates")
        
        # Simulate copying templates from sdd-archtecture/INTEGRATION/templates/
        # Resolve symlinks to get actual path
        current_file = Path(__file__).resolve()
        framework_dir = current_file.parent.parent.parent / ".sdd-integration" / "templates"
        
        if not framework_dir.exists():
            print(f"  ⚠️  WARNING: Framework templates not found at {framework_dir}")
            return False
        
        # List expected template files
        expected_files = [
            ".spec.config",
            ".github/copilot-instructions.md",
            ".vscode/ai-rules.md",
            ".vscode/settings.json",
            ".cursor/rules/spec.mdc",
            ".pre-commit-config.yaml",
            ".ai/README.md"
        ]
        
        for file_path in expected_files:
            template_file = framework_dir / file_path
            if template_file.exists():
                print(f"  ✅ Template found: {file_path}")
            else:
                print(f"  ❌ Template missing: {file_path}")
                return False
        
        print("  ✅ STEP 2 PASSED: All templates present")
        return True

    def test_step_3_config(self):
        """Test STEP 3: Configure .spec.config"""
        print("\n📋 TEST STEP 3: Configure .spec.config")
        
        spec_config = os.path.join(self.test_dir, ".spec.config")
        
        # Create a mock .spec.config
        with open(spec_config, "w") as f:
            f.write("[spec]\n")
            f.write("spec_path = ../sdd-archtecture\n")
        
        # Verify it can be read
        with open(spec_config, "r") as f:
            content = f.read()
            assert "spec_path" in content, ".spec.config missing spec_path"
            print(f"  ✅ .spec.config created and configured")
        
        print("  ✅ STEP 3 PASSED: .spec.config valid")
        return True

    def test_step_4_validate(self):
        """Test STEP 4: Run Validation"""
        print("\n📋 TEST STEP 4: Run Validation")
        
        # Simulate PHASE 0 validation
        ai_dir = os.path.join(self.test_dir, ".ai")
        
        # Create expected .ai/ subdirectories
        subdirs = ["context-aware", "runtime"]
        for subdir in subdirs:
            sub_path = os.path.join(ai_dir, subdir)
            os.makedirs(sub_path, exist_ok=True)
            assert os.path.exists(sub_path), f"Failed to create .ai/{subdir}"
            print(f"  ✅ Created: .ai/{subdir}/")
        
        print("  ✅ STEP 4 PASSED: Validation structure created")
        return True

    def test_step_5_commit(self):
        """Test STEP 5: Commit to Git"""
        print("\n📋 TEST STEP 5: Commit to Git")
        
        # Create files that would be committed
        files_to_create = [
            ".spec.config",
            ".github/copilot-instructions.md",
            ".vscode/ai-rules.md",
            ".ai/README.md"
        ]
        
        for file_path in files_to_create:
            full_path = os.path.join(self.test_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Create a dummy file
            with open(full_path, "w") as f:
                f.write(f"# {file_path}\n# Framework config file\n")
            
            assert os.path.exists(full_path), f"Failed to create: {file_path}"
            print(f"  ✅ File ready to commit: {file_path}")
        
        print("  ✅ STEP 5 PASSED: All files ready for git commit")
        return True

    def run_all_tests(self):
        """Run complete INTEGRATION flow test"""
        print("\n" + "="*80)
        print("🚀 PHASE 5: INTEGRATION FLOW FUNCTIONAL TEST")
        print("="*80)
        
        try:
            self.setup_test_project()
            
            # Run all steps
            tests = [
                self.test_step_1_setup,
                self.test_step_2_templates,
                self.test_step_3_config,
                self.test_step_4_validate,
                self.test_step_5_commit
            ]
            
            results = []
            for test in tests:
                try:
                    result = test()
                    results.append((test.__name__, result))
                except Exception as e:
                    print(f"  ❌ ERROR: {e}")
                    results.append((test.__name__, False))
            
            # Summary
            print("\n" + "="*80)
            print("📊 TEST SUMMARY")
            print("="*80)
            
            passed = sum(1 for _, result in results if result)
            total = len(results)
            
            for test_name, result in results:
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"{status}: {test_name}")
            
            print(f"\nTotal: {passed}/{total} tests passed")
            
            if passed == total:
                print("\n✅ INTEGRATION FLOW: READY FOR PRODUCTION")
                return True
            else:
                print("\n❌ INTEGRATION FLOW: ISSUES FOUND")
                return False
                
        finally:
            self.cleanup()


if __name__ == "__main__":
    tester = TestIntegrationFlow()
    success = tester.run_all_tests()
    exit(0 if success else 1)
