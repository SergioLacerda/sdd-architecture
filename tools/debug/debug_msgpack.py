"""Debug helper for governance msgpack artifacts."""

import json
from pathlib import Path

import msgpack
from build.governance.compile import GovernanceCompiler
from build.governance.pipeline_builder import PipelineBuilder


def main() -> int:
    print("Building pipeline...")
    builder = PipelineBuilder("../_spec")
    builder.save_outputs("compiled")

    print("Compiling...")
    compiler = GovernanceCompiler("compiled")
    result = compiler.compile("compiled")

    core_msgpack_file = Path(result["core_msgpack_file"])
    print(f"\nCore msgpack file: {core_msgpack_file}")
    print(f"File exists: {core_msgpack_file.exists()}")
    if core_msgpack_file.exists():
        print(f"File size: {core_msgpack_file.stat().st_size} bytes")

    core_data = msgpack.unpackb(core_msgpack_file.read_bytes(), raw=False)
    print(f"\nCore data keys: {list(core_data.keys())}")
    print(f"Core data category: {core_data.get('category')}")
    print(f"Core data items length: {len(core_data.get('items', []))}")
    print(f"Core data fingerprint: {core_data.get('fingerprint')}")
    print(f"\nCore data items: {core_data.get('items')}")
    print(f"\nFull core_data:\n{json.dumps(core_data, indent=2, default=str)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
