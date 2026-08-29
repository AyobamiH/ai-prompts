# Authority Architecture Kit

## Role map

| Component | Primary role | May do | Must not do | Independent check |
| --- | --- | --- | --- | --- |
| Controller | Reconcile desired state | Plan and request bounded work | Self-approve policy expansion | Verifier result |
| Executor | Perform an admitted action | Use scoped credentials | Change its own authority | Controller admission |
| Verifier | Re-observe effects | Compute evidence verdicts | Perform the effect it judges | Pinned signer identity |
| Notary | Record consequential transactions | Sign receipts | Claim the external effect succeeded | Independent evidence |

## Boundary matrix

Use `allow`, `deny`, or `conditional` for every cell. Do not leave blank cells.

| Actor | Read | Propose | Execute | Approve | Merge | Deploy | Sign | Administer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Human owner | | | | | | | | |
| Controller | | | | | | | | |
| Executor | | | | | | | | |
| Verifier | | | | | | | | |

## Authority envelope

```json
{
  "authority_id": "auth_...",
  "subject": {"repository": "owner/repo", "ref": "refs/heads/main"},
  "actions": ["pull_request:create"],
  "conditions": {"path_allowlist": ["docs/**"], "required_checks": ["ci"]},
  "limits": {"max_files": 10, "max_runs_per_day": 5},
  "expires_at": "2026-12-31T23:59:59Z",
  "revocation_ref": "policy/revocations.json"
}
```

## Governance file set

- `BOUNDARIES.md`: constitutional role, protected actions, independence requirements.
- `BOT.md`: bot permissions, forbidden operations, escalation rules, audit fields.
- `.github/CODEOWNERS`: reviewers for policy, schemas, workflows, and release files.
- `docs/adr/`: durable decisions and rejected alternatives.
- `schemas/`: request, result, policy, and receipt contracts.
- `tests/authority/`: allowed and denied path tests.

## Expansion test

Before granting new authority, answer:

1. Which concrete blocked outcome requires it?
2. Can narrower scope or shorter duration solve the problem?
3. Which independent evidence proves correct use?
4. How is the grant revoked?
5. Which denial test fails before the change and passes after it?
