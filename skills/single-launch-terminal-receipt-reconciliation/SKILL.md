---
name: single-launch-terminal-receipt-reconciliation
description: "Make a long-running implementation effect exactly-once at the orchestrator boundary by persisting intent before launch and using one durable terminal receipt as the sole completion oracle. Use when launch acknowledgement, process registries, or control RPCs can disappear before the implementation result is known."
---

# Single-Launch Terminal Receipt Reconciliation

Lost acknowledgement is not permission to launch again.

## Workflow

1. Persist a durable implementation intent before the first effect. Bind run, action, repository, base subject, command contract, and receipt location.
2. Admit exactly one implementation launch. Record the start attempt before invoking the managed runtime.
3. Place the receipt outside the mutable repository workspace and write it atomically only at terminal completion.
4. Bind the receipt to the same run/action/repository/base subject and include terminal exit classification plus non-secret timing metadata.
5. Treat the receipt as the sole implementation-completion oracle. Process registries, `getProcess()`, logs, or launch acknowledgements remain diagnostic only.
6. If launch acknowledgement or control RPC is interrupted after intent admission, reacquire the runtime and perform bounded read-only receipt reconciliation.
7. Never relaunch the implementation while the admitted effect is unresolved. Missing or mismatched receipt at the deadline settles `AMBIGUOUS_EFFECT`.
8. Only after a verified terminal receipt may validation or publication continue.

## Outcomes

- `READY`: intent precedes one launch, the receipt is atomic and subject-bound, and all alternate completion oracles are non-authoritative.
- `REFUSED`: launch can repeat after an acknowledgement loss, the receipt sits inside mutable output, or process-registry state can declare success.

Read [references/receipt-contract.md](references/receipt-contract.md). Run `python scripts/check_terminal_receipt.py MANIFEST.json` before relying on a managed runtime for an exactly-once long implementation.
