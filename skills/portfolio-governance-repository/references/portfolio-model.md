# Portfolio Governance Model

## Product registry fields

- Stable product identifier and display name
- Repository and ownership
- Primary role and explicit non-goals
- Lifecycle state
- Current release and exact status commit
- Customer-facing or internal classification
- Authority boundary document
- Supported integration contract versions

## Integration registry fields

- Stable integration identifier
- Provider and consumer product identifiers
- Lifecycle state: `live`, `preview`, `experimental`, `planned`, or `retired`
- Contract path and schema version
- Authentication and authority relationship
- Exact subject bindings
- Failure and retry semantics
- Independent verification requirement
- Compatibility evidence

## Compact drift manifest

```json
{
  "products": [
    {
      "id": "controller",
      "primary_role": "desired-state controller",
      "current_state": "live",
      "status_commit": "0123456789abcdef0123456789abcdef01234567"
    }
  ],
  "integrations": [
    {
      "id": "controller-to-verifier",
      "from": "controller",
      "to": "verifier",
      "state": "live",
      "contract": "contracts/controller-verifier-v1.json"
    }
  ],
  "status_records": [
    {
      "product": "controller",
      "current_state": "live",
      "commit": "0123456789abcdef0123456789abcdef01234567"
    }
  ]
}
```

## Review rules

- Product-role changes require a decision record.
- Live integration changes require provider and consumer review.
- Contract changes require compatibility classification.
- A status document cannot advance beyond its evidence.
- Planned adapters stay out of current-runtime diagrams and dependency claims.
- Product repositories own local runbooks; the portfolio repository owns cross-product contracts and combined status.
