---
name: oauth-state-recovery
description: "Diagnose and recover OAuth authorization failures caused by expired, stale, mismatched, or repeatedly reused state without weakening CSRF protection. Use when a ChatGPT app, MCP server, GitHub App, or other provider connection reports expired browser state, invalid state, callback mismatch, consent loops, stale client configuration, or a retry button that keeps reproducing the same failure."
---

# Oauth State Recovery

Recover by creating a new authorization transaction. Never bypass or relax state validation to make the callback succeed.

## Workflow

1. Capture the public error, attempt time, authorization URL host, redirect URI, client identity, and deployed auth version without recording codes, tokens, cookies, or full state values.
2. Determine whether the failed link represents a short-lived transaction that has expired, a draft connection caching old client metadata, a redirect mismatch, cookie loss, CSP failure, clock skew, or a server-side state-store problem.
3. Verify the live authorization and callback routes use the intended deployment and current client configuration.
4. Fix and deploy configuration before generating another authorization link.
5. Clear only the affected app draft or connection state when the platform is caching stale OAuth metadata. Do not delete unrelated apps, credentials, or provider grants.
6. Start a completely fresh authorization transaction. Do not reuse the expired URL or retry the same cached button state.
7. Present the exact scopes, provider account, app identity, data exchange, and actions to the verified owner immediately before consent.
8. After consent, verify callback consumption, token storage, connected-account identity, granted scopes, revocation path, and one bounded authenticated read.
9. Record the resolved cause and remove diagnostic logging that could expose sensitive values.

## Security invariants

- State values are random, single-use, short-lived, bound to the client and redirect, and consumed atomically.
- Authorization codes and tokens never enter chat, screenshots, logs, URLs retained in documentation, or source control.
- A state mismatch is a refusal, not a warning.
- Credentials are entered only through the provider's advertised secure authentication surface.
- Scope expansion requires a new explicit owner decision.

Read [references/oauth-recovery-matrix.md](references/oauth-recovery-matrix.md) for diagnosis and stop conditions.
