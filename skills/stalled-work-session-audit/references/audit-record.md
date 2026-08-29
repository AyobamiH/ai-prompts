# Stalled Session Audit Record

## Report structure

1. Session identity and observed stopping point
2. Claimed plan state
3. Evidence source inventory
4. Task-by-task verdict matrix
5. Contradictions
6. Actions that may already have happened
7. Owner-only or provider gates
8. Exact resume point
9. Do-not-repeat list

## Compact matrix

```json
{
  "session_id": "run-123",
  "tasks": [
    {
      "id": "deploy-worker",
      "claimed_status": "complete",
      "subject": {"repository": "owner/repo", "commit": "0123456789abcdef0123456789abcdef01234567"},
      "required_evidence": ["ci", "deployment", "live_readback"],
      "evidence": [
        {
          "kind": "ci",
          "status": "pass",
          "subject": {"repository": "owner/repo", "commit": "0123456789abcdef0123456789abcdef01234567"}
        }
      ],
      "blocker": "deployment evidence unavailable"
    }
  ]
}
```

## Verdict matrix

| Task | Session claim | Live evidence | Actual state | Blocker | Resume action |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## Waiting test

Waiting is justified only when an active provider or workflow operation has a durable identifier and a normal pending state. Waiting is not justified when the browser session expired, no workflow run exists, a tool call disconnected, approval is missing, or the process has no durable operation to poll.
