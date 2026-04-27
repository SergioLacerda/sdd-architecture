"""
DSL Compiler - Binary compilation module for SDD v3.1

Compiles human-readable DSL files (.spec, .dsl) to optimized binary format
for 65% size reduction and 3-4x faster parsing.

Example:
    >>> from compiler import compile_file
    >>>
    >>> metrics = compile_file(
    ...     "core/CANONICAL/mandate.spec",
    ...     "mandate.spec.bin"
    ... )
    >>>
    >>> print(f"Compressed to {metrics.compression_ratio:.1%}")
"""

from pathlib import Path

__version__ = "3.1.0-dev"
__author__ = "SDD Development Team"

# Central path to the compiled governance artifacts
COMPILED_DIR = Path(__file__).parent / "compiled"
