# Architecture and Autonomous Operations Skills

This collection converts the reusable methods exercised in the shared "Architecture Foundation Implemented" work session into installable Codex skills. It covers architecture, governance, autonomous control, secure delivery, independent proof, and continuity. It intentionally excludes the separate GTM skill collection.

Source session: <https://chatgpt.com/share/6a92903c-4c8c-83eb-9724-ad78aef6ff17>

## Coverage

| Skill | Session capability captured |
| --- | --- |
| [authority-first-product-architecture](authority-first-product-architecture/SKILL.md) | Product constitutions, role separation, trust boundaries, authority envelopes, BOT policy, CODEOWNERS, ADRs, and denial paths |
| [deterministic-evidence-graph](deterministic-evidence-graph/SKILL.md) | Exact-subject evidence, contradiction detection, deterministic verdicts, canonical snapshots, and offline proof |
| [exact-commit-release-promotion](exact-commit-release-promotion/SKILL.md) | Exact-head review, CI, merge, artifact, deployment, live readback, listing, and release promotion |
| [autonomous-desired-state-controller](autonomous-desired-state-controller/SKILL.md) | Desired-state reconciliation, standing policy, admission, effect sandwich, idempotency, leases, fencing, and escalation |
| [secure-product-repository-bootstrap](secure-product-repository-bootstrap/SKILL.md) | Greenfield repository foundations, schemas, persistence, policy, tests, CI, security, and release controls |
| [verified-npm-package-release](verified-npm-package-release/SKILL.md) | Version alignment, tarball inspection, registry authentication, publishing, metadata readback, and clean install verification |
| [cloudflare-mcp-plugin-platform](cloudflare-mcp-plugin-platform/SKILL.md) | Worker-hosted MCP, OAuth, Durable Objects, sandbox and container execution, per-user credentials, limits, CSP diagnosis, and live validation |
| [independent-execution-verification](independent-execution-verification/SKILL.md) | Sealed objectives, fresh re-observation, pinned Ed25519 verifier identities, signed results, and claim-precision limits |
| [provider-adapter-ownership](provider-adapter-ownership/SKILL.md) | Product-owned interfaces, optional discovery, repair and runner providers, pinning, provenance, mirrors, and exit paths |
| [documentation-closure-gate](documentation-closure-gate/SKILL.md) | Documentation routing and the invariant that code, docs, CI, deployment, evidence, and Git agree on one commit |
| [autonomous-repository-maintenance](autonomous-repository-maintenance/SKILL.md) | GitHub App registry, webhook and schedule reconciliation, read-only discovery, sandboxed repair, PR-only change, and governed rollout |
| [portfolio-governance-repository](portfolio-governance-repository/SKILL.md) | Canonical constitution, product registry, integration contracts, combined status, roadmap, compatibility evidence, and drift checks |

## Deterministic helpers

Five skills include standard-library Python checks for the failure-prone parts of their workflows:

- Evidence subject binding and contradiction detection
- Exact-commit release-stage alignment
- Objective, handoff, and verifier binding checks
- Documentation closure alignment
- Cross-product status and integration drift

These helpers are deliberately scoped. They do not replace provider-specific CI validation, live observation, policy evaluation, or cryptographic signature verification.

## Installation

Copy a skill directory into a Codex skills location or use the repository path directly in a supported installer. Each directory contains `SKILL.md`, `agents/openai.yaml`, and only the references or scripts required by that skill.
