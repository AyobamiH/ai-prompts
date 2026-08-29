# Cloudflare MCP Platform Checklist

## Public surface

- Stable HTTPS MCP endpoint
- Versioned tool names and JSON schemas
- OAuth metadata and exact redirect URIs
- Health endpoint with no secret-bearing details
- CORS and CSP restricted to required origins and actions

## OAuth

- Random state, PKCE where supported, and short-lived authorization transactions
- One-time callback consumption
- Secure, HttpOnly, SameSite cookies appropriate to the redirect topology
- Token encryption at rest and key rotation plan
- Disconnect and revocation path
- Redacted error codes that remain actionable

## Durable state

- Tenant key and ownership checks
- Schema version and migration plan
- Serialized mutation or conflict handling
- Alarm and retry semantics
- Retention, export, and deletion behavior

## Execution

- Pinned runtime image or digest
- CPU, memory, duration, disk, and concurrency limits
- Network allowlist or documented network policy
- Ephemeral workspace and cleanup
- Idempotency and correlation keys
- No ambient platform credentials inside user code

## Live tests

1. MCP discovery without authentication where intended.
2. Full OAuth authorization and callback.
3. Read-only tool invocation.
4. Denied consequential action without standing authority.
5. Allowed bounded action with exact subject binding.
6. Restart and Durable Object state recovery.
7. Secret validation failure with redacted diagnostics.
8. Revocation and disconnected-account behavior.
9. Per-user limit enforcement.
10. Independent post-effect verification.
