#!/usr/bin/env python3
"""Validate a least-authority external reviewer access manifest."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


DENIED = {"write", "execute", "approve", "merge", "deploy", "administer", "read_secrets"}
TESTS = {"authenticated_read", "write_refused", "execute_refused", "admin_refused", "revocation"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_reviewer_boundary.py ACCESS.json", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    failures = []
    if data.get("schema") != "external-reviewer-access.v1":
        failures.append("unsupported schema")
    if data.get("identity_type") != "dedicated_application_reviewer":
        failures.append("reviewer must use a dedicated application identity")
    if data.get("owner_account_reused") is not False:
        failures.append("owner or provider account must not be reused")
    if set(data.get("allowed_actions", [])) - {"read"}:
        failures.append("only read may be allowed")
    missing_denials = sorted(DENIED - set(data.get("denied_actions", [])))
    if missing_denials:
        failures.append("missing denied actions: " + ", ".join(missing_denials))
    origins = data.get("callback_origins", [])
    if not origins or any("*" in origin or not origin.startswith("https://") for origin in origins):
        failures.append("callback origins must be exact HTTPS origins without wildcards")
    if data.get("synthetic_data_only") is not True or data.get("contains_credentials") is not False:
        failures.append("review data must be synthetic and credential-free")
    try:
        expiry = datetime.fromisoformat(data.get("expires_at", "").replace("Z", "+00:00"))
        if expiry <= datetime.now(timezone.utc):
            failures.append("reviewer access is expired")
    except ValueError:
        failures.append("expires_at must be an ISO-8601 timestamp")
    if not data.get("revocation_path"):
        failures.append("revocation_path is required")
    missing_tests = sorted(TESTS - set(data.get("tests", [])))
    if missing_tests:
        failures.append("missing tests: " + ", ".join(missing_tests))
    verdict = "READY" if not failures else "REFUSED"
    print(json.dumps({"verdict": verdict, "failures": failures}, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
