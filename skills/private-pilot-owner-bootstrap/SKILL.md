---
name: private-pilot-owner-bootstrap
description: "Prepare, execute, and verify a one-owner private pilot bootstrap through a protected, single-use, least-authority workflow. Use when a product needs its first real local owner after hardened authentication is deployed, without turning a provider admin, platform admin, or separate tester into product evidence."
---

# Private Pilot Owner Bootstrap

Bootstrap one product-local owner only after the exact hardened authentication revision has converged.

## Workflow

1. Freeze the repository, source SHA, deployment ID, target environment, and approved product scopes. Prove authentication hardening is deployed and the runtime has converged before creating an account.
2. Create a dedicated protected deployment environment restricted to the exact branch or revision and an explicit human approval.
3. Store only references to an owner email, a bcrypt or Argon2id password hash, and the target database URI. Never place the raw email, password, hash, connection string, or provider credentials in the repository, logs, or receipt.
4. Use a manual, idempotent workflow with a maximum of one successful use. Create exactly one product workspace and exactly one product-local owner.
5. Keep identities separate by authority. The pilot owner is not a provider administrator, infrastructure administrator, or additional tester account.
6. Grant only the approved product scopes. Do not infer broader authority from GitHub, cloud, database, or ChatGPT ownership.
7. Verify valid sign-in, wrong-password rejection, revoked-grant rejection, tenant isolation, out-of-scope denial, and cleanup after a failed attempt.
8. On failure, remove partial accounts and prove the product user count returns to zero. On success, retain a sanitized, immutable execution receipt.
9. Treat downstream ChatGPT connection and OAuth consent as a separate gate; account bootstrap alone does not prove that integration.

## Outcomes

- `READY_FOR_OWNER`: the protected environment and single-use plan are verified, with zero current owners.
- `BOOTSTRAP_VERIFIED`: exactly one local owner and workspace exist, all refusal tests pass, and a sanitized receipt is present.
- `REFUSED`: rollout, authority, secret handling, scope, test, cleanup, or evidence binding is unsafe or incomplete.

Read [references/bootstrap-record.md](references/bootstrap-record.md) for the record. Run `python scripts/check_private_pilot_bootstrap.py RECORD.json` before provisioning or claiming the first owner is ready.
