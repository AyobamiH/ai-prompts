---
name: documentation-closure-gate
description: "Enforce the invariant that implementation, documentation, status, CI, deployment, evidence, and Git history describe the same exact commit. Use when finishing repository work, designing a completion gate, deciding which documents a change requires, preventing documentation-only follow-up commits from bypassing CI, or validating an agent's claim that work is done."
---

# Documentation Closure Gate

Work is not closed until the implementation, documentation, validation, and evidence record agree on one immutable subject.

## Closure sequence

Follow `IMPLEMENT -> VALIDATE -> DOCUMENT -> COMMIT -> CI -> DEPLOY -> LIVE VERIFY -> RECORD EVIDENCE -> DONE`.

If documentation or evidence changes the commit after CI, rerun CI for the new head. If deployment is commit-bound, redeploy or prove the deployed artifact was built from the new head. Do not waive subject drift because the final change appears harmless.

## Documentation routing

- User-visible behavior: `CHANGELOG.md` and relevant user documentation.
- Current product position: `docs/CURRENT-STATUS.md` or the repository equivalent.
- Future or completed milestone: `docs/ROADMAP.md`.
- Architecture decision: ADR or decision log.
- Operational procedure: runbook.
- Release or deployment proof: evidence record.
- Authority or bot behavior: `AGENTS.md`, `BOT.md`, or policy files.
- Portfolio-wide role or integration: canonical portfolio registry and status.

## Workflow

1. Resolve the exact commit being closed.
2. Classify changed behavior and required document destinations.
3. Update documents before the final validation commit.
4. If no documentation changes are required, record a specific no-impact rationale and validate it against the changed paths.
5. Run required validation and CI on the documented head.
6. Bind deployment and live verification to that same subject or explicitly model the merge or artifact subject transition.
7. Record evidence without creating an unvalidated source change. Prefer external immutable evidence or include the record before the final CI run.
8. Refuse `DONE` when any required record is missing, stale, ambiguous, or points to another commit.

Run `python scripts/check_closure_manifest.py MANIFEST.json` for the compact closure manifest in [references/closure-record.md](references/closure-record.md).
