---
name: stalled-work-session-audit
description: "Determine what an interrupted, hanging, or long-running AI work session actually completed by reconciling the visible plan with repository, CI, deployment, provider, and runtime evidence. Use when a chat spinner, checked task, screenshot, video, or agent completion claim may disagree with live state, or when deciding the exact safe point from which work should resume."
---

# Stalled Work Session Audit

Audit the outcome, not the animation. A spinning step may be dead, and a checked step may still lack durable proof.

## Workflow

1. Capture the visible session state, including plan items, last meaningful output, blocking question, errors, and timestamps.
2. Identify every claimed deliverable and its authoritative proof surface. Examples include repository commit, pull request, CI run, deployment identifier, live route, provider object, or directory draft.
3. Inspect those surfaces read-only. Do not resume mutation until the audit establishes the last proven checkpoint.
4. Bind evidence to exact subjects. A green run for an earlier commit does not prove the current head. A reachable host does not prove the intended deployment.
5. Classify each task as `VERIFIED_COMPLETE`, `IN_PROGRESS`, `BLOCKED`, `UNPROVEN`, or `NOT_STARTED`.
6. Preserve contradictions between the session and live evidence. Explain which source outranks the other.
7. Identify whether waiting can change the state. A disconnected tool call, expired browser state, missing approval, or absent workflow trigger requires intervention, not more waiting.
8. Produce the smallest safe resume point, remaining owner-only gates, and actions that must not be repeated.

## Evidence order

Use provider and runtime readback, exact repository and CI state, durable application records, current source and configuration, maintained documentation, session claims, then inference.

## Completion rules

- Do not mark an item complete from prose, a checkbox, or a zero exit code alone.
- Do not classify a provider effect as absent until authoritative readback supports it.
- Treat unavailable evidence as unproven, not failed.
- Keep draft, review-submitted, approved, and published states distinct.
- Never repeat an ambiguous external action before reconciling its provider-side outcome.

Use [references/audit-record.md](references/audit-record.md) for the report. Run `python scripts/check_completion_matrix.py MATRIX.json` when the task evidence fits the compact matrix schema.
