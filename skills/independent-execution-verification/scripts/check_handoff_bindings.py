#!/usr/bin/env python3
"""Check objective, subject, and verifier bindings without verifying signatures."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def digest(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(data).hexdigest()


def check(record: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    objective = record.get("objective")
    handoff = record.get("handoff")
    result = record.get("verification_result")
    trusted = record.get("trusted_verifiers")
    if not isinstance(objective, dict) or not objective:
        errors.append("objective must be a non-empty object")
        objective = {}
    if not isinstance(handoff, dict):
        errors.append("handoff must be an object")
        handoff = {}
    if not isinstance(result, dict):
        errors.append("verification_result must be an object")
        result = {}
    if not isinstance(trusted, dict):
        errors.append("trusted_verifiers must be an object")
        trusted = {}

    objective_digest = digest(objective)
    if handoff.get("objective_sha256") != objective_digest:
        errors.append("handoff objective digest mismatch")
    if result.get("objective_sha256") != objective_digest:
        errors.append("verification result objective digest mismatch")
    objective_subject = objective.get("subject")
    if not isinstance(objective_subject, dict) or not objective_subject:
        errors.append("objective subject must be a non-empty object")
    else:
        if handoff.get("subject") != objective_subject:
            errors.append("handoff subject mismatch")
        if result.get("subject") != objective_subject:
            errors.append("verification result subject mismatch")

    verifier_id = result.get("verifier_id")
    verifier = trusted.get(verifier_id) if isinstance(verifier_id, str) else None
    if not isinstance(verifier, dict):
        errors.append("verifier is not trusted")
    else:
        if result.get("algorithm") != verifier.get("algorithm"):
            errors.append("verifier algorithm mismatch")
        if result.get("key_id") != verifier.get("key_id"):
            errors.append("verifier key mismatch")
    if result.get("algorithm") != "Ed25519":
        errors.append("only Ed25519 is accepted by this contract")
    if result.get("verdict") != "VERIFIED":
        errors.append("verification verdict is not VERIFIED")
    if not isinstance(result.get("signature"), str) or not result.get("signature"):
        errors.append("signature is missing")

    return {
        "verdict": "BINDINGS_VALID" if not errors else "REFUSED",
        "objective_sha256": objective_digest,
        "errors": errors,
        "cryptographic_verification_required": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.record.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "REFUSED", "errors": [str(exc)]}))
        return 2
    if not isinstance(value, dict):
        print(json.dumps({"verdict": "REFUSED", "errors": ["record must be an object"]}))
        return 2
    result = check(value)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["verdict"] == "BINDINGS_VALID" else 1


if __name__ == "__main__":
    sys.exit(main())
