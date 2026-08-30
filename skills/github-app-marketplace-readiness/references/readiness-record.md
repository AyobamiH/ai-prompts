# GitHub App Marketplace Readiness Record

## Evidence boundaries

Bind every gate to one `app_subject`, for example `github-app:<app-id>:<slug>:<listing-revision>`. Evidence should contain provider URLs, immutable IDs, timestamps, commit SHAs, workflow run IDs, or redacted screenshots. It must not contain credential values, webhook secrets, tokens, authorization codes, cookies, private keys, or full signed payloads.

Keep these states distinct:

- `draft_saved`: the listing or App configuration is saved, but no owner or review outcome is implied.
- `owner_action_ready`: technical preparation is complete and one precise owner checkpoint remains.
- `review_ready`: required technical, agreement, billing, legal-owner, and validation gates passed; submission is still a separate action.
- `published_verified`: GitHub approved the listing and an unauthenticated readback resolves the intended public listing.

## Required gates

All states require:

- `app_identity`
- `public_profile`
- `trust_and_support_pages`
- `callback_and_webhook_urls`
- `webhook_secret_configured`
- `permission_model`
- `installation_policy`

`owner_action_ready` also requires `owner_checkpoint`.

`review_ready` also requires:

- `marketplace_agreement`
- `listing_content`
- `billing_and_legal_declarations`
- `webhook_delivery`
- `install_uninstall_test`
- `release_validation`

`published_verified` also requires `review_approval` and `public_listing_readback`.

## Webhook-secret closure

1. Generate at least 32 random bytes through a password manager or a controlled terminal, such as `openssl rand -hex 32`.
2. Transfer the value only through the providers' secure secret inputs. Record the secret name or version, never the value.
3. Update the App webhook configuration and the receiving runtime or repository secret under one planned rotation.
4. Read back configuration metadata without exposing the value.
5. Observe a signed delivery accepted by the receiver and a deliberately invalid signature rejected.
6. If the update acknowledgement is missing, mark the write ambiguous and reconcile before retrying.

## Compact manifest

```json
{
  "app_subject": "github-app:123456:example-app:listing-v3",
  "target_state": "review_ready",
  "expected_installation_scope": "selected_repositories",
  "observed_installation_scope": "selected_repositories",
  "expected_permissions": {"contents": "read", "pull_requests": "write"},
  "observed_permissions": {"contents": "read", "pull_requests": "write"},
  "expected_events": ["installation", "installation_repositories", "pull_request"],
  "observed_events": ["installation", "installation_repositories", "pull_request"],
  "gates": {
    "app_identity": {
      "subject": "github-app:123456:example-app:listing-v3",
      "status": "pass",
      "evidence_ref": "https://github.com/settings/apps/example-app"
    }
  }
}
```

Each required gate must have the exact subject, `status: pass`, and a non-sensitive evidence reference. A provider settings URL is an evidence location, not proof by itself; retain the corresponding bounded readback outside the public package.
