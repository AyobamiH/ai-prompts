#!/usr/bin/env python3
"""Evaluate a compact task matrix against required exact-subject evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def evaluate(value: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    false_completion_claims: list[str] = []
    results: list[dict[str, Any]] = []
    tasks = value.get("tasks")
    if not isinstance(tasks, list):
        return {"verdict": "REFUSED", "errors": ["tasks must be an array"], "tasks": []}

    seen: set[str] = set()
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            errors.append(f"tasks[{index}] must be an object")
            continue
        task_id = task.get("id")
        if not isinstance(task_id, str) or not task_id:
            errors.append(f"tasks[{index}] needs a non-empty id")
            continue
        if task_id in seen:
            errors.append(f"duplicate task id: {task_id}")
        seen.add(task_id)
        subject = task.get("subject")
        required = task.get("required_evidence", [])
        evidence = task.get("evidence", [])
        if not isinstance(subject, dict) or not subject:
            errors.append(f"task {task_id} needs a non-empty subject")
            subject = {}
        if not isinstance(required, list) or not required or not all(isinstance(item, str) and item for item in required):
            errors.append(f"task {task_id} needs non-empty required_evidence")
            required = []
        if not isinstance(evidence, list):
            errors.append(f"task {task_id} evidence must be an array")
            evidence = []

        passing: set[str] = set()
        mismatched: list[str] = []
        failed: list[str] = []
        for item in evidence:
            if not isinstance(item, dict) or not isinstance(item.get("kind"), str):
                continue
            kind = item["kind"]
            if item.get("subject") != subject:
                mismatched.append(kind)
            elif item.get("status") == "pass":
                passing.add(kind)
            elif item.get("status") == "fail":
                failed.append(kind)
        missing = sorted(set(required) - passing)
        blocker = task.get("blocker")
        if not missing and not mismatched and not failed:
            actual = "VERIFIED_COMPLETE"
        elif isinstance(blocker, str) and blocker.strip():
            actual = "BLOCKED"
        elif evidence:
            actual = "IN_PROGRESS"
        elif task.get("claimed_status") == "not_started":
            actual = "NOT_STARTED"
        else:
            actual = "UNPROVEN"
        if task.get("claimed_status") == "complete" and actual != "VERIFIED_COMPLETE":
            false_completion_claims.append(task_id)
        results.append({
            "id": task_id,
            "actual_status": actual,
            "missing_evidence": missing,
            "mismatched_evidence": sorted(set(mismatched)),
            "failed_evidence": sorted(set(failed)),
        })

    if errors:
        verdict = "REFUSED"
    elif all(item["actual_status"] == "VERIFIED_COMPLETE" for item in results) and results:
        verdict = "COMPLETE"
    else:
        verdict = "PARTIAL"
    return {"verdict": verdict, "errors": errors, "false_completion_claims": false_completion_claims, "tasks": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("matrix", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.matrix.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "REFUSED", "errors": [str(exc)]}))
        return 2
    if not isinstance(value, dict):
        print(json.dumps({"verdict": "REFUSED", "errors": ["matrix must be an object"]}))
        return 2
    result = evaluate(value)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["verdict"] == "COMPLETE" else 1


if __name__ == "__main__":
    sys.exit(main())
