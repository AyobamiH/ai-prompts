---
name: ephemeral-runtime-read-retry
description: "Retry a failed idempotent read or materialisation operation in a fresh ephemeral runtime without widening credentials or retrying mutations. Use when a failed shell or container poisons the session that owned the original retry loop."
---

# Ephemeral Runtime Read Retry

A retry loop inside a dead runtime is not a retry strategy. Move retry ownership into the durable orchestrator.

## Workflow

1. Classify the operation before retrying. This skill permits only idempotent, consequence-free reads such as anonymous public clone or fetch.
2. Keep credentials absent from the read path. Introduce mutation credentials only at the later publication boundary that already requires them.
3. Give every retry attempt a fresh runtime identity. Destroy or abandon the failed runtime before the next attempt.
4. Use a small fixed attempt budget and bounded backoff. Record the configured delays rather than sleeping indefinitely.
5. Promote only the first successful runtime into the execution workspace.
6. Preserve one durable logical action even though it spans multiple runtime attempts.
7. Never apply the same retry policy to push, merge, deploy, payment, secret, or other mutating effects.
8. If all attempts fail, settle the read action fail-safe and preserve the failed run as evidence.

## Outcomes

- `READY`: a credential-free idempotent read has bounded fresh-runtime retries and mutations remain non-retriable.
- `REFUSED`: retry occurs inside one poisoned runtime, credentials leak into the read path, or a mutating operation can be replayed.

Read [references/retry-contract.md](references/retry-contract.md). Run `python scripts/check_ephemeral_read_retry.py MANIFEST.json` before enabling retries around an ephemeral runtime.
