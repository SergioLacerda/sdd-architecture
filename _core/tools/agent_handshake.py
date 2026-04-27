#!/usr/bin/env python3
"""
SDD Architecture - Agent Handshake Protocol (AHP) v1.0

Implicit context validation protocol executed before technical responses.

🎯 Design Principles:
- Semantic: Runs only when appropriate (technical context)
- Smart: Caches state, avoids redundant checks
- Agnóstic: Works for any governed system (not SDD-specific)
- Non-intrusive: 3 output modes (silent/compact/verbose)
- State-based: 5-state machine with clear transitions

🧩 4-Layer Validation:
  1. DISCOVERY       → Is governance present?
  2. LINK_VALIDATION → Are connections valid?
  3. RUNTIME         → Is it operational?
  4. GOVERNANCE      → Is it healthy?

🎯 5-State Machine:
  NOT_CONNECTED      → No governance found
  MISCONFIGURED      → Found but broken
  NOT_INITIALIZED    → Found but not setup
  PARTIAL            → Runtime incomplete
  HEALTHY            → Everything OK

Usage:
    from agent_handshake import AgentHandshakeProtocol

    ahp = AgentHandshakeProtocol()
    state, report = ahp.validate(output_mode="compact")
"""

import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple

# ========== DATA MODELS ==========


@dataclass
class ValidationResult:
    """Result of a single validation check"""

    name: str
    passed: bool
    message: str
    layer: str


@dataclass
class HandshakeReport:
    """Complete handshake validation report"""

    state: str  # NOT_CONNECTED | MISCONFIGURED | NOT_INITIALIZED | PARTIAL | HEALTHY
    confidence: float  # 0-100%
    checks: List[Dict]
    actions: List[str]
    cached: bool
    cache_age_seconds: Optional[int]


class AgentHandshakeProtocol:
    """
    Agent Handshake Protocol - Smart context validation engine

    Validates system state before technical operations without being intrusive.
    Caches results to avoid redundant checks and supports 3 output modes.
    """

    # State definitions
    STATES = {
        "NOT_CONNECTED": {"emoji": "❌", "description": "No governance detected"},
        "MISCONFIGURED": {"emoji": "⚠️ ", "description": "Governance broken/invalid"},
        "NOT_INITIALIZED": {"emoji": "⚠️ ", "description": "Setup incomplete (PHASE 0 needed)"},
        "PARTIAL": {"emoji": "🟡", "description": "Runtime incomplete"},
        "HEALTHY": {"emoji": "🟢", "description": "Fully operational"},
    }

    # Recommended actions per state
    ACTIONS = {
        "NOT_CONNECTED": ["proceed_normally"],
        "MISCONFIGURED": ["warn_user", "suggest_review"],
        "NOT_INITIALIZED": ["suggest_phase_0_setup"],
        "PARTIAL": ["suggest_fix"],
        "HEALTHY": ["proceed_silently"],
    }

    def __init__(self, project_root: Optional[Path] = None, cache_ttl_minutes: int = 30):
        """
        Initialize handshake protocol

        Args:
            project_root: Project root directory (auto-detected if None)
            cache_ttl_minutes: Cache validity in minutes
        """
        self.project_root = project_root or self._find_project_root()
        self.cache_dir = self.project_root / ".ai" / "runtime"
        self.cache_file = self.cache_dir / "governance-state.json"
        self.cache_ttl = timedelta(minutes=cache_ttl_minutes)

        self.validation_results = []
        self.current_state = "NOT_CONNECTED"
        self.current_confidence = 0.0

    def _find_project_root(self) -> Path:
        """Find project root directory"""
        current = Path.cwd()
        if current.name == "_core":
            return current.parent

        for parent in [current] + list(current.parents):
            if (parent / "_core").exists():
                return parent

        return current

    # ========== SEMANTIC TRIGGERING ==========

    def should_run_handshake(self, user_input: str) -> bool:
        """
        Detect if user input is technical/contextual

        Returns True if handshake should run automatically
        """
        if not user_input:
            return False

        input_lower = user_input.lower()

        # Keywords that trigger handshake
        technical_keywords = [
            # Direct queries
            "estou conectado",
            "connected",
            "status",
            "health",
            "handshake",
            "verificar",
            "validate",
            # Project references
            "código",
            "code",
            "arquivo",
            "file",
            "implementar",
            "implement",
            "arquitetura",
            "architecture",
            "estrutura",
            "structure",
            "projeto",
            "project",
            # System references
            ".sdd",
            "governance",
            "mandates",
            "guidelines",
            "spec",
            "fase",
            "phase",
            "wizard",
            # Config references
            ".vscode",
            ".cursor",
            ".ia",
            ".github",
        ]

        # Keywords that suppress handshake (casual conversation)
        # Use longer/more specific phrases to avoid false positives
        casual_keywords = [
            "oi",
            "olá",
            "hello world",
            "hi there",
            "obrigado",
            "thanks for",
            "muito legal",
            "pretty cool",
            "que legal",
            "muito nice",
            "como você está",
            "how are you",
            "qual seu nome",
            "your name",
            "qual é seu nome",
            "piada",
            "joke",
            "meme",
            "funny",
        ]

        # Check casual first (suppress if present)
        # Use stricter matching to avoid false positives with embedded words
        for casual_kw in casual_keywords:
            # Match if it's a standalone phrase or at word boundaries
            if casual_kw in input_lower:
                # Additional check: make sure it's not part of a technical word
                # Simple heuristic: if input is mostly punctuation/code, it's technical
                if not any(tech_kw in input_lower for tech_kw in [".sdd", ".vscode", ".cursor", "-architecture", "-project"]):
                    if len(casual_kw.split()) > 1 or casual_kw in [" oi ", " olá ", " hi ", "obrigado"]:
                        return False

        # Trigger if technical keyword found
        return any(kw in input_lower for kw in technical_keywords)

    # ========== 4-LAYER VALIDATION ==========

    def _layer_1_discovery(self) -> Tuple[str, List[ValidationResult]]:
        """
        Layer 1: DISCOVERY - Is governance present?

        Checks for:
        - .spec.config exists
        - SDD structure detected
        - Governance config readable

        Returns: (state, results)
        """
        results = []

        # Check .spec.config
        spec_config_path = self.project_root / ".spec.config"
        spec_config_exists = spec_config_path.exists()
        results.append(
            ValidationResult(
                name=".spec.config",
                passed=spec_config_exists,
                message=f"Found at {spec_config_path}" if spec_config_exists else "Not found",
                layer="DISCOVERY",
            )
        )

        # Check .sdd structure
        dir = self.project_root / ".sdd"
        exists = dir.exists()
        results.append(
            ValidationResult(
                name=".sdd/ directory",
                passed=exists or True,  # Optional
                message="Found" if exists else "Not initialized (optional)",
                layer="DISCOVERY",
            )
        )

        # Check governance-core.json
        governance_path = self.project_root / "compiler" / "compiled" / "governance-core.json"
        governance_exists = governance_path.exists()
        results.append(
            ValidationResult(
                name="governance files",
                passed=governance_exists or True,  # Optional
                message="Found" if governance_exists else "Not compiled (optional)",
                layer="DISCOVERY",
            )
        )

        # Determine layer state
        if spec_config_exists:
            layer_state = "CONNECTED"
        else:
            layer_state = "NOT_CONNECTED"

        return layer_state, results

    def _layer_2_link_validation(self) -> Tuple[str, List[ValidationResult]]:
        """
        Layer 2: LINK VALIDATION - Are connections valid?

        Checks for:
        - spec_path points to valid location
        - Framework accessible
        - Config parseable

        Returns: (state, results)
        """
        results = []

        spec_config_path = self.project_root / ".spec.config"

        # Check if config is readable
        config_readable = False
        config_path_valid = False

        if spec_config_path.exists():
            try:
                with open(spec_config_path, "r") as f:
                    config_data = json.load(f)
                config_readable = True

                # Check if spec_path in config is valid
                spec_path = config_data.get("spec_path")
                if spec_path:
                    spec_target = self.project_root / spec_path
                    config_path_valid = spec_target.exists()
            except Exception:
                config_readable = False

        results.append(
            ValidationResult(
                name="spec config readable",
                passed=config_readable,
                message="Config parses correctly" if config_readable else "Config invalid or missing",
                layer="LINK_VALIDATION",
            )
        )

        results.append(
            ValidationResult(
                name="spec_path valid",
                passed=config_path_valid or not spec_config_path.exists(),  # Optional if no config
                message="Points to valid location" if config_path_valid else "Invalid path (optional)",
                layer="LINK_VALIDATION",
            )
        )

        # Check core framework accessible
        core_accessible = (self.project_root / "_core").exists()
        results.append(
            ValidationResult(
                name="_core framework",
                passed=core_accessible or True,  # Optional
                message="Framework accessible" if core_accessible else "Not found (optional)",
                layer="LINK_VALIDATION",
            )
        )

        # Determine layer state
        if config_readable and config_path_valid:
            layer_state = "LINK_OK"
        elif spec_config_path.exists():
            layer_state = "BROKEN_LINK"
        else:
            layer_state = "NO_CONFIG"

        return layer_state, results

    def _layer_3_runtime_validation(self) -> Tuple[str, List[ValidationResult]]:
        """
        Layer 3: RUNTIME VALIDATION - Is it operational?

        Checks for:
        - .ai/runtime/ exists
        - State files present
        - PHASE 0 executed

        Returns: (state, results)
        """
        results = []

        # Check .ai/runtime/
        runtime_dir = self.project_root / ".ai" / "runtime"
        runtime_exists = runtime_dir.exists()
        results.append(
            ValidationResult(
                name=".ai/runtime/",
                passed=runtime_exists or True,  # Optional
                message="Initialized" if runtime_exists else "Not initialized",
                layer="RUNTIME_VALIDATION",
            )
        )

        # Check governance-state.json
        state_file = runtime_dir / "governance-state.json" if runtime_dir.exists() else None
        state_file_exists = state_file and state_file.exists()
        results.append(
            ValidationResult(
                name="state cache",
                passed=state_file_exists or True,  # Optional
                message="Cache initialized" if state_file_exists else "Cache not created",
                layer="RUNTIME_VALIDATION",
            )
        )

        # Check for PHASE 0 marker
        phase_0_marker = runtime_dir / ".phase-0-complete" if runtime_dir.exists() else None
        phase_0_done = phase_0_marker and phase_0_marker.exists()
        results.append(
            ValidationResult(
                name="PHASE 0 setup",
                passed=phase_0_done or True,  # Optional
                message="Completed" if phase_0_done else "Not run yet",
                layer="RUNTIME_VALIDATION",
            )
        )

        # Determine layer state
        if phase_0_done and state_file_exists:
            layer_state = "READY"
        elif runtime_exists:
            layer_state = "PARTIAL"
        else:
            layer_state = "NOT_INITIALIZED"

        return layer_state, results

    def _layer_4_governance_health(self) -> Tuple[str, List[ValidationResult]]:
        """
        Layer 4: GOVERNANCE HEALTH - Is it healthy?

        Checks for:
        - Minimum governance items present
        - Structural coherence
        - No critical gaps

        Returns: (state, results)
        """
        results = []

        # Check governance-core.json integrity
        governance_path = self.project_root / "_core" / "compiler" / "compiled" / "governance-core.json"
        governance_valid = False
        governance_items = 0

        if governance_path.exists():
            try:
                with open(governance_path, "r") as f:
                    gov_data = json.load(f)
                governance_valid = True
                governance_items = len(gov_data.get("items", []))
            except Exception:
                governance_valid = False

        results.append(
            ValidationResult(
                name="governance integrity",
                passed=governance_valid or True,  # Optional
                message=f"Valid ({governance_items} items)" if governance_valid else "Not compiled",
                layer="GOVERNANCE_HEALTH",
            )
        )

        # Check for critical files
        critical_files = ["_core/core", "_core/cli", "_core/wizard", "_core/compiler"]

        critical_present = 0
        for cfile in critical_files:
            if (self.project_root / cfile).exists():
                critical_present += 1

        critical_ok = critical_present >= 2  # At least 2 present
        critical_msg = (
            f"Present ({critical_present}/{len(critical_files)})"
            if critical_ok
            else f"Missing ({critical_present}/{len(critical_files)})"
        )
        results.append(
            ValidationResult(
                name="critical subsystems",
                passed=critical_ok or True,  # Optional
                message=critical_msg,
                layer="GOVERNANCE_HEALTH",
            )
        )

        # Determine layer state
        if governance_valid and critical_ok:
            layer_state = "HEALTHY"
        elif governance_valid or critical_ok:
            layer_state = "DEGRADED"
        else:
            layer_state = "UNKNOWN"

        return layer_state, results

    # ========== STATE MACHINE ==========

    def _compute_final_state(self, l1: str, l2: str, l3: str, l4: str) -> str:
        """
        Compute final system state from 4-layer results

        State priority:
        1. If NOT_CONNECTED in L1 → NOT_CONNECTED
        2. If BROKEN_LINK in L2 → MISCONFIGURED
        3. If NOT_INITIALIZED in L3 → NOT_INITIALIZED
        4. If PARTIAL in any layer → PARTIAL
        5. Otherwise → HEALTHY
        """
        # Priority-based state determination
        if l1 == "NOT_CONNECTED":
            return "NOT_CONNECTED"

        if l2 == "BROKEN_LINK":
            return "MISCONFIGURED"

        if l3 == "NOT_INITIALIZED":
            return "NOT_INITIALIZED"

        if "PARTIAL" in [l1, l2, l3, l4]:
            return "PARTIAL"

        return "HEALTHY"

    def _compute_confidence(self, all_results: List[ValidationResult]) -> float:
        """
        Compute confidence score (0-100%)

        Score = (passed_checks / total_checks) * 100
        """
        if not all_results:
            return 0.0

        passed = sum(1 for r in all_results if r.passed)
        total = len(all_results)
        return (passed / total) * 100

    # ========== PERSISTENCE ==========

    def _load_cache(self) -> Optional[Dict]:
        """Load cached state if valid"""
        if not self.cache_file.exists():
            return None

        try:
            with open(self.cache_file, "r") as f:
                cache = json.load(f)

            # Check cache age
            last_check = datetime.fromisoformat(cache.get("last_check", ""))
            age = datetime.now() - last_check

            if age < self.cache_ttl:
                return cache
        except Exception:
            pass

        return None

    def _save_cache(self, state: str, checks: List[Dict], confidence: float):
        """Save state to persistent cache"""
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

            cache = {
                "state": state,
                "confidence": round(confidence, 1),
                "last_check": datetime.now().isoformat(),
                "checks": checks,
            }

            with open(self.cache_file, "w") as f:
                json.dump(cache, f, indent=2)
        except Exception:
            pass  # Silently fail if cache write fails

    # ========== PUBLIC API ==========

    def validate(
        self, output_mode: Literal["silent", "compact", "verbose"] = "compact", force_recheck: bool = False
    ) -> Tuple[str, HandshakeReport]:
        """
        Execute full handshake protocol

        Args:
            output_mode: "silent" (minimal), "compact" (summary), "verbose" (detailed)
            force_recheck: Force revalidation even if cached

        Returns:
            (state, report) tuple
        """
        # Try cache first
        if not force_recheck:
            cache = self._load_cache()
            if cache:
                report = HandshakeReport(
                    state=cache["state"],
                    confidence=cache["confidence"],
                    checks=[],
                    actions=self.ACTIONS.get(cache["state"], []),
                    cached=True,
                    cache_age_seconds=int((datetime.now() - datetime.fromisoformat(cache["last_check"])).total_seconds()),
                )
                return cache["state"], report

        # Run 4-layer validation
        l1_state, l1_results = self._layer_1_discovery()
        l2_state, l2_results = self._layer_2_link_validation()
        l3_state, l3_results = self._layer_3_runtime_validation()
        l4_state, l4_results = self._layer_4_governance_health()

        all_results = l1_results + l2_results + l3_results + l4_results

        # Compute final state
        final_state = self._compute_final_state(l1_state, l2_state, l3_state, l4_state)
        confidence = self._compute_confidence(all_results)

        # Convert results to dicts
        checks = [asdict(r) for r in all_results]

        # Save to cache
        self._save_cache(final_state, checks, confidence)

        # Build report
        report = HandshakeReport(
            state=final_state,
            confidence=round(confidence, 1),
            checks=checks,
            actions=self.ACTIONS.get(final_state, []),
            cached=False,
            cache_age_seconds=None,
        )

        return final_state, report

    # ========== OUTPUT FORMATTING ==========

    def _format_compact_output(
        self,
        state: str,
        emoji: str,
        report: HandshakeReport,
    ) -> str:
        output = f"\n🧠 SDD STATUS\nState: {emoji} {state}\n"
        for check in report.checks:
            symbol = "✔" if check["passed"] else "✖"
            output += f"  {symbol} {check['name']}\n"
        if report.actions:
            output += f"\nActions: → {', '.join(report.actions)}\n"
        return output

    def _group_checks_by_layer(self, report: HandshakeReport) -> Dict[str, List[Dict]]:
        by_layer: Dict[str, List[Dict]] = {}
        for check in report.checks:
            layer = check["layer"]
            if layer not in by_layer:
                by_layer[layer] = []
            by_layer[layer].append(check)
        return by_layer

    def _format_verbose_output(
        self,
        state: str,
        emoji: str,
        report: HandshakeReport,
    ) -> str:
        output = "\n" + "=" * 60 + "\n"
        output += "🧠 SDD STATUS REPORT\n"
        output += f"State: {emoji} {state}\n"
        output += f"Confidence: {report.confidence}%\n"
        output += "=" * 60 + "\n\n"

        by_layer = self._group_checks_by_layer(report)
        for layer in ["DISCOVERY", "LINK_VALIDATION", "RUNTIME_VALIDATION", "GOVERNANCE_HEALTH"]:
            if layer in by_layer:
                output += f"📍 {layer}\n"
                for check in by_layer[layer]:
                    symbol = "✅" if check["passed"] else "❌"
                    output += f"  {symbol} {check['name']}: {check['message']}\n"
                output += "\n"

        if report.cached:
            output += f"💾 Cached ({report.cache_age_seconds}s old)\n"

        if report.actions:
            output += "\n🎯 Recommended Actions:\n"
            for action in report.actions:
                output += f"  → {action}\n"

        output += "=" * 60 + "\n"
        return output

    def format_output(
        self, state: str, report: HandshakeReport, mode: Literal["silent", "compact", "verbose"] = "compact"
    ) -> str:
        """Format handshake result for display."""
        state_info = self.STATES.get(state, {})
        emoji = state_info.get("emoji", "❓")

        if mode == "silent":
            return f"🧠 SDD: {emoji}"
        if mode == "compact":
            return self._format_compact_output(state, emoji, report)
        if mode == "verbose":
            return self._format_verbose_output(state, emoji, report)
        return self._format_compact_output(state, emoji, report)


def main():
    """Main entry point for CLI usage"""
    import argparse

    parser = argparse.ArgumentParser(description="Agent Handshake Protocol - Smart context validation")
    parser.add_argument("--mode", choices=["silent", "compact", "verbose"], default="compact", help="Output mode")
    parser.add_argument("--force", action="store_true", help="Force recheck (skip cache)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    ahp = AgentHandshakeProtocol()
    state, report = ahp.validate(output_mode=args.mode, force_recheck=args.force)

    if args.json:
        data = {
            "state": state,
            "confidence": report.confidence,
            "checks": report.checks,
            "actions": report.actions,
            "cached": report.cached,
        }
        print(json.dumps(data, indent=2))
    else:
        print(ahp.format_output(state, report, mode=args.mode))

    return 0 if state == "HEALTHY" else (1 if state == "NOT_CONNECTED" else 2)


if __name__ == "__main__":
    sys.exit(main())
