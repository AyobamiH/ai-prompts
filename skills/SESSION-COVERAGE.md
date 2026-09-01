# Session Coverage and Deduplication

Snapshot source: <https://chatgpt.com/share/6a92a4f9-35f0-83eb-8386-5233769b71dc>

Initial snapshot endpoint: fresh OAuth consent page ready, with consent, GitHub scopes, and icon upload awaiting owner confirmation.

First continuation endpoint: GitHub App `donestate-maintenance-ayobamih` (App ID `4761698`) installed as installation `157513439` only on `AyobamiH/donestate`; a PR-only docs canary produced PR #22 at commit `ffec48e6...`, passed 22/22 tests and CI, and was not merged. Independent verification remained `uncertain`, so the gate stayed awaiting verification.

Later continuation evidence: public DoneState PRs #28-#56 recorded concurrent and cross-browser OAuth repair, strongly consistent and sealed transaction state, bounded reviewer access, OpenAI review submission, owned-domain cutover, signed Marketplace lifecycle ingestion, binding trust pages, a machine-readable governance ledger, lifecycle hardening, development/production isolation, recovery from a mis-targeted secret upload, and privacy-minimal lifecycle receipts. These implementation, CI, deployment, live-delivery, review, approval, and publication states remain separate; this coverage record extracts reusable methods rather than claiming provider approval.

## Ongoing-chat evidence snapshot

The authenticated workspace chats "Verify report Steps" (currently titled "PR 576 Next Steps"), "Verify remaining gates", and "OpenAI submission status" were reviewed on 2026-09-01. They are ongoing sources, so these statements are a bounded snapshot rather than a claim that their plans are complete.

- The package report was actioned on NHS UK PR #576 at exact head `87c401a7fa0fee8e6cb50ce0dcaaec85272b3811`: repository-owned package tests build, pack, clean-install, exercise the historical import, cover the minimum Sass compiler, inspect the alternate release archive, and update documentation and changelog. Upstream workflow approval and NHS maintainer review remain separate human gates.
- The remaining-gates work reconciled a merged bootstrap change into the default branch instead of merging the duplicate PR, then diagnosed a rolling-deployment race after provider success preceded container convergence. At the snapshot, the narrow correction passed 342 Vitest tests, 10 Python tests, builds, validators, type checking, and audit locally, but was not merged or deployed. Real ChatGPT OAuth and an approved real-data evaluation remained open.
- The submission-status work used authenticated provider readback to distinguish an OpsTruth 0.4.0 ChatGPT listing marked published from a DoneState GitHub Marketplace listing still pending publication. An authenticated owner preview and its preview install count were rejected as public-discoverability evidence. Reconciliation was read-only; repair PRs were not treated as merged, deployed, submitted, or published.

## Coverage map

| Session method | Coverage decision |
| --- | --- |
| Audit a spinner and checked plan against live GitHub, CI, deployment, and provider state | New: `stalled-work-session-audit` |
| Prepare OpenAI directory metadata, MCP URL, icons, tests, and review handoff | New: `chatgpt-app-directory-readiness` |
| Repair missing public health, privacy, and terms routes | New: `public-app-trust-pages` |
| Add and deploy the one-time OpenAI domain challenge route | New: `openai-domain-verification` |
| Recover repeated expired browser state and stale draft OAuth configuration | New: `oauth-state-recovery` |
| Refresh the connected DoneState app and verify current maintenance tools | New: `chatgpt-app-connection-refresh` |
| Diagnose absent workflow runs for connector-authored commits | New: `ci-trigger-provenance-recovery` |
| Group unavoidable account actions into one precise owner checkpoint | New: `owner-only-provider-checkpoint` |
| Prepare a GitHub App Marketplace listing while separating agreement, webhook, legal-owner, review, approval, and publication states | New: `github-app-marketplace-readiness` |
| Synchronize a Marketplace webhook secret without recording its value and require signed-delivery readback | Included in `github-app-marketplace-readiness`; the observed session stopped before provider update confirmation |
| Recover OAuth failures across concurrent attempts, cookie-free browser handoff, cross-region read-after-write, and provider-object portability, then select strongly consistent or sealed state without removing CSRF | Expanded: `oauth-state-recovery`; the earlier package recorded the symptom but missed the actual failure-driven recovery ladder |
| Make tamper, expiry, concurrency, cookie-loss, cross-region, provider-shaped, and single-use OAuth tests deterministic | Included in the expanded `oauth-state-recovery` package and helper |
| Give an external reviewer a dedicated application identity with representative reads and explicit denial of write, execute, approve, merge, deploy, administer, and secret access | New: `external-reviewer-access-boundary` |
| Allowlist the exact reviewer callback/form origin while preserving the rest of the CSP and accurately disclose internal state writes in tool annotations | Included in `external-reviewer-access-boundary`; directory metadata remains covered by `chatgpt-app-directory-readiness` |
| Process signed Marketplace purchase, change, cancellation, pending-change, and pending-change-cancelled events monotonically and idempotently | New: `marketplace-lifecycle-entitlements` |
| Accept a signed Marketplace ping without granting an entitlement, keep billing separate from repository authority, and return a versioned privacy-minimal delivery receipt | Included in `marketplace-lifecycle-entitlements` |
| Make one machine-readable project ledger canonical, generate human status views, reject governance drift in CI, and report stale owners through a read-only scheduled check | New: `self-documenting-project-governance` |
| Preserve evidence stories as situation, verification, accountability, outcome, content, and measurement with explicit re-entry conditions for deferred work | Included in `self-documenting-project-governance` |
| Separate production and development services, configs, endpoints, credential sources, secret targets, deploy triggers, OAuth apps, and Marketplace listings | New: `deployment-environment-secret-isolation` |
| Treat a generic secret uploader resolving the wrong Worker as an incident, restore both environments independently, verify both with direct probes, and remove temporary recovery triggers | Included in `deployment-environment-secret-isolation` |
| Keep Cloudflare or other provider credentials out of checkout, dependency installation, validation, and job-wide CI context, exposing them only to exact mutation steps | Expanded: `deployment-environment-secret-isolation` |
| Build, pack, install into a clean consumer, exercise documented and historical entrypoints, test minimum toolchains, compare output, inspect alternate release artifacts, and wire the contract into CI | New: `package-consumer-contract-gate` |
| Reconcile overlapping PRs after one merge by content identity, close already-landed duplicates, and rebuild only the missing delta without force-updating or merging during reconciliation | New: `overlapping-pr-convergence` |
| Require consecutive exact-revision observations across direct and independent surfaces before parsing new schemas or running authenticated probes | New: `deployment-revision-convergence` |
| Permit one reconciled identical-revision retry, then stop on the repeated stage with sanitized diagnostics and exact rollback provenance | Included in `deployment-revision-convergence`; bounded retry and exact rollback concepts were reused rather than duplicated |
| Bootstrap one product-local owner through a protected, idempotent, single-use workflow after authentication hardening converges | New: `private-pilot-owner-bootstrap` |
| Approve a target-market real dataset by provenance, rights, purpose, retention, deletion, minimization, isolation, and no-training controls before evaluating real users | New: `authorized-real-data-pilot` |
| Treat five real users and ten completed tasks as bounded market evidence, preserve failures and a baseline, and refuse a product-market-fit claim | Included in `authorized-real-data-pilot` |
| Model draft, developer verification, submission, review, approval, publication, discoverability, clean installation, and live outcome as separate subject-bound states | New: `distribution-channel-state-reconciliation` |
| Reject owner preview as public discoverability and prefer fresh authenticated provider-control readback over repository ledgers for provider-managed states | Included in `distribution-channel-state-reconciliation` |
| Cut over to an owned service domain while preserving the legacy review transport and exact deployment evidence | Reused: `exact-commit-release-promotion`, `cloudflare-mcp-plugin-platform`, and `documentation-closure-gate` |
| Publish binding privacy and service terms and keep review submission distinct from approval and public listing | Reused: `public-app-trust-pages`, `chatgpt-app-directory-readiness`, and `github-app-marketplace-readiness` |
| Exercise one selected-repository PR-only maintenance canary and stop on an `uncertain` independent-verifier result | Reused: `autonomous-repository-maintenance` and `independent-execution-verification`; no duplicate canary skill created |
| Resume bounded repository work from durable state | Reused: `agent/autonomous-coding-workflow` |
| Classify missing connector, runtime, configuration, and approval capabilities | Reused: `agent/capability-gap-learning-system` |
| Inspect repositories, services, packages, routes, and live state without mutation | Reused: `agent/read-only-production-reconnaissance` |
| Verify uncertain external writes through provider readback | Reused: `agent/evidence-first-live-diagnostic-repair` |
| Build the Proof and State governance repository and reconcile product roles | Reused: `agent/proof-and-state-architecture-skills`, `portfolio-governance-repository` and `secure-product-repository-bootstrap` |
| Implement DoneState selected-repository, PR-only maintenance | Reused: `agent/proof-and-state-architecture-skills`, `autonomous-repository-maintenance` |
| Keep validation, documentation, CI, deployment, and evidence on the same subject | Reused: `agent/proof-and-state-architecture-skills`, `documentation-closure-gate` and `exact-commit-release-promotion` |
| Preserve executor, controller, verifier, and notary authority boundaries | Reused: `agent/proof-and-state-architecture-skills`, `authority-first-product-architecture` and `independent-execution-verification` |
| Recover authenticated browser navigation and secure sign-in handoffs | Reused: `agent/proof-and-state-gtm-skills`, `authenticated-browser-recovery` |
| Generate a directory icon and verify its actual file type | Included as a conditional step in `chatgpt-app-directory-readiness`; no separate image skill created |
| Use GitHub, File search, Personal Context or Memory, authenticated browser control, OpenAI documentation, web search, command execution, Cloudflare or Atlas consoles, and parallel review agents | Platform-owned capabilities were not copied. The new skills record only session-specific decisions and evidence contracts |
| Use image generation and plugin management | Platform-owned capabilities were not copied |

## No-copy rule

An earlier skill was not copied merely because it ran again. This branch contains the newly learned rollout and recovery methods plus this coverage record, so the branch remains installable without creating competing names for the same workflow.
