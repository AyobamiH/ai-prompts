#!/usr/bin/env python3
"""Validate explicit deployment and secret targets across environments."""

import json
import sys
from pathlib import Path


REQUIRED = {"name", "providerAccount", "service", "config", "endpoint", "deployWorkflow", "deployTrigger", "credentialSource", "secretTarget", "preflightTargetAssertion", "liveProbes"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_environment_isolation.py MANIFEST.json", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    failures = []
    if data.get("schema") != "environment-isolation.v1":
        failures.append("unsupported schema")
    environments = data.get("environments", [])
    if len(environments) < 2:
        failures.append("at least two environments are required")
    for env in environments:
        missing = sorted(field for field in REQUIRED if not env.get(field))
        if missing:
            failures.append(f"environment {env.get('name')} missing: {', '.join(missing)}")
        if env.get("preflightTargetAssertion") is not True:
            failures.append(f"environment {env.get('name')} lacks a preflight target assertion")
    for field in ("service", "config", "endpoint", "credentialSource", "secretTarget"):
        values = [env.get(field) for env in environments]
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
