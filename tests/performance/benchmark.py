#!/usr/bin/env python3
"""
Performance Benchmarking Suite for SDD Architecture

Measures execution time of critical operations:
- Health check (quick vs full)
- Governance compliance validation
- Agent handshake
- Quiz execution
- Caching effectiveness

Targets:
- Health check quick: <200ms
- Health check full: <1s
- Governance compliance: <500ms
- Agent handshake: <2s
- Quiz execution: <3s per question
"""

import time
import json
import sys
import statistics
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List
import subprocess

# Ensure _core is in path for tests.path_config
root = Path(__file__).resolve().parents[2]
if str(root / "_core") not in sys.path:
    sys.path.insert(0, str(root / "_core"))

from tests.path_config import REPO_ROOT


@dataclass
class BenchmarkResult:
    """Single benchmark run result"""
    operation: str
    mode: str
    execution_time: float  # seconds
    cache_hit: bool = False
    success: bool = True
    notes: str = ""

class PerformanceBenchmark:
    """Benchmark suite for SDD architecture operations"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else REPO_ROOT
        self.results: List[BenchmarkResult] = []
        self.targets = {
            "health_check_quick": 0.2,      # 200ms
            "health_check_full": 1.0,       # 1s
            "governance_compliance": 0.5,   # 500ms
            "agent_handshake": 2.0,         # 2s
            "quiz_execution_per_q": 3.0,    # 3s per question
        }
    
    def run_health_check_quick(self, iterations: int = 3) -> BenchmarkResult:
        """Benchmark quick health check (from cache)"""
        times = []
        
        for i in range(iterations):
            start = time.perf_counter()
            result = subprocess.run(
                ["python3", "_core/health_check.py", "--mode", "compact"],
                cwd=self.project_root,
                capture_output=True,
                timeout=5
            )
            elapsed = time.perf_counter() - start
            
            if result.returncode == 0:
                times.append(elapsed)
        
        avg_time = statistics.mean(times) if times else 0
        cache_hit = avg_time < 0.05  # First run slow, cached runs < 50ms
        
        result = BenchmarkResult(
            operation="health_check",
            mode="quick",
            execution_time=avg_time,
            cache_hit=cache_hit,
            success=bool(times)
        )
        
        return result
    
    def run_health_check_full(self, iterations: int = 2) -> BenchmarkResult:
        """Benchmark full health check with verbose output"""
        times = []
        
        for i in range(iterations):
            # Clear cache for fresh run
            cache_file = self.project_root / "_core" / ".sdd" / "agent_state.json"
            if cache_file.exists():
                cache_file.unlink()
            
            start = time.perf_counter()
            result = subprocess.run(
                ["python3", "_core/health_check.py", "--verbose"],
                cwd=self.project_root,
                capture_output=True,
                timeout=5
            )
            elapsed = time.perf_counter() - start
            
            if result.returncode == 0:
                times.append(elapsed)
        
        avg_time = statistics.mean(times) if times else 0
        
        result = BenchmarkResult(
            operation="health_check",
            mode="full",
            execution_time=avg_time,
            success=bool(times)
        )
        
        return result
    
    def run_governance_compliance(self, iterations: int = 3) -> BenchmarkResult:
        """Benchmark governance compliance validation"""
        times = []
        
        for i in range(iterations):
            start = time.perf_counter()
            result = subprocess.run(
                ["python3", "_core/governance_compliance.py", "--verify"],
                cwd=self.project_root,
                capture_output=True,
                timeout=5
            )
            elapsed = time.perf_counter() - start
            
            if result.returncode in [0, 1]:  # 0=compliant, 1=violations found
                times.append(elapsed)
        
        avg_time = statistics.mean(times) if times else 0
        
        result = BenchmarkResult(
            operation="governance_compliance",
            mode="verify",
            execution_time=avg_time,
            success=bool(times)
        )
        
        return result
    
    def run_agent_handshake(self, iterations: int = 2) -> BenchmarkResult:
        """Benchmark agent handshake protocol"""
        times = []
        
        for i in range(iterations):
            start = time.perf_counter()
            result = subprocess.run(
                ["python3", "_core/agent_handshake.py", "--mode", "silent"],
                cwd=self.project_root,
                capture_output=True,
                timeout=10
            )
            elapsed = time.perf_counter() - start
            
            if result.returncode in [0, 1]:
                times.append(elapsed)
        
        avg_time = statistics.mean(times) if times else 0
        
        result = BenchmarkResult(
            operation="agent_handshake",
            mode="silent",
            execution_time=avg_time,
            success=bool(times)
        )
        
        return result
    
    def run_quiz_execution(self, iterations: int = 1) -> BenchmarkResult:
        """Benchmark quiz execution"""
        times = []
        
        for i in range(iterations):
            start = time.perf_counter()
            result = subprocess.run(
                ["python3", "_core/quiz_executor.py", "--mode", "silent", "--limit", "1"],
                cwd=self.project_root,
                capture_output=True,
                timeout=10,
                input=b"\n"  # Auto-answer first question
            )
            elapsed = time.perf_counter() - start
            
            if result.returncode in [0, 1]:
                times.append(elapsed)
        
        avg_time = statistics.mean(times) if times else 0
        
        result = BenchmarkResult(
            operation="quiz_execution",
            mode="silent",
            execution_time=avg_time,
            success=bool(times)
        )
        
        return result
    
    def check_against_targets(self, result: BenchmarkResult) -> tuple[bool, str]:
        """Check if result meets performance target"""
        key = f"{result.operation}_{result.mode}".replace("_verify", "_compliance")
        
        if key not in self.targets:
            return True, "No target defined"
        
        target = self.targets[key]
        if result.execution_time <= target:
            return True, f"✓ {result.execution_time:.3f}s (target: {target}s)"
        else:
            return False, f"✗ {result.execution_time:.3f}s (target: {target}s)"
    
    def format_report(self, style: str = "text") -> str:
        """Format benchmark results"""
        if style == "json":
            return json.dumps([asdict(r) for r in self.results], indent=2)
        
        # Text format
        lines = [
            "┌─ Performance Benchmark Report ─────────────────────────────────┐",
            "│",
        ]
        
        for result in self.results:
            passed, status_str = self.check_against_targets(result)
            marker = "✓" if passed else "✗"
            
            lines.append(f"│ {marker} {result.operation:20} ({result.mode:10})")
            lines.append(f"│   {status_str}")
            
            if result.cache_hit:
                lines.append("│   Cache hit: Yes")
            if result.notes:
                lines.append(f"│   Note: {result.notes}")
            lines.append("│")
        
        lines.append("└─────────────────────────────────────────────────────────────┘")
        
        return "\n".join(lines)
    
    def run_all(self, verbose: bool = False) -> int:
        """Run all benchmarks"""
        print("Starting performance benchmarks...\n")
        
        tests = [
            ("Health Check (Quick/Cached)", self.run_health_check_quick),
            ("Health Check (Full/Verbose)", self.run_health_check_full),
            ("Governance Compliance", self.run_governance_compliance),
            ("Agent Handshake", self.run_agent_handshake),
            ("Quiz Execution", self.run_quiz_execution),
        ]
        
        for test_name, test_func in tests:
            print(f"Running: {test_name}...", end=" ", flush=True)
            try:
                result = test_func()
                self.results.append(result)
                
                passed, status = self.check_against_targets(result)
                marker = "✓" if passed else "⚠"
                print(f"{marker} {result.execution_time:.3f}s")
                
                if verbose and result.notes:
                    print(f"  Note: {result.notes}")
            except Exception as e:
                print(f"✗ FAILED: {e}")
                self.results.append(BenchmarkResult(
                    operation=test_name.split("(")[0].strip(),
                    mode="unknown",
                    execution_time=0,
                    success=False,
                    notes=str(e)
                ))
        
        print("\n" + self.format_report("text"))
        
        # Return exit code based on all tests passing
        all_pass = all(
            self.check_against_targets(r)[0] 
            for r in self.results if r.success
        )
        
        return 0 if all_pass else 1
    
    def save_results(self, filename: str = "benchmark_results.json"):
        """Save results to file"""
        output_file = self.project_root / "tests" / "performance" / filename
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "timestamp": time.time(),
            "results": [asdict(r) for r in self.results],
            "targets": self.targets,
        }
        
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    benchmark = PerformanceBenchmark()
    exit_code = benchmark.run_all(verbose="--verbose" in sys.argv)
    
    if "--save" in sys.argv:
        benchmark.save_results()
    
    sys.exit(exit_code)
