# Owner-Only Checkpoint Contract

## User-facing checkpoint

State:

1. Why the owner is needed now.
2. Exact actions awaiting confirmation.
3. Provider, account, app, draft, repository, or domain targeted.
4. Requested scopes and their purpose.
5. External effects and reversibility.
6. Actions explicitly excluded.
7. Secure surface the owner will use.
8. Evidence that will be checked afterward.

## Machine-readable shape

```json
{
  "checkpoint_id": "owner-123",
  "owner_identity": "verified publisher account",
  "expires_at": "2099-01-01T00:00:00Z",
  "actions": [
    {
      "id": "oauth-consent",
      "provider": "GitHub",
      "target": "DoneState app",
      "account": "selected account",
      "operation": "grant OAuth access",
      "scopes": ["read:user"],
      "external_effect": "stores an encrypted access token",
      "maximum_uses": 1,
      "owner_confirmation_required": true,
      "consent_text": "Grant read:user to identify the connected account.",
      "evidence_after": ["connected account", "granted scopes", "revocation path"]
    }
  ],
  "excluded_actions": ["submit for review", "publish publicly"]
}
```

Do not include credentials, authorization codes, raw state values, tokens, private keys, payment data, or unnecessary personal information.
