# Governance Ledger Contract

## Work item

Every item needs a stable ID, title, stream, status, owner, last-updated date, stale date, next action, wait condition, re-entry condition, dependencies, and evidence IDs. Use explicit statuses such as `planned`, `active`, `waiting_owner`, `waiting_provider`, `blocked`, `complete`, and `cancelled`.

## Evidence story

Every evidence item needs a stable ID, date, immutable subject where available, situation, verification, accountability, outcome, content, and measurement. Record residual gaps and the difference between candidate, merged, CI-passed, deployed, live-verified, and provider-approved states.

## Governance-impact gate

Map protected path classes to required ledger streams and generated views. Reject:

- behavior changes with no durable record or validated no-impact declaration;
- generated views that differ from regeneration;
- completed items without evidence;
- deferred items without an owner, re-entry condition, or stale date;
- secrets or credential values in the ledger;
- evidence bound to a different commit, deployment, environment, or provider object.

The scheduled freshness check is read-only. It reports stale records; it does not silently change status or assign owners.
