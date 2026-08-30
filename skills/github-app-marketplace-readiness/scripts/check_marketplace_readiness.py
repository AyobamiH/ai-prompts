#!/usr/bin/env python3
"""Validate a secret-safe GitHub App Marketplace readiness manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


BASE_GATES = {
    "app_identity",
    "public_profile",
    "trust_and_support_pages",
    "callback_and_webhook_urls",
    "webhook_secret_configured",
    "permission_model",
    "installation_policy",
}
TARGET_GATES = {
    "draft_saved": BASE_GATES,
    "owner_action_ready": BASE_GATES | {"owner_checkpoint"},
    "review_ready": BASE_GATES
    | {
        "marketplace_agreement",
        "listing_content",
        "billing_and_legal_declarations",
        "webhook_delivery",
        "install_uninstall_test",
        "release_validation",
    },
    "published_verified": BASE_GATES
    | {
        "marketplace_agreement",
        "listing_content",
        "billing_and_legal_declarations",
        "webhook_delivery",
        "install_uninstall_test",
        "release_validation",
        "review_approval",
        "public_listing_readback",
    },
}
VERDICTS = {
    "draft_saved": "DRAFT_SAVED",
    "owner_action_ready": "OWNER_ACTION_READY",
    "review_ready": "READY_FOR_REVIEW",
    "published_verified": "PUBLISHED_VERIFIED",
}
FORBIDDEN_KEYS = {
    "secret",
    "secret_value",
    "webhook_secret",
    "token",
    "access_token",
    "refresh_token",
    "client_secret",
    "private_key",
    "authorization_code",
    "cookie",
    "signed_payload",
}


def sensitive_paths(value: Any, path: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key.lower() in FORBIDDEN_KEYS:
                found.append(child_path)
            found.extend(sensitive_paths(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(sensitive_paths(child, f"{path}[{index}]"))
    return found


def string_map(value: Any, label: str, errors: list[str]) -> dict[str, str]:
    if not isinstance(value, dict) or not all(
        isinstance(key, str) and key and isinstance(item, str) and item
        for key, item in value.items()
    ):
        errors.append(f"{label} must be an object of non-empty string values")
        return {}
    return value


def string_list(value: Any, label: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        errors.append(f"{label} must be an array of non-empty strings")
        return []
    return value


def check(value: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    subject = value.get("app_subject")
    target = value.get("target_state")
    if not isinstance(subject, str) or not subject:
        errors.append("app_subject must be a non-empty string")
    if target not in TARGET_GATES:
        errors.append("target_state must be draft_saved, owner_action_ready, review_ready, or published_verified")

    sensitive = sensitive_paths(value)
    if sensitive:
        errors.append("manifest contains forbidden sensitive fields: " + ", ".join(sorted(sensitive)))

    expected_scope = value.get("expected_installation_scope")
    observed_scope = value.get("observed_installation_scope")
    if not isinstance(expected_scope, str) or not expected_scope:
        errors.append("expected_installation_scope must be a non-empty string")
    if observed_scope != expected_scope:
        errors.append("observed installation scope does not match the approved scope")

    expected_permissions = string_map(value.get("expected_permissions"), "expected_permissions", errors)
    observed_permissions = string_map(value.get("observed_permissions"), "observed_permissions", errors)
    if observed_permissions != expected_permissions:
        errors.append("observed permissions do not exactly match expected permissions")

    expected_events = string_list(value.get("expected_events"), "expected_events", errors)
    observed_events = string_list(value.get("observed_events"), "observed_events", errors)
    if sorted(set(observed_events)) != sorted(set(expected_events)):
        errors.append("observed events do not exactly match expected events")

    gates = value.get("gates")
    if not isinstance(gates, dict):
        errors.append("gates must be an object")
        gates = {}
    required = TARGET_GATES.get(target, set())
    for name in sorted(required):
        gate = gates.get(name)
        if not isinstance(gate, dict):
            errors.append(f"missing gate: {name}")
            continue
        if gate.get("subject") != subject:
            errors.append(f"gate {name} has a subject mismatch")
        if gate.get("status") != "pass":
            errors.append(f"gate {name} did not pass")
        evidence_ref = gate.get("evidence_ref")
        if not isinstance(evidence_ref, str) or not evidence_ref:
            errors.append(f"gate {name} lacks evidence_ref")
        elif evidence_ref.startswith(("http://", "https://")) and urlsplit(evidence_ref).query:
            errors.append(f"gate {name} evidence_ref must not include a URL query")

    verdict = VERDICTS.get(target, "BLOCKED") if not errors else "BLOCKED"
    return {"verdict": verdict, "app_subject": subject, "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "BLOCKED", "errors": [str(exc)]}))
        return 2
    if not isinstance(value, dict):
        print(json.dumps({"verdict": "BLOCKED", "errors": ["manifest must be an object"]}))
        return 2
    result = check(value)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["verdict"] != "BLOCKED" else 1


if __name__ == "__main__":
    sys.exit(main())
