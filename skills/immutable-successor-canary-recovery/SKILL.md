---
name: immutable-successor-canary-recovery
description: "Preserve failed, ambiguous, or capability-blocked production canaries as immutable evidence, repair only the proven layer, and prove the repair with a fresh successor run. Use when replay could duplicate an uncertain effect or rewrite operational history."
---

# Immutable Successor Canary Recovery

Never turn an uncertain production run into a cleaner story by resetting it. Repair forward.

## Workflow

1. Freeze every predecessor run with its terminal state, exact source, deployment, runtime identity, and known effects.
2. Classify whether the predecessor failed before effect, after an admitted effect, or at an unknown boundary. `AMBIGUOUS_EFFECT` forbids relaunch.
3. Identify the narrowest proven blocker. Change only that layer and list the invariants intentionally preserved.
4. Require exact-head CI on the repair, then merge and deploy the repair as a separate subject before any successor canary.
5. Create exactly one fresh successor issue/run identity. Never reset, reuse, reopen, or relaunch the predecessor run.
6. Require the full proof chain for the successor: durable run, implementation receipt, bounded validation, run branch, one PR, exact-head required CI, independent verifier response, and truthful terminal state.
7. Keep the canary PR open and unmerged when the canary's purpose is proof rather than product delivery.
8. Treat branch creation, PR creation, green CI, or `AWAITING_VERIFICATION` as intermediate evidence, not success.

## Outcomes

- `READY`: predecessors are immutable, the repair subject is separately proven and deployed, and the successor is distinct with a complete proof chain.
- `REFUSED`: a predecessor is replayed or rewritten, a repair and canary share one subject, or success is claimed before independent verification.

Read [references/successor-record.md](references/successor-record.md). Run `python scripts/check_successor_canary.py MANIFEST.json` before launching or declaring a successor canary.
