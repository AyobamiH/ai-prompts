# DoneState Production Canary Coverage and Deduplication

Snapshot date: 2026-09-03.

Primary evidence surface: the current DoneState production-reliability work plus public `AyobamiH/donestate` repair/canary history through PR #115. The sequence includes the webhook-driven maintenance repairs around PRs #67-#78, Cloudflare Sandbox compatibility/lifecycle experiments around PRs #80-#93, long-running implementation reconciliation around PRs #95-#113, and the fresh post-quiescence successor canary in PR #115.

This file records reusable engineering methods. It does not claim that a canary, deployment, marketplace submission, or independent verification reached a state not proven by its exact subject.

## What the session actually taught

- A signed webhook is a liveness signal only after duplicate deliveries converge and the durable queue claim exists before the `2xx` response.
- A retry loop owned by a dead ephemeral shell cannot retry. Safe read-only retries need orchestration-owned attempts with fresh runtime identities.
- Long implementation calls must not be made retryable merely because acknowledgement or process-registry state disappears.
- Intent-before-effect plus one terminal receipt creates a stronger completion boundary than provider process history.
- A short-lived Durable Object or serverless coordinator should reconcile long work in bounded alarm slices instead of waiting in one invocation.
- A verified implementation receipt and a ready managed-runtime channel are different facts. A post-receipt quiescence gate can prevent the next long command from racing runtime teardown.
- A production runtime investigation is most useful when every canary changes one variable while the workload, authority, verifier, and publication contract stay frozen.
- `FAILED_SAFE`, `AMBIGUOUS_EFFECT`, and `BLOCKED_CAPABILITY` runs are evidence. They are not scratch state to reset after the fix.
- A repair proves only its own exact head and deployment. The repaired production path needs a fresh successor canary with a distinct run identity.
- Autonomous branch deletion requires a narrower contract than branch creation: independent `VERIFIED`, exact sealed subject, closed-and-merged PR, selected repository, and preserved historical evidence.
- Bounded Cloudflare/GitHub observability should freeze one source/deployment/run/time window and identify the first unresolved stage before any patch or successor is allowed.

## Coverage map

| Session method | Coverage decision |
| --- | --- |
| Authenticate GitHub issue deliveries, deduplicate them, atomically claim `OPEN -> REPAIR_QUEUED`, and await only durable queue setup before webhook acceptance | New: `durable-webhook-queue-handoff` |
| Keep the hourly schedule as reconciliation after signed webhooks become the primary maintenance liveness signal | Included in `durable-webhook-queue-handoff`; no separate cron skill |
| Retry anonymous public materialisation after a dead Sandbox shell by moving retry ownership into TypeScript/orchestrator state and creating a fresh Sandbox per attempt | New: `ephemeral-runtime-read-retry` |
| Keep GitHub credentials absent from clone/read materialisation until the existing publication boundary | Included in `ephemeral-runtime-read-retry`; authority constraints also reuse earlier least-privilege skills |
| Use exact Cloudflare time windows and raw progression needles to separate webhook delivery, queueing, coordinator creation/start, runtime execution, and later verification | New: `bounded-production-observability-reconciliation` |
| Freeze the evidence boundary during diagnosis so no patch, PR, deploy, reset, or successor changes the subject being reconciled | Included in `bounded-production-observability-reconciliation` |
| Align Sandbox SDK/container image, then change transport, keep-alive, and default-session policy one variable at a time against the same Codex workload | New: `managed-runtime-one-variable-recovery` |
| Preserve exact unchanged runtime/workload/verifier/publication invariants in each repair PR and test them | Included in `managed-runtime-one-variable-recovery` |
| Replace unreliable process-registry success with one DoneState-owned atomic terminal receipt outside the mutable repository workspace | New: `single-launch-terminal-receipt-reconciliation` |
| Persist implementation intent before the effect, allow exactly one launch, and reconcile a lost acknowledgement without blind Codex relaunch | Included in `single-launch-terminal-receipt-reconciliation` |
| Move long implementation completion out of one Durable Object alarm invocation and resume through a durable checkpoint with one bounded read-only reconciliation slice per alarm | New: `alarm-sliced-resumable-execution` |
| Keep unrelated unsettled actions fail-closed as `AMBIGUOUS_EFFECT` rather than resuming them through the implementation checkpoint | Included in `alarm-sliced-resumable-execution` |
| Keep a detached receipt worker alive beyond a managed session while retaining a tracked waiter until terminal completion | Covered by `single-launch-terminal-receipt-reconciliation` plus `alarm-sliced-resumable-execution`; the exact `setsid` command is an implementation detail, not a separate skill |
| After the terminal receipt, wait a fixed runtime-quiescence interval before package installation/validation on the same managed runtime | New: `post-receipt-runtime-quiescence` |
| Classify a post-receipt runtime-close failure as a capability/runtime failure without invalidating the already-proven implementation receipt | Included in `post-receipt-runtime-quiescence` |
| Preserve #105/#108/#110/#112-like predecessor runs as immutable terminal evidence, deploy the narrow repair separately, then launch one fresh successor | New: `immutable-successor-canary-recovery` |
| Treat branch, PR, green exact-head CI, or `AWAITING_VERIFICATION` as intermediate states rather than end-to-end success | Included in `immutable-successor-canary-recovery`; independent verification semantics reuse earlier verifier skills |
| Require the fresh successor proof chain to reach independent verification and a truthful terminal `VERIFIED` state while leaving the canary PR unmerged | Included in `immutable-successor-canary-recovery` |
| Retire only `donestate/<UUID>` branches whose sealed run is independently verified and whose exact PR is closed and merged in the selected repository | New: `verified-run-branch-retirement` |
| Preserve failed, uncertain, ambiguous, foreign, historical, and closed-unmerged branches, and keep cleanup failure separate from verification state | Included in `verified-run-branch-retirement` |
| Enforce repository-native governance/generated-state requirements over conflicting instructions that appear only in untrusted issue text | Reused: `self-documenting-project-governance`; no duplicate policy-precedence skill |
| Retry independent verification only for a completed workflow whose `head_sha` exactly matches the sealed published run head | Reused: earlier independent-execution verification and exact-subject CI contracts; no duplicate verifier-retry skill |
| Require `{ contractVersion, report, attestation }`, sealed subject binding, nonce/replay protection, and exact verifier identity | Reused: earlier independent-verification contracts; no duplicate OpsTruth skill |
| Raise a production quota only after a run fails before implementation launch with `BLOCKED_CAPABILITY`, preserve that blocked run, and use a fresh successor | Included in `immutable-successor-canary-recovery`; quota configuration itself is product-specific |
| Audit historical run branches and selectively restore only semantics still valid against current verified product identity | Reused: `overlapping-pr-convergence`, architecture/governance skills, and current-state reconciliation; no separate historical-diff skill |
| Use GitHub, Cloudflare logs/observability, Sandbox SDK documentation, workflow jobs/logs, provider control planes, web research, and command execution | Platform/provider tools are dependencies, not copied skills |

## Tooling observed

The work exercised GitHub issues, branches, pull requests, exact-head Actions status, job logs, deployments, GitHub App webhooks, Cloudflare Worker and Durable Object observability, Cloudflare Sandbox runtime controls, provider documentation, bounded web research, local/repository test execution, generated governance state, and independent OpsTruth verification.

Those tools are intentionally not represented as standalone skill names. The reusable value is the sequencing, authority boundaries, evidence contracts, retry rules, and refusal conditions above.

## No-copy rule

An existing skill is reused when the new session only supplies another example of the same contract. New skill names are reserved for newly learned control boundaries that would materially change how a future agent plans, validates, or refuses work.
