#!/usr/bin/env python3
"""Create or verify a canonical publication payload fingerprint."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_KEYS = {
    "platform",
    "account_id",
    "copy",
    "assets",
    "cta",
    "audience",
    "disclosure",
    "scheduled_for",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def load_input(path: str) -> dict[str, Any]:
    if path == "-":
        value = json.load(sys.stdin)
    else:
        with Path(path).open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("payload must be a JSON object")
    return value


def validate(payload: dict[str, Any]) -> None:
    missing = sorted(REQUIRED_KEYS - payload.keys())
    extra = sorted(payload.keys() - REQUIRED_KEYS)
    if missing:
        raise ValueError(f"missing frozen keys: {', '.join(missing)}")
    if extra:
        raise ValueError(f"unexpected keys must be explicitly modelled: {', '.join(extra)}")
    for key in ("platform", "account_id", "copy"):
        if not isinstance(payload[key], str) or not payload[key].strip():
            raise ValueError(f"{key} must be a non-empty string")
    if not isinstance(payload["assets"], list):
        raise ValueError("assets must be an ordered array")
    for index, asset in enumerate(payload["assets"]):
        if not isinstance(asset, dict) or set(asset) != {"id", "sha256"}:
            raise ValueError(f"assets[{index}] must contain exactly id and sha256")
        if not isinstance(asset["id"], str) or not asset["id"].strip():
            raise ValueError(f"assets[{index}].id must be a non-empty string")
        if not isinstance(asset["sha256"], str) or not SHA256.fullmatch(asset["sha256"]):
            raise ValueError(f"assets[{index}].sha256 must be a lowercase SHA-256 digest")
    if payload["cta"] is not None:
        if not isinstance(payload["cta"], dict) or set(payload["cta"]) != {"type", "destination"}:
            raise ValueError("cta must be null or contain exactly type and destination")
        if not all(isinstance(payload["cta"][key], str) and payload["cta"][key].strip() for key in ("type", "destination")):
            raise ValueError("cta type and destination must be non-empty strings")
    for key in ("audience", "disclosure", "scheduled_for"):
        if payload[key] is not None and not isinstance(payload[key], str):
            raise ValueError(f"{key} must be a string or null")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="payload JSON path, or - for stdin")
    parser.add_argument("--approved-fingerprint", help="fail when this digest does not match")
    args = parser.parse_args()

    try:
        payload = load_input(args.input)
        validate(payload)
        canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        matches = args.approved_fingerprint is None or digest == args.approved_fingerprint
        output = {
            "fingerprint": digest,
            "matches_approved": matches,
            "canonical_payload": canonical,
        }
        json.dump(output, sys.stdout, indent=2, sort_keys=True, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0 if matches else 1
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"publication fingerprint failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
