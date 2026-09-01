#!/usr/bin/env python3
"""Validate runtime convergence before authenticated rollout verification."""

import json
import sys
from pathlib import Path


IDENTITY_FIELDS = ("source_sha", "artifact_digest", "deployment_id", "environment", "revision_marker")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_deployment_convergence.py MANIFEST.json", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "REFUSED", "failures": [str(exc)]}))
        return 2
    if not isinstance(data, dict):
        print(json.dumps({"verdict": "REFUSED", "failures": ["manifest must be a JSON object"]}))
        return 1

    failures = []
    if data.get("schema") != "deployment-revision-convergence.v1":
        failures.append("unsupported schema")
    for field in IDENTITY_FIELDS:
        if not isinstance(data.get(field), str) or not data.get(field):
            failures.append(f"{field} must be a non-empty immutable identifier")
    if data.get("provider_deploy_state") != "success":
        failures.append("provider deployment state must be success before convergence observations")
    if data.get("provider_readback") is not True:
        failures.append("provider readback is required")

    required = data.get("required_consecutive_matches")
    if not isinstance(required, int) or isinstance(required, bool) or not 2 <= required <= 10:
        failures.append("required_consecutive_matches must be an integer from 2 through 10")
        required = 2
    observations = data.get("observations", [])
    if not isinstance(observations, list):
        failures.append("observations must be a list")
        observations = []
    for observation in observations:
        if not isinstance(observation, dict):
            failures.append("observations must be objects")
            continue
        if observation.get("source") not in {"direct", "independent"}:
            failures.append("observation source must be direct or independent")
        if not observation.get("observed_at"):
            failures.append("each observation requires observed_at")

    final = observations[-required:]
    expected_marker = data.get("revision_marker")
    converged = (
        len(final) == required
        and all(item.get("status") == "ready" and item.get("revision_marker") == expected_marker for item in final if isinstance(item, dict))
        and {item.get("source") for item in final if isinstance(item, dict)} == {"direct", "independent"}
    )

    retry = data.get("retry_policy", {})
    if not isinstance(retry, dict):
        failures.append("retry_policy must be an object")
        retry = {}
    if retry.get("maximum_retries") != 1:
        failures.append("maximum_retries must be exactly one")
    if retry.get("retries_used") not in {0, 1}:
        failures.append("retries_used must be zero or one")
    if retry.get("reconcile_before_retry") is not True or retry.get("stop_after_repeat") is not True:
        failures.append("retry requires reconciliation first and a stop after repetition")

    diagnostics = data.get("diagnostics", {})
    if not isinstance(diagnostics, dict):
        failures.append("diagnostics must be an object")
        diagnostics = {}
    for field in ("sanitized", "remote_tool_names_only"):
        if diagnostics.get(field) is not True:
            failures.append(f"diagnostics.{field} must be true")
    for field in ("response_bodies_logged", "secret_values_logged", "old_revision_response_treated_as_new_schema"):
        if diagnostics.get(field) is not False:
            failures.append(f"diagnostics.{field} must be false")

    repeated = data.get("repeated_failure_after_retry") is True
    rollback = data.get("rollback", {})
    if not isinstance(rollback, dict):
        failures.append("rollback must be an object")
        rollback = {}
    if repeated:
        if retry.get("retries_used") != 1:
            failures.append("a repeated failure requires the single retry to have been used")
        for field in ("known_good_sha", "deployment_id"):
            if not rollback.get(field):
                failures.append(f"rollback.{field} is required")
        for field in ("provenance_verified", "restoration_probe"):
            if rollback.get(field) is not True:
                failures.append(f"rollback.{field} must be true")

    if converged and not repeated:
        probe = data.get("authenticated_probe", {})
        if not isinstance(probe, dict):
            failures.append("authenticated_probe must be an object")
            probe = {}
        if probe.get("after_convergence") is not True:
            failures.append("authenticated probe must run after convergence")
        if probe.get("revision_marker") != expected_marker:
            failures.append("authenticated probe is not bound to the expected revision")
        if probe.get("status") != "pass":
            failures.append("authenticated probe did not pass")

    if failures:
        verdict = "REFUSED"
    elif repeated:
        verdict = "ROLLBACK_REQUIRED"
    elif not converged:
        verdict = "WAIT_FOR_CONVERGENCE"
    else:
        verdict = "CONVERGED"
    print(json.dumps({"verdict": verdict, "deployment_id": data.get("deployment_id"), "failures": failures}, indent=2))
    return 0 if verdict == "CONVERGED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
