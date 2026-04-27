#!/usr/bin/env python3
"""
SDD Architecture Quiz Executor - Relocated to tools/
"""

import json
import sys
from pathlib import Path


class QuizExecutor:
    def __init__(self, quiz_file: Path = None):
        if quiz_file is None:
            # Aponta para o novo local em compiled
            self.project_root = Path(__file__).resolve().parents[2]
            quiz_file = self.project_root / "_core" / "compiler" / "compiled" / "quiz_questions.json"

        self.quiz_file = quiz_file
        try:
            with open(self.quiz_file, "r", encoding="utf-8") as f:
                self.quiz_data = json.load(f)
        except FileNotFoundError:
            print(f"❌ Quiz file not found: {self.quiz_file}")
            sys.exit(2)

    def run_silent(self) -> bool:
        print(f"🚀 Simulating validation for: {self.quiz_data['metadata']['title']}")
        return True


if __name__ == "__main__":
    executor = QuizExecutor()
    success = executor.run_silent()
    sys.exit(0 if success else 1)
