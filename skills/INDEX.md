# Rollout, Recovery and Autonomous Execution Skills

This collection packages reusable methods mined from production engineering sessions spanning ChatGPT app rollout, marketplace and OAuth recovery, Proof & State governance, real-data pilot gates, and DoneState autonomous-maintenance canaries. The newest expansion captures the production reliability ladder exercised through signed webhook dispatch, ephemeral Cloudflare Sandbox execution, durable terminal receipts, resumable alarms, exact-head CI, OpsTruth verification, and immutable successor canaries.

The collection is intentionally deduplicated: provider tools and platform capabilities are not copied as skills, and earlier skill contracts are reused when the session did not add a new decision boundary. The 2026-09-04 expansion adds submission-safe DOCX provenance scrubbing for CVs and other job-application documents.

## Skills

| Skill | Capability captured |
| --- | --- |
| [stalled-work-session-audit](stalled-work-session-audit/SKILL.md) | Reconcile a hanging agent plan with exact repository, CI, deployment, provider, and runtime evidence |
| [chatgpt-app-directory-readiness](chatgpt-app-directory-readiness/SKILL.md) | Prepare a verified app-directory draft and distinguish draft, review, approval, and publication states |
| [public-app-trust-pages](public-app-trust-pages/SKILL.md) | Implement truthful health, privacy, terms, support, revocation, and deletion surfaces |
| [openai-domain-verification](openai-domain-verification/SKILL.md) | Serve, deploy, read back, and verify an exact OpenAI domain challenge |
| [oauth-state-recovery](oauth-state-recovery/SKILL.md) | Recover concurrent, cookie-free, cross-region, or non-portable OAuth handoffs without weakening state validation |
| [chatgpt-app-connection-refresh](chatgpt-app-connection-refresh/SKILL.md) | Refresh a changed MCP connection and compare the consumer-visible tool manifest |
| [ci-trigger-provenance-recovery](ci-trigger-provenance-recovery/SKILL.md) | Diagnose missing workflow runs and restore exact-commit CI proof |
| [owner-only-provider-checkpoint](owner-only-provider-checkpoint/SKILL.md) | Batch precise unavoidable owner confirmations while preserving separate publication gates |
| [github-app-marketplace-readiness](github-app-marketplace-readiness/SKILL.md) | Prepare and verify a GitHub App Marketplace listing, webhook signing, owner declarations, review handoff, and publication readback |
| [external-reviewer-access-boundary](external-reviewer-access-boundary/SKILL.md) | Provide stable least-authority application access for an external reviewer and prove consequential actions remain denied |
| [marketplace-lifecycle-entitlements](marketplace-lifecycle-entitlements/SKILL.md) | Ingest signed marketplace lifecycle events with monotonic, idempotent entitlements and privacy-minimal receipts |
| [self-documenting-project-governance](self-documenting-project-governance/SKILL.md) | Make a machine ledger canonical, generate human status views, and reject undocumented governance drift in CI |
| [deployment-environment-secret-isolation](deployment-environment-secret-isolation/SKILL.md) | Prevent cross-environment writes and keep provider credentials scoped to exact mutation steps |
| [package-consumer-contract-gate](package-consumer-contract-gate/SKILL.md) | Verify built, packed, clean-installed, and alternate release artifacts against the documented consumer contract |
| [overlapping-pr-convergence](overlapping-pr-convergence/SKILL.md) | Reconcile merged or conflicting overlapping PRs by content and preserve only the remaining delta |
| [deployment-revision-convergence](deployment-revision-convergence/SKILL.md) | Prove the exact revision is consistently serving before authenticated or schema-sensitive verification |
| [private-pilot-owner-bootstrap](private-pilot-owner-bootstrap/SKILL.md) | Bootstrap exactly one protected product-local owner after hardened authentication converges |
| [authorized-real-data-pilot](authorized-real-data-pilot/SKILL.md) | Gate lawful, relevant real data and bounded real-user evidence without claiming product-market fit |
| [distribution-channel-state-reconciliation](distribution-channel-state-reconciliation/SKILL.md) | Reconcile draft, review, publication, discoverability, installation, and live-outcome states |
| [durable-webhook-queue-handoff](durable-webhook-queue-handoff/SKILL.md) | Bind authenticated webhook acceptance to one durable atomic queue claim without waiting for asynchronous execution |
| [ephemeral-runtime-read-retry](ephemeral-runtime-read-retry/SKILL.md) | Retry idempotent credential-free reads in fresh runtimes while keeping mutating effects non-retriable |
| [bounded-production-observability-reconciliation](bounded-production-observability-reconciliation/SKILL.md) | Localize one production progression boundary with exact subjects, windows, raw needles, and a frozen evidence boundary |
| [managed-runtime-one-variable-recovery](managed-runtime-one-variable-recovery/SKILL.md) | Diagnose managed runtime failures with a frozen workload and one variable changed per fresh production canary |
| [single-launch-terminal-receipt-reconciliation](single-launch-terminal-receipt-reconciliation/SKILL.md) | Persist intent before exactly one long implementation launch and use an atomic subject-bound terminal receipt as the sole completion oracle |
| [alarm-sliced-resumable-execution](alarm-sliced-resumable-execution/SKILL.md) | Reconcile one long implementation across bounded serverless alarm slices without relaunching it |
| [post-receipt-runtime-quiescence](post-receipt-runtime-quiescence/SKILL.md) | Separate implementation completion from runtime channel readiness with a fixed post-receipt quiescence gate |
| [immutable-successor-canary-recovery](immutable-successor-canary-recovery/SKILL.md) | Preserve failed and ambiguous runs immutably, repair the proven layer, then prove it with one fresh successor canary |
| [verified-run-branch-retirement](verified-run-branch-retirement/SKILL.md) | Delete only exact independently verified, merged autonomous run branches while preserving historical evidence |
| [job-application-metadata-scrub](job-application-metadata-scrub/SKILL.md) | Remove hidden DOCX authoring provenance from job applications while preserving visible content and refusing unresolved review artifacts |

## Deterministic helpers

27 standard-library Python helpers validate:

- Task completion against required exact-subject evidence
- App-directory readiness gates against one release subject
- Expected and observed MCP tool manifests
- CI observation state for one exact commit
- Precision and limits of an owner-only provider checkpoint
- GitHub App Marketplace identity, least-privilege configuration, secret-safe evidence, and exact publication state
- OAuth handoff entropy, binding, consistency, portability, and adversarial coverage
- External reviewer read-only authority, exact callback origins, expiry, revocation, and refusal tests
- Marketplace signature, complete lifecycle, monotonicity, authority separation, and receipt privacy
- Project-ledger completeness, evidence binding, generated views, governance-impact enforcement, and secret exclusion
- Distinct environment, service, configuration, credential, secret, deployment, live-probe, and credential-bearing workflow-step targets
- Shipped package paths, clean-consumer entrypoints, supported toolchains, output equivalence, durable CI, documentation, and upstream review state
- Overlapping pull-request changes against current default-branch content, exact-head checks, and no-force/no-merge boundaries
- Consecutive exact-revision observations, authenticated-probe sequencing, bounded retry, sanitized diagnostics, and rollback provenance
- Protected single-use owner bootstrap, product-local authority, exact scopes, refusal tests, cleanup, and sanitized receipts
- Real-dataset provenance, rights, purpose, retention, deletion, isolation, user authority, outcome measurement, and bounded evidence thresholds
- Immutable distribution subjects across provider control, public directory, clean installation, and runtime outcome surfaces
- Webhook authentication, deduplication, atomic queue claims, awaited durable setup, duplicate convergence, and periodic reconciliation
- Fresh-runtime retries for credential-free idempotent reads with bounded attempts, backoff, and mutation-retry refusal
- Single-subject production observability windows, ordered progression stages, raw needles, redaction, and frozen non-mutating evidence boundaries
- Frozen-workload one-variable runtime experiments with compatibility alignment, exact deployments, and distinct successor canaries
- Intent-before-effect, one implementation launch, atomic terminal receipt binding, and ambiguous-effect refusal on missing receipt
- Durable resumable checkpoints, one read-only reconciliation slice per alarm, safe rescheduling, and no relaunch on resume
- Fixed post-receipt quiescence, interval regression pinning, and separate capability classification for runtime-close validation failures
- Immutable predecessor canaries, separately merged/deployed repairs, fresh successor identities, and full independent-verification proof chains
- Exact verified+merged run-branch retirement with sealed subject reconciliation and preservation of non-verified history
- Job-application DOCX properties, generator markers, review artifacts, revision identifiers, timestamps, content invariants, and render-safe output

The helpers do not replace live provider readback, cryptographic checks, legal review, OAuth consent, directory attestations, runtime telemetry, or independent verification.

See [SESSION-COVERAGE.md](SESSION-COVERAGE.md) for the earlier rollout deduplication record and [DONESTATE-PRODUCTION-CANARY-COVERAGE.md](DONESTATE-PRODUCTION-CANARY-COVERAGE.md) for the 2026-09-03 production-canary expansion. See [CV-APPLICATION-METADATA-COVERAGE.md](CV-APPLICATION-METADATA-COVERAGE.md) for the 2026-09-04 CV metadata scrub evidence.
