---
name: exact-commit-release-promotion
description: "Promote one immutable commit through validation, documentation, CI, deployment, live verification, evidence recording, and release without subject drift. Use for production releases, merge and deploy workflows, marketplace or plugin publication, release-readiness checks, or any task where completion claims must name the exact tested and deployed revision."
---

# Exact Commit Release Promotion

Treat a commit change as a reset of downstream proof. Evidence for an earlier head does not promote a later head.

## State model

Use explicit states: `DRAFT`, `VALIDATED`, `REVIEWED`, `MERGED`, `CI_PASSED`, `DEPLOYED`, `LIVE_VERIFIED`, `EVIDENCE_RECORDED`, `RELEASED`, and `REFUSED`. Record the immutable commit at every state transition.

## Workflow

1. Resolve the candidate branch and full commit SHA.
2. Inspect repository instructions, protected paths, release policy, and required approvals.
3. Run validation on the candidate SHA and persist the command, outcome, and environment.
4. Finish required documentation on that same branch. If documentation changes the head, rerun validation.
5. Open or update the review artifact and confirm it still points to the candidate SHA.
6. Confirm required CI completed successfully for that exact SHA.
7. Merge without assuming the merge commit equals the reviewed head. Resolve and record the resulting release subject.
8. Build and deploy an artifact traceable to the release subject. Record immutable artifact and deployment identifiers.
9. Perform live readback against the intended environment and bind the observation to the deployment.
10. Record evidence and create the release or listing only when every required stage agrees.

## Stop conditions

Refuse promotion on stale reviews, missing checks, ambiguous artifact provenance, environment mismatch, unverifiable runtime readback, documentation added after the last CI run, or any commit mismatch.

Use [references/promotion-record.md](references/promotion-record.md) as a handoff template. Run `python scripts/check_release_manifest.py MANIFEST.json` to check the compact exact-commit manifest before claiming readiness.
