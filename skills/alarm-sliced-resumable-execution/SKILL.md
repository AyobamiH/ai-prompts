---
name: alarm-sliced-resumable-execution
description: "Run a long external implementation through short-lived coordinator invocations by persisting a resumable checkpoint and performing bounded read-only reconciliation on each alarm. Use with Durable Objects, jobs, leases, or serverless control planes whose invocation lifetime is shorter than the work."
---

# Alarm-Sliced Resumable Execution

Do not make a short-lived coordinator hold one long provider call open merely to know when work is done.

## Workflow

1. Persist a checkpoint bound to the durable implementation intent before launching the long action.
2. Launch the implementation exactly once, using the terminal-receipt contract for completion.
3. On each alarm or wake-up, perform one bounded read-only reconciliation slice: receipt, minimal repository continuity, and deadline checks.
4. If the action is still unsettled but safe to resume, persist the checkpoint and schedule the next alarm rather than sleeping inside the invocation.
5. Retain or renew only the lease and runtime identity needed for the recognized implementation checkpoint.
6. Never resume an unrelated unsettled action under the implementation checkpoint. Unknown effect boundaries fail closed as `AMBIGUOUS_EFFECT`.
7. Stop scheduling alarms when a verified terminal receipt or terminal deadline outcome settles the action.
8. Keep reconciliation non-mutating until the implementation is known terminal.

## Outcomes

- `READY`: one launch, durable checkpoint, bounded read-only alarm slices, safe rescheduling, and fail-closed handling of unrelated effects.
- `REFUSED`: a coordinator waits for the full implementation in one invocation, relaunches on wake-up, or performs mutations while completion is unresolved.

Read [references/resume-checkpoint.md](references/resume-checkpoint.md). Run `python scripts/check_alarm_resumption.py MANIFEST.json` before deploying long work into a short-lived coordinator.
