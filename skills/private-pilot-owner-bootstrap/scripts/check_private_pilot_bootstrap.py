#!/usr/bin/env python3
"""Validate a protected one-owner private pilot bootstrap record."""

import json
import sys
from pathlib import Path


TESTS = {"valid_sign_in", "wrong_password", "revoked_grant", "tenant_isolation", "scope_denial", "failure_cleanup"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_private_pilot_bootstrap.py RECORD.json", file=sys.stderr)
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
    if data.get("schema") != "private-pilot-owner-bootstrap.v1":
        failures.append("unsupported schema")
    target = data.get("target_state")
    if target not in {"ready_for_bootstrap", "bootstrap_verified"}:
        failures.append("target_state must be ready_for_bootstrap or bootstrap_verified")
    subject = data.get("subject", {})
    if not isinstance(subject, dict):
        failures.append("subject must be an object")
        subject = {}
    for field in ("repository", "source_sha", "deployment_id", "environment"):
        if not subject.get(field):
            failures.append(f"subject.{field} is required")
    for field in ("rollout_converged", "auth_hardening_deployed_before_account", "provider_readback"):
        if data.get(field) is not True:
            failures.append(f"{field} must be true")

    protected = data.get("protected_environment", {})
    if not isinstance(protected, dict):
        failures.append("protected_environment must be an object")
        protected = {}
    if not protected.get("name"):
        failures.append("protected environment name is required")
    for field in ("exact_target", "branch_restriction", "approval_recorded"):
        if protected.get(field) is not True:
            failures.append(f"protected_environment.{field} must be true")

    refs = data.get("secret_refs", {})
    if not isinstance(refs, dict):
        failures.append("secret_refs must be an object")
        refs = {}
    for field in ("owner_email_ref", "password_hash_ref", "database_uri_ref"):
        if not refs.get(field):
            failures.append(f"secret_refs.{field} is required")
    if refs.get("password_hash_scheme") not in {"bcrypt", "argon2id"}:
        failures.append("password hash scheme must be bcrypt or argon2id")
    if data.get("contains_secret_values") is not False:
        failures.append("record must not contain secret values")

    workflow = data.get("workflow", {})
    if not isinstance(workflow, dict):
        failures.append("workflow must be an object")
        workflow = {}
    if workflow.get("maximum_uses") != 1:
        failures.append("workflow maximum_uses must be one")
    for field in ("manual_only", "idempotent", "cleanup_on_failure", "sanitized_receipt"):
        if workflow.get(field) is not True:
            failures.append(f"workflow.{field} must be true")

    account = data.get("account", {})
    if not isinstance(account, dict):
        failures.append("account must be an object")
        account = {}
    if account.get("planned_owner_count") != 1 or account.get("role") != "owner":
        failures.append("plan must create exactly one product-local owner")
    if any(account.get(field) is not False for field in ("provider_admin", "platform_admin", "separate_tester")):
        failures.append("pilot owner must not be a provider admin, platform admin, or separate tester")
    approved = account.get("approved_scopes", [])
    granted = account.get("granted_scopes", [])
    approved_is_valid = (
        isinstance(approved, list)
        and bool(approved)
        and all(isinstance(scope, str) and scope for scope in approved)
        and len(approved) == len(set(approved))
    )
    if not approved_is_valid or granted != approved:
        failures.append("granted scopes must exactly equal the unique non-empty approved scope list")

    tests = data.get("tests", {})
    if not isinstance(tests, dict):
        failures.append("tests must be an object")
        tests = {}
    if set(tests) != TESTS:
        failures.append("all required positive, refusal, isolation, and cleanup tests must be recorded")
    if target == "ready_for_bootstrap":
        if account.get("current_owner_count") != 0 or account.get("workspace_count") != 0:
            failures.append("ready_for_bootstrap requires zero current owners and workspaces")
        if any(status != "planned" for status in tests.values()):
            failures.append("ready_for_bootstrap tests must be planned")
        if data.get("execution_receipt_ref") not in {None, ""}:
            failures.append("ready_for_bootstrap must not claim an execution receipt")
    elif target == "bootstrap_verified":
        if account.get("current_owner_count") != 1 or account.get("workspace_count") != 1:
            failures.append("bootstrap_verified requires exactly one owner and one workspace")
        if any(status != "pass" for status in tests.values()):
            failures.append("every bootstrap verification test must pass")
        if not data.get("execution_receipt_ref"):
            failures.append("bootstrap_verified requires a sanitized execution receipt reference")
    if data.get("failure_cleanup_user_count") != 0:
        failures.append("failure cleanup must restore the product user count to zero")

    if failures:
        verdict = "REFUSED"
    elif target == "ready_for_bootstrap":
        verdict = "READY_FOR_OWNER"
    else:
        verdict = "BOOTSTRAP_VERIFIED"
    print(json.dumps({"verdict": verdict, "subject": subject, "failures": failures}, indent=2))
    return 0 if verdict != "REFUSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
