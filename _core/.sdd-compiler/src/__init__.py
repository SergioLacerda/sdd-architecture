"""
DSL Compiler source module

Integrated pipeline:
1. DSL Parser (dsl_compiler.py) → Parse v3.0 DSL
2. String Pool → Deduplicate strings
3. Runtime Telemetry Kit (runtime_telemetry_kit/) → Compress with patterns
4. MessagePack Encoder (msgpack_encoder.py) → Binary output
5. Orchestrator (integrate.py) → Deployment pipeline

Entry Points:
  - Main CLI: python .sdd-compiler/compiler.py (from repository root)
  - Alt CLI: python -m src (from .sdd-compiler/)
  - Library: from .sdd-compiler.src.integrate import SDDIntegrator
"""

from .dsl_compiler import DSLCompiler, DSLValidator, DSLParser, compile_string, compile_file
from .msgpack_encoder import MessagePackEncoder
from .integrate import SDDIntegrator
from . import runtime_telemetry_kit

__all__ = [
    "DSLCompiler",
    "DSLValidator",
    "DSLParser",
    "compile_string",
    "compile_file",
    "MessagePackEncoder",
    "SDDIntegrator",
    "runtime_telemetry_kit",
]
