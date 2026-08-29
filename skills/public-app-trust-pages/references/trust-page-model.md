# Public App Trust Page Model

## Health

Include service name, public version, status, observation time, and bounded dependency states. Use degraded status when a required dependency is unavailable. Avoid secret names, internal IPs, stack traces, account identifiers, and configuration values.

## Privacy

Cover:

- Controller or operator identity
- Support and privacy contact
- Data categories received
- Purpose and lawful basis where applicable
- Data sent to GitHub, OpenAI, Cloudflare, or other processors
- User-provided API keys and how they are encrypted
- Logs, telemetry, and abuse prevention
- Retention by data class
- User access, correction, export, revocation, and deletion
- International processing if applicable
- Effective date and change notice

## Terms

Cover service scope, eligibility, authorization to connect accounts, acceptable use, usage limits, user-funded provider costs, third-party services, availability, suspension, intellectual property, disclaimers, liability language reviewed for the jurisdiction, changes, termination, and contact.

## Revocation and deletion

Explain separately:

1. How to disconnect the ChatGPT app.
2. How to revoke the OAuth provider grant.
3. How to delete stored credentials.
4. How to request deletion of durable account data.
5. What cannot be deleted immediately and why.

## Verification record

For each route record the public URL, expected status, content type, exact deployment identifier, checked time, content digest, and result. A source file alone does not prove public reachability.
