# Autonomous Maintenance Runbook

## Phases

| Phase | Authority | Evidence required to advance |
| --- | --- | --- |
| Observe | Read and record candidates | Low false-positive rate and complete deduplication |
| Draft | Create local patches only | Deterministic validation and safe recovery |
| Propose | Open scoped pull requests | Exact-head CI and independent verification |
| Governed action | Selected merge or release action | Explicit standing policy and signed receipts |
| Fleet | Multiple selected repositories | Tenant isolation, capacity controls, and portfolio reporting |

## Pull request record

- Installation, repository, base, branch, and exact head
- Candidate source and observation time
- Policy and plan versions
- Changed paths and diff statistics
- Sandbox image and limits
- Validation commands and results
- CI run identifiers
- Independent verifier, verdict, and signature reference
- Retry and reconciliation state
- Known limitations and human decisions required

## Stop conditions

Disable mutation and continue read-only reconciliation when:

- GitHub App permissions expand unexpectedly.
- Webhook signature verification fails.
- Repository policy is missing, invalid, or stale.
- Protected paths enter the proposed diff.
- The base branch moves beyond allowed rebase policy.
- Provider output is malformed or an effect outcome is unknown.
- Required CI or independent verification is unavailable.
- Daily action, failure, or spend limits are exceeded.
- A kill switch or installation suspension is active.

## Recovery

Retain durable correlation identifiers for webhook deliveries, candidates, plans, sandbox runs, branches, pull requests, CI runs, and verifier results. On restart, re-observe GitHub before repeating any write.
