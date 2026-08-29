---
name: live-gtm-readiness-audit
description: "Audit a technical product's current market and launch readiness using live repository, CI, deployment, directory, onboarding, legal, web, and usage evidence. Use for initial baselines, scheduled re-audits, pre-campaign freshness checks, and Product Hunt gates. Do not use it to implement fixes unless the user also asks for changes."
---

# Live GTM Readiness Audit

Produce a time-stamped readiness decision that separates what is proven from what is merely present in code or documentation.

## Audit modes

- `baseline`: inspect every relevant surface and establish the first evidence ledger.
- `delta`: compare fresh observations against a named earlier baseline and report only material movement plus the new verdict.
- `pre-publication`: recheck every factual statement in a proposed campaign immediately before approval or publication.
- `launch-gate`: test whether onboarding, outcomes, repeat usage, proof assets, support, and distribution satisfy a declared threshold.

## Evidence rules

Prefer evidence in this order when sources conflict:

1. canonical provider or public-object readback;
2. current runtime observation tied to a version or deployment;
3. exact-commit CI, tests, and repository state;
4. active configuration and manifests;
5. current documentation;
6. inference, always labelled.

A passing build does not prove deployment, a live endpoint does not prove onboarding, configured analytics do not prove recorded events, and a roadmap does not prove interoperability.

## Procedure

1. Record the audit time, scope, products, exact versions or commits, previous baseline, and freshness window.
2. Inspect product surfaces independently: source, CI, releases, deployment, directory/listing, legal URLs, onboarding path, core user outcome, analytics, web presence, social proof, support, and cross-product handoffs.
3. For each claim store status, weight, criticality, observation time, source, and the smallest next proof needed.
4. Mark contradictory current evidence as `contradicted`, missing evidence as `unproven`, weak evidence as `risky`, and expired evidence as `stale`.
5. Run `scripts/score_readiness.py` when a reproducible score is useful. The score supports the verdict but never overrides a critical failed gate.
6. Compare the new ledger with the prior baseline. Explain which facts changed, which previous campaign copy became stale, and whether the operating decision changed.
7. Return a bounded next queue. Do not repair or publish unless separately authorised.

When the user asks for another audit later, create the appropriate automation with this exact scope and baseline reference. Do not claim a scheduled audit already ran until its new evidence exists.

## Output contract

Return:

- audit timestamp and scope;
- `verified`, `risky`, `unproven`, `contradicted`, and `stale` findings;
- material delta from the previous audit;
- readiness by product or surface;
- critical blockers;
- campaign claim changes;
- overall `go`, `hold`, or `no-go` verdict;
- next evidence-producing actions.

Read [references/audit-contract.md](references/audit-contract.md) before preparing a machine-readable ledger or scoring a launch gate.
