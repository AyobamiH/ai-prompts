---
name: oauth-state-recovery
description: "Diagnose and recover OAuth authorization failures caused by expired, stale, mismatched, concurrent, non-portable, or cross-request state without weakening CSRF protection. Use when a ChatGPT app, MCP server, GitHub App, or provider connection reports expired browser state, invalid state, callback mismatch, consent loops, cookie loss, cross-region read-after-write failure, or a retry that reproduces the same failure."
---

# OAuth State Recovery

Recover the transaction design that failed. Do not turn off state, CSRF, expiry, client binding, redirect binding, or scope binding merely to make a live callback succeed.

## Workflow

1. Capture the public error, attempt time, authorization host, redirect URI, client identity, deployed auth version, and handoff path without recording codes, tokens, cookies, or full state values.
2. Reproduce the original detector before changing code. Classify the failure as stale configuration, concurrent-attempt collision, cookie continuity loss, eventual-consistency read-after-write, non-portable runtime objects, callback mismatch, CSP, clock skew, or token persistence failure.
3. Inspect the full transaction boundary: issue, consent rendering, owner approval, provider redirect, callback consumption, token exchange, storage, revocation, and bounded authenticated read.
4. Choose the narrowest design that survives the actual handoff:
   - Namespace cookie-backed state per attempt when simultaneous flows overwrite one another.
   - Do not require cookie continuity when the authorised browser handoff cannot preserve it; keep a one-time random proof bound to the server-side transaction.
   - Use strongly consistent state when the next request must immediately observe a write. Do not use eventually consistent storage as a transaction lock.
   - Use an authenticated, expiring sealed transaction when cross-request storage is itself the unreliable boundary. Project provider objects to a plain versioned record before sealing.
5. Bind the transaction to the exact client, redirect URI, requested scopes, issued time, expiry, and cryptographic nonce. Use domain-separated key derivation and authenticated encryption for sealed state.
6. Preserve atomic or equivalent single-use consumption. A sealed approval token does not make a reusable callback safe; rely on a consumed transaction identifier and the provider's one-time authorization code.
7. Test valid, expired, tampered, concurrent, cookie-free, cross-region, and provider-shaped requests. Make tamper tests deterministic by changing known decoded bytes rather than assuming a character edit changes the payload.
8. Deploy the exact tested revision, start a fresh authorization transaction, and verify callback consumption, connected identity, granted scopes, revocation, and one bounded authenticated read.
9. Record the resolved cause and remove diagnostic logging that could expose sensitive values.

## Stop conditions

Stop on client, provider account, scope, redirect host, app identity, or environment drift. Also stop if the proposed recovery disables validation, exposes credentials, accepts a legal attestation, reuses an expired link, or silently widens authority.

Read [references/oauth-recovery-matrix.md](references/oauth-recovery-matrix.md) for the recovery ladder. For a complex handoff design, run `python scripts/check_oauth_handoff_design.py DESIGN.json` before deployment.
