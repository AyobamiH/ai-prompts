---
name: distribution-channel-state-reconciliation
description: "Reconcile repository, deployment, provider-review, publication, directory, installation, and runtime evidence for one immutable distribution subject. Use when an app, plugin, package, or marketplace listing is described as live even though owner preview, approval, publication, discoverability, installation, and real outcomes may differ."
---

# Distribution Channel State Reconciliation

Never collapse distribution progress into a single `live` flag.

## State chain

`DRAFT → DEVELOPER_MODE_VERIFIED → SUBMITTED → IN_REVIEW → APPROVED → PUBLISHED → DISCOVERABLE → INSTALLED → LIVE_OUTCOME_VERIFIED`

Each transition adds evidence; none is implied by a repository ledger, owner preview, earlier version, or adjacent channel.

## Workflow

1. Freeze one subject ID containing product, channel, artifact type, version, source SHA, and deployed SHA. Do not mix provider versions or substitute a moving branch.
2. Read the repository ledger and deployment state, then perform fresh authenticated provider-control readback for submission, review, approval, and publication.
3. Treat provider control as higher authority than repository assertions for provider-managed state. Preserve contradictions and lower the result to `UNPROVEN` until reconciled.
4. Verify public discoverability from an unauthenticated public directory or marketplace surface. An owner-only preview, listing-control page, or preview install count is not public evidence.
5. Verify installation from a clean consumer account or environment rather than the owner session.
6. Verify a real tool or product outcome through a subject-bound runtime receipt. A health page, successful install, or static signature does not prove the consequential outcome.
7. Record exact evidence references and observation times for every state. Require the full prefix of the state chain through the claimed target.
8. Keep provider reconciliation read-only. Repair PRs, provider submissions, settings changes, deployment, merge, and publication require their own authority and evidence.
9. Update the repository ledger only after fresh provider readback, without promoting pending or unpublished states.

## Outcomes

- The highest verified state name when every preceding state is bound to the same subject and uses the required surface.
- `UNPROVEN` when evidence is incomplete, stale, contradictory, preview-only, or belongs to another subject.
- `REFUSED` when the record is malformed or attempts to treat owner preview as public proof.

Read [references/channel-state-record.md](references/channel-state-record.md) for the surface rules. Run `python scripts/reconcile_distribution_state.py RECORD.json` before describing a listing or integration as published, discoverable, installed, or live.
