# Independent Verification Record

## Compact record

```json
{
  "objective": {
    "objective_id": "obj_123",
    "required_effects": ["change:README.md"],
    "subject": {"repository": "owner/repo", "commit": "0123456789abcdef0123456789abcdef01234567"}
  },
  "handoff": {
    "objective_sha256": "computed canonical objective digest",
    "subject": {"repository": "owner/repo", "commit": "0123456789abcdef0123456789abcdef01234567"}
  },
  "trusted_verifiers": {
    "opstruth-prod": {"algorithm": "Ed25519", "key_id": "key-2026-01"}
  },
  "verification_result": {
    "verifier_id": "opstruth-prod",
    "algorithm": "Ed25519",
    "key_id": "key-2026-01",
    "objective_sha256": "computed canonical objective digest",
    "subject": {"repository": "owner/repo", "commit": "0123456789abcdef0123456789abcdef01234567"},
    "verdict": "VERIFIED",
    "observed_at": "2026-08-29T00:00:00Z",
    "signature": "base64 signature"
  }
}
```

## Cryptographic gate

After structural validation:

1. Resolve the pinned public key by verifier and key identifier.
2. Check revocation and validity at the verification time.
3. Canonicalize the signed result with the signature field omitted.
4. Prefix a protocol-specific domain such as `proof-state-verification-v1`.
5. Verify the Ed25519 signature over the exact bytes.
6. Reject unknown algorithms, keys, contexts, or canonicalization versions.

Do not accept a successful structural check as a valid signature.
