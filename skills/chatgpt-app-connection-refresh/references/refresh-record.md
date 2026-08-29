# App Connection Refresh Record

## Manifest shape

```json
{
  "endpoint": "https://app.example.com/mcp",
  "release_subject": "0123456789abcdef0123456789abcdef01234567",
  "tools": [
    {"name": "repository_status", "schema_digest": "sha256:...", "authority": "read_only"}
  ]
}
```

The expected and observed files passed to the helper use the same `tools` array. Tool identity is the name plus schema digest and authority classification.

## Evidence

Record direct MCP discovery, connected-app discovery, refresh or reconnection action, bounded invocation, expected denial, observed account identity digest, granted scopes, and checked time. Redact tokens and user content.

## Outcomes

- `MATCH`: all expected tools match and no unexpected tools exist.
- `DRIFT`: missing, unexpected, or changed tools exist.
- `UNPROVEN`: the consumer-side manifest could not be observed.
