---
name: bounded-production-observability-reconciliation
description: "Localize a production failure with an exact subject, deployment, time window, raw event needles, and ordered stage evidence before mutating code. Use when provider delivery is known but queue, coordinator, runtime, or verifier progression is uncertain."
---

# Bounded Production Observability Reconciliation

Logs are most useful when they answer one bounded question, not when they become an unstructured search for anything suspicious.

## Workflow

1. Freeze the production subject: source SHA, deployment/runtime version, issue or request ID, run ID if known, and exact UTC window.
2. Define the ordered stages expected for one path, for example provider delivery → ingress → durable queue intent → coordinator create/start → runtime launch → receipt → validation → publication → verifier.
3. Search raw structured telemetry using a small explicit needle set for those stages. Keep the window narrow enough that duplicate traffic can be attributed.
4. Mark each stage as observed, absent, or not-yet-applicable. Do not infer an unobserved stage merely because a later UI object exists.
5. Identify the first unresolved boundary and stop diagnosis there. Avoid patching downstream code before upstream progression is proven.
6. Keep the evidence boundary frozen while diagnostics run: no patch, PR, deploy, reset, or successor canary unless the diagnostic itself is consequence-free.
7. Redact secrets and request bodies. Preserve timestamps, delivery IDs, run IDs, runtime objects, and provider correlation IDs.
8. Convert the bounded result into either a proven blocker, a capability gap, or a justified next probe.

## Outcomes

- `READY`: subject, window, ordered stages, raw needles, redaction, and first unresolved boundary are explicit and no mutation occurred during reconciliation.
- `REFUSED`: diagnosis spans mixed deployments/runs, the window is unbounded, or repair starts before the progression boundary is known.

Read [references/observability-window.md](references/observability-window.md). Run `python scripts/check_observability_reconciliation.py MANIFEST.json` before turning production telemetry into a repair decision.
