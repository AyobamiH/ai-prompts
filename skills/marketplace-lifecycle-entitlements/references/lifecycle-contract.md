# Marketplace Lifecycle Contract

## Required provider actions

Model the provider's complete action set. For the GitHub Marketplace purchase lifecycle this includes `purchased`, `changed`, `cancelled`, `pending_change`, and `pending_change_cancelled`.

Each accepted event binds:

- marketplace and schema version;
- delivery identifier and event name;
- action and effective time;
- account and plan identity in protected state;
- prior and resulting entitlement state;
- duplicate and stale classification;
- observed deployment and environment.

## Receipt

A public or provider-facing receipt should expose only a versioned schema, delivery identifier, action, duplicate flag, stale result, current entitlement state, and current effective time. For a duplicate, use `stale: null` unless the original application result was durably recorded; do not invent it from the current state.

## Refusals

Reject invalid signatures, unknown actions, malformed effective times, unbounded payloads, missing delivery IDs, and environment-secret mismatch. Accepting a signed ping may return success but must not create or change an entitlement.

Never derive repository selection, write scope, execution admission, merge permission, or deployment permission solely from an entitlement.
