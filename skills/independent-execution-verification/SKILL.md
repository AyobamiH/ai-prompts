---
name: independent-execution-verification
description: "Gate a consequential action on fresh, independently collected, signed verification bound to the sealed objective and exact execution subject. Use when connecting a controller to an external verifier, validating execution handoffs and Ed25519 signer identity, preventing an executor from self-certifying, or distinguishing scope and substring checks from true exact-content verification."
---

# Independent Execution Verification

Separate execution from judgment. The executor may provide a handoff, but the verifier must obtain the authoritative facts it uses for the verdict.

## Protocol

1. Seal the objective in canonical form before execution. Include required effects, allowed scope, forbidden effects, subject bindings, and evidence policy.
2. Record the pre-execution snapshot and its immutable identifiers.
3. Admit and execute the action under a separate authority decision.
4. Produce a handoff containing the objective digest, attempted action, resulting identifiers, and evidence locators. Treat it as a claim, not proof.
5. Have the verifier re-observe the repository, CI, artifact, deployment, runtime, or other authoritative systems.
6. Bind every observation to the exact subject. Refuse stale, missing, or conflicting bindings.
7. Compute the verdict deterministically under a versioned policy.
8. Sign the canonical result with a pinned verifier identity and context-specific signature domain.
9. Have the controller verify algorithm, key identifier, trust state, signature, objective digest, subject bindings, freshness, and verdict before entering `VERIFIED`.
10. Persist the full record and any known coverage limits.

## Claim precision

File allowlists, required substrings, and CI success do not prove byte-for-byte file equality. Name the strongest property actually checked. Add exact-content digests or a deterministic tree comparison before claiming exact content verification.

Run `python scripts/check_handoff_bindings.py RECORD.json` to validate structural and digest bindings described in [references/verification-record.md](references/verification-record.md). The helper does not verify the cryptographic signature. Complete that step with a reviewed Ed25519 implementation before accepting the result.
