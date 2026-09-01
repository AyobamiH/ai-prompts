#!/usr/bin/env python3
"""Validate a package's artifact-level consumer contract."""

import json
import sys
from pathlib import Path


ARTIFACTS = {"built", "packed", "installed", "release"}
TOOLCHAINS = {"locked", "minimum-supported"}
UPSTREAM_STATES = {"pass", "pending", "action_required", "fail", "missing"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_package_consumer_contract.py CONTRACT.json", file=sys.stderr)
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
    if data.get("schema") != "package-consumer-contract.v1":
        failures.append("unsupported schema")
    if not isinstance(data.get("subject"), str) or not data.get("subject"):
        failures.append("subject must be a non-empty immutable identifier")

    documented_values = data.get("documented_entrypoints", [])
    required_values = data.get("required_entrypoints", [])
    if not isinstance(documented_values, list) or any(not isinstance(item, str) or not item for item in documented_values):
        failures.append("documented_entrypoints must contain non-empty strings")
        documented_values = []
    if not isinstance(required_values, list) or any(not isinstance(item, str) or not item for item in required_values):
        failures.append("required_entrypoints must contain non-empty strings")
        required_values = []
    documented = set(documented_values)
    required = set(required_values)
    if len(documented) != len(documented_values) or len(required) != len(required_values):
        failures.append("entrypoint lists must not contain duplicates")
    if not required or not required <= documented:
        failures.append("required entrypoints must be non-empty and documented")

    artifacts = data.get("artifacts", [])
    if not isinstance(artifacts, list):
        failures.append("artifacts must be a list")
        artifacts = []
    kinds = [item.get("kind") for item in artifacts if isinstance(item, dict) and isinstance(item.get("kind"), str)]
    if set(kinds) != ARTIFACTS or len(kinds) != len(ARTIFACTS):
        failures.append("built, packed, installed, and release artifacts are required exactly once")
    for item in artifacts:
        if not isinstance(item, dict):
            failures.append("artifact entries must be objects")
            continue
        for field in ("passed", "expected_paths_verified", "forbidden_paths_verified"):
            if item.get(field) is not True:
                failures.append(f"artifact {item.get('kind')} lacks {field}")

    toolchains = data.get("toolchains", [])
    if not isinstance(toolchains, list):
        failures.append("toolchains must be a list")
        toolchains = []
    by_id = {item.get("id"): item for item in toolchains if isinstance(item, dict) and isinstance(item.get("id"), str)}
    if len(by_id) != len(toolchains):
        failures.append("toolchain IDs must be present, unique strings")
    if not TOOLCHAINS <= set(by_id):
        failures.append("locked and minimum-supported toolchains are required")
    for toolchain_id in TOOLCHAINS:
        item = by_id.get(toolchain_id, {})
        if item.get("supported") is not True or item.get("passed") is not True:
            failures.append(f"toolchain {toolchain_id} did not pass as supported")

    for field in (
        "minimum_supported_documented",
        "clean_consumer_install",
        "workspace_resolution_disabled",
        "historical_issue_reproduction",
        "repository_owned_test",
        "remote_ci_wires_test",
        "changelog_updated",
    ):
        if data.get(field) is not True:
            failures.append(f"{field} must be true")

    assertions = data.get("equivalence_assertions", [])
    if not isinstance(assertions, list):
        failures.append("equivalence_assertions must be a list")
        assertions = []
    if not assertions:
        failures.append("at least one output-equivalence assertion is required")
    for item in assertions:
        if not isinstance(item, dict):
            failures.append("equivalence assertions must be objects")
            continue
        if item.get("strength") not in {"byte-identical", "semantic"}:
            failures.append("equivalence strength must be byte-identical or semantic")
        if item.get("passed") is not True or not item.get("left") or not item.get("right"):
            failures.append("equivalence assertion is incomplete or failed")

    upstream = data.get("upstream_checks")
    if upstream not in UPSTREAM_STATES:
        failures.append("upstream_checks has an unsupported state")
    if upstream in {"fail", "missing"}:
        failures.append("upstream checks failed or are missing")
    if data.get("agent_merge_authority") is not False:
        failures.append("agent_merge_authority must be false")
    if data.get("contains_secret_values") is not False:
        failures.append("contract must not contain secret values")

    if failures:
        verdict = "REFUSED"
    elif upstream == "pass" and data.get("maintainer_approval") is True:
        verdict = "READY_FOR_MAINTAINER"
    else:
        verdict = "CONTRACT_VERIFIED"
    print(json.dumps({"verdict": verdict, "subject": data.get("subject"), "failures": failures}, indent=2))
    return 0 if verdict != "REFUSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
