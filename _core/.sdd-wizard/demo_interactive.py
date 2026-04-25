#!/usr/bin/env python3
"""
Demonstration of interactive wizard - shows a full walkthrough
with automated inputs for testing/demonstration purposes
"""

import subprocess
import time
from pathlib import Path

def run_interactive_demo():
    """Run interactive wizard with automated inputs"""
    
    # Prepare inputs for the wizard
    # These are the responses to the interactive prompts
    inputs = [
        "",                    # Press ENTER to continue (Step intro)
        "y",                   # Preview mandate.spec? y
        "y",                   # Preview guidelines.dsl? y
        "1",                   # Select language: 1 (python)
        "y",                   # Include M001? y
        "y",                   # Include M002? y
        "",                    # Project output directory (use default)
    ]
    
    # Join inputs with newlines and encode to bytes
    input_text = "\n".join(inputs)
    
    print("=" * 70)
    print("🧙 SDD WIZARD - INTERACTIVE MODE DEMONSTRATION")
    print("=" * 70)
    print()
    print("This script runs the wizard in INTERACTIVE mode with automated inputs.")
    print("Watch how the wizard guides you through project generation!")
    print()
    
    # Run the wizard
    cmd = ["./wizard.sh"]
    try:
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=Path(__file__).parent.parent.parent  # sdd-architecture root
        )
        
        # Send inputs
        output, _ = process.communicate(input=input_text, timeout=120)
        
        print(output)
        
        if process.returncode == 0:
            print()
            print("=" * 70)
            print("✅ WIZARD COMPLETED SUCCESSFULLY!")
            print("=" * 70)
        else:
            print()
            print("=" * 70)
            print(f"❌ Wizard exited with code: {process.returncode}")
            print("=" * 70)
        
    except subprocess.TimeoutExpired:
        process.kill()
        print("❌ Wizard timed out")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_interactive_demo()
