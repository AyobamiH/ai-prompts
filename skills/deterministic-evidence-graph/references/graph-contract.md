# Compact Evidence Graph Contract

The bundled evaluator accepts a JSON object with these fields:

```json
{
  "schema_version": "1",
  "policy_version": "release-v1",
  "subject": {
    "repository": "owner/repo",
    "commit": "0123456789abcdef0123456789abcdef01234567"
  },
  "required_kinds": ["source", "ci"],
  "evidence": [
    {
      "id": "ev_source",
      "kind": "source",
      "status": "pass",
      "subject": {
        "repository": "owner/repo",
        "commit": "0123456789abcdef0123456789abcdef01234567"
      },
      "source": "github",
      "observed_at": "2026-08-29T00:00:00Z"
    }
  ]
}
```

Every evidence subject must contain every key in the root subject and match its value exactly. Required kinds need at least one passing observation and no failing observation.

## Canonicalization

The evaluator serializes JSON with sorted keys and compact separators, then calculates SHA-256. Array order remains significant. Producers should sort evidence by stable `id` before signing when arrival order is not meaningful.

## Domain extensions

Add policy-specific validators for:

- CI conclusion, workflow identity, and trusted trigger.
- Artifact digest and provenance attestation.
- Deployment target, deployment identifier, and runtime readback.
- Signature algorithm, trusted key, revocation state, and signing context.
- Evidence freshness and minimum independent-source count.

Do not change the meaning of the base fields silently. Introduce a new schema or policy version.
