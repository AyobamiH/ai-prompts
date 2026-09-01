#!/usr/bin/env python3
"""Classify overlapping pull requests against one current default branch."""

import json
import sys
from pathlib import Path


ACTIONS = {
    "ALREADY_IN_BASE": "close_without_merge",
    "REMAINING_DELTA": "rebuild_remaining_delta",
    "REBASE_REQUIRED": "rebase_and_retest",
    "CONFLICT_REVIEW_REQUIRED": "manual_conflict_review",
    "READY": "review_ready",
}


def identifiers(value: object) -> set[str] | None:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        return None
    result = set(value)
    return result if len(result) == len(value) else None


def expected(pr: dict, default_sha: str, intended: set[str], present: set[str], remaining: set[str]) -> str:
    if pr.get("semantic_conflict") is True:
        return "CONFLICT_REVIEW_REQUIRED"
    if intended and present == intended and not remaining:
        return "ALREADY_IN_BASE"
    if present and remaining:
        return "REMAINING_DELTA"
    if pr.get("head_base_sha") != default_sha:
        return "REBASE_REQUIRED"
    return "READY"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: classify_pr_convergence.py RECORD.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "REFUSED", "failures": [str(exc)]}))
        return 2
    if not isinstance(data, dict):
        print(json.dumps({"verdict": "REFUSED", "failures": ["record must be a JSON object"]}))
        return 1

    failures = []
    if data.get("schema") != "overlapping-pr-convergence.v1":
        failures.append("unsupported schema")
    default = data.get("default_branch", {})
    if not isinstance(default, dict):
        failures.append("default_branch must be an object")
        default = {}
    if not default.get("sha") or not default.get("tree_sha"):
        failures.append("default branch SHA and tree SHA are required")
    for field in ("provider_readback", "content_digests_verified", "history_preserved", "no_force_update", "no_merge_performed"):
        if data.get(field) is not True:
            failures.append(f"{field} must be true")

    results = []
    seen = set()
    pull_requests = data.get("pull_requests", [])
    if not isinstance(pull_requests, list):
        failures.append("pull_requests must be a list")
        pull_requests = []
    for pr in pull_requests:
        if not isinstance(pr, dict):
            failures.append("pull request records must be objects")
            continue
        pr_id = pr.get("id")
        if not isinstance(pr_id, (str, int)) or isinstance(pr_id, bool) or not str(pr_id) or pr_id in seen:
            failures.append("pull request IDs must be present and unique")
            continue
        seen.add(pr_id)
        intended = identifiers(pr.get("intended_change_ids"))
        present = identifiers(pr.get("change_ids_present_in_base"))
        remaining = identifiers(pr.get("remaining_change_ids"))
        if intended is None or present is None or remaining is None:
            failures.append(f"PR {pr_id} change IDs must be unique non-empty strings")
            intended, present, remaining = set(), set(), set()
        if not intended or present & remaining or present | remaining != intended:
            failures.append(f"PR {pr_id} change partitions are incomplete or overlapping")
        classification = expected(pr, default.get("sha"), intended, present, remaining)
        if pr.get("classification") != classification:
            failures.append(f"PR {pr_id} classification should be {classification}")
        if pr.get("requested_action") != ACTIONS[classification]:
            failures.append(f"PR {pr_id} action should be {ACTIONS[classification]}")
        if classification == "READY" and pr.get("exact_head_ci") != "pass":
            failures.append(f"PR {pr_id} cannot be READY without exact-head CI")
        if not pr.get("head_sha"):
            failures.append(f"PR {pr_id} lacks head_sha")
        results.append({"id": pr_id, "classification": classification, "action": ACTIONS[classification]})

    if not results:
        failures.append("at least one pull request is required")
    verdict = "RECONCILED" if not failures else "REFUSED"
    print(json.dumps({"verdict": verdict, "default_sha": default.get("sha"), "pull_requests": results, "failures": failures}, indent=2))
    return 0 if verdict == "RECONCILED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
