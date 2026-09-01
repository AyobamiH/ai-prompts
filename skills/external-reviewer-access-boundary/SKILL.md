---
name: external-reviewer-access-boundary
description: "Create and verify a least-authority application identity for an external directory, marketplace, security, or compliance reviewer. Use when a reviewer needs stable sign-in and representative read access without inheriting an owner account, MFA dependency, repository authority, paid execution, administration, or production mutation rights."
---

# External Reviewer Access Boundary

Give reviewers enough application access to inspect the submitted capability while keeping owner, execution, and mutation authority unavailable.

## Workflow

1. Freeze the exact review subject: app version, endpoint, environment, tool manifest, test data, and submitted capability.
2. Create a dedicated application-level reviewer identity. Never reuse a provider owner, administrator, personal, or production operator account.
3. Grant only the reads required by the review. Explicitly deny writes, execution, approvals, merges, deployments, billing, secrets, user administration, and authority changes.
4. Make the login stable for the review window without asking the reviewer to obtain the owner's second factor. This exception applies only to the bounded application test identity, never to the owner or provider account.
5. Use synthetic or purpose-built review data. Do not expose customer data, credentials, private repositories, or unrelated tenants.
6. Allowlist exact review callback and form-action origins. Reject wildcards and preserve the existing frame, base, script, and referrer restrictions.
7. Test authenticated read success and every consequential denial. Confirm the reviewer sees truthful tool annotations, including internal state writes that make a tool non-read-only.
8. Record creation, expiry, revocation path, last validation, and the exact review subject. Revoke or rotate the identity when review ends or the subject changes.

## Stop conditions

Stop if review requires an owner credential, broad provider grant, production write, live customer data, disabled security control on an owner account, or access to a capability outside the submitted version.

Read [references/reviewer-access-record.md](references/reviewer-access-record.md) for the evidence contract. Run `python scripts/check_reviewer_boundary.py ACCESS.json` for a complex reviewer handoff.
