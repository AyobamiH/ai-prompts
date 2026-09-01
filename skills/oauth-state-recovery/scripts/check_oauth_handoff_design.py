#!/usr/bin/env python3
"""Fail closed on missing OAuth handoff security invariants."""

import json
import sys
from pathlib import Path


REQUIRED_TESTS = {
    "valid", "expired", "tampered", "concurrent", "cookie_free",
    "cross_region", "provider_shaped", "single_use",
}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_oauth_handoff_design.py DESIGN.json", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    failures = []
    if data.get("schema") != "oauth-handoff-design.v1":
        failures.append("unsupported schema")
    if data.get("state_entropy_bits", 0) < 128 or data.get("csrf_entropy_bits", 0) < 128:
        failures.append("state and CSRF proofs require at least 128 bits of entropy")
    ttl = data.get("ttl_seconds")
    if not isinstance(ttl, int) or not 60 <= ttl <= 900:
        failures.append("ttl_seconds must be between 60 and 900")
    for field in ("client_bound", "redirect_bound", "scopes_bound", "single_use", "authenticated_state"):
        if data.get(field) is not True:
            failures.append(f"{field} must be true")
    if data.get("storage_model") not in {"strongly_consistent", "sealed_transaction"}:
        failures.append("storage_model must survive immediate cross-request handoff")
    if data.get("storage_model") == "sealed_transaction":
        if data.get("plain_record_projection") is not True or data.get("domain_separated_key") is not True:
            failures.append("sealed transactions require a plain record and domain-separated key")
    tests = set(data.get("tests", []))
    missing = sorted(REQUIRED_TESTS - tests)
    if missing:
        failures.append("missing tests: " + ", ".join(missing))
    if data.get("records_raw_secrets") is not False:
        failures.append("raw state, proofs, codes, tokens, cookies, and keys must not be recorded")
    verdict = "READY" if not failures else "REFUSED"
    print(json.dumps({"verdict": verdict, "failures": failures}, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
