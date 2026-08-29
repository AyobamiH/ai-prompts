# GTM Work Session Skill Set

These skills capture the reusable capabilities exercised during the referenced GTM operating session. They are deliberately separated so drafting, public mutation, browser recovery, brand operations, and product delivery do not inherit one another's authority.

| Capability from the session | Skill |
| --- | --- |
| Live product, distribution, and Product Hunt readiness auditing | [`live-gtm-readiness-audit`](live-gtm-readiness-audit/SKILL.md) |
| Evidence-led strategy, story banking, measurement, and campaign queues | [`evidence-led-gtm-operator`](evidence-led-gtm-operator/SKILL.md) |
| Parent, product, category, domain, and account topology | [`product-brand-architecture`](product-brand-architecture/SKILL.md) |
| Threads, Instagram, Reddit, LinkedIn, Facebook, GitHub, and GBP adaptation | [`platform-native-campaign`](platform-native-campaign/SKILL.md) |
| One-time approval, immutable payload, one write, and provider readback | [`approval-safe-social-publishing`](approval-safe-social-publishing/SKILL.md) |
| Reconnecting composers, forms, uploads, and authenticated UI state | [`authenticated-browser-recovery`](authenticated-browser-recovery/SKILL.md) |
| Image-backed Google Business Profile updates and review-state handling | [`google-business-profile-post`](google-business-profile-post/SKILL.md) |
| Company and social profile creation, repair, assets, and public verification | [`brand-profile-operations`](brand-profile-operations/SKILL.md) |
| Product architecture, design, build, deployment, domain, and launch proof | [`product-site-launch`](product-site-launch/SKILL.md) |

## Recommended composition

```text
live-gtm-readiness-audit
  -> evidence-led-gtm-operator
  -> platform-native-campaign
  -> approval-safe-social-publishing
       -> authenticated-browser-recovery when needed
       -> google-business-profile-post for GBP

product-brand-architecture
  -> brand-profile-operations
  -> product-site-launch
```

The arrows indicate handoff, not inherited permission. Publishing and live profile or site changes still require the authority appropriate to that action.
