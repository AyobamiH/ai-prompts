# Consumer Contract Manifest

Use `package-consumer-contract.v1` and bind the record to one immutable source subject.

Record:

- every documented and required entrypoint, including the exact historical failure path;
- `built`, `packed`, `installed`, and `release` artifact checks, with expected and forbidden paths verified independently;
- a clean archive installation with workspace resolution disabled;
- locked and minimum-supported toolchain results;
- output-equivalence assertions and their strength (`byte-identical` or `semantic`);
- repository-owned test and CI wiring, documentation, changelog, exact upstream check state, and maintainer approval;
- `agent_merge_authority: false` and `contains_secret_values: false`.

The checker reports `CONTRACT_VERIFIED` while an upstream workflow is `pending` or `action_required`, or while maintainer approval is absent. That verdict is not merge readiness.

Treat alternate archives as separate consumer products. An npm tarball may need a resolver shim that a flattened release ZIP must exclude.
