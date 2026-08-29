---
name: openai-domain-verification
description: "Complete an OpenAI app domain challenge by serving the exact one-time value from the required public path and proving the live deployment before verification. Use when an app-directory draft generates a domain challenge, when the verification route is missing or stale, or when GitHub and Cloudflare deployment state must be reconciled before retrying verification."
---

# Openai Domain Verification

Treat the challenge value as public proof of domain control, not as a runtime credential. Still keep it scoped to the exact draft and route.

## Workflow

1. Capture the exact challenge path, value, target hostname, draft identity, and expiry from the provider UI.
2. Confirm the value grants no API, OAuth, account, or deployment authority. If it does, treat it as a secret instead of using this workflow.
3. Add a minimal route that returns only the exact required value with a plain, stable content type and no authentication, redirect, template wrapper, or extra whitespace.
4. Prefer deployment configuration for the value when the provider supports it. Do not place unrelated credentials in source or CI.
5. Add a route test that checks path, status, body equality, method handling, and absence of secret-bearing headers.
6. Commit the route and configuration documentation, then run required validation and CI on the exact head.
7. Deploy that exact subject through the repository's supported path. Do not assume a merged change became live.
8. Read the public URL from outside the authenticated application path. Compare response bytes with the challenge value.
9. Trigger provider verification only after public readback passes.
10. Record draft, commit, deployment, path, response digest, verification result, and cleanup policy.

## Failure handling

- A 404 means the live deployment lacks the route, even if local tests pass.
- A correct route on an older hostname does not verify the submitted domain.
- A merged commit with no deployment evidence remains unproven.
- If CI did not trigger, diagnose the missing run instead of inventing a successful check.
- If the provider issued a new challenge, replace the old value and repeat exact readback.

Use [references/challenge-record.md](references/challenge-record.md) to preserve the evidence without exposing unrelated configuration.
