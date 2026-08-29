# Desired-State Controller Blueprint

## State machine

Recommended states:

- `PENDING`: desired state accepted but not observed.
- `PLANNED`: delta and action plan persisted.
- `ADMITTED`: policy allows the next action.
- `EXECUTING`: intent persisted and lease held.
- `SETTLING`: external effect returned but needs durable settlement.
- `VERIFYING`: independent re-observation in progress.
- `CONVERGED`: observed state satisfies desired state.
- `WAITING`: a retry or external condition is pending.
- `ESCALATED`: human decision or new authority is required.
- `REFUSED`: policy forbids the requested outcome or action.

## Admission record

```json
{
  "action_id": "act_...",
  "subject": {"repository": "owner/repo", "commit": "..."},
  "policy_id": "policy_...",
  "policy_version": "7",
  "decision": "allow",
  "conditions": ["required-checks-pass"],
  "limits_consumed": {"daily_actions": 1},
  "decided_at": "2026-08-29T00:00:00Z"
}
```

## Recovery table

| Failure point | Durable fact | Recovery action |
| --- | --- | --- |
| Before intent | No action attempt | Re-plan safely |
| After intent, before effect | Pending attempt | Acquire new fenced lease and execute once |
| During effect | Outcome unknown | Query provider by idempotency or correlation key |
| After effect, before settlement | External identifier may exist | Read provider, then persist settlement |
| After settlement, before verification | Settlement recorded | Re-observe independently |

## Concurrency rules

- Lease the smallest stable subject.
- Increment a fence token on every lease acquisition.
- Reject writes carrying an older token.
- Keep idempotency keys stable across retries of the same logical action.
- Use separate keys after the plan or subject changes.
- Treat timeouts as unknown outcomes, not automatic failures.
