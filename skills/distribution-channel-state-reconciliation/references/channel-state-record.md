# Distribution Channel State Record

Use `distribution-channel-state.v1` for one immutable `subject_id`. Repeat the same subject ID in every observation and record product, channel, artifact type, version, source SHA, and deployed SHA at the top level.

Required evidence surfaces are:

| State | Evidence surface |
| --- | --- |
| `DRAFT` | Repository or authenticated provider control |
| `DEVELOPER_MODE_VERIFIED` | Developer mode or a clean consumer |
| `SUBMITTED`, `IN_REVIEW`, `APPROVED`, `PUBLISHED` | Authenticated provider control |
| `DISCOVERABLE` | Unauthenticated public directory |
| `INSTALLED` | Clean consumer |
| `LIVE_OUTCOME_VERIFIED` | Subject-bound runtime receipt |

Every state through the target must be `verified`, freshly timestamped, and carry an evidence reference. Provider-managed states require current authenticated readback. Public discoverability requires an unauthenticated surface. Never use an owner preview or preview install count as public proof.

Keep contradictions empty only after they have been resolved against the higher-authority surface. Provider reconciliation performs no provider mutation, and the repository ledger is reconciled without promoting the state.
