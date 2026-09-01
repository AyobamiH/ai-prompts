---
name: marketplace-lifecycle-entitlements
description: "Implement and verify signed marketplace purchase lifecycle ingestion, monotonic entitlement state, idempotent redelivery, privacy-minimal receipts, and strict separation from product authority. Use when a GitHub App or other marketplace must process purchases, plan changes, pending changes, cancellations, retries, or stale events without granting repository or execution rights from billing alone."
---

# Marketplace Lifecycle Entitlements

Treat marketplace state as a billing entitlement input, not as standing authority to access repositories, execute work, or publish changes.

## Workflow

1. Define a versioned entitlement state machine and every provider action before accepting live events.
2. Verify the raw request body with a marketplace-specific signing secret before parsing or mutating state. Keep this secret separate from OAuth, session, GitHub App, and deployment credentials.
3. Validate event name, action, delivery identifier, account identity, plan identity, and effective time. Reject unknown actions and malformed dates.
4. Deduplicate by provider delivery identifier. A redelivery returns the current stored state without reapplying the effect.
5. Apply events monotonically by effective time. Record an older event as stale without rolling the entitlement backward.
6. Cover purchase, plan change, cancellation, pending change, and pending-change cancellation. Define whether each state is active, scheduled, grace-limited, or inactive.
7. Keep entitlement, installation, selected-repository registration, OAuth connection, execution admission, and maintenance authority as separate gates. A signed purchase or ping must not add a repository or create an execution grant.
8. Return a versioned privacy-minimal receipt containing only delivery identity, action, duplicate/stale semantics, current state, and current effective time. Exclude account and plan identity unless the caller is separately authorised to view them.
9. Test invalid signatures, signed pings with no entitlement effect, duplicates, stale events, every transition, and cancellation. Verify live provider delivery and runtime state separately from unit tests and deployment status.

## Completion boundary

Implementation, exact CI, production deployment, isolated development deployment, live delivery, resulting entitlement, review approval, and public listing are different states. Do not collapse them into “Marketplace complete.”

Read [references/lifecycle-contract.md](references/lifecycle-contract.md) for the state and receipt contract. Run `python scripts/check_marketplace_lifecycle.py MANIFEST.json` before live validation.
