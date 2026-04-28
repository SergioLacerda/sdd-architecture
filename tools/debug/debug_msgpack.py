import importlib
import json
import sys
from pathlib import Path

import msgpack

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "compiler"))
sys.path.insert(0, str(ROOT / "build_scripts"))

GovernanceCompiler = importlib.import_module("governance_compiler").GovernanceCompiler
PipelineBuilder = importlib.import_module("pipeline_builder").PipelineBuilder

# Build and compile
print("Building pipeline...")
builder = PipelineBuilder("../_spec")
builder.save_outputs("compiled")

print("Compiling...")
compiler = GovernanceCompiler("compiled")
result = compiler.compile("compiled")

# Deserialize core msgpack
core_msgpack_file = result["core_msgpack_file"]
print(f"\nCore msgpack file: {core_msgpack_file}")
print(f"File exists: {Path(core_msgpack_file).exists()}")
if Path(core_msgpack_file).exists():
    print(f"File size: {Path(core_msgpack_file).stat().st_size} bytes")

core_data = msgpack.unpackb(Path(core_msgpack_file).read_bytes(), raw=False)

print(f"\nCore data keys: {list(core_data.keys())}")
print(f"Core data category: {core_data.get('category')}")
print(f"Core data items length: {len(core_data.get('items', []))}")
print(f"Core data fingerprint: {core_data.get('fingerprint')}")
print(f"\nCore data items: {core_data.get('items')}")
print(f"\nFull core_data:\n{json.dumps(core_data, indent=2, default=str)}")
