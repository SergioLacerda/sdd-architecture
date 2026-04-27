"""
DSL Compiler source module

Integrated pipeline:
1. DSL Parser (dsl_compiler.py) → Parse v3.0 DSL
2. String Pool → Deduplicate strings
3. Runtime Telemetry Kit (runtime_telemetry_kit/) → Compress with patterns
4. MessagePack Encoder (msgpack_encoder.py) → Binary output
5. Orchestrator (integrate.py) → Deployment pipeline

Entry Points:
  - Main CLI: python compiler/compiler.py (from repository root)
  - Alt CLI: python -m src (from compiler/)
  - Library: from compiler.src.integrate import SDDIntegrator
"""

from . import runtime_telemetry_kit
from .dsl_compiler import DSLCompiler, DSLParser, DSLValidator, compile_file, compile_string
from .integrate import SDDIntegrator
from .msgpack_encoder import MessagePackEncoder

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
