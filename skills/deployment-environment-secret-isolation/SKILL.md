---
name: deployment-environment-secret-isolation
description: "Design, verify, and recover strict deployment and secret-target separation between production, development, staging, or review environments. Use when a generic uploader, CLI default, shared workflow, or ambiguous configuration may write credentials or deploy code to the wrong service, Worker, project, account, or listing."
---

# Deployment Environment Secret Isolation

Treat an ambiguous secret or deployment target as a potentially cross-environment incident, even when the deployment command itself reports success.

## Workflow

1. Inventory every environment's provider account, service name, configuration file, endpoint, deployment trigger, credential source, secret target, OAuth app, marketplace listing, and observable route contract.
2. Require the mutation command to name the target explicitly. Do not rely on a default config, current directory, friendly label, or a generic secret uploader that resolves a production name while deploying development code.
3. Keep production and non-production credentials separately stored and separately authorised. Never copy or display secret values to prove separation.
4. Scope provider credentials to the exact mutation steps that require them. Checkout, dependency installation, lint, test, validation, and ordinary build steps must not receive production credentials unless an unavoidable exception is documented and independently reviewed; job-wide provider credentials fail the gate.
5. Make non-production deployment an explicit operation when automatic deployment could touch production. Log the resolved target name before processing credentials or code.
6. Add target-name assertions before mutation and independent route probes after deployment. Probe both intended and protected environments so success in one does not hide damage to the other.
7. If any log or probe indicates cross-targeting, stop further writes, classify the scope as unknown, restore each affected environment independently, redeploy exact known-good subjects, and verify both with direct readback.
8. Remove temporary incident triggers and return to the intended steady-state deployment policy after recovery.
9. Record the incident without secret values: triggering command, resolved targets, affected environments, exact recovery commits and deployments, probe results, residual risk, and prevention control.

## Stop conditions

Stop on unresolved provider account, service, environment, config, secret target, endpoint identity, or credential-bearing workflow step. Do not retry a generic upload until target resolution is deterministic.

Read [references/isolation-manifest.md](references/isolation-manifest.md) for the environment contract. Run `python scripts/check_environment_isolation.py MANIFEST.json` before a credential or deployment mutation.
