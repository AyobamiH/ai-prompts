#!/usr/bin/env python3
"""Reconcile an immutable subject across distribution-channel states."""

import json
import sys
from pathlib import Path


STATES = [
    "DRAFT",
    "DEVELOPER_MODE_VERIFIED",
    "SUBMITTED",
    "IN_REVIEW",
    "APPROVED",
    "PUBLISHED",
    "DISCOVERABLE",
    "INSTALLED",
    "LIVE_OUTCOME_VERIFIED",
]
SURFACES = {
    "DRAFT": {"repository", "provider_control"},
    "DEVELOPER_MODE_VERIFIED": {"developer_mode", "clean_consumer"},
    "SUBMITTED": {"provider_control"},
    "IN_REVIEW": {"provider_control"},
    "APPROVED": {"provider_control"},
    "PUBLISHED": {"provider_control"},
    "DISCOVERABLE": {"public_directory"},
    "INSTALLED": {"clean_consumer"},
    "LIVE_OUTCOME_VERIFIED": {"runtime_receipt"},
}


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: reconcile_distribution_state.py RECORD.json", file=sys.stderr)
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
    unproven = []
    if data.get("schema") != "distribution-channel-state.v1":
        failures.append("unsupported schema")
    subject_id = data.get("subject_id")
    if not isinstance(subject_id, str) or not subject_id:
        failures.append("subject_id must be a non-empty immutable identifier")
    subject = data.get("subject", {})
    if not isinstance(subject, dict):
        failures.append("subject must be an object")
        subject = {}
    for field in ("product", "channel", "artifact_type", "version", "source_sha", "deployed_sha"):
        if not subject.get(field):
            failures.append(f"subject.{field} is required")
    target = data.get("target_state")
    if target not in STATES:
        failures.append("target_state is unsupported")
        target_index = -1
    else:
        target_index = STATES.index(target)

    if data.get("provider_readback_at_execution_time") is not True:
        unproven.append("fresh provider readback is missing")
    if data.get("provider_mutations_performed") is not False:
        failures.append("provider reconciliation must not perform provider mutations")
    if data.get("repository_ledger_reconciled_without_promotion") is not True:
        unproven.append("repository ledger was not reconciled without promotion")
    if data.get("owner_preview_used_as_public_proof") is not False:
        failures.append("owner preview cannot be used as public proof")
    contradictions = data.get("contradictions")
    if contradictions != []:
        unproven.append("provider or channel contradictions remain")

    observations = data.get("observations", {})
    if not isinstance(observations, dict):
        failures.append("observations must be an object keyed by state")
        observations = {}
    if target_index >= 0:
        for state in STATES[: target_index + 1]:
            observation = observations.get(state)
            if not isinstance(observation, dict):
                unproven.append(f"{state} evidence is missing")
                continue
            if observation.get("status") != "verified":
                unproven.append(f"{state} is not verified")
            if observation.get("subject_id") != subject_id:
                unproven.append(f"{state} belongs to another subject")
            if not observation.get("evidence_ref") or not observation.get("observed_at"):
                unproven.append(f"{state} lacks an evidence reference or observation time")
            surface = observation.get("surface")
            if surface not in SURFACES[state]:
                unproven.append(f"{state} uses the wrong evidence surface")
            if state in {"SUBMITTED", "IN_REVIEW", "APPROVED", "PUBLISHED"} and observation.get("authenticated") is not True:
                unproven.append(f"{state} requires authenticated provider control")
            if state == "DISCOVERABLE" and observation.get("authenticated") is not False:
                unproven.append("DISCOVERABLE requires an unauthenticated public surface")
        for state in STATES[target_index + 1 :]:
            observation = observations.get(state)
            if isinstance(observation, dict) and observation.get("status") == "verified":
                unproven.append(f"target_state is stale because {state} is already verified")

    expected_public_claim = target_index >= STATES.index("DISCOVERABLE") if target_index >= 0 else False
    if data.get("public_discoverability_claimed") is not expected_public_claim:
        unproven.append("public discoverability claim does not match the verified target state")

    if failures:
        verdict = "REFUSED"
    elif unproven:
        verdict = "UNPROVEN"
    else:
        verdict = target
    print(json.dumps({"verdict": verdict, "subject_id": subject_id, "failures": failures, "unproven": unproven}, indent=2))
    return 0 if verdict in STATES else 1


if __name__ == "__main__":
    raise SystemExit(main())
