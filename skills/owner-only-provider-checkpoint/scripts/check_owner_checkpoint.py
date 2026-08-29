#!/usr/bin/env python3
"""Validate that an owner-only provider checkpoint is precise and bounded."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any


def check(value: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(value.get("checkpoint_id"), str) or not value.get("checkpoint_id"):
        errors.append("checkpoint_id is required")
    if not isinstance(value.get("owner_identity"), str) or not value.get("owner_identity"):
        errors.append("owner_identity is required")
    expiry = value.get("expires_at")
    try:
        parsed = dt.datetime.fromisoformat(expiry.replace("Z", "+00:00")) if isinstance(expiry, str) else None
        if parsed is None or parsed.tzinfo is None:
            raise ValueError
        if parsed <= dt.datetime.now(dt.timezone.utc):
            errors.append("expires_at must be in the future")
    except ValueError:
        errors.append("expires_at must be a timezone-aware ISO timestamp")
    actions = value.get("actions")
    if not isinstance(actions, list) or not actions:
        errors.append("actions must be a non-empty array")
        actions = []
    for index, action in enumerate(actions):
        if not isinstance(action, dict):
            errors.append(f"actions[{index}] must be an object")
            continue
        for field in ("id", "provider", "target", "account", "operation", "external_effect", "consent_text"):
            if not isinstance(action.get(field), str) or not action.get(field):
                errors.append(f"actions[{index}].{field} is required")
        scopes = action.get("scopes")
        if not isinstance(scopes, list) or not all(isinstance(item, str) and item for item in scopes):
            errors.append(f"actions[{index}].scopes must be a string array")
        if action.get("maximum_uses") != 1:
            errors.append(f"actions[{index}].maximum_uses must equal 1")
        if action.get("owner_confirmation_required") is not True:
            errors.append(f"actions[{index}] must require owner confirmation")
        evidence = action.get("evidence_after")
        if not isinstance(evidence, list) or not evidence:
            errors.append(f"actions[{index}].evidence_after is required")
    excluded = value.get("excluded_actions")
    if not isinstance(excluded, list) or not excluded or not all(isinstance(item, str) and item for item in excluded):
        errors.append("excluded_actions must be a non-empty string array")
    return {"verdict": "READY_FOR_OWNER" if not errors else "REFUSED", "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", type=Path)
    args = parser.parse_args()
    try:
        value = json.loads(args.checkpoint.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"verdict": "REFUSED", "errors": [str(exc)]}))
        return 2
    if not isinstance(value, dict):
        print(json.dumps({"verdict": "REFUSED", "errors": ["checkpoint must be an object"]}))
        return 2
    result = check(value)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["verdict"] == "READY_FOR_OWNER" else 1


if __name__ == "__main__":
    sys.exit(main())
