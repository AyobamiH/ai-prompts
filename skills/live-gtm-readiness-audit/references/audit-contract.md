# Live GTM Audit Contract

## Claim schema

```json
{
  "audit_id": "audit-2026-08-29T09:00:00Z",
  "observed_at": "2026-08-29T09:00:00Z",
  "launch_threshold": 70,
  "claims": [
    {
      "id": "deployment-current-head",
      "surface": "deployment",
      "claim": "The current main commit is deployed",
      "status": "verified",
      "weight": 10,
      "critical": true,
      "required": true,
      "observed_at": "2026-08-29T08:55:00Z",
      "max_age_hours": 6,
      "source": "provider receipt and runtime version readback",
      "next_proof": null
    }
  ]
}
```

Allowed statuses:

- `verified`: direct current evidence proves the scoped claim;
- `risky`: evidence exists but is weak, partial, indirect, or has a material caveat;
- `unproven`: the necessary evidence was not found;
- `contradicted`: current evidence disproves the claim;
- `stale`: evidence exceeded its declared freshness window.

## Scoring

`scripts/score_readiness.py` uses declared weights and these multipliers:

| Status | Multiplier |
| --- | ---: |
| verified | 1.00 |
| risky | 0.50 |
| stale | 0.25 |
| unproven | 0.00 |
| contradicted | 0.00 |

The score is the weighted percentage rounded to one decimal. It is reproducible only when `--now` is supplied or the input includes a stable audit time.

A `go` verdict additionally requires:

- score at or above `launch_threshold`;
- every `required` claim verified;
- every `critical` claim verified.

A critical contradiction produces `no-go`. Other failures produce `hold`.

## Delta schema

For a re-audit, compare by stable claim ID and return:

```json
{
  "claim_id": "claim-id",
  "before": "unproven",
  "after": "verified",
  "evidence_changed": true,
  "campaign_impact": "The old failure-focused draft is stale"
}
```

Do not treat a higher score as meaningful when the claim set or weights changed without explanation.
