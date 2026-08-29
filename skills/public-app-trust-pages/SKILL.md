---
name: public-app-trust-pages
description: "Create and verify public health, privacy, terms, support, revocation, and deletion surfaces that match an app's real behavior. Use when preparing an MCP server, ChatGPT app, OAuth integration, or public API for directory review; when required routes return 404; or when publisher identity, retention, subprocessors, user-funded credentials, and account deletion need truthful documentation."
---

# Public App Trust Pages

Document observed product behavior. Do not invent legal terms to make a submission form pass.

## Workflow

1. Inventory the operator identity, support channel, service purpose, users, data flows, credentials, subprocessors, storage, retention, deletion, security controls, and governing jurisdiction.
2. Trace actual code and configuration for each claim. Distinguish transient processing, durable storage, logs, backups, and third-party provider retention.
3. Implement stable public routes for health, privacy, terms, support, account or data deletion, and OAuth revocation where applicable.
4. Keep `/health` bounded. Report service identity, version, and dependency readiness without disclosing secrets, tenant data, internal topology, or stack traces.
5. Make privacy text explain what data is received, why, where it goes, how long it remains, how users revoke access, and how they request deletion.
6. Make terms explain eligibility, acceptable use, service limits, user responsibilities, third-party services, suspension, warranty limits, and contact details only where verified.
7. Ensure consent screens, app-directory declarations, repository documentation, and public pages use the same identity and data model.
8. Test each route from the public hostname after deployment. Check status, content type, accessibility, mobile readability, link integrity, and cache behavior.
9. Record the exact commit and deployment supporting the pages.

## Boundaries

- Preserve legal review as an explicit open item when professional advice is required.
- Do not publish a personal address, phone number, or identity detail without verified user intent.
- Do not claim zero retention when infrastructure, security logs, backups, or providers retain data.
- Do not call an authenticated endpoint public merely because the source route exists.
- Keep health success separate from deep dependency verification.

Read [references/trust-page-model.md](references/trust-page-model.md) when drafting or reviewing the pages.
