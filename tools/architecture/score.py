import asyncio
import json
from typing import Dict, Sequence

CHECKS = [
    # Scope to architecture gate checks used by this repository pipeline.
    (["ruff", "check", "tools/architecture/score.py"], 20, "lint"),
    (["mypy", "tools/architecture/score.py"], 20, "types"),
    (["pytest", "tests/unit", "tests/integration", "-q"], 30, "tests"),
]


async def run(cmd: Sequence[str]) -> int:
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await proc.communicate()
    return proc.returncode if proc.returncode is not None else 1


async def main() -> None:
    score = 100
    results: Dict[str, str] = {}

    tasks = [run(cmd) for cmd, _, _ in CHECKS]
    codes = await asyncio.gather(*tasks)

    for (_, penalty, name), code in zip(CHECKS, codes, strict=True):
        if code != 0:
            score -= penalty
            results[name] = "fail"
        else:
            results[name] = "ok"

    report = {
        "score": score,
        "results": results,
    }

    print(json.dumps(report, indent=2))

    if score < 70:
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
