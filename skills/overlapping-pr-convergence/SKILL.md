---
name: overlapping-pr-convergence
description: "Reconcile stacked or overlapping pull requests after one is merged, closed, recreated, or made conflicting, using default-branch content and tree evidence instead of commit ancestry alone. Use when a merge makes another PR conflict, two PRs contain the same change under different SHAs, or only the still-missing delta should survive."
---

# Overlapping PR Convergence

A conflict is an observation, not an instruction to merge both branches or rewrite history.

## Workflow

1. Read the current remote default-branch SHA and tree, every affected PR head and base, merge or close events, exact-head checks, and changed-file content.
2. Assign stable change identifiers or content digests to each intended behavior. Do not use commit SHA alone as the change identity.
3. Prove which intended changes already exist on the default branch. Connector-created commits may have different commit SHAs while preserving the reviewed tree exactly.
4. Classify each candidate:
   - `ALREADY_IN_BASE`: every intended change is present and no unique delta remains; close or supersede without merging.
   - `REMAINING_DELTA`: some changes are present and some remain; rebuild a branch from current base with only the missing delta.
   - `REBASE_REQUIRED`: nothing is duplicated, but the head was built from an older base; update normally and rerun validation.
   - `CONFLICT_REVIEW_REQUIRED`: the same behavior changed incompatibly; stop for semantic review.
   - `READY`: the head is based on current default, contains only unique work, and exact-head CI passes.
5. Preserve the original PR, commits, comments, checks, and receipts as history. Never force-update merely to make the graph look tidy.
6. After rebuilding or updating a branch, resolve the new head, rerun all exact-head checks, and update the PR evidence.
7. Keep merge authority separate. Reconciliation may prove that closing a duplicate preserves the original path; it does not authorize another merge.

## Stop conditions

Stop when content digests are absent, remote base state is stale, remaining changes cannot be isolated, or a conflict is semantic rather than mechanical.

Read [references/convergence-record.md](references/convergence-record.md) for the record. Run `python scripts/classify_pr_convergence.py RECORD.json` before closing, rebuilding, or presenting an overlapping PR as ready.
