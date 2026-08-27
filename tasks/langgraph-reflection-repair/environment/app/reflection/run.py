"""CLI entry point for running the repair pipeline on one instance.

    python -m reflection.run --instance /app/data/public_instance.json \
        --recursion-limit 25 --out /app/result.json

Writes a JSON result with the final record and verdict. This CLI is for your own
iteration; the verifier imports `build_graph` directly and drives it with hidden
instances and its own recursion limit.
"""

from __future__ import annotations

import argparse
import json
import sys

from .graph import build_graph


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the record-repair pipeline.")
    parser.add_argument("--instance", required=True, help="Path to an instance JSON.")
    parser.add_argument("--recursion-limit", type=int, default=25)
    parser.add_argument("--out", default=None, help="Where to write the result JSON.")
    args = parser.parse_args(argv)

    with open(args.instance, "r", encoding="utf-8") as fh:
        instance = json.load(fh)

    app = build_graph(instance)
    final = app.invoke(
        {"record": instance},
        config={"recursion_limit": args.recursion_limit},
    )

    result = {"record": final.get("record"), "verdict": final.get("verdict")}
    text = json.dumps(result, indent=2, sort_keys=True)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
