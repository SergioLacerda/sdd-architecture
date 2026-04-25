#!/usr/bin/env python3
"""
Interactive mode for SDD Wizard v3 - Phase-based template generation

3-phase flow:
1. Phase 1: Generate markdown templates with status fields
2. Phase 2: Manual user customization (instructions only)
3. Phase 3: Compile templates
"""

import sys
from pathlib import Path
from datetime import datetime


class InteractiveWizard:
    """Interactive guide for SDD Wizard v3"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
    
    def print_header(self, title: str, icon: str = "🧙"):
        """Print formatted header"""
        print(f"\n{icon} {title}")
        print("=" * 70)
    
    def show_phase_menu(self) -> str:
        """Show menu to choose which phase to start at"""
        self.print_header("SDD Wizard v3 - Choose Starting Phase", "🧙")
        print(f"\nStarted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        print("""Which phase would you like to run?

  [1] Phase 1: Generate governance templates
              (Creates Markdown files with status fields)
              ✅ Use this if you're starting fresh

  [2] Phase 2: How to customize templates
              (Shows step-by-step instructions)
              ✅ Use this for guidance on editing

  [3] Phase 3: Compile your choices
              (Processes YAML to final governance)
              ✅ Use this if Phase 2 is done
""")
        
        choice = input("Select phase (1-3): ").strip()
        return choice
    
    def phase_1_generate_templates(self) -> bool:
        """Execute Phase 1: Generate templates"""
        self.print_header("PHASE 1: Generate Governance Templates", "📝")
        
        try:
            from orchestration.phase_wizard_v3 import Phase1Generator
            
            # Adjust repo_root if we're inside _core (wizard.sh changes to _core)
            repo_root = self.repo_root
            if repo_root.name == '_core':
                repo_root = repo_root.parent
            
            sdd_core_path = repo_root / '_core'
            output_path = repo_root / '_core' / 'sdd-generated' / 'phase-1-choices'
            
            generator = Phase1Generator(sdd_core_path, output_path, verbose=True)
            result = generator.run()
            
            return result['success']
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def phase_2_show_instructions(self) -> bool:
        """Show Phase 2 instructions"""
        self.print_header("PHASE 2: Customize Your Governance Rules", "📋")
        
        # Adjust repo_root if we're inside _core
        repo_root = self.repo_root
        if repo_root.name == '_core':
            repo_root = repo_root.parent
        
        phase1_path = repo_root / '_core' / 'sdd-generated' / 'phase-1-choices'
        
        print(f"""
You now have governance templates in:
  {phase1_path}

HOW TO CUSTOMIZE:

1. OPEN AND EDIT FILES:
   - mandates-*.md (Hard rules - required by default)
   - guidelines-*.md (Soft rules - customizable)

2. FOR EACH RULE, DECIDE ITS STATUS:
   ├─ required: true  → Keep as mandatory (default)
   ├─ optional: true  → Skip this rule
   └─ custom: true    → Include but customizable

3. CHANGE LINES LIKE:
   FROM: **Status:** `required: true` (Default: include)
   TO:   **Status:** `optional: true` (or custom: true)

4. WHEN DONE EDITING:
   Just save the markdown files! No YAML conversion needed.
   Phase 3 will read your edited files directly.

5. RUN PHASE 3:
   ./wizard.sh → Choose [3] Phase 3
   
   Phase 3 will:
   - Read your edited markdown files
   - Parse the status fields
   - Skip items marked as optional
   - Compile to final governance JSON
   This compiles your YAML to final governance JSON

QUESTION: What's the difference?
- Mandates (M001, M002): Hard rules, cannot be changed → always required
- Guidelines (G01-G150): Soft rules, you decide → required/optional/custom

DEFAULT: Everything starts as REQUIRED
YOUR CHOICE: Change any guideline to optional/custom as needed
""")
        
        input("\nPress ENTER when you've completed Phase 2...")
        return True
    
    def phase_3_compile_templates(self) -> bool:
        """Execute Phase 3: Compile edited templates to governance JSON"""
        self.print_header("PHASE 3: Compile Governance", "⚙️")
        
        # Adjust repo_root if we're inside _core
        repo_root = self.repo_root
        if repo_root.name == '_core':
            repo_root = repo_root.parent
        
        # Phase 3 reads edited markdown from phase-1-choices
        markdown_path = repo_root / '_core' / 'sdd-generated' / 'phase-1-choices'
        
        if not markdown_path.exists():
            print(f"\n❌ Templates not found: {markdown_path}")
            print("\nYou need to:")
            print("1. Run Phase 1 to generate templates")
            print("2. Edit the markdown files (change status fields)")
            print("3. Run Phase 3 to compile")
            return False
        
        try:
            from orchestration.phase_wizard_v3 import Phase3Compiler
            
            output_path = repo_root / '_core' / 'sdd-generated' / 'phase-4-output'
            
            compiler = Phase3Compiler(markdown_path, output_path, repo_root, verbose=True)
            result = compiler.run()
            
            if result['success']:
                print(f"\n✅ Governance compiled successfully!")
                print(f"   Files: {', '.join(result['files'])}")
                print(f"   Location: {result['output_path']}")
                print(f"   Mandates: {result.get('mandates', 0)}, Guidelines: {result.get('guidelines', 0)}")
                return True
            else:
                print(f"\n❌ Failed: {result.get('error', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run(self) -> bool:
        """Main interactive flow"""
        try:
            choice = self.show_phase_menu()
            
            if choice == '1':
                return self.phase_1_generate_templates()
            elif choice == '2':
                return self.phase_2_show_instructions()
            elif choice == '3':
                return self.phase_3_compile_templates()
            else:
                print("\n❌ Invalid choice. Please select 1, 2, or 3.")
                return False
        
        except KeyboardInterrupt:
            print("\n\n❌ Wizard cancelled by user")
            return False
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False


def run_interactive_wizard(repo_root: Path) -> bool:
    """Entry point for interactive wizard"""
    wizard = InteractiveWizard(repo_root)
    return wizard.run()
