#!/usr/bin/env python3
"""Validate explicit deployment and secret targets across environments."""

import json
import sys
from pathlib import Path


REQUIRED = {
    "name",
    "providerAccount",
    "service",
    "config",
    "endpoint",
    "deployWorkflow",
    "deployTrigger",
    "credentialSource",
    "secretTarget",
    "preflightTargetAssertion",
    "liveProbes",
    "credentialSteps",
    "mutationSteps",
}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_environment_isolation.py MANIFEST.json", file=sys.stderr)
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
    if data.get("schema") != "environment-isolation.v1":
        failures.append("unsupported schema")
    environments = data.get("environments", [])
    if not isinstance(environments, list):
        failures.append("environments must be a list")
        environments = []
    if len(environments) < 2:
        failures.append("at least two environments are required")
    for env in environments:
        if not isinstance(env, dict):
            failures.append("environment entries must be objects")
            continue
        missing = sorted(field for field in REQUIRED if not env.get(field))
        if missing:
            failures.append(f"environment {env.get('name')} missing: {', '.join(missing)}")
        if env.get("preflightTargetAssertion") is not True:
            failures.append(f"environment {env.get('name')} lacks a preflight target assertion")
        credential_steps = env.get("credentialSteps", [])
        mutation_steps = env.get("mutationSteps", [])
        if (
            not isinstance(credential_steps, list)
            or not credential_steps
            or any(not isinstance(step, str) or not step for step in credential_steps)
            or len(credential_steps) != len(set(credential_steps))
        ):
            failures.append(f"environment {env.get('name')} credentialSteps must be unique and non-empty")
            credential_steps = []
        if (
            not isinstance(mutation_steps, list)
            or not mutation_steps
            or any(not isinstance(step, str) or not step for step in mutation_steps)
            or len(mutation_steps) != len(set(mutation_steps))
        ):
            failures.append(f"environment {env.get('name')} mutationSteps must be unique and non-empty")
            mutation_steps = []
        if not set(credential_steps) <= set(mutation_steps):
            failures.append(f"environment {env.get('name')} exposes credentials outside mutation steps")
        if env.get("jobWideCredentials") is not False:
            failures.append(f"environment {env.get('name')} must not use job-wide provider credentials")
        for field in (
            "checkoutReceivesProviderCredentials",
            "dependencyInstallReceivesProviderCredentials",
            "validationReceivesProviderCredentials",
        ):
            if env.get(field) is not False:
                failures.append(f"environment {env.get('name')} must set {field} to false")
    for field in ("service", "config", "endpoint", "credentialSource", "secretTarget"):
        values = [env.get(field) for env in environments if isinstance(env, dict)]
        if None not in values and len(values) != len(set(values)):
            failures.append(f"{field} must be distinct across environments")
    if data.get("mutation_requires_explicit_environment") is not True:
        failures.append("mutations must require an explicit environment")
    if data.get("independent_post_deploy_probes") is not True:
        failures.append("both intended and protected environments require independent probes")
    if data.get("contains_secret_values") is not False:
        failures.append("manifest must not contain secret values")
    verdict = "READY" if not failures else "REFUSED"
    print(json.dumps({"verdict": verdict, "failures": failures}, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
