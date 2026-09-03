---
name: post-receipt-runtime-quiescence
description: "Separate implementation completion from managed-runtime channel readiness by enforcing a bounded quiescence interval after a verified terminal receipt before validation begins. Use when the implementation finishes but the next command is interrupted while the runtime connection is still closing."
---

# Post-Receipt Runtime Quiescence

A terminal implementation receipt proves the effect completed. It does not prove the managed runtime is ready for the next long validation command.

## Workflow

1. Verify the terminal receipt and its subject binding first.
2. Record the receipt time as the implementation completion boundary.
3. Start a fixed, versioned quiescence interval before issuing the next validation command through the same managed runtime.
4. During quiescence, do not relaunch implementation or reinterpret process-registry state as success.
5. Resume validation only after the interval has elapsed and the durable checkpoint is still current.
6. If a post-receipt validation command is interrupted by runtime shutdown, classify it at the capability/runtime layer rather than invalidating the already-proven implementation receipt.
7. Preserve that run as terminal evidence and repair forward with a fresh successor after any runtime fix.
8. Pin the quiescence interval in regression tests and governance evidence so an accidental removal cannot recreate the race.

## Outcomes

- `READY`: receipt completion and runtime readiness are separate, the quiescence interval is fixed and enforced, and no second implementation launch is possible.
- `REFUSED`: validation starts immediately after receipt, the delay is unbounded/adaptive without evidence, or a runtime-close error causes implementation replay.

Read [references/quiescence-contract.md](references/quiescence-contract.md). Run `python scripts/check_post_receipt_quiescence.py MANIFEST.json` before chaining long validation immediately after managed-runtime implementation.
