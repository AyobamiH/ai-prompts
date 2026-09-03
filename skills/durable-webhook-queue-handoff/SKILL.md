---
name: durable-webhook-queue-handoff
description: "Make an authenticated webhook acceptance boundary wait for durable queue intent without waiting for asynchronous execution. Use when duplicate deliveries, detached dispatch, or provider retries can lose work or create duplicate runs."
---

# Durable Webhook Queue Handoff

A `2xx` webhook response may mean only that a request was parsed. Treat acceptance as truthful only after the durable queue intent exists.

## Workflow

1. Authenticate the delivery before reading authority-bearing fields. Bind the provider delivery ID, event type, repository, and installation or tenant identity.
2. Deduplicate and upsert the finding first. Duplicate `opened`, `edited`, `labeled`, or retried deliveries must converge on one logical finding.
3. Atomically claim the eligible finding into the queued state with a fresh run ID before any coordinator mutation.
4. Await only bounded queue setup before returning success to the webhook provider. Do not wait for agent execution, CI, verification, or publication.
5. If queue setup fails after the claim, record the failure locally and reconcile from durable state. Do not ask the provider to replay a possibly mutating operation blindly.
6. Keep a periodic reconciliation path as fallback, not as the primary liveness signal.
7. Prove with duplicate-delivery tests that one logical finding creates at most one run.
8. Keep execution, merge, deployment, and verification authority unchanged.

## Outcomes

- `READY`: authenticated delivery, durable claim, awaited queue setup, duplicate convergence, and fallback reconciliation are all proven.
- `REFUSED`: acceptance can race ahead of durable queue intent, duplicate deliveries can create multiple runs, or execution is incorrectly awaited inside the webhook.

Read [references/handoff-contract.md](references/handoff-contract.md). Run `python scripts/check_webhook_queue_handoff.py MANIFEST.json` before treating a webhook `2xx` as durable dispatch evidence.
