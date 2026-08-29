# Provider Adapter Contract

## Required operations

```text
capabilities() -> CapabilitySet
validate_config(redacted_config) -> ValidationResult
start(request, idempotency_key, deadline) -> OperationHandle
status(operation_handle) -> OperationStatus
cancel(operation_handle) -> CancellationResult
evidence(operation_handle) -> ProviderEvidence
```

Use operation names appropriate to the domain, but preserve capability discovery, validation, durable correlation, cancellation, and evidence access.

## Contract fields

- Provider and adapter versions
- Immutable subject bindings
- Correlation and idempotency keys
- Requested and effective scope
- Start, deadline, and completion times
- Result status including `unknown`
- External identifiers
- Redacted diagnostics
- Evidence provenance

## Adoption record

| Dimension | Decision |
| --- | --- |
| Capability gap | |
| Current provider | |
| Why an adapter is sufficient | |
| Licence and notices | |
| Version or digest pin | |
| Security review | |
| Failure semantics | |
| Compatibility tests | |
| Local exit path | |
| Fork or mirror trigger | |

## Switch gate

Do not replace a live provider until both adapters pass the same contract suite and the new provider demonstrates equivalent subject binding, idempotency, cancellation, redaction, and evidence behavior.
