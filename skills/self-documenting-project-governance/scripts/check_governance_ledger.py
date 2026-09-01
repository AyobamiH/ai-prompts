#!/usr/bin/env python3
"""Validate durable work and evidence records for self-documenting governance."""

import json
import sys
from pathlib import Path


WORK_FIELDS = {"id", "title", "stream", "status", "owner", "lastUpdated", "staleDate", "nextAction", "waitCondition", "reentryCondition", "dependencies", "evidenceIds"}
EVIDENCE_FIELDS = {"id", "date", "subject", "situation", "verification", "accountability", "outcome", "content", "measurement"}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_governance_ledger.py LEDGER.json", file=sys.stderr)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    failures = []
    if data.get("schema") != "project-governance-ledger.v1":
        failures.append("unsupported schema")
    work = data.get("work", [])
    evidence = data.get("evidence", [])
    work_ids = [item.get("id") for item in work]
    evidence_ids = [item.get("id") for item in evidence]
    if len(work_ids) != len(set(work_ids)) or None in work_ids:
        failures.append("work IDs must be present and unique")
    if len(evidence_ids) != len(set(evidence_ids)) or None in evidence_ids:
        failures.append("evidence IDs must be present and unique")
    for item in work:
        missing = sorted(field for field in WORK_FIELDS if field not in item)
        if missing:
            failures.append(f"work {item.get('id')} missing: {', '.join(missing)}")
        if item.get("status") == "complete" and not item.get("evidenceIds"):
            failures.append(f"complete work {item.get('id')} has no evidence")
        unknown = sorted(set(item.get("evidenceIds", [])) - set(evidence_ids))
        if unknown:
            failures.append(f"work {item.get('id')} references unknown evidence: {', '.join(unknown)}")
    for item in evidence:
        missing = sorted(field for field in EVIDENCE_FIELDS if field not in item)
        if missing:
            failures.append(f"evidence {item.get('id')} missing: {', '.join(missing)}")
    if data.get("generated_views_verified") is not True or data.get("governance_impact_gate") is not True:
        failures.append("generated views and governance-impact gate must be verified")
    serialized = json.dumps(data).lower()
    if any(marker in serialized for marker in ("private_key", "access_token", "client_secret", "api_key")):
        failures.append("ledger contains a credential-shaped field")
    verdict = "READY" if not failures else "REFUSED"
    print(json.dumps({"verdict": verdict, "failures": failures}, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
