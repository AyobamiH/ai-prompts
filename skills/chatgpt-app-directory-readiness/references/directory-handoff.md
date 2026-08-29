# ChatGPT App Directory Handoff

## Required evidence areas

- Exact release subject and deployment
- Publisher identity and support contact
- Listing name, description, category, and prompts
- Current MCP endpoint and discovered tools
- OAuth scopes, redirect path, consent copy, and revocation path
- Health, privacy, terms, deletion, and support pages
- Directory and composer icon files
- Data sent, stored, retained, shared, and deleted
- Positive and negative test matrix
- Known limitations and excluded capabilities
- Domain verification status
- Draft, submission, review, approval, and publication status

## Compact manifest

```json
{
  "release_subject": "0123456789abcdef0123456789abcdef01234567",
  "target_state": "review_ready",
  "required_gates": [
    "identity",
    "mcp_connection",
    "authentication",
    "trust_pages",
    "icons",
    "data_declarations",
    "positive_tests",
    "negative_tests",
    "documentation",
    "exact_release"
  ],
  "gates": {
    "identity": {"subject": "0123456789abcdef0123456789abcdef01234567", "status": "pass"}
  }
}
```

Every required gate must use the same release subject. Provider-owned form state should be captured by a draft identifier or bounded screenshot in the evidence pack, but credentials and one-time authorization codes must remain outside it.

## Icon check

Confirm pixel dimensions, aspect ratio, alpha handling, colour contrast, file type, and visual legibility at small size. Do not rely on a filename extension to establish the actual file type.
