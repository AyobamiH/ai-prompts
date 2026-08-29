# OAuth Recovery Matrix

| Symptom | Likely class | Evidence to check | Safe recovery |
| --- | --- | --- | --- |
| Expired immediately after old page was reopened | Expired transaction | Issue and callback times | Generate a new authorization transaction |
| Same retry button fails repeatedly | Cached draft connection | Client and redirect metadata in the provider draft | Clear only the draft connection and reconnect |
| Callback says redirect mismatch | Configuration mismatch | Exact registered and requested redirect URIs | Correct registration, deploy, then start fresh |
| State cookie missing | Cookie or proxy issue | Secure, SameSite, domain, path, forwarded protocol | Fix cookie and proxy handling, then start fresh |
| Callback form is blocked | CSP issue | Browser console and `form-action` policy | Permit only the required trusted form target |
| State exists but cannot be consumed | Durable-store or tenant mismatch | State-store key, tenant binding, TTL, atomic consumption | Repair the store, invalidate old transactions, retry fresh |
| Consent succeeds but app remains disconnected | Token exchange or persistence failure | Redacted provider error, one-time code consumption, encrypted storage | Reconcile before asking for consent again |

## Stop conditions

Stop when the requested client, scopes, redirect hostname, provider account, or app identity differs from the approved configuration. Also stop if recovery would require disabling state checks, exposing credentials, accepting a final legal attestation, or granting broader account access than the owner reviewed.

## Evidence record

Store redacted error class, deployed auth version, client identifier digest, redirect URI, issue and callback times, resolved cause, granted scope names, connected account identifier digest, and revocation test. Do not store the raw state, code, token, cookie, or API key.
