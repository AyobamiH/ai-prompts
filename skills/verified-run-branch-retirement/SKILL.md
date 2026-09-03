---
name: verified-run-branch-retirement
description: "Retire autonomous run branches only after independent verification and exact merged-PR subject reconciliation. Use when evidence branches must be cleaned up without deleting failed, uncertain, historical, foreign, or closed-unmerged work."
---

# Verified Run Branch Retirement

Branch cleanup is a consequence-bearing action. Make deletion narrower than publication.

## Workflow

1. Parse only the exact governed run-branch shape, such as `product/<UUID-v4>`. Reject friendly prefixes and arbitrary refs.
2. Require the durable run to be independently `VERIFIED` and of the permitted objective class.
3. Require the bound pull request to be closed and merged, not merely closed.
4. Reconcile repository, head repository, base ref, branch name, head SHA, PR number, and queued finding against the sealed run subject immediately before deletion.
5. Refuse deletion for forks, foreign repositories, failed/uncertain/ambiguous runs, closed-unmerged PRs, historical canaries, and branches that do not exactly match the run.
6. Permit an authenticated PR-close event to attempt immediate retirement.
7. Keep a read-only periodic reconciliation pass for event-ordering races or already-absent branches.
8. Treat retirement failure as cleanup debt only. It must not alter the verifier decision or grant merge authority.

## Outcomes

- `READY`: deletion is exact-subject, verified, merged, narrow, and replay-safe.
- `REFUSED`: deletion can occur based on branch prefix alone, a closed-unmerged PR, or a non-verified run.

Read [references/retirement-contract.md](references/retirement-contract.md). Run `python scripts/check_branch_retirement.py MANIFEST.json` before granting autonomous branch-deletion authority.
