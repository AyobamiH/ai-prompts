# Session Coverage and Deduplication

Snapshot source: <https://chatgpt.com/share/6a92a4f9-35f0-83eb-8386-5233769b71dc>

Initial snapshot endpoint: fresh OAuth consent page ready, with consent, GitHub scopes, and icon upload awaiting owner confirmation.

First continuation endpoint: GitHub App `donestate-maintenance-ayobamih` (App ID `4761698`) installed as installation `157513439` only on `AyobamiH/donestate`; a PR-only docs canary produced PR #22 at commit `ffec48e6...`, passed 22/22 tests and CI, and was not merged. Independent verification remained `uncertain`, so the gate stayed awaiting verification.

Later continuation evidence: public DoneState PRs #28-#56 recorded concurrent and cross-browser OAuth repair, strongly consistent and sealed transaction state, bounded reviewer access, OpenAI review submission, owned-domain cutover, signed Marketplace lifecycle ingestion, binding trust pages, a machine-readable governance ledger, lifecycle hardening, development/production isolation, recovery from a mis-targeted secret upload, and privacy-minimal lifecycle receipts. These implementation, CI, deployment, live-delivery, review, approval, and publication states remain separate; this coverage record extracts reusable methods rather than claiming provider approval.

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
| Use Cloudflare Workers, Wrangler, GitHub, browser, image generation, and plugin management | Platform-owned capabilities were not copied. The new skills record only session-specific decisions and evidence contracts |

## No-copy rule

An earlier skill was not copied merely because it ran again. This branch contains the newly learned rollout and recovery methods plus this coverage record, so the branch remains installable without creating competing names for the same workflow.
