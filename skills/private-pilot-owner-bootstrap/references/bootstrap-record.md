# Private Pilot Bootstrap Record

Use `private-pilot-owner-bootstrap.v1` and choose `ready_for_bootstrap` or `bootstrap_verified` as the target state.

Bind the record to one repository, source SHA, deployment ID, and environment. Record the protected environment's exact target restriction and approval, plus identifiers for the owner-email, password-hash, and database-URI references. State the hash scheme, but never store the values.

The manual workflow is single-use, idempotent, cleans up on failure, and emits a sanitized receipt. The account plan names one workspace, one local owner role, and an exact non-empty scope set. It explicitly denies provider-admin, platform-admin, and separate-tester status.

For `ready_for_bootstrap`, current owner and workspace counts are zero and refusal tests are planned. For `bootstrap_verified`, both counts are exactly one, every positive and negative test passes, and the execution receipt is present. A failed bootstrap must prove cleanup returned the user count to zero.
