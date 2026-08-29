#!/usr/bin/env python3
"""Check that every required release stage passed for one exact commit."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
DEFAULT_STAGES = ["validation", "documentation", "ci", "deployment", "live_verification", "evidence"]


def check(manifest: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    commit = manifest.get("commit")
    stages = manifest.get("stages")
    required = manifest.get("required_stages", DEFAULT_STAGES)
    if not isinstance(commit, str) or not SHA_PATTERN.fullmatch(commit):
        errors.append("commit must be a lowercase 40-character Git SHA")
    if not isinstance(stages, dict):
        errors.append("stages must be an object")
        stages = {}
    if not isinstance(required, list) or not all(isinstance(item, str) and item for item in required):
        errors.append("required_stages must be an array of non-empty strings")
        required = []
    for name in required:
        stage = stages.get(name)
        if not isinstance(stage, dict):
            errors.append(f"missing required stage: {name}")
            continue
        if stage.get("commit") != commit:
            errors.append(f"stage {name} is not bound to the candidate commit")
        if stage.get("status") != "pass":
            errors.append(f"stage {name} did not pass")
    return {"verdict": "READY" if not errors else "REFUSED", "commit": commit, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "REFUSED", "errors": [str(exc)]}))
        return 2
    if not isinstance(value, dict):
        print(json.dumps({"verdict": "REFUSED", "errors": ["manifest must be an object"]}))
        return 2
    result = check(value)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["verdict"] == "READY" else 1


if __name__ == "__main__":
    sys.exit(main())
