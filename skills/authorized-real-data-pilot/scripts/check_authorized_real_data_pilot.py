#!/usr/bin/env python3
"""Validate authorization and evidence boundaries for a real-data pilot."""

import json
import sys
from pathlib import Path


def nonnegative_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_authorized_real_data_pilot.py RECORD.json", file=sys.stderr)
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
    if data.get("schema") != "authorized-real-data-pilot.v1":
        failures.append("unsupported schema")
    target = data.get("target_state")
    if target not in {"dataset_approved", "pilot_executed", "market_evidence"}:
        failures.append("unsupported target_state")

    dataset = data.get("dataset", {})
    if not isinstance(dataset, dict):
        failures.append("dataset must be an object")
        dataset = {}
    for field in ("id", "jurisdiction", "source_ref", "acquired_at", "provenance_ref", "rights_basis", "allowed_purpose", "deletion_path", "classification", "approval_ref"):
        if not dataset.get(field):
            failures.append(f"dataset.{field} is required")
    if dataset.get("source_kind") not in {"owner_supplied", "licensed", "public"}:
        failures.append("dataset.source_kind must be owner_supplied, licensed, or public")
    checksum = dataset.get("checksum", "")
    if not isinstance(checksum, str) or not checksum.startswith("sha256:") or len(checksum) <= len("sha256:"):
        failures.append("dataset.checksum must be an immutable sha256 identifier")
    retention = dataset.get("retention_days")
    if not isinstance(retention, int) or isinstance(retention, bool) or not 1 <= retention <= 3650:
        failures.append("dataset.retention_days must be an integer from 1 through 3650")
    if dataset.get("schema_validation") != "pass":
        failures.append("dataset schema validation must pass")
    if dataset.get("target_market_relevance") is not True:
        failures.append("dataset must be relevant to the target market")

    approvals = data.get("approvals", {})
    if not isinstance(approvals, dict):
        failures.append("approvals must be an object")
        approvals = {}
    for field in ("rights", "use", "retention", "no_shared_training"):
        if approvals.get(field) is not True:
            failures.append(f"approvals.{field} must be true")
    for field in ("tenant_isolation", "data_minimized"):
        if data.get(field) is not True:
            failures.append(f"{field} must be true")
    for field in ("shared_training_use", "raw_records_in_manifest"):
        if data.get(field) is not False:
            failures.append(f"{field} must be false")

    evaluation = data.get("evaluation", {})
    if not isinstance(evaluation, dict):
        failures.append("evaluation must be an object")
        evaluation = {}
    for field in ("real_users", "non_founder_users", "completed_tasks"):
        if not nonnegative_int(evaluation.get(field)):
            failures.append(f"evaluation.{field} must be a non-negative integer")
    real_users = evaluation.get("real_users", -1)
    non_founder_users = evaluation.get("non_founder_users", -1)
    tasks = evaluation.get("completed_tasks", -1)
    if nonnegative_int(real_users) and nonnegative_int(non_founder_users) and non_founder_users > real_users:
        failures.append("non-founder users cannot exceed real users")
    if evaluation.get("product_market_fit_claimed") is not False:
        failures.append("this bounded pilot must not claim product-market fit")

    if target in {"pilot_executed", "market_evidence"}:
        if not evaluation.get("product_revision") or evaluation.get("dataset_checksum") != checksum:
            failures.append("evaluation must bind one product revision to the dataset checksum")
        for field in ("baseline_defined", "failures_recorded", "authorized_user_participation"):
            if evaluation.get(field) is not True:
                failures.append(f"evaluation.{field} must be true")
        if not evaluation.get("outcome_metric"):
            failures.append("evaluation.outcome_metric is required")
        if not nonnegative_int(real_users) or real_users < 1 or not nonnegative_int(tasks) or tasks < 1:
            failures.append("pilot execution requires at least one real user and completed task")
    if target == "market_evidence":
        if not nonnegative_int(real_users) or real_users < 5 or not nonnegative_int(tasks) or tasks < 10:
            failures.append("market evidence requires at least five real users and ten completed tasks")

    if failures:
        verdict = "REFUSED"
    elif target == "dataset_approved":
        verdict = "DATASET_APPROVED"
    elif target == "pilot_executed":
        verdict = "PILOT_EXECUTED"
    else:
        verdict = "MARKET_EVIDENCE_READY"
    print(json.dumps({"verdict": verdict, "dataset": dataset.get("id"), "failures": failures}, indent=2))
    return 0 if verdict != "REFUSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
