#!/usr/bin/env python3
"""Compare expected and observed MCP tool manifests exactly by tool name."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def index_tools(value: dict[str, Any], label: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    tools = value.get("tools")
    if not isinstance(tools, list):
        errors.append(f"{label}.tools must be an array")
        return {}
    indexed: dict[str, dict[str, Any]] = {}
    for position, tool in enumerate(tools):
        if not isinstance(tool, dict) or not isinstance(tool.get("name"), str) or not tool.get("name"):
            errors.append(f"{label}.tools[{position}] needs a name")
            continue
        name = tool["name"]
        if name in indexed:
            errors.append(f"duplicate {label} tool: {name}")
        indexed[name] = tool
    return indexed


def compare(expected: dict[str, Any], observed: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    exp = index_tools(expected, "expected", errors)
    obs = index_tools(observed, "observed", errors)
    missing = sorted(set(exp) - set(obs))
    unexpected = sorted(set(obs) - set(exp))
    changed = sorted(name for name in set(exp) & set(obs) if exp[name] != obs[name])
    verdict = "MATCH" if not errors and not missing and not unexpected and not changed else "DRIFT"
    return {"verdict": verdict, "errors": errors, "missing": missing, "unexpected": unexpected, "changed": changed}


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expected", type=Path)
    parser.add_argument("observed", type=Path)
    args = parser.parse_args()
    try:
        result = compare(load(args.expected), load(args.observed))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"verdict": "DRIFT", "errors": [str(exc)]}))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0 if result["verdict"] == "MATCH" else 1


if __name__ == "__main__":
    sys.exit(main())
