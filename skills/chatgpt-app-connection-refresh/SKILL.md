---
name: chatgpt-app-connection-refresh
description: "Refresh a connected ChatGPT app after its MCP tool surface, schemas, authentication, prompts, or metadata change, then prove that ChatGPT discovers the intended live version. Use when new tools are absent, old tool descriptions remain cached, a connector was redeployed, or directory and runtime views disagree about the current app capabilities."
---

# Chatgpt App Connection Refresh

Verify discovery from the consumer side. A deployed MCP server does not prove ChatGPT has refreshed its cached connection.

## Workflow

1. Freeze an expected manifest containing endpoint, release subject, protocol version, tool names, schema digests, annotations, authentication mode, and prompts.
2. Read the live MCP discovery response directly and bind it to the deployed release.
3. Inspect the connected ChatGPT app or draft. Record its connection identity and observed tool manifest.
4. If the consumer is stale, use the supported refresh, reconnect, or draft-connection reset path. Preserve provider grants unless reauthorization is actually required.
5. Re-run discovery after refresh and compare tool names and schema digests exactly.
6. Confirm removed tools are no longer exposed and new tools appear once, with the intended descriptions and authority annotations.
7. Invoke one bounded read-only tool and one expected denial path. Use owner consent separately if an authenticated or consequential tool must be tested.
8. Record expected and observed versions, missing or unexpected tools, schema drift, auth result, and final connection state.

## Rules

- Do not claim refresh from a settings-page reload alone.
- Do not broaden OAuth scopes merely because a new tool exists.
- Treat a tool with the right name and wrong input schema as drift.
- Keep live runtime, connected app, directory draft, and published listing versions distinct.
- Do not delete the connection before preserving its identity and current evidence.

Use [references/refresh-record.md](references/refresh-record.md) for the manifest. Run `python scripts/compare_tool_manifest.py EXPECTED.json OBSERVED.json` for exact comparison.
