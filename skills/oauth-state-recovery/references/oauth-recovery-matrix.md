# OAuth Recovery Matrix

| Symptom | Likely class | Evidence to check | Safe recovery |
| --- | --- | --- | --- |
| One flow expires after a second flow opens | Shared browser-state names | Per-attempt cookie names and concurrent trace | Namespace browser state per opaque attempt |
| Manual or cloud-browser continuation loses approval state | Cookie continuity assumption | Browser boundary and cookie jar | Bind a one-time proof to the server transaction; do not require the missing cookie |
| Approval write is immediately absent in another region | Eventual consistency | Write/read regions and store guarantees | Serialize the transaction in strongly consistent storage |
| Durable state works locally but fails across provider-shaped requests | Runtime-object portability | Stored record fields and serialization | Project to a plain versioned record before persistence or sealing |
| Cross-request store repeatedly expires the handoff | Storage is the fragile boundary | TTL, read path, deployment bindings | Carry an authenticated, expiring sealed transaction with exact bindings |
| Old page fails immediately | Expired transaction | Issue and callback times | Generate a completely fresh transaction |
| Same retry button repeats the failure | Cached draft connection | Provider draft client and redirect metadata | Clear only the affected draft connection, deploy, and reconnect |
| Callback says redirect mismatch | Configuration mismatch | Exact registered and requested redirect URIs | Correct registration, deploy, then start fresh |
| Callback form is blocked | CSP issue | Browser console and `form-action` policy | Add only the exact trusted callback or form origin |
| Consent succeeds but app remains disconnected | Exchange or persistence failure | Redacted provider error and one-time code use | Reconcile before asking for consent again |

## Required adversarial tests

- Two concurrent attempts remain isolated.
- Cookie-free handoff succeeds only with the correct one-time proof.
- Invalid proof, expired transaction, tampered sealed state, wrong client, wrong redirect, and broader scopes fail closed.
- A provider-shaped request round-trips through the selected storage or sealed format.
- The callback cannot consume the same transaction twice.

## Evidence record

Store the redacted error class, deployed auth version, client digest, redirect URI, issue and callback times, storage model, resolved cause, granted scope names, connected-account digest, denial-test outcomes, and revocation result. Never store raw state, proof, authorization code, token, cookie, encryption key, or API key.
