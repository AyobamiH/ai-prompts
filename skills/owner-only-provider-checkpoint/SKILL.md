---
name: owner-only-provider-checkpoint
description: "Prepare one precise, time-bounded checkpoint for provider actions that only the verified account owner can authorize, while completing all safe preparation first. Use for OAuth consent, account grants, icon uploads, publisher attestations, review submission, publication, billing acceptance, or other browser and provider steps whose legal or security confirmation cannot be delegated."
---

# Owner Only Provider Checkpoint

Minimize interruption without blurring consent. Batch only actions whose targets, scopes, effects, and exclusions are already known.

## Workflow

1. Complete all read-only inspection, draft preparation, validation, deployment, and evidence gathering that does not require owner confirmation.
2. Identify each unavoidable owner action and why technical delegation is unavailable or inappropriate.
3. Resolve the exact provider, account, app or draft, operation, scopes, external effect, reversibility, expiry, and maximum uses.
4. Separate actions that can be approved together from actions requiring a later fresh decision. Final legal attestations, review submission, publication, spending, and broad scope grants should remain separate when their consequences differ.
5. Present one short checkpoint listing what approval will do, what it will not do, the secure surface the owner will use, and what verification follows.
6. For sign-in and credentials, use only the provider's advertised secure authentication surface. Never ask the owner to paste credentials or codes into chat.
7. After approval, perform only the named actions. Stop if the provider, account, target, scope, or consequence differs.
8. Verify each effect and report any remaining owner gate. Do not infer publication from a saved draft or consent from a loaded page.

## Checkpoint quality

The owner should be able to answer once without guessing. Avoid repeated prompts caused by incomplete preparation, but never pre-authorize a future unknown action.

## Hard boundaries

- Access to an account does not imply consent to new scopes or public publication.
- Approval to save a draft does not authorize review submission.
- Approval to submit does not authorize accepting changed terms later.
- Approval expires when its named target, payload, scopes, or provider state changes.
- Failed or expired OAuth transactions require a fresh consent checkpoint.

Use [references/checkpoint-contract.md](references/checkpoint-contract.md) to draft the request. Run `python scripts/check_owner_checkpoint.py CHECKPOINT.json` before presenting a complex checkpoint.
