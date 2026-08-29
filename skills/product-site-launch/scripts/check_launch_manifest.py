#!/usr/bin/env python3
"""Evaluate a product-site launch manifest without performing mutations."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


BASE_GATES = {
    "product_truth",
    "build",
    "routes",
    "primary_cta",
    "accessibility",
    "canonical_metadata",
    "deployment",
    "public_readback",
}
DOMAIN_GATES = {"dns", "tls", "canonical_redirect"}
ALLOWED = {"pass", "fail", "unproven", "not_applicable"}


def load_input(path: str) -> dict[str, Any]:
    if path == "-":
        value = json.load(sys.stdin)
    else:
        with Path(path).open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("manifest must be a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="launch manifest JSON path, or - for stdin")
    args = parser.parse_args()

    try:
        data = load_input(args.input)
        gates = data.get("gates")
        if not isinstance(gates, dict):
            raise ValueError("gates must be an object")
        required = set(BASE_GATES)
        if data.get("domain_required", True):
            required.update(DOMAIN_GATES)
        if data.get("analytics_required", False):
            required.add("analytics")
        missing = sorted(required - gates.keys())
        if missing:
            raise ValueError(f"missing required gates: {', '.join(missing)}")

        evaluated: dict[str, dict[str, Any]] = {}
        failures: list[str] = []
        unproven: list[str] = []
        for name in sorted(required):
            gate = gates[name]
            if not isinstance(gate, dict):
                raise ValueError(f"gate {name} must be an object")
            status = gate.get("status")
            evidence = gate.get("evidence")
            if status not in ALLOWED:
                raise ValueError(f"gate {name} has invalid status: {status}")
            if not isinstance(evidence, list) or not all(isinstance(item, str) and item.strip() for item in evidence):
                raise ValueError(f"gate {name} evidence must be an array of non-empty strings")
            if status == "pass" and not evidence:
                raise ValueError(f"gate {name} cannot pass without evidence")
            if status == "not_applicable":
                raise ValueError(f"required gate {name} cannot be not_applicable")
            if status == "fail":
                failures.append(name)
            elif status == "unproven":
                unproven.append(name)
            evaluated[name] = {"status": status, "evidence": evidence}

        if failures:
            verdict = "no-go"
            highest_state = "blocked"
        elif unproven:
            verdict = "hold"
            highest_state = "not_publicly_verified"
        else:
            verdict = "go"
            highest_state = "publicly_verified"

        output = {
            "site_id": data.get("site_id"),
            "commit_sha": data.get("commit_sha"),
            "verdict": verdict,
            "highest_state": highest_state,
            "failed_gates": failures,
            "unproven_gates": unproven,
            "gates": evaluated,
        }
        json.dump(output, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"launch manifest check failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
