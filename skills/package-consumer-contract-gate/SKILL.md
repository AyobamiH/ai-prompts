---
name: package-consumer-contract-gate
description: "Verify a package's shipped consumer contract across built output, packed archives, clean installation, alternate release artifacts, documented entrypoints, supported toolchains, output equivalence, and durable CI. Use when a pull request changes exports, resolvers, entrypoints, build packaging, or compiler requirements and repository-local tests alone cannot prove what consumers receive."
---

# Package Consumer Contract Gate

Test the artifact a consumer installs, not only the source tree that produced it.

## Workflow

1. Freeze the exact pull-request head, base, package version, documented entrypoints, supported toolchains, and the historical import or invocation that exposed the defect.
2. Trace every packaging path separately: source to build tree, package archive, clean installed package, and any release ZIP or flattened distribution. Do not assume these artifacts share a layout.
3. Run the repository's real build or prepack operation. Assert required paths exist and resolver shims or source-only files are absent where the contract excludes them.
4. Create the package archive, install that archive into a new temporary consumer, and disable workspace or repository resolution that could hide a missing packed file.
5. Exercise the documented modern path, supported legacy path, exact historical reproduction, and representative subpath entrypoints from the clean consumer.
6. Run the locked toolchain and the declared minimum supported toolchain. Document unsupported compilers explicitly rather than broadening the compatibility claim.
7. Compare outputs at the strength the contract requires. Use byte equality when output identity is promised; otherwise record the narrower semantic or marker assertion.
8. Build and unpack every alternate release artifact. Test its own public entrypoint against its actual flattened or namespaced layout.
9. Wire the consumer test into a repository-owned command and remote CI matrix. Update user documentation and the changelog on the same head.
10. Reconcile upstream checks and human review separately. `pending` or `action_required` is not green; stop for the upstream maintainer when workflow approval or merge authority is theirs.

## Outcomes

- `CONTRACT_VERIFIED`: the artifact contract passes, but upstream checks or maintainer approval remain outstanding.
- `READY_FOR_MAINTAINER`: the contract and exact-head checks pass and the maintainer has approved.
- `REFUSED`: any artifact, clean-consumer, minimum-toolchain, documentation, or evidence binding is missing or failed.

Do not force-push, merge, or repeatedly prompt maintainers to convert a verified consumer contract into upstream approval.

Read [references/consumer-contract.md](references/consumer-contract.md) for the manifest. Run `python scripts/check_package_consumer_contract.py CONTRACT.json` before making a package-compatibility or upstream-readiness claim.
