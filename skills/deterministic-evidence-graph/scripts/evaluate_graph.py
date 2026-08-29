#!/usr/bin/env python3
"""Evaluate exact subject bindings in a compact evidence graph."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def evaluate(graph: dict[str, Any]) -> dict[str, Any]:
    subject = graph.get("subject")
    evidence = graph.get("evidence")
    required = graph.get("required_kinds")
    errors: list[str] = []
    mismatches: list[dict[str, Any]] = []

    if not isinstance(subject, dict) or not subject:
        errors.append("subject must be a non-empty object")
        subject = {}
    if not isinstance(evidence, list):
        errors.append("evidence must be an array")
        evidence = []
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        errors.append("required_kinds must be an array of strings")
        required = []

    statuses: dict[str, set[str]] = {}
    for index, item in enumerate(evidence):
        if not isinstance(item, dict):
            errors.append(f"evidence[{index}] must be an object")
            continue
        kind = item.get("kind")
        status = item.get("status")
        item_subject = item.get("subject")
        if not isinstance(kind, str) or not kind:
            errors.append(f"evidence[{index}].kind must be a non-empty string")
            continue
        if status not in {"pass", "fail", "unavailable"}:
            errors.append(f"evidence[{index}].status is invalid")
            continue
        statuses.setdefault(kind, set()).add(status)
        if not isinstance(item_subject, dict):
            mismatches.append({"index": index, "field": "subject", "reason": "missing"})
            continue
        for key, expected in subject.items():
            if key not in item_subject:
                mismatches.append({"index": index, "field": key, "reason": "missing"})
            elif item_subject[key] != expected:
                mismatches.append(
                    {"index": index, "field": key, "expected": expected, "actual": item_subject[key]}
                )

    contradictory = sorted(kind for kind, values in statuses.items() if "pass" in values and "fail" in values)
    failed = sorted(kind for kind, values in statuses.items() if "fail" in values)
    missing = sorted(kind for kind in set(required) if "pass" not in statuses.get(kind, set()))

    if errors:
        verdict = "REFUSED"
    elif mismatches or contradictory:
        verdict = "CONTRADICTORY_EVIDENCE"
    elif failed:
        verdict = "REFUSED"
    elif missing:
        verdict = "INSUFFICIENT_EVIDENCE"
    else:
        verdict = "VERIFIED"

    return {
        "verdict": verdict,
        "graph_sha256": hashlib.sha256(canonical_bytes(graph)).hexdigest(),
        "errors": errors,
        "subject_mismatches": mismatches,
        "contradictory_kinds": contradictory,
        "failed_kinds": failed,
        "missing_required_kinds": missing,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    try:
        graph = json.loads(args.graph.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "REFUSED", "errors": [str(exc)]}))
        return 2
    if not isinstance(graph, dict):
        print(json.dumps({"verdict": "REFUSED", "errors": ["graph must be an object"]}))
        return 2
    result = evaluate(graph)
    print(json.dumps(result, indent=2 if args.pretty else None, sort_keys=True))
    return 0 if result["verdict"] == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
