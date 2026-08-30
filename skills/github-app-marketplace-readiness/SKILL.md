---
name: github-app-marketplace-readiness
description: "Prepare and verify a GitHub App for Marketplace without confusing a saved listing, accepted agreement, configured webhook, submitted review, approval, and public publication. Use when setting up Marketplace metadata, permissions, installation scope, webhook signing, billing or legal declarations, owner checkpoints, or exact provider readback for a GitHub App listing."
---

# GitHub App Marketplace Readiness

Treat App configuration, a Marketplace draft, agreement acceptance, review, approval, and publication as separate claims. Complete technical preparation first, but reserve legal declarations, spending decisions, changed permissions, submission, and publication for the verified owner.

## Workflow

1. Resolve one immutable App subject: App ID, slug, owner, listing draft or revision, intended release, and the exact installation policy being evaluated.
2. Read back the live App configuration. Compare expected and observed permissions, subscribed events, callback URLs, setup URL, webhook URL, public profile, and installation scope. Do not infer configuration from repository files alone.
3. Minimize permissions and repository reach. Preserve the user's selected-repository or PR-only boundary; any broader permission or installation scope requires a new explicit decision.
4. Verify public support, privacy, terms, deletion or revocation, documentation, branding, contact, and pricing surfaces against the same App identity.
5. Close webhook signing safely: configure one high-entropy value through secure provider surfaces, keep only secret references in evidence, update both producer and verifier, then observe one signed delivery and rejection of an invalid signature. A stored repository secret alone does not prove the App webhook uses it.
6. Fetch the current GitHub Marketplace agreement and form language before presenting legal or business choices. Do not infer trader, tax, territorial, or consumer-law status from residence, company type, revenue, or tax thresholds. The owner supplies and accepts those declarations.
7. Test install, selected-repository selection when applicable, permission display, setup or OAuth handoff, webhook delivery, repository removal, suspension, and uninstall or revocation. Do not use a production repository for destructive tests.
8. Prepare a short owner checkpoint for the exact outstanding provider actions. Saving the webhook, accepting terms, updating a listing, submitting for review, and publishing are separate effects unless the provider explicitly combines them and the owner approves that combined effect.
9. After each action, read back the provider state. Report only `DRAFT_SAVED`, `OWNER_ACTION_READY`, `READY_FOR_REVIEW`, or `PUBLISHED_VERIFIED` when the corresponding evidence exists.
10. Record remaining blockers without retrying ambiguous writes. If a webhook update, review submission, or publication acknowledgement is uncertain, reconcile by readback before another mutation.

## Refuse or stop when

- A credential, webhook secret, private key, token, code, cookie, or full signed payload would enter chat, logs, source control, screenshots, or a readiness record.
- The observed permissions, events, installation scope, App identity, listing identity, or target account differ from the approved subject.
- A legal or trader declaration is being guessed on the owner's behalf.
- The request would push to a default branch, merge, deploy, publish, or contribute upstream without explicit authority.
- A saved draft, accepted agreement, configured secret, submitted review, or approval is being presented as public publication.

Use [references/readiness-record.md](references/readiness-record.md) for the evidence model. Run `python scripts/check_marketplace_readiness.py MANIFEST.json` before presenting a readiness or publication claim.
