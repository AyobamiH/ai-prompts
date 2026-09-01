---
name: authorized-real-data-pilot
description: "Approve and evaluate a lawful, target-market-relevant real dataset without turning data access or a small pilot into product-market-fit evidence. Use when a product gate requires real records, provenance, rights, retention, deletion, no-training controls, real users, or a bounded market-evidence threshold."
---

# Authorized Real-Data Pilot

Real data is useful evidence only when its authority, purpose, handling, and market relevance are explicit.

## Workflow

1. Define the target jurisdiction, intended user, task, outcome metric, baseline, and evidence threshold before selecting data.
2. Accept only an owner-supplied, licensed, or public source with an immutable source reference, acquisition time, checksum, and provenance record. Do not use arbitrary demo records merely to unblock a gate.
3. Record the rights basis, allowed purpose, classification, schema validation, retention period, and deletion path. Minimize the dataset to fields required for the approved task.
4. Obtain separate approvals for rights, use, retention, and prohibition on shared-model training. Dataset approval is not pilot execution.
5. Keep raw records outside the evidence manifest. Preserve tenant isolation and prohibit shared training unless a later, explicit opt-in authority exists.
6. Recruit authorized real users and record completed real tasks. Preserve failures, abandonment, and negative outcomes rather than filtering them out.
7. Compare the predefined outcome with its baseline. Bind results to the exact dataset checksum and product revision.
8. Use the bounded label `MARKET_EVIDENCE_READY` only at five or more real users and ten or more completed tasks. That threshold is not proof of product-market fit.

## Outcomes

- `DATASET_APPROVED`: the dataset is lawful, relevant, minimized, and governed, but no pilot outcome is claimed.
- `PILOT_EXECUTED`: at least one authorized real user completed at least one measured task.
- `MARKET_EVIDENCE_READY`: at least five real users completed at least ten tasks with failures and baseline recorded.
- `REFUSED`: provenance, rights, approvals, retention, deletion, isolation, user authority, measurement, or claim discipline is missing.

Read [references/real-data-record.md](references/real-data-record.md) for the manifest. Run `python scripts/check_authorized_real_data_pilot.py RECORD.json` before importing data or advancing a real-data evaluation gate.
