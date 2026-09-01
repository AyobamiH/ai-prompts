---
name: deployment-revision-convergence
description: "Prove that an exact newly deployed revision is consistently serving before schema-sensitive or authenticated verification begins. Use for rolling deployments, stale edge or container responses, provider success signals that precede runtime convergence, and bounded retry or rollback decisions."
---

# Deployment Revision Convergence

Treat provider deployment success as permission to observe convergence, not proof that every request reaches the new revision.

## Workflow

1. Freeze the source SHA, artifact digest, provider deployment ID, environment, expected runtime revision marker, and exact known-good rollback subject.
2. Wait for the provider's deployment state to succeed, then observe the revision marker with bounded backoff. Do not use a blind fixed sleep as evidence.
3. Require a configured streak of consecutive ready responses for the expected marker. Include both a direct deployment or origin surface and an independent routed surface in the final streak.
4. Classify an unexpected marker as a stale revision. Never parse an old revision's response body using the newly deployed schema or report that parse failure as an authentication defect.
5. Run schema-sensitive, OAuth, tenancy, and tool probes only after the convergence streak passes. Bind every result to the frozen revision.
6. Permit at most one governed retry of the identical revision after cleanup and provider reconciliation. If the same stage fails again, stop retrying and diagnose the boundary.
7. Keep diagnostics sanitized: stage and remote tool names are allowed; tokens, secret values, cookies, and response bodies are not.
8. If rollback is required, redeploy one exact known-good subject with verified provenance and prove restoration through a fresh runtime probe.

## Outcomes

- `CONVERGED`: the exact revision has a qualifying observation streak and its post-convergence authenticated probe passes.
- `WAIT_FOR_CONVERGENCE`: the deployment succeeded but the required revision streak is not yet present.
- `ROLLBACK_REQUIRED`: the governed retry repeated the failure and the rollback record is complete.
- `REFUSED`: identity, sequencing, diagnostics, retry, authentication, or rollback evidence is unsafe or incomplete.

Read [references/convergence-manifest.md](references/convergence-manifest.md) for the evidence contract. Run `python scripts/check_deployment_convergence.py MANIFEST.json` before interpreting an authenticated rollout probe or declaring a deployment live.
