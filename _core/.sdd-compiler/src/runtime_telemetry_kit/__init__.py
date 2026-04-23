"""
Runtime Telemetry Kit (RTK) - Sub-layer of DSL Compiler

Deduplication engine for telemetry events with 60-70% overhead reduction.
Integrated as optimization layer within the compilation pipeline.

Version: 3.1.0-dev
Status: Phase 8 (v3.1 Enhancement)

Location: .sdd-compiler/src/runtime_telemetry_kit/
"""

from .engine import (
    DeduplicationEngine,
    PatternRegistry,
    CompressionMetrics,
    deduplicate_event,
    get_engine,
    get_compression_metrics,
)
from .patterns import ExtendedPatterns

__all__ = [
    "DeduplicationEngine",
    "PatternRegistry",
    "CompressionMetrics",
    "deduplicate_event",
    "get_engine",
    "get_compression_metrics",
    "ExtendedPatterns",
]
