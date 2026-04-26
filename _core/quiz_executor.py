#!/usr/bin/env python3
"""
SDD Architecture Quiz Executor
===============================

Interactive quiz runner for SDD Architecture foundational knowledge assessment.
Validates understanding of governance, seedlings, phases, health checks, and AI integration.

Usage:
    python quiz_executor.py                 # Interactive mode (default)
    python quiz_executor.py --mode=silent   # Silent mode (no feedback)
    python quiz_executor.py --mode=verbose  # Verbose mode (detailed explanations)
    python quiz_executor.py --json          # JSON output mode
    python quiz_executor.py --random        # Randomize question order
    python quiz_executor.py --topic=governance  # Filter by topic

Features:
    ✓ 12 questions covering 6 topics
    ✓ Multiple difficulty levels (easy/medium/hard)
    ✓ 70% pass threshold
    ✓ Detailed feedback and explanations
    ✓ Score tracking and analysis
    ✓ JSON export for CI/CD integration
    ✓ Topic filtering
    ✓ Random question ordering

Exit Codes:
    0 = PASS (≥70%)
    1 = FAIL (<70%)
    2 = ERROR (invalid input/file)
"""

import json
import sys
import random
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import argparse
from datetime import datetime


@dataclass
class QuizQuestion:
    """Represents a single quiz question"""
    id: int
    topic: str
    difficulty: str
    question: str
    options: List[str]
    correct_answer: int
    explanation: str


@dataclass
class QuizResult:
    """Represents quiz completion result"""
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    score_percentage: float
    passed: bool
    pass_threshold: int
    topics_covered: Dict[str, int]
    difficulty_breakdown: Dict[str, int]
    answered_questions: List[Dict]
    timestamp: str


class QuizExecutor:
    """Manages quiz execution, scoring, and feedback"""

    def __init__(self, quiz_file: Path = None):
        """Initialize quiz executor"""
        if quiz_file is None:
            quiz_file = Path(__file__).parent / "quiz_questions.json"
        
        self.quiz_file = quiz_file
        self.quiz_data = self._load_quiz()
        self.questions: List[QuizQuestion] = []
        self._parse_questions()
        
    def _load_quiz(self) -> Dict:
        """Load quiz from JSON file"""
        try:
            with open(self.quiz_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Quiz file not found: {self.quiz_file}")
            sys.exit(2)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in quiz file: {e}")
            sys.exit(2)

    def _parse_questions(self):
        """Parse questions from quiz data"""
        for q in self.quiz_data.get('questions', []):
            self.questions.append(QuizQuestion(
                id=q['id'],
                topic=q['topic'],
                difficulty=q['difficulty'],
                question=q['question'],
                options=q['options'],
                correct_answer=q['correct_answer'],
                explanation=q['explanation']
            ))

    def filter_by_topic(self, topic: str) -> List[QuizQuestion]:
        """Filter questions by topic"""
        return [q for q in self.questions if q.topic == topic]

    def filter_by_difficulty(self, difficulty: str) -> List[QuizQuestion]:
        """Filter questions by difficulty"""
        return [q for q in self.questions if q.difficulty == difficulty]

    def run_interactive(
        self,
        questions: List[QuizQuestion] = None,
        verbose: bool = False
    ) -> QuizResult:
        """Run interactive quiz mode"""
        if questions is None:
            questions = self.questions

        print("\n" + "="*60)
        print("🧠 SDD Architecture Foundation Quiz")
        print("="*60)
        print(f"Total Questions: {len(questions)}")
        print(f"Pass Threshold: {self.quiz_data['metadata']['pass_threshold']}%")
        print(f"Topics: {', '.join(set(q.topic for q in questions))}")
        print("="*60 + "\n")

        answered_questions = []
        correct_count = 0

        for idx, question in enumerate(questions, 1):
            print(f"\n[{idx}/{len(questions)}] {question.question}")
            print(f"Difficulty: {question.difficulty} | Topic: {question.topic}\n")

            # Display options
            for opt_idx, option in enumerate(question.options, 1):
                print(f"  {opt_idx}. {option}")

            # Get user answer
            while True:
                try:
                    user_input = input("\nYour answer (1-4): ").strip()
                    answer_idx = int(user_input) - 1
                    
                    if 0 <= answer_idx < len(question.options):
                        break
                    else:
                        print("❌ Invalid option. Please choose 1-4.")
                except ValueError:
                    print("❌ Invalid input. Please enter a number 1-4.")

            # Check answer
            is_correct = answer_idx == question.correct_answer
            if is_correct:
                correct_count += 1
                print("✅ Correct!")
            else:
                print(f"❌ Incorrect. The correct answer is: {question.options[question.correct_answer]}")

            if verbose:
                print(f"\n📖 Explanation: {question.explanation}")

            answered_questions.append({
                'id': question.id,
                'question': question.question,
                'user_answer': answer_idx,
                'correct_answer': question.correct_answer,
                'correct': is_correct,
                'topic': question.topic,
                'difficulty': question.difficulty
            })

        # Calculate results
        return self._calculate_result(
            questions,
            correct_count,
            answered_questions
        )

    def run_silent(
        self,
        questions: List[QuizQuestion] = None,
    ) -> QuizResult:
        """Run quiz in silent mode (automated, no user interaction)"""
        if questions is None:
            questions = self.questions

        answered_questions = []
        correct_count = 0

        for question in questions:
            # Simulate random answer selection for testing
            user_answer = random.randint(0, len(question.options) - 1)
            is_correct = user_answer == question.correct_answer
            
            if is_correct:
                correct_count += 1

            answered_questions.append({
                'id': question.id,
                'question': question.question,
                'user_answer': user_answer,
                'correct_answer': question.correct_answer,
                'correct': is_correct,
                'topic': question.topic,
                'difficulty': question.difficulty
            })

        return self._calculate_result(questions, correct_count, answered_questions)

    def _calculate_result(
        self,
        questions: List[QuizQuestion],
        correct_count: int,
        answered_questions: List[Dict]
    ) -> QuizResult:
        """Calculate quiz results"""
        total = len(questions)
        incorrect_count = total - correct_count
        percentage = (correct_count / total * 100) if total > 0 else 0
        pass_threshold = self.quiz_data['metadata']['pass_threshold']
        passed = percentage >= pass_threshold

        # Topic breakdown
        topics_covered = {}
        for q in answered_questions:
            topic = q['topic']
            if topic not in topics_covered:
                topics_covered[topic] = {'correct': 0, 'total': 0}
            topics_covered[topic]['total'] += 1
            if q['correct']:
                topics_covered[topic]['correct'] += 1

        # Difficulty breakdown
        difficulty_breakdown = {}
        for q in answered_questions:
            diff = q['difficulty']
            if diff not in difficulty_breakdown:
                difficulty_breakdown[diff] = {'correct': 0, 'total': 0}
            difficulty_breakdown[diff]['total'] += 1
            if q['correct']:
                difficulty_breakdown[diff]['correct'] += 1

        return QuizResult(
            total_questions=total,
            correct_answers=correct_count,
            incorrect_answers=incorrect_count,
            score_percentage=percentage,
            passed=passed,
            pass_threshold=pass_threshold,
            topics_covered=topics_covered,
            difficulty_breakdown=difficulty_breakdown,
            answered_questions=answered_questions,
            timestamp=datetime.now().isoformat()
        )

    def print_result(self, result: QuizResult, verbose: bool = False):
        """Print formatted quiz result"""
        status_symbol = "✅" if result.passed else "❌"
        
        print("\n" + "="*60)
        print(f"{status_symbol} Quiz Results")
        print("="*60)
        print(f"Score: {result.correct_answers}/{result.total_questions} ({result.score_percentage:.1f}%)")
        print(f"Pass Threshold: {result.pass_threshold}%")
        print(f"Status: {'PASSED 🟢' if result.passed else 'FAILED ❌'}")
        print("="*60)

        # Topic breakdown
        print("\n📊 Topic Breakdown:")
        for topic, scores in result.topics_covered.items():
            pct = (scores['correct'] / scores['total'] * 100) if scores['total'] > 0 else 0
            symbol = "✅" if pct >= result.pass_threshold else "❌"
            print(f"  {symbol} {topic}: {scores['correct']}/{scores['total']} ({pct:.0f}%)")

        # Difficulty breakdown
        print("\n📈 Difficulty Breakdown:")
        for diff, scores in result.difficulty_breakdown.items():
            pct = (scores['correct'] / scores['total'] * 100) if scores['total'] > 0 else 0
            print(f"  • {diff}: {scores['correct']}/{scores['total']} ({pct:.0f}%)")

        if verbose:
            print("\n📝 Question Review:")
            for q in result.answered_questions:
                symbol = "✅" if q['correct'] else "❌"
                print(f"  {symbol} Q{q['id']}: {q['topic']}")
                if not q['correct']:
                    print(f"     Your answer: {q['user_answer'] + 1}")
                    print(f"     Correct answer: {q['correct_answer'] + 1}")

        print("\n" + "="*60 + "\n")

    def to_json(self, result: QuizResult) -> str:
        """Convert result to JSON"""
        result_dict = asdict(result)
        result_dict['passed'] = result.passed
        return json.dumps(result_dict, indent=2)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="SDD Architecture Foundation Quiz"
    )
    parser.add_argument(
        '--mode',
        choices=['interactive', 'silent', 'verbose'],
        default='interactive',
        help="Quiz mode (default: interactive)"
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help="Output results in JSON format"
    )
    parser.add_argument(
        '--random',
        action='store_true',
        help="Randomize question order"
    )
    parser.add_argument(
        '--topic',
        type=str,
        help="Filter by topic (governance, seedlings, phases, health-check, architecture, ai-integration)"
    )
    parser.add_argument(
        '--difficulty',
        type=str,
        choices=['easy', 'medium', 'hard'],
        help="Filter by difficulty level"
    )
    parser.add_argument(
        '--list-topics',
        action='store_true',
        help="List available topics and exit"
    )

    args = parser.parse_args()

    # Initialize quiz
    quiz = QuizExecutor()

    # List topics if requested
    if args.list_topics:
        topics = set(q.topic for q in quiz.questions)
        print("\n📚 Available Topics:")
        for topic in sorted(topics):
            questions = quiz.filter_by_topic(topic)
            print(f"  • {topic} ({len(questions)} questions)")
        print()
        sys.exit(0)

    # Filter questions
    questions = quiz.questions
    if args.topic:
        questions = quiz.filter_by_topic(args.topic)
        if not questions:
            print(f"❌ No questions found for topic: {args.topic}")
            sys.exit(2)

    if args.difficulty:
        questions = [q for q in questions if q.difficulty == args.difficulty]
        if not questions:
            print(f"❌ No questions found for difficulty: {args.difficulty}")
            sys.exit(2)

    # Randomize if requested
    if args.random:
        random.shuffle(questions)

    # Run quiz
    if args.mode == 'silent':
        result = quiz.run_silent(questions)
    elif args.mode == 'verbose':
        result = quiz.run_interactive(questions, verbose=True)
    else:  # interactive (default)
        result = quiz.run_interactive(questions, verbose=False)

    # Output result
    if args.json:
        print(quiz.to_json(result))
    else:
        quiz.print_result(result, verbose=args.mode == 'verbose')

    # Exit with appropriate code
    sys.exit(0 if result.passed else 1)


if __name__ == '__main__':
    main()
