#!/usr/bin/env python3
"""
SDD Architecture - Agent Confidence Evaluator

Evaluates AI agent confidence and safety:
- Model information (if available in context)
- Temperature settings (determinism level)
- Token budget validation
- Response safety markers
- Overall confidence score (0-100%)

Usage:
    python _core/agent_confidence.py [--model=<model>] [--temperature=<0-2>]
"""

import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, Optional, Tuple


class AgentConfidenceEvaluator:
    """Evaluates AI agent confidence and operational safety"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.scores = {}
        self.confidence_score = 0
        self.safety_level = "UNKNOWN"
        self.metrics = {
            "timestamp": datetime.now().isoformat(),
            "evaluations": {},
            "safety_markers": [],
            "risk_factors": [],
            "recommendations": []
        }

    def log(self, message: str):
        """Log message if verbose"""
        if self.verbose:
            print(f"  ℹ️  {message}")

    # ========== EVALUATION METRICS ==========

    def evaluate_model(self, model_name: Optional[str]) -> Tuple[int, str]:
        """
        Evaluate model type for determinism
        
        Scoring:
        - GPT-4/Claude-3-Opus: 95 (most confident)
        - GPT-4-Turbo/Claude-3-Sonnet: 90
        - GPT-3.5-Turbo/Claude-3-Haiku: 80
        - Smaller models: 70
        - Unknown: 60
        """
        if not model_name:
            self.log("No model specified, using neutral score")
            return 60, "Unknown model (neutral confidence)"

        model_lower = model_name.lower()

        # Top-tier models
        if "gpt-4" in model_lower or "gpt4" in model_lower:
            if "turbo" in model_lower or "32k" in model_lower:
                return 90, "GPT-4 Turbo (high confidence)"
            return 95, "GPT-4 (very high confidence)"

        if "claude-3-opus" in model_lower or "claude-opus" in model_lower:
            return 95, "Claude-3-Opus (very high confidence)"

        if "claude-3-sonnet" in model_lower or "claude-sonnet" in model_lower:
            return 90, "Claude-3-Sonnet (high confidence)"

        # Mid-tier
        if "gpt-3.5" in model_lower or "gpt35" in model_lower:
            return 80, "GPT-3.5-Turbo (moderate confidence)"

        if "claude-3-haiku" in model_lower or "claude-haiku" in model_lower:
            return 80, "Claude-3-Haiku (moderate confidence)"

        if "claude-2" in model_lower:
            return 75, "Claude-2 (moderate confidence)"

        # Lower-tier
        if "gemini" in model_lower or "palm" in model_lower:
            return 70, "Smaller model (baseline confidence)"

        return 60, f"Unknown model: {model_name}"

    def evaluate_temperature(self, temperature: Optional[float]) -> Tuple[int, str]:
        """
        Evaluate temperature setting for determinism
        
        Scoring:
        - 0.0 (deterministic): 100
        - 0.0-0.5 (low): 90
        - 0.5-1.0 (moderate): 75
        - 1.0-1.5 (high): 50
        - 1.5-2.0 (very high): 25
        - Unknown: 50
        """
        if temperature is None:
            self.log("Temperature not specified, assuming default (0.7)")
            return 75, "Default temperature (0.7 assumed)"

        if temperature < 0 or temperature > 2:
            return 40, f"Invalid temperature: {temperature} (should be 0.0-2.0)"

        if temperature == 0.0:
            return 100, "Deterministic mode (temperature=0.0)"

        if temperature < 0.5:
            return 90, f"Low randomness (temp={temperature:.1f})"

        if temperature < 1.0:
            return 75, f"Moderate randomness (temp={temperature:.1f})"

        if temperature < 1.5:
            return 50, f"High randomness (temp={temperature:.1f})"

        return 25, f"Very high randomness (temp={temperature:.1f})"

    def evaluate_token_budget(self, max_tokens: Optional[int]) -> Tuple[int, str]:
        """
        Evaluate token budget sufficiency
        
        Scoring:
        - 4000+ tokens: 100
        - 2000-4000: 90
        - 1000-2000: 75
        - 500-1000: 50
        - <500: 25
        - Unknown: 60
        """
        if max_tokens is None:
            self.log("Token budget not specified")
            return 60, "Token budget unknown (neutral)"

        if max_tokens >= 4000:
            return 100, f"Generous budget: {max_tokens} tokens"

        if max_tokens >= 2000:
            return 90, f"Good budget: {max_tokens} tokens"

        if max_tokens >= 1000:
            return 75, f"Moderate budget: {max_tokens} tokens"

        if max_tokens >= 500:
            return 50, f"Limited budget: {max_tokens} tokens"

        return 25, f"Very limited budget: {max_tokens} tokens"

    def evaluate_response_safety(self, response_text: Optional[str]) -> Tuple[int, str]:
        """
        Evaluate response for safety markers
        
        Looks for:
        - Confidence indicators ("confident", "certain", "sure")
        - Uncertainty markers ("uncertain", "might", "could")
        - Error acknowledgment ("error", "failed", "problem")
        """
        if not response_text:
            return 50, "No response text to evaluate"

        text_lower = response_text.lower()

        safe_markers = [
            "confirmed", "verified", "validated",
            "confident", "certain", "sure",
            "completed successfully", "working correctly"
        ]

        risk_markers = [
            "uncertain", "might fail", "could be wrong",
            "not sure", "possibly", "maybe",
            "error", "failed", "problem", "issue",
            "warning", "deprecated", "broken"
        ]

        safe_count = sum(1 for marker in safe_markers if marker in text_lower)
        risk_count = sum(1 for marker in risk_markers if marker in text_lower)

        # Calculate score based on markers
        if risk_count > safe_count:
            score = 40 + (safe_count * 5)
            status = f"Caution detected (risks: {risk_count}, safe: {safe_count})"
        elif safe_count > risk_count:
            score = 75 + (safe_count * 3)
            status = f"Positive indicators (safe: {safe_count})"
        else:
            score = 60
            status = "Neutral safety profile"

        return min(100, score), status

    def evaluate_context_awareness(self, has_sdd_context: bool) -> Tuple[int, str]:
        """
        Evaluate if agent is aware of SDD Architecture context
        
        Scoring:
        - With SDD context loaded: 90
        - Without SDD context: 50
        """
        if has_sdd_context:
            return 90, "Agent has SDD Architecture context loaded"
        return 50, "No SDD context detected (neutral awareness)"

    # ========== ORCHESTRATION ==========

    def evaluate(
        self,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_text: Optional[str] = None,
        has_sdd_context: bool = False
    ) -> Dict[str, Any]:
        """Execute all confidence evaluations"""

        # Run all evaluations
        model_score, model_msg = self.evaluate_model(model)
        temp_score, temp_msg = self.evaluate_temperature(temperature)
        token_score, token_msg = self.evaluate_token_budget(max_tokens)
        safety_score, safety_msg = self.evaluate_response_safety(response_text)
        context_score, context_msg = self.evaluate_context_awareness(has_sdd_context)

        # Store results
        self.metrics["evaluations"] = {
            "model": {"score": model_score, "message": model_msg},
            "temperature": {"score": temp_score, "message": temp_msg},
            "token_budget": {"score": token_score, "message": token_msg},
            "response_safety": {"score": safety_score, "message": safety_msg},
            "context_awareness": {"score": context_score, "message": context_msg}
        }

        # Calculate overall confidence (average)
        all_scores = [model_score, temp_score, token_score, safety_score, context_score]
        self.confidence_score = sum(all_scores) / len(all_scores)

        # Determine safety level
        if self.confidence_score >= 85:
            self.safety_level = "VERY HIGH ✅"
        elif self.confidence_score >= 70:
            self.safety_level = "HIGH ✅"
        elif self.confidence_score >= 55:
            self.safety_level = "MODERATE ⚠️"
        else:
            self.safety_level = "LOW ❌"

        self.metrics["confidence_score"] = round(self.confidence_score, 1)
        self.metrics["safety_level"] = self.safety_level

        return self.metrics

    def print_report(self):
        """Print formatted confidence report"""
        print("\n" + "=" * 60)
        print("🤖 Agent Confidence Evaluation")
        print("=" * 60 + "\n")

        print("📊 Evaluation Results:")
        for eval_name, eval_data in self.metrics["evaluations"].items():
            score = eval_data["score"]
            message = eval_data["message"]
            bar_length = score // 10
            bar = "█" * bar_length + "░" * (10 - bar_length)
            print(f"  {eval_name:20} [{bar}] {score:3}% - {message}")

        print("")
        print(f"🎯 Overall Confidence Score: {self.confidence_score:.1f}%")
        print(f"📈 Safety Level: {self.safety_level}")
        print("")
        print("=" * 60 + "\n")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Evaluate AI agent confidence and safety"
    )
    parser.add_argument(
        "--model",
        help="Model name (e.g., gpt-4, claude-opus)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        help="Temperature setting (0.0-2.0)"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        help="Maximum tokens available"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true"
    )
    parser.add_argument(
        "--json",
        action="store_true"
    )

    args = parser.parse_args()

    evaluator = AgentConfidenceEvaluator(verbose=args.verbose)
    metrics = evaluator.evaluate(
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        has_sdd_context=os.environ.get("SDD_CONTEXT_LOADED") == "true"
    )

    if args.json:
        print(json.dumps(metrics, indent=2))
    else:
        evaluator.print_report()

    return 0


if __name__ == "__main__":
    sys.exit(main())
