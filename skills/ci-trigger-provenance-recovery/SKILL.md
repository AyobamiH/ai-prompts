---
name: ci-trigger-provenance-recovery
description: "Diagnose why CI did not run for an exact commit and restore trustworthy workflow evidence without misclassifying absence as failure or fabricating proof. Use when connector-authored, bot-authored, API-created, merged, or documentation commits have no workflow run; when branch, event, path, permission, or skip rules may suppress CI; or when release work is blocked on exact-head checks."
---

# Ci Trigger Provenance Recovery

First prove whether a run exists for the exact commit. Missing, pending, stale, failed, and successful are different states.

## Workflow

1. Resolve the repository, branch, full commit SHA, changed paths, authoring mechanism, and expected workflow names and events.
2. Query workflow runs, check suites, and commit statuses for that exact SHA.
3. Inspect the workflow definition as it existed on the relevant default or candidate branch. Record `on` events, branch filters, path filters, permissions, concurrency, and manual dispatch support.
4. Check repository Actions state, fork context, rulesets, skip directives, workflow file location, and whether the event source suppresses recursive or bot-triggered runs.
5. Classify the observation as `PROVEN`, `PENDING`, `FAILED`, `MISSING_TRIGGER`, `STALE_EVIDENCE`, or `INCOMPLETE` before proposing a repair.
6. Choose the least disruptive supported recovery: wait on a durable pending run, dispatch an existing workflow for the exact ref, open or update a pull request that legitimately triggers required checks, or repair the workflow when its configuration is the defect.
7. Do not create an empty commit solely to make a green badge appear unless repository policy explicitly uses that mechanism and the new commit becomes the release subject.
8. After any source or workflow change, resolve the new head and restart exact-subject validation.
9. Record run IDs, event, workflow revision, head SHA, conclusions, and remaining gaps.

## Rules

- No run observed is not the same as a failed run.
- A run for another SHA is stale evidence.
- A manual run is valid only if policy accepts its event and inputs for the release gate.
- Local tests support diagnosis but do not replace required remote CI.
- Do not weaken branch protection or workflow permissions to recover a run.

Use [references/trigger-diagnosis.md](references/trigger-diagnosis.md) for the evidence packet. Run `python scripts/classify_ci_observation.py OBSERVATION.json` for the compact manifest.
