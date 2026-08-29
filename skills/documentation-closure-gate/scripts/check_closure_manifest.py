#!/usr/bin/env python3
"""Check exact-commit closure across code, docs, CI, deployment, and evidence."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
REQUIRED = ["implementation", "documentation", "ci", "deployment", "live_verification", "evidence"]


def check(value: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    commit = value.get("commit")
    if not isinstance(commit, str) or not SHA_PATTERN.fullmatch(commit):
        errors.append("commit must be a lowercase 40-character Git SHA")
    for name in REQUIRED:
        record = value.get(name)
        if not isinstance(record, dict):
            errors.append(f"missing record: {name}")
            continue
        if record.get("commit") != commit:
            errors.append(f"{name} record does not match closure commit")
        if record.get("status") != "pass":
            errors.append(f"{name} record did not pass")
    docs = value.get("documentation")
    if isinstance(docs, dict):
        changed = docs.get("changed")
        rationale = docs.get("no_impact_rationale")
        has_changed = isinstance(changed, list) and bool(changed) and all(isinstance(item, str) and item for item in changed)
        has_rationale = isinstance(rationale, str) and bool(rationale.strip())
        if not has_changed and not has_rationale:
            errors.append("documentation needs changed files or a no-impact rationale")
    return {"verdict": "CLOSED" if not errors else "OPEN", "commit": commit, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "OPEN", "errors": [str(exc)]}))
        return 2
    if not isinstance(value, dict):
        print(json.dumps({"verdict": "OPEN", "errors": ["manifest must be an object"]}))
        return 2
    result = check(value)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["verdict"] == "CLOSED" else 1


if __name__ == "__main__":
    sys.exit(main())
