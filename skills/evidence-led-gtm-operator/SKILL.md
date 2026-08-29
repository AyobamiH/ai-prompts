---
name: evidence-led-gtm-operator
description: "Build or run evidence-led go-to-market systems for technical products when strategy must connect live product truth, platform-native campaigns, user outcomes, and launch gates. Use for GTM baselines, warm-up campaigns, Evidence Story Banks, campaign queues, measurement reviews, or Product Hunt readiness. Do not use it only to publish an already-approved post."
---

# Evidence-Led GTM Operator

Operate growth as a product feedback system whose claims are bounded by current evidence.

## Operating invariants

- Begin with a live baseline. A prior report, draft, deployment, or campaign is historical context until rechecked.
- Market a painful user moment, observed result, failure, disagreement, or lesson. Do not lead with "try my plugin."
- Keep execution and independent verification distinct. Never imply that one product certifies itself or that two products interoperate until a real end-to-end handoff proves it.
- Derive content from real work. Label unsupported claims as unproven and remove stale claims before approval.
- Prefer successful outcomes, repeat use, qualified activation, referrals, and cross-product use over followers or impressions.
- Treat Product Hunt as a multiplier of existing demand. Do not manufacture a launch date to create urgency.
- A content draft is not permission to publish. For public writes, use `approval-safe-social-publishing` after the payload is approved.

## Workflow

1. Establish the current product, distribution, audience, analytics, onboarding, testimonial, repository, and web-presence baseline.
2. Build a claim ledger. For every marketable statement record its evidence, source time, owner, and status: `verified`, `risky`, `unproven`, `contradicted`, or `stale`.
3. Define the category, each product's one-sentence job, target users, natural invocation language, and the boundary between current capability and roadmap.
4. Create Evidence Story Bank records from actual incidents. Each record must include the believed state, checks performed, evidence found, consequence, lesson, reusable assets, and suitable channels.
5. Select a small campaign queue by evidence quality, audience relevance, business impact, freshness, platform fit, and repetition risk.
6. Adapt each selected story with `platform-native-campaign`. Preserve the factual core while changing format and framing per channel.
7. Measure the path from awareness to useful outcome and repeat use. Feed recurring language, objections, failure modes, and use cases into product and positioning changes.
8. Re-audit before high-consequence claims, broad demos, or launch recommendations. Use `live-gtm-readiness-audit` when product state may have moved.

## Minimum deliverables

Return only what the task needs, selected from:

- current GTM baseline with evidence dates;
- positioning and claim ledger;
- Evidence Story Bank;
- campaign hypotheses and platform roles;
- measurement plan;
- product feedback loop;
- launch-readiness verdict with missing evidence;
- prioritised immediate queue.

Use a clear `go`, `hold`, or `no-go` decision for each consequential campaign or launch claim. Explain the blocking evidence rather than hiding it inside a score.

## References

Read [references/operating-system.md](references/operating-system.md) when creating a baseline, story bank, metrics hierarchy, weekly review, or launch gate.

Read [references/proof-and-state-context.md](references/proof-and-state-context.md) only for OpsTruth, DoneState, Proof & State, or AI Work Accountability work. Reverify every time-sensitive status before using it publicly.
