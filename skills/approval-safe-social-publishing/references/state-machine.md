# Approval-Safe Publication State Machine

## Publication record

```json
{
  "publication_id": "stable-id",
  "platform": "linkedin",
  "account_id": "provider-account-id",
  "slot": "immediate-or-scheduled-slot",
  "payload_fingerprint": "sha256",
  "approval": {
    "approved": true,
    "approved_fingerprint": "sha256",
    "approved_at": "ISO-8601",
    "scope": "one publication write"
  },
  "state": "approved",
  "provider_id": null,
  "permalink": null,
  "attempt_count": 0,
  "last_evidence": null
}
```

## States

```text
draft
  -> frozen
  -> approved
  -> staged
  -> publishing
  -> submitted_unverified
  -> verified_published
```

Bounded alternatives:

```text
approval_required
validation_failed
provider_rejected
submitted_for_review
confirmed_absent
reconciliation_required
blocked_account_mismatch
blocked_policy
superseded
```

Only `verified_published`, `provider_rejected`, `confirmed_absent`, `blocked_policy`, and `superseded` are terminal. `submitted_for_review` and `reconciliation_required` require later observation.

## Retry decision

| Prior evidence | Next action |
| --- | --- |
| Composer lost before submit | Restore identical fields; approval remains valid |
| Provider explicitly rejected and no object exists | Repair cause, create new fingerprint if payload changes, request approval when required |
| Provider returned canonical object and readback matches | Mark verified, never resubmit |
| Timeout or crash after submit | Reconcile, do not resubmit |
| Submitted for review | Poll or revisit provider state, do not resubmit |
| Readback proves absence after the provider's visibility window | A new separately approved publication may be considered |
| Multiple plausible objects | Escalate for reconciliation |

## Readback comparison

Check:

- canonical provider ID;
- expected account ownership;
- copy or content hash;
- ordered media identity;
- CTA and destination;
- plausible publication time;
- public or provider permalink;
- moderation or review state.

A successful HTTP response, upload completion, scheduler completion, or provider ID without matching readback is not verified publication.
