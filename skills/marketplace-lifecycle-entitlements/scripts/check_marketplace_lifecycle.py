#!/usr/bin/env python3
"""Validate marketplace lifecycle and authority-separation invariants."""

import json
import sys
from pathlib import Path


ACTIONS = {"purchased", "changed", "cancelled", "pending_change", "pending_change_cancelled"}
RECEIPT = {"schema", "deliveryId", "action", "duplicate", "stale", "currentState", "currentEffectiveAt"}
TESTS = {"invalid_signature", "signed_ping_no_effect", "duplicate", "stale", "all_transitions", "cancellation"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_marketplace_lifecycle.py MANIFEST.json", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    failures = []
    if data.get("schema") != "marketplace-lifecycle.v1":
        failures.append("unsupported schema")
    for field in ("raw_body_signature_required", "marketplace_secret_isolated", "delivery_idempotency", "monotonic_effective_time"):
        if data.get(field) is not True:
            failures.append(f"{field} must be true")
    missing_actions = sorted(ACTIONS - set(data.get("actions", [])))
    if missing_actions:
        failures.append("missing actions: " + ", ".join(missing_actions))
    if data.get("purchase_grants_repository_authority") is not False:
        failures.append("purchase must not grant repository authority")
    if data.get("signed_ping_changes_entitlement") is not False:
        failures.append("signed ping must not change entitlement")
    if set(data.get("receipt_fields", [])) != RECEIPT:
        failures.append("receipt fields must match the privacy-minimal contract exactly")
    forbidden = {"accountId", "accountLogin", "planId", "planName", "secret", "token"}
    if set(data.get("receipt_fields", [])) & forbidden:
        failures.append("receipt exposes protected identity or credentials")
    missing_tests = sorted(TESTS - set(data.get("tests", [])))
    if missing_tests:
        failures.append("missing tests: " + ", ".join(missing_tests))
    verdict = "READY" if not failures else "REFUSED"
    print(json.dumps({"verdict": verdict, "failures": failures}, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
