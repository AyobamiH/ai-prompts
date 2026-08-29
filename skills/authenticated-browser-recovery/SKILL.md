---
name: authenticated-browser-recovery
description: "Recover an authorised authenticated-browser workflow after a tab, composer, form, upload, or connection loses state. Use for live site actions that already have a frozen target and approval. Do not use it as a fallback for ordinary public web research or to bypass login, anti-bot, permission, or provider restrictions."
---

# Authenticated Browser Recovery

Restore the same authorised action without changing its consequence or creating duplicate side effects.

## Preconditions

Require:

- exact provider and account identity;
- exact target page or object;
- frozen approved payload or bounded mutation;
- known last confirmed state;
- one-write or idempotency rule;
- expected readback evidence.

If any of these are unknown, inspect read-only state first. Stop on account mismatch, permission loss, unexpected terms, anti-bot challenge, or a request for new authority.

## Recovery ladder

1. Reconnect to the existing authenticated session and inspect the current page, modal, composer, and provider messages.
2. Determine whether the prior action was only staged, definitely submitted, definitely rejected, or ambiguous.
3. If staged and unchanged, restore only missing fields from the frozen payload. Do not regenerate copy or substitute assets.
4. Revalidate all visible fields, hidden account context, CTA, destination, media order, and submit availability.
5. Submit once only when no prior write may have succeeded.
6. Read back the provider object or public page. Capture the canonical URL or provider state.
7. Preserve screenshots or receipts needed to explain a blocked or ambiguous outcome.

For media failures, inspect actual file type, dimensions, size, and upload state. Prefer the provider's crop workflow with the full-resolution source when pre-cropped derivatives repeatedly fail. Preserve the current live asset until the replacement has saved successfully.

Do not request control from the user merely because a tab reloaded. Request intervention only for authentication choices, acceptance of terms, CAPTCHA or anti-bot challenges, missing permissions, or consequences outside the existing approval.

Read [references/recovery-runbook.md](references/recovery-runbook.md) for state classification, retry limits, and evidence capture.
