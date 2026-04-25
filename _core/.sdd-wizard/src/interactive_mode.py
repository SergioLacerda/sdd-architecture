#!/usr/bin/env python3
"""
Interactive mode for SDD Wizard v3 - Phase-based template generation

4-phase flow:
1. Phase 1: Generate markdown templates (asks: language, adoption_level)
2. Phase 2: Manual user customization (instructions only)
3. Phase 3: Compile templates
4. Phase 4: Generate project structure
"""

import sys
import json
from pathlib import Path
from datetime import datetime


class InteractiveWizard:
    """Interactive guide for SDD Wizard v3"""
    
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.config = {}
    
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
              (Asks for language & adoption level)
              ✅ Start here or use to reset/regenerate

  [2] Phase 2: How to customize templates
              (Shows step-by-step instructions)
              ✅ Use this for guidance on editing

  [3] Phase 3: Compile governance
              (Reads edited markdown → final JSON)
              ✅ Use after editing Phase 1 output

  [4] Phase 4-6: Generate project structure
              (Creates ready-to-use project output)
              ✅ Use after Phase 3 is complete
""")
        
        choice = input("Select phase (1-4): ").strip()
        return choice
    
    def ask_user_preferences(self) -> dict:
        """Ask user for preferences: language and adoption level"""
        self.print_header("User Preferences Setup", "⚙️")
        
        # Ask for language
        print("""\n1️⃣  Which language would you like examples in?
(This is for code examples only - governance applies to all languages)

  [1] Python
  [2] Java
  [3] TypeScript
""")
        language_choice = input("Select language (1-3): ").strip()
        language_map = {'1': 'Python', '2': 'Java', '3': 'TypeScript'}
        language = language_map.get(language_choice, 'Python')
        print(f"   ✅ Selected: {language}")
        
        # Ask for adoption level
        print(f"""\n2️⃣  What adoption level would you like?

  [1] LITE - Minimal governance
             (Essential guidelines, quick onboarding)
             
  [2] FULL - Complete governance framework
             (All guidelines, comprehensive setup)
""")
        adoption_choice = input("Select adoption level (1-2): ").strip()
        adoption_level = 'LITE' if adoption_choice == '1' else 'FULL'
        print(f"   ✅ Selected: {adoption_level}")
        
        config = {
            'language': language,
            'adoption_level': adoption_level,
            'generated_at': datetime.now().isoformat()
        }
        
        return config
    
    def save_config(self, config: dict) -> Path:
        """Save configuration to wizard-config.json"""
        repo_root = self.repo_root
        if repo_root.name == '_core':
            repo_root = repo_root.parent
        
        config_dir = repo_root / '_core' / 'sdd-generated'
        config_dir.mkdir(parents=True, exist_ok=True)
        
        config_path = config_dir / 'wizard-config.json'
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        return config_path
    
    def phase_1_generate_templates(self) -> bool:
        """Execute Phase 1: Generate templates with user preferences"""
        self.print_header("PHASE 1: Generate Governance Templates", "📝")
        
        try:
            from orchestration.phase_wizard_v3 import Phase1Generator
            
            # Collect user preferences
            config = self.ask_user_preferences()
            self.config = config
            
            # Save config
            config_path = self.save_config(config)
            print(f"\n✅ Configuration saved to: {config_path}")
            
            # Adjust repo_root if we're inside _core (wizard.sh changes to _core)
            repo_root = self.repo_root
            if repo_root.name == '_core':
                repo_root = repo_root.parent
            
            sdd_core_path = repo_root / '_core'
            output_path = repo_root / '_core' / 'sdd-generated' / 'phase-1-choices'
            
            generator = Phase1Generator(sdd_core_path, output_path, verbose=True, config=config)
            result = generator.run()
            
            if result['success']:
                print(f"""
✅ Phase 1 Complete!

📝 Templates generated: {output_path}
   Language: {config.get('language')}
   Adoption: {config.get('adoption_level')}

Next steps:
1. Review markdown files in phase-1-choices/
2. Edit status fields (required/optional/custom)
3. Run Phase 2 for step-by-step instructions
4. Run Phase 3 to compile
5. Run Phase 4 to generate final project
""")
            
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
    
    def phase_4_generate_project(self) -> bool:
        """Execute Phase 4-6: Generate project structure from compiled governance"""
        self.print_header("PHASE 4-6: Generate Project Structure", "🏗️")
        
        try:
            # Adjust repo_root if we're inside _core
            repo_root = self.repo_root
            if repo_root.name == '_core':
                repo_root = repo_root.parent
            
            # Load config from wizard-config.json
            config_path = repo_root / '_core' / 'sdd-generated' / 'wizard-config.json'
            
            if not config_path.exists():
                print(f"\n❌ Configuration not found!")
                print("You must run Phase 1 first to set preferences.")
                return False
            
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Check if Phase 3 completed
            phase3_output = repo_root / '_core' / 'sdd-generated' / 'phase-4-output'
            if not phase3_output.exists():
                print(f"\n❌ Phase 3 output not found!")
                print("You must run Phase 3 first to compile governance.")
                return False
            
            print(f"""
✅ Configuration and Phase 3 output loaded
   Language: {config.get('language', 'Python')}
   Adoption: {config.get('adoption_level', 'FULL')}

Generating project structure...
""")
            
            output_structure = [
                '.sdd/source/',
                '.sdd/runtime/',
                '.sdd/examples/',
                '.vscode/',
                '.cursor/',
                '.ia/'
            ]
            
            print("📁 Structure to be created:\n")
            for item in output_structure:
                print(f"   ✓ {item}")
            
            print(f"""
✅ Phase 4-6 Generation Framework Complete!

📂 Output structure (phase-5-output/):
   .sdd/source/          → mandate.spec, guidelines.dsl (edited)
   .sdd/runtime/         → Dynamic context directories
   .sdd/examples/        → Code examples in {config.get('language')}
   .vscode/              → VS Code settings (copy to project root)
   .cursor/              → Cursor IDE settings (copy to project root)
   .ia/                  → AI agent configuration (copy to project root)

🎉 Your SDD Wizard workflow is ready!
Next: Implement full Phase 4-6 generators
""")
            
            return True
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
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
                print(f"""
✅ Phase 3 Complete!

📊 Compilation results:
   Mandates: {result.get('mandates', 0)}
   Guidelines: {result.get('guidelines', 0)}
   Files: {', '.join(result.get('files', []))}
   Location: {result.get('output_path')}

Next: Run Phase 4 to generate final project structure
""")
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
            elif choice == '4':
                return self.phase_4_generate_project()
            else:
                print("\n❌ Invalid choice. Please select 1, 2, 3, or 4.")
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
