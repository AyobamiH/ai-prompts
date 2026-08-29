---
name: authority-first-product-architecture
description: "Define product roles, trust boundaries, authority envelopes, and governance contracts before implementation. Use when separating an executor, controller, verifier, receipt service, maintainer bot, or other agentic product; when deciding which component may read, write, approve, merge, deploy, or sign; or when adding BOUNDARIES, BOT, CODEOWNERS, ADR, and integration-contract files to a repository."
---

# Authority-First Product Architecture

Make authority explicit before choosing implementation details. Treat every capability as denied until a policy grants it.

## Workflow

1. Inventory actors, protected resources, consequential effects, and current trust assumptions.
2. Assign one primary role to every product or service. Prefer narrow roles such as controller, executor, verifier, or notary.
3. Write a boundary matrix covering read, propose, execute, approve, merge, deploy, sign, and administer.
4. Define authority envelopes with subjects, actions, conditions, limits, duration, revocation, and required evidence.
5. Specify typed contracts at each boundary. Bind requests and results to immutable subjects such as repository, commit, artifact digest, deployment, and verifier identity.
6. Encode governance in repository files. Use `BOUNDARIES.md` for the constitution, `BOT.md` for bot policy, `CODEOWNERS` for protected review, ADRs for decisions, and schemas for machine-enforced contracts.
7. Test denied paths as first-class behavior. Include missing approval, stale commit, expanded scope, unavailable verifier, and expired authority.
8. Record unresolved assumptions and the exact conditions required to expand authority later.

## Invariants

- Do not let the component that performs an effect be the sole judge of that effect.
- Do not represent a roadmap integration as a live dependency.
- Do not infer write, merge, deployment, secret, or signing authority from read access.
- Require a new decision record when a capability crosses a trust boundary.
- Prefer revocable, scoped, time-bounded grants over global credentials.
- Preserve a human recovery path for policy, identity, and key changes.

## Deliverables

Return a role map, boundary matrix, authority-envelope schema, contract list, repository governance files, denial tests, and a list of open risks. Use the templates in [references/architecture-kit.md](references/architecture-kit.md) when the repository has no equivalent format.
