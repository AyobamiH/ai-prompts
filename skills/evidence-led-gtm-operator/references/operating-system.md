# Evidence-Led GTM Operating System

## Baseline

Record each surface independently. Do not collapse them into one readiness claim.

| Surface | Minimum evidence | Common false conclusion |
| --- | --- | --- |
| Product source | Exact branch, commit, version, current docs | Code exists, so users can use it |
| CI and build | Checks on the exact current commit | Green CI proves deployment |
| Deployment | Provider state plus runtime observation | Reachable health route proves the user journey |
| Directory or marketplace | Current public listing readback | Submitted means published |
| Onboarding | Fresh first-user journey | Existing operator session proves onboarding |
| Core outcome | Recorded successful user result | Features imply value |
| Analytics | Event receipt and queryable result | SDK configuration proves measurement |
| Distribution | Current accounts, audiences, and content | Followers prove qualified demand |
| Social proof | Attributable outcome or testimonial | Likes are testimonials |
| Cross-product path | Versioned handoff and real end-to-end proof | Compatible positioning proves interoperability |

## Claim ledger

Each claim needs:

```yaml
id: claim-id
text: Exact public claim
status: verified | risky | unproven | contradicted | stale
evidence:
  source: Canonical URL, receipt, commit, run, or artifact
  observed_at: ISO-8601 timestamp
  scope: What this evidence actually proves
owner: Product or company
allowed_channels: []
next_proof: Smallest action that could strengthen the claim
```

## Evidence Story Bank

```yaml
id: story-id
situation: What was happening
believed_state: What the user or agent thought was true
checks: []
evidence_found: []
verified: []
risky: []
unproven: []
consequence: Why the distinction mattered
lesson: Standalone value for the audience
product_role: Which product participated and how
assets: []
angles: []
suitable_channels: []
prohibited_claims: []
```

The best stories still teach something if the reader never buys the product.

## Campaign selection

Score only eligible stories. Reject stories whose central evidence is stale, private without permission, contradicted, or impossible to explain without overclaiming.

Useful score components:

- successful-user-outcome potential;
- audience relevance;
- evidence quality;
- freshness;
- category-learning value;
- platform fit;
- repetition risk;
- cost to produce.

Persist the hypothesis before publication. Example: developers will respond more strongly to "verify what your coding agent did" than to an abstract category label.

## Operating cadence

Daily or per natural work cycle:

1. observe product usage, agent work, repositories, discussions, and existing posts;
2. extract the strongest evidenced insight;
3. create the smallest set of high-quality native assets;
4. participate where genuinely relevant;
5. measure activation and useful outcomes;
6. record language, objections, confusion, and gaps;
7. feed the learning into product, onboarding, documentation, or the next experiment.

Weekly review:

- actions and outcomes;
- signal versus vanity noise;
- repeated user language;
- strongest story;
- product insight;
- channel performance;
- awareness-to-repeat-use funnel;
- launch-readiness delta;
- next high-information experiments.

## Metrics hierarchy

Prefer, in order:

1. successful user outcomes;
2. repeat users;
3. cross-product use that solves the next problem;
4. qualified activation;
5. organic referrals and independent mentions;
6. qualified inbound conversations;
7. meaningful repository or community activity;
8. saves, comments, and shares;
9. reach, impressions, and follower counts.

Unavailable metrics are unknown, not zero.

## Product Hunt gate

Do not recommend launch from a score alone. Require credible evidence for most of:

- clear one-sentence positioning;
- stable onboarding;
- multiple compelling use cases;
- successful first-user outcomes;
- repeat usage;
- testimonials or attributable proof;
- reliable website, listing, support, and legal surfaces;
- launch screenshots or video based on real workflows;
- known objections answered;
- active market familiarity;
- existing users willing to participate naturally;
- no unresolved critical product or trust-boundary contradiction.

If the market still needs to learn the problem, continue category recognition and product association before selecting a date.
