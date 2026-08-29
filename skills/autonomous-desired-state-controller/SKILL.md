---
name: autonomous-desired-state-controller
description: "Design autonomous systems that reconcile a desired outcome under standing authority while escalating only true exceptions. Use when building an outcome-driven controller, maintenance agent, policy-governed orchestrator, or long-running workflow that needs idempotency, durable state, leases, fencing, admission control, and safe recovery around uncertain external effects."
---

# Autonomous Desired State Controller

Translate a human outcome into durable intent and a bounded reconciliation loop. Do not convert natural language directly into unbounded tool authority.

## Control loop

1. Capture desired state separately from the natural-language request.
2. Resolve the applicable standing policy and its version.
3. Observe current state using read-only providers.
4. Calculate a deterministic or inspectable delta.
5. Produce a plan with explicit subjects, effects, preconditions, and evidence requirements.
6. Admit each action against scope, limits, freshness, conflicts, and approval rules.
7. Persist intent before starting an uncertain external effect.
8. Execute with an idempotency key and a fenced lease.
9. Persist settlement after the effect, including unknown outcomes.
10. Re-observe independently and update convergence state.
11. Continue, back off, or escalate based on policy. Never silently widen authority to make progress.

## Effect sandwich

Use `persist intent -> perform effect -> persist settlement`. If the process fails between steps, recovery must query the external system with a stable correlation or idempotency key before retrying.

## Required state

Persist desired state, policy version, observation version, plan hash, action attempts, idempotency keys, lease owner and fence token, external identifiers, settlements, verification results, and escalation reason.

## Escalate when

Authority is missing or expired, the plan exceeds limits, observations conflict, a high-consequence action requires approval, the external effect remains ambiguous, an invariant fails, or retries exceed policy.

Use [references/controller-blueprint.md](references/controller-blueprint.md) to define the state machine and recovery table before implementing workers.
