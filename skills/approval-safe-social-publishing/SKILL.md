---
name: approval-safe-social-publishing
description: "Publish approved social or business-profile content through a provider API or authenticated browser while preserving one-time approval, payload immutability, idempotency, ambiguous-write reconciliation, and provider readback. Use only when the user has authorised the public write. Do not use it for drafting or unapproved publication."
---

# Approval Safe Social Publishing

Carry an approved payload to a verified provider outcome without making the user babysit harmless transport recovery.

## Approval identity

Freeze these fields before approval:

- platform and exact account;
- copy and formatting;
- ordered asset hashes;
- CTA type and destination;
- scheduled slot or immediate action;
- disclosure and audience settings.

Use `scripts/publication_fingerprint.py` to create the canonical SHA-256 fingerprint. Store the approval against that fingerprint.

Approval remains valid across a connector outage, browser reconnection, tab reload, or composer reconstruction when the frozen fields have not changed and no provider warning changes the consequence. Do not ask for the same approval again.

Fresh approval is required when copy, assets, order, CTA, destination, account, platform, audience, disclosure, or publication timing materially changes.

## Publication flow

1. Confirm the account identity, platform, approval record, payload fingerprint, write authority, and current provider state.
2. Check for an existing provider object or unresolved attempt with the same identity.
3. Validate copy, assets, destination, and platform policy immediately before the write.
4. Perform at most one provider write for the publication identity.
5. Persist the receipt or visible provider state.
6. Read the object back from the provider or public surface and compare account, copy, assets, CTA, and permalink.
7. Return one terminal or bounded state from the state machine reference.

Never wrap a public write in blind automatic retry. A timeout, connection reset, missing response, crash after submit, or uncertain provider `5xx` is an ambiguous write. Reconcile by readback or duplicate discovery before another write.

## Claim language

- `drafted`: content exists locally or in a composer.
- `submitted`: provider accepted a request but visibility is not proven.
- `submitted_for_review`: provider is reviewing it.
- `verified_published`: provider or public readback proves the expected object exists.
- `reconciliation_required`: the write outcome is ambiguous.

Do not replace these with vague "done" language.

Read [references/state-machine.md](references/state-machine.md) before any public write or retry decision. Use `authenticated-browser-recovery` when the authorised path is an authenticated UI and its state is lost.
