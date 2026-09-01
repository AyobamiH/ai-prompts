# Reviewer Access Record

Record:

- immutable application version and endpoint under review;
- identity purpose, environment, issue time, expiry, and revocation path;
- permitted reads and explicit denied actions;
- exact callback and form-action origins;
- synthetic dataset or tenant used;
- successful authenticated read;
- refused write, execute, approve, merge, deploy, administer, and secret-access attempts;
- current tool annotations and any internal persistence side effects;
- final revocation or rotation evidence.

Do not record passwords, recovery codes, cookies, tokens, private keys, customer data, or owner authentication material.

The record proves the access boundary, not directory approval. Keep draft, submitted, in-review, approved, published, expired, and revoked states separate.
