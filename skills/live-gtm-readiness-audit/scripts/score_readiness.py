#!/usr/bin/env python3
"""Score a time-bounded GTM readiness claim ledger."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ALLOWED_STATUSES = {"verified", "risky", "unproven", "contradicted", "stale"}
MULTIPLIERS = {
    "verified": 1.0,
    "risky": 0.5,
    "stale": 0.25,
    "unproven": 0.0,
    "contradicted": 0.0,
}


def parse_time(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError(f"timestamp must include a timezone: {value}")
    return parsed.astimezone(timezone.utc)


def load_input(path: str) -> dict[str, Any]:
    if path == "-":
        data = json.load(sys.stdin)
    else:
        with Path(path).open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    return data


def validate_claim(claim: Any, index: int) -> dict[str, Any]:
    if not isinstance(claim, dict):
        raise ValueError(f"claims[{index}] must be an object")
    for key in ("id", "claim", "status", "weight"):
        if key not in claim:
            raise ValueError(f"claims[{index}] is missing {key}")
    if not isinstance(claim["id"], str) or not claim["id"].strip():
        raise ValueError(f"claims[{index}].id must be a non-empty string")
    if claim["status"] not in ALLOWED_STATUSES:
        raise ValueError(f"claims[{index}].status is invalid: {claim['status']}")
    if isinstance(claim["weight"], bool) or not isinstance(claim["weight"], (int, float)):
        raise ValueError(f"claims[{index}].weight must be numeric")
    if claim["weight"] <= 0:
        raise ValueError(f"claims[{index}].weight must be greater than zero")
    return claim


def effective_status(claim: dict[str, Any], now: datetime) -> tuple[str, bool]:
    status = claim["status"]
    observed_at = claim.get("observed_at")
    max_age_hours = claim.get("max_age_hours")
    if observed_at is None or max_age_hours is None:
        return status, False
    if isinstance(max_age_hours, bool) or not isinstance(max_age_hours, (int, float)):
        raise ValueError(f"claim {claim['id']} max_age_hours must be numeric")
    if max_age_hours < 0:
        raise ValueError(f"claim {claim['id']} max_age_hours must not be negative")
    age_hours = (now - parse_time(observed_at)).total_seconds() / 3600
    if age_hours < 0:
        raise ValueError(f"claim {claim['id']} observed_at is later than the audit time")
    if age_hours > max_age_hours and status in {"verified", "risky"}:
        return "stale", True
    return status, False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON ledger path, or - for stdin")
    parser.add_argument("--now", help="ISO-8601 audit time for reproducible freshness checks")
    args = parser.parse_args()

    try:
        data = load_input(args.input)
        now_value = args.now or data.get("observed_at")
        now = parse_time(now_value) if now_value else datetime.now(timezone.utc)
        claims_value = data.get("claims")
        if not isinstance(claims_value, list) or not claims_value:
            raise ValueError("claims must be a non-empty array")
        claims = [validate_claim(item, index) for index, item in enumerate(claims_value)]
        ids = [claim["id"] for claim in claims]
        duplicates = sorted(item for item, count in Counter(ids).items() if count > 1)
        if duplicates:
            raise ValueError(f"duplicate claim ids: {', '.join(duplicates)}")
        threshold = data.get("launch_threshold", 70)
        if isinstance(threshold, bool) or not isinstance(threshold, (int, float)):
            raise ValueError("launch_threshold must be numeric")
        if not 0 <= threshold <= 100:
            raise ValueError("launch_threshold must be between 0 and 100")

        evaluated: list[dict[str, Any]] = []
        earned = 0.0
        total = 0.0
        critical_blockers: list[str] = []
        required_blockers: list[str] = []
        critical_contradictions: list[str] = []

        for claim in claims:
            status, became_stale = effective_status(claim, now)
            weight = float(claim["weight"])
            points = weight * MULTIPLIERS[status]
            total += weight
            earned += points
            if claim.get("critical") and status != "verified":
                critical_blockers.append(claim["id"])
            if claim.get("required") and status != "verified":
                required_blockers.append(claim["id"])
            if claim.get("critical") and status == "contradicted":
                critical_contradictions.append(claim["id"])
            evaluated.append(
                {
                    "id": claim["id"],
                    "surface": claim.get("surface"),
                    "declared_status": claim["status"],
                    "effective_status": status,
                    "became_stale": became_stale,
                    "weight": weight,
                    "earned_points": points,
                    "critical": bool(claim.get("critical", False)),
                    "required": bool(claim.get("required", False)),
                }
            )

        score = round((earned / total) * 100, 1)
        if critical_contradictions:
            verdict = "no-go"
        elif score >= threshold and not critical_blockers and not required_blockers:
            verdict = "go"
        else:
            verdict = "hold"

        output = {
            "audit_id": data.get("audit_id"),
            "evaluated_at": now.isoformat().replace("+00:00", "Z"),
            "score": score,
            "threshold": threshold,
            "verdict": verdict,
            "earned_weight": round(earned, 3),
            "total_weight": round(total, 3),
            "critical_blockers": sorted(critical_blockers),
            "required_blockers": sorted(required_blockers),
            "critical_contradictions": sorted(critical_contradictions),
            "status_counts": dict(sorted(Counter(item["effective_status"] for item in evaluated).items())),
            "claims": evaluated,
        }
        json.dump(output, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"readiness scoring failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
