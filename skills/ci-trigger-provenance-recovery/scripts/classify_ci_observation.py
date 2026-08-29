#!/usr/bin/env python3
"""Classify CI evidence for one exact commit without guessing the root cause."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def classify(value: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    commit = value.get("commit")
    expected = value.get("expected_workflows")
    runs = value.get("observed_runs")
    if not isinstance(commit, str) or not commit:
        errors.append("commit must be a non-empty string")
    if not isinstance(expected, list) or not expected or not all(isinstance(item, str) and item for item in expected):
        errors.append("expected_workflows must be a non-empty string array")
        expected = []
    if not isinstance(runs, list):
        errors.append("observed_runs must be an array")
        runs = []
    if errors:
        return {"verdict": "REFUSED", "errors": errors}
    if not runs:
        return {"verdict": "MISSING_TRIGGER", "errors": [], "missing_workflows": sorted(set(expected))}
    exact = [run for run in runs if isinstance(run, dict) and run.get("head_sha") == commit]
    if not exact:
        return {"verdict": "STALE_EVIDENCE", "errors": [], "missing_workflows": sorted(set(expected))}
    by_name = {run.get("workflow"): run for run in exact if isinstance(run.get("workflow"), str)}
    missing = sorted(set(expected) - set(by_name))
    if missing:
        return {"verdict": "INCOMPLETE", "errors": [], "missing_workflows": missing}
    selected = [by_name[name] for name in expected]
    if any(run.get("status") != "completed" for run in selected):
        return {"verdict": "PENDING", "errors": [], "missing_workflows": []}
    failed = sorted(name for name in expected if by_name[name].get("conclusion") != "success")
    if failed:
        return {"verdict": "FAILED", "errors": [], "failed_workflows": failed, "missing_workflows": []}
    return {"verdict": "PROVEN", "errors": [], "missing_workflows": []}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("observation", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.observation.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "REFUSED", "errors": [str(exc)]}))
        return 2
    if not isinstance(value, dict):
        print(json.dumps({"verdict": "REFUSED", "errors": ["observation must be an object"]}))
        return 2
    result = classify(value)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["verdict"] == "PROVEN" else 1


if __name__ == "__main__":
    sys.exit(main())
