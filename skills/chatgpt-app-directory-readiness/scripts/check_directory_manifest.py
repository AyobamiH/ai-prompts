#!/usr/bin/env python3
"""Check exact-subject gates for a ChatGPT app directory handoff."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_REVIEW_GATES = [
    "identity", "mcp_connection", "authentication", "trust_pages", "icons",
    "data_declarations", "positive_tests", "negative_tests", "documentation", "exact_release",
]


def check(value: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    subject = value.get("release_subject")
    target = value.get("target_state")
    gates = value.get("gates")
    required = value.get("required_gates", DEFAULT_REVIEW_GATES)
    if not isinstance(subject, str) or not subject:
        errors.append("release_subject must be a non-empty string")
    if target not in {"draft_saved", "review_ready"}:
        errors.append("target_state must be draft_saved or review_ready")
    if not isinstance(gates, dict):
        errors.append("gates must be an object")
        gates = {}
    if not isinstance(required, list) or not all(isinstance(item, str) and item for item in required):
        errors.append("required_gates must be an array of non-empty strings")
        required = []
    if target == "review_ready":
        for name in DEFAULT_REVIEW_GATES:
            if name not in required:
                errors.append(f"review_ready cannot omit gate: {name}")
    for name in required:
        gate = gates.get(name)
        if not isinstance(gate, dict):
            errors.append(f"missing gate: {name}")
            continue
        if gate.get("subject") != subject:
            errors.append(f"gate {name} has a subject mismatch")
        if gate.get("status") != "pass":
            errors.append(f"gate {name} did not pass")
    verdict = "READY_FOR_REVIEW" if target == "review_ready" and not errors else "DRAFT_READY" if not errors else "BLOCKED"
    return {"verdict": verdict, "release_subject": subject, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "BLOCKED", "errors": [str(exc)]}))
        return 2
    if not isinstance(value, dict):
        print(json.dumps({"verdict": "BLOCKED", "errors": ["manifest must be an object"]}))
        return 2
    result = check(value)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["verdict"] in {"DRAFT_READY", "READY_FOR_REVIEW"} else 1


if __name__ == "__main__":
    sys.exit(main())
