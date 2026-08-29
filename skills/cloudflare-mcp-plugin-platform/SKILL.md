---
name: cloudflare-mcp-plugin-platform
description: "Design and validate a secure MCP or ChatGPT plugin platform on Cloudflare Workers using OAuth, Durable Objects, sandboxed execution, and scoped user credentials. Use when building or debugging a remote MCP server, GitHub-connected plugin, Cloudflare Worker agent, OAuth callback flow, per-user secret store, or paid-plan sandbox and container architecture."
---

# Cloudflare Mcp Plugin Platform

Keep authentication, durable control state, and untrusted execution in separate trust zones. Load the applicable Cloudflare and MCP skills before writing provider-specific code or running deployment commands.

## Architecture

Use a Worker for the public MCP and OAuth surface, Durable Objects for serialized per-tenant state, and a sandbox or container for code execution. Keep GitHub, OpenAI, and other user-funded credentials encrypted and scoped to the user and standing policy.

## Workflow

1. Define tools, protected actions, tenants, data residency, cost limits, and authority boundaries.
2. Specify OAuth clients, redirect URIs, state and PKCE handling, token storage, refresh, revocation, and account-link semantics.
3. Make MCP tool schemas narrow and versioned. Separate read-only discovery from consequential actions.
4. Put per-user state behind a stable tenant key. Define concurrency, alarms, migrations, retention, and deletion.
5. Execute code in an isolated sandbox with explicit image, resource limits, timeouts, network policy, and filesystem lifetime.
6. Add policy admission before execution and independent verification after consequential effects.
7. Validate OAuth with direct HTTP and provider tooling. Use a browser only for the human authorization step when required.
8. Diagnose callback failures across redirect registration, state, cookie attributes, proxy headers, and Content Security Policy. In particular, ensure a callback form is permitted by `form-action`.
9. Validate secrets by a minimal provider request, return redacted diagnostics, and store only after success.
10. Deploy through supported CLI or API workflows, then test discovery, authorization, tool invocation, restart recovery, and revocation from the live endpoint.

## Operational rules

- Never log authorization codes, access tokens, API keys, cookies, or decrypted secret values.
- Enforce per-user request, execution, and spend limits before invoking paid providers.
- Treat a sandbox timeout as an unknown execution outcome until reconciled.
- Record actual current integrations separately from planned adapters.
- Maintain a local runner exit path when a managed sandbox is replaceable.

Use [references/platform-checklist.md](references/platform-checklist.md) for design and live verification.
