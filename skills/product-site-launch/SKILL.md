---
name: product-site-launch
description: "Plan, build, deploy, connect, and verify a credible multi-product or technical product website from product truth through information architecture, design system, implementation, deployment, domain, TLS, analytics, and public readback. Use for a site launch or substantial product-site build, not a small copy edit."
---

# Product Site Launch

Treat the website as product infrastructure and proof, not a decorative landing page.

## Sequence

1. Establish product truth, audience, category, trust boundaries, current and roadmap capabilities, and available proof assets.
2. Define information architecture for the parent, each product, use cases, how it works, evidence, docs, security or trust, pricing when known, company, support, and legal pages.
3. Choose a visual direction from the product's character. Avoid default AI aesthetics, arbitrary purple, decorative gradients, empty glass cards, and unearned enterprise imagery.
4. Build a reusable design system with typography, spacing, motion, states, responsive behaviour, and accessible interaction rules.
5. Implement from the canonical repository. Preserve source control, existing conventions, and unrelated user changes.
6. Add discoverability: metadata, canonical URLs, structured data, sitemap, robots policy, semantic headings, meaningful internal links, and an `llms.txt` or equivalent when appropriate.
7. Validate content claims, routes, forms, performance, responsive layouts, keyboard access, contrast, reduced motion, and error states.
8. Build, commit, push, save the deployable version, deploy, and inspect provider status using the platform's required workflow.
9. Connect the domain only with explicit authority. Verify DNS, TLS, canonical redirects, public content, and rollback or fallback state.
10. Run `scripts/check_launch_manifest.py`. Do not call the site live while a critical gate is missing.

When `.openai/hosting.json` exists, use the Sites building and hosting workflows. When another builder such as Lovable is explicitly selected, preserve the same source, verification, and deployment boundaries.

## Completion claim

Distinguish `designed`, `implemented`, `build_passed`, `version_saved`, `deployed`, `domain_connected`, and `publicly_verified`. A private preview, saved version, DNS record, or deployment request is not the same as a verified public launch.

Read [references/launch-gates.md](references/launch-gates.md) before implementation planning or final handoff.
