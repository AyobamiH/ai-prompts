---
name: autonomous-repository-maintenance
description: "Design bounded autonomous maintenance for selected repositories using a GitHub App, durable registry, webhooks and schedules, read-only discovery, PR-only repair, independent verification, and receipts for high-consequence actions. Use when automating dependency, documentation, CI, security, or hygiene work without granting an agent unrestricted merge or deployment authority."
---

# Autonomous Repository Maintenance

Start with one selected repository and one low-consequence maintenance class. Expand only after the closed loop is observable and recoverable.

## Architecture

Separate the maintenance source, controller, repair provider, runner, verifier, and notary. A single implementation may host several roles initially, but policy and records must preserve the boundaries.

## Workflow

1. Install a GitHub App only on explicitly selected repositories with minimal read permissions and pull-request write access when needed.
2. Maintain a durable registry of installations, repository policy, enabled maintenance classes, limits, schedules, and revocations.
3. Ingest webhooks idempotently and use schedules for reconciliation, not as the sole source of truth.
4. Discover candidate work read-only. Store evidence, deduplicate by stable subject, and apply policy before planning repairs.
5. Run the repair provider in a sandbox with path, command, time, network, and token limits.
6. Validate the patch locally and in repository CI. Never push directly to the protected branch.
7. Open a pull request with scope, rationale, commands, evidence, limitations, and machine-readable correlation identifiers.
8. Require independent verification of the exact pull-request head before recording `VERIFIED`.
9. Leave merge, deployment, and release under existing policy. If later automated, require explicit standing authority and a signed action receipt.
10. Reconcile closed, superseded, stale, or externally modified pull requests and release leases safely.

## Initial limits

- One repository and one maintenance category
- PR-only changes
- File and diff-size limits
- No workflow, policy, secret, ownership, or deployment-file changes
- No approval, merge, release, or deploy authority
- Daily action and provider-spend limits
- Human-visible kill switch and installation revocation

## Rollout

Advance from observe-only to draft PRs, then active PRs, then selected high-consequence automation. Add fleet management last. Use [references/maintenance-runbook.md](references/maintenance-runbook.md) for the rollout and incident controls.
