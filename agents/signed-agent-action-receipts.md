# Signed agent action receipts

A production prompt for building an evidence-bound execution system in which consequential agent actions require transaction-specific approval, execute exactly once, are independently verified and produce offline-verifiable signed receipts.

This prompt is based on a working TypeScript implementation that protects one bounded repository-patch action. It deliberately starts with one action instead of pretending to secure every tool call at once.

## Requirements

- Node.js 22.5 or newer with ESM and TypeScript strict mode.
- Git and a local filesystem.
- Durable SQL storage such as SQLite or PostgreSQL.
- Separate key material for approval authority and receipt signing.
- Ed25519 and SHA-256 support.
- A disposable Git repository for the end-to-end test.
- A process-spawning API so mutation, signing and verification can be kept outside the proposer process.

No hosted service, graph framework or external cryptography package is required. Prefer Node's standard cryptography primitives and the repository's existing SQL layer.

## Prompt: build independently verifiable receipts for agent actions

Paste everything below the line into an AI coding assistant. Replace bracketed repository names and paths where required, but keep the trust boundaries, canonicalisation rules and failure semantics unchanged.

---

Build a production-grade signed receipt system for consequential agent actions.

The first supported action must be a bounded repository patch named:

```text
agentproof.repository_patch.v1
```

Do not begin by building a generic framework that claims to secure arbitrary tools. Complete and verify this one action end to end, then expose extension points for future actions.

## Objective

A proposer should be able to describe an intended repository change, prepare an exact bounded transaction, obtain approval for that exact prepared state, execute it once, independently observe the resulting repository state and receive a signed receipt that an offline verifier can validate without trusting the executor.

The terminal result must prove:

1. the exact approved transaction was the transaction executed;
2. the action was claimed exactly once;
3. retries cannot cause a second mutation;
4. verification observed the resulting state independently of the executor's success claim;
5. the signed receipt binds the authority, transaction, correlation, policy, evidence and outcome;
6. a cryptographically valid receipt is not automatically trusted;
7. recovery can reconcile a crash after mutation without inventing success;
8. compensation creates an authenticated successor receipt rather than rewriting history.

## Trust roles

Keep these five roles distinct in both code and data:

1. **Proposer**
   - Describes intent.
   - Selects the requested action.
   - Prepares a bounded transaction.
   - Cannot approve the transaction.
   - Cannot sign the receipt.

2. **Approval authority**
   - Approves or rejects one exact prepared request.
   - Binds the decision to the request digest, transaction ID, correlation ID, authority environment, issuer, expiry and nonce.
   - Cannot mutate the repository through the executor interface.
   - Uses separate key material from the receipt signer.

3. **Executor**
   - Applies only a valid, unexpired and previously unused approval.
   - Runs in a separate process from the proposer.
   - Cannot mint approval decisions.
   - Cannot possess the receipt-signing private key.

4. **Receipt signer**
   - Signs independently assembled verified evidence through an injected signing provider.
   - Does not perform the repository mutation.
   - Must not accept an executor-authored success statement as sufficient evidence.

5. **Offline verifier**
   - Reconstructs the canonical signature input.
   - Recomputes all digests.
   - Verifies Ed25519.
   - Applies a separately supplied signer fingerprint and authority policy.
   - Returns identities only from the signed payload.
   - Does not trust the executor, transport envelope or embedded key by default.

Do not collapse these roles merely because a development build runs them under one operating-system account. Process separation is a capability boundary, not an OS sandbox.

## Package shape

Create a small ESM TypeScript package with:

```text
src/
  actions/
    repository-patch/
      prepare.ts
      execute.ts
      verify.ts
      compensate.ts
      types.ts
  approval/
    request.ts
    decision.ts
    verify.ts
  canonical/
    canonical-json.ts
    digest.ts
  cli/
    agentproof.ts
    development-authority.ts
  crypto/
    ed25519.ts
    fingerprint.ts
    signing-provider.ts
  execution/
    claim.ts
    reconcile.ts
    state-machine.ts
  receipts/
    assemble.ts
    sign.ts
    verify.ts
    types.ts
  storage/
    migrations/
    store.ts
  index.ts
docs/
  trust-model.md
  signed-receipt-v2.md
  repository-patch-v1.md
test/
  unit/
  integration/
  adversarial/
```

Use strict TypeScript. Do not use `any`. Package imports must not perform network calls, scan environment variables, discover repositories, start services or create background timers.

Every operation must receive an explicit absolute state directory and explicit repository root.

## Protected action

The first action is an exact allowlisted patch against a local Git repository.

Support operations:

```ts
type RepositoryPatchOperation =
  | {
      kind: "write";
      path: string;
      contentBase64: string;
    }
  | {
      kind: "delete";
      path: string;
    };
```

The action request must include:

```ts
interface RepositoryPatchRequest {
  schema: "agentproof.protocol.repository-patch-request";
  schemaVersion: "1.0.0";
  actionType: "agentproof.repository_patch.v1";
  correlationId: string;
  stateDirectory: string;
  action: {
    type: "agentproof.repository_patch.v1";
    repositoryRoot: string;
    operations: RepositoryPatchOperation[];
  };
  intent: {
    summary: string;
    requestedBy: string;
    acceptanceCriteria: string[];
  };
  policy: {
    allowedRepositoryRoot: string;
    allowedTrackedPaths: string[];
    allowedNewPaths: string[];
    maxPatchBytes: number;
    maxFiles: number;
  };
}
```

For the reproducible example use:

```text
maxPatchBytes = 1024
maxFiles = 1
allowedTrackedPaths = ["protected.txt"]
allowedNewPaths = []
```

The preparer must reject:

- a non-absolute repository root or state directory;
- a repository root outside the allowed root;
- a dirty working tree;
- a detached HEAD;
- symlinks in any protected path;
- submodules;
- path traversal;
- absolute patch paths;
- `.git` writes;
- undeclared tracked or new paths;
- files exceeding the approved count or byte budget;
- secret-bearing paths or obvious secret material;
- duplicated operations for the same path;
- unsupported operation kinds;
- malformed Base64;
- a repository whose before-state changes while preparation is occurring.

Do not commit, push, tag, deploy or change remotes.

## Prepared transaction

Preparation must be read-only.

Create an immutable prepared transaction containing at least:

```ts
interface PreparedTransaction {
  schema: "agentproof.protocol.prepared-transaction";
  schemaVersion: "1.0.0";
  actionType: "agentproof.repository_patch.v1";
  transactionId: string;
  correlationId: string;
  stateDirectory: string;
  preparedAt: string;
  repository: {
    root: string;
    headSha: string;
    branch: string;
    remotesDigest: string;
    beforeManifestDigest: string;
    clean: true;
  };
  intent: RepositoryPatchRequest["intent"];
  policy: RepositoryPatchRequest["policy"];
  operations: Array<
    RepositoryPatchOperation & {
      beforeDigest: string | null;
      afterDigest: string | null;
      byteLength: number;
    }
  >;
  requestDigest: string;
}
```

Generate `transactionId` independently from `correlationId`.

The request digest must cover the complete canonical prepared transaction except the digest field itself. It must bind:

- transaction ID;
- correlation ID;
- action type;
- repository identity;
- before-state;
- exact operations;
- intent;
- acceptance criteria;
- policy;
- preparation timestamp.

Do not treat a human-readable summary as the approval target.

## Canonical JSON

Implement one canonical JSON function and use it for every signed or digested object.

Rules:

- recursively sort object keys by Unicode code-unit order;
- preserve array order;
- preserve JSON string code points;
- preserve `null`;
- normalise negative zero to zero;
- reject `NaN`, positive infinity and negative infinity;
- reject `undefined`, functions, symbols and bigint values;
- reject non-plain objects;
- reject cyclic values;
- reject duplicate object keys while parsing CLI JSON.

Do not rely on ordinary `JSON.stringify` insertion order as a security boundary.

## Approval request

Create an approval request from the prepared transaction:

```ts
interface ApprovalRequest {
  schema: "agentproof.protocol.approval-request";
  schemaVersion: "1.0.0";
  actionType: "agentproof.repository_patch.v1";
  transactionId: string;
  correlationId: string;
  requestDigest: string;
  intentSummary: string;
  authorityEnvironmentRequired: "development" | "production";
  expiresAt: string;
  nonce: string;
}
```

The approval request must be deterministic for the same prepared transaction, expiry and nonce.

The development quickstart should use a ten-minute expiry.

## Approval decision

The authority signs a decision:

```ts
interface ApprovalDecisionPayload {
  schema: "agentproof.protocol.approval-decision";
  schemaVersion: "1.0.0";
  decision: "approved" | "rejected";
  actionType: "agentproof.repository_patch.v1";
  transactionId: string;
  correlationId: string;
  requestDigest: string;
  authorityEnvironment: "development" | "production";
  issuer: string;
  issuedAt: string;
  expiresAt: string;
  nonce: string;
}
```

The decision proof must include:

```ts
interface SignatureProof {
  algorithm: "Ed25519";
  publicKeyPem: string;
  keyFingerprint: string;
  payloadDigest: string;
  signatureBase64: string;
}
```

Use a separate development-authority binary:

```text
agentproof-dev-authority --development
```

It must require the explicit `--development` flag for key generation and decisions.

Development decisions must contain:

```text
authorityEnvironment = "development"
```

They must fail closed when execution requires production authority.

The primary CLI must have no:

- `--force`;
- `--skip-approval`;
- `--auto-approve`;
- implicit development-authority fallback.

## Execution request

Execution must receive only identifiers, trusted authority policy and the signed approval:

```ts
interface ExecutionRequest {
  schema: "agentproof.protocol.execution-request";
  schemaVersion: "1.0.0";
  actionType: "agentproof.repository_patch.v1";
  correlationId: string;
  transactionId: string;
  stateDirectory: string;
  idempotencyKey: string;
  requiredAuthorityEnvironment: "development" | "production";
  trustedAuthorityFingerprints: string[];
  approvalDecision: {
    payload: ApprovalDecisionPayload;
    proof: SignatureProof;
  };
}
```

Before mutation, verify:

- complete schema and version;
- action type;
- transaction ID;
- correlation ID;
- request digest;
- decision is `approved`;
- signature;
- authority fingerprint;
- required authority environment;
- expiry;
- nonce format;
- prepared state still exists;
- before-state still matches;
- approval has not been consumed by another transaction;
- idempotency key is valid and consistently bound.

Any mismatch must fail before the write.

## Durable state machine

Persist this state machine:

```text
PREPARED
  → APPROVAL_ACCEPTED
  → CLAIMED
  → EXECUTING
  → MUTATION_OBSERVED
  → VERIFIED
  → RECEIPT_SIGNED
  → COMPLETED

Any state may transition to:
  → REJECTED
  → FAILED
  → RECONCILIATION_REQUIRED
  → COMPENSATION_REQUIRED
  → COMPENSATED
```

Transitions must be append-only events with:

- transaction ID;
- correlation ID;
- sequence number;
- previous event digest;
- event digest;
- event type;
- timestamp;
- actor role;
- bounded metadata.

Do not overwrite history when status changes.

## Durable SQL records

Create durable records equivalent to:

```sql
CREATE TABLE transactions (
  transaction_id TEXT PRIMARY KEY,
  correlation_id TEXT NOT NULL,
  action_type TEXT NOT NULL,
  request_digest TEXT NOT NULL,
  prepared_json TEXT NOT NULL,
  state TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE idempotency_claims (
  idempotency_key TEXT PRIMARY KEY,
  transaction_id TEXT NOT NULL,
  request_digest TEXT NOT NULL,
  claimed_at TEXT NOT NULL,
  terminal_receipt_json TEXT
);

CREATE TABLE approval_consumption (
  approval_payload_digest TEXT PRIMARY KEY,
  transaction_id TEXT NOT NULL,
  consumed_at TEXT NOT NULL
);

CREATE TABLE transaction_events (
  transaction_id TEXT NOT NULL,
  sequence_number INTEGER NOT NULL,
  event_type TEXT NOT NULL,
  event_json TEXT NOT NULL,
  previous_event_digest TEXT,
  event_digest TEXT NOT NULL,
  created_at TEXT NOT NULL,
  PRIMARY KEY (transaction_id, sequence_number)
);

CREATE TABLE receipts (
  transaction_id TEXT NOT NULL,
  receipt_payload_digest TEXT PRIMARY KEY,
  receipt_json TEXT NOT NULL,
  predecessor_payload_digest TEXT,
  created_at TEXT NOT NULL
);
```

Use database uniqueness, not in-memory maps, for idempotency and approval consumption.

## Exactly-once semantics

Exactly-once means one externally observable mutation for one approved transaction under one idempotency key.

Implement these rules:

1. Claim the idempotency key durably before mutation.
2. Bind it to transaction ID and request digest.
3. If the same key is retried with different transaction data, reject it.
4. If a completed claim has a receipt, return the exact original signed receipt bytes.
5. If a claim is non-terminal, inspect durable state and reconcile.
6. Concurrent claims must have exactly one winner.
7. Never rerun the mutation merely because receipt signing or transport failed.

The end-to-end test must run the same execution request twice and prove both output files have the same SHA-256 value.

## Separate executor process

Run repository mutation in a child process with a narrow input document.

The child process may receive:

- repository root;
- exact operations;
- expected before digests;
- expected HEAD;
- bounded policy;
- transaction identifier.

It must not receive:

- approval private key;
- receipt-signing private key;
- arbitrary shell text;
- network credentials;
- unrelated environment variables.

Use an explicit environment allowlist when spawning it.

Capture bounded stdout, stderr, exit code and timing evidence. Do not interpret exit code zero as verified success.

## Independent verification

After execution, a verifier that did not perform the mutation must re-read the repository and determine the result.

Verify at least:

- repository root identity;
- branch and HEAD;
- worktree state;
- exact changed paths;
- exact file digests;
- no undeclared paths;
- remotes unchanged;
- `.git` metadata not modified outside expected worktree effects;
- acceptance criteria represented by deterministic checks;
- bounded command evidence where explicitly approved.

Represent evidence as structured data:

```ts
interface VerifiedEvidence {
  verifierVersion: string;
  observedAt: string;
  repository: {
    rootDigest: string;
    headSha: string;
    branch: string;
    remotesDigest: string;
    changedPaths: string[];
    afterManifestDigest: string;
  };
  operations: Array<{
    path: string;
    expectedAfterDigest: string | null;
    observedAfterDigest: string | null;
    matches: boolean;
  }>;
  checks: Array<{
    name: string;
    commandDigest?: string;
    exitCode?: number;
    stdoutDigest?: string;
    stderrDigest?: string;
    passed: boolean;
  }>;
  outcome: "verified_success" | "verified_failure" | "unresolved";
}
```

Only `verified_success` may produce a success receipt.

`unresolved` must remain unresolved. Do not transform absence of evidence into success.

## Signed Receipt V2

Use this exact domain separator:

```text
agentproof.signed-receipt.v2\0
```

The signature input is:

```text
UTF-8("agentproof.signed-receipt.v2\0" + canonicalJson(payload))
```

The receipt contains only:

```ts
interface SignedReceiptV2 {
  payload: SignedReceiptPayloadV2;
  proof: SignatureProof;
}
```

The signed payload must include:

```ts
interface SignedReceiptPayloadV2 {
  schema: "agentproof.signed-receipt";
  schemaVersion: "2.0.0";
  receiptId: string;
  actionType: "agentproof.repository_patch.v1";
  transactionId: string;
  correlationId: string;
  idempotencyKeyDigest: string;
  requestDigest: string;
  authority: {
    environment: "development" | "production";
    issuer: string;
    approvalPayloadDigest: string;
    authorityKeyFingerprint: string;
    expiresAt: string;
    nonce: string;
  };
  execution: {
    claimedAt: string;
    startedAt: string;
    observedAt: string;
    completedAt: string;
    executorVersion: string;
  };
  intent: {
    summary: string;
    requestedBy: string;
    acceptanceCriteria: string[];
  };
  policyDigest: string;
  evidence: VerifiedEvidence;
  result: {
    status: "verified_success" | "verified_failure" | "compensated";
    summary: string;
  };
  predecessorPayloadDigest?: string;
}
```

`proof.payloadDigest` is SHA-256 of the exact domain-separated signature-input bytes.

Every identity or policy claim returned by the verifier must come from this signed payload, never from an unsigned transport wrapper.

## Signer fingerprint

Derive the signer fingerprint from the canonical public key representation using SHA-256 and format it consistently, for example:

```text
sha256:<lowercase-hex>
```

The receipt may embed the public key so an offline verifier can check signature self-consistency.

That embedded key does not establish identity.

Trust requires the caller to supply an acceptable signer fingerprint out of band:

```text
agentproof verify-receipt \
  --input ./receipt.json \
  --trust-fingerprint sha256:<trusted-fingerprint>
```

Return separate fields:

```ts
{
  cryptographicallyValid: boolean;
  trusted: boolean;
  signerFingerprint: string;
  authorityEnvironment: "development" | "production" | null;
  reasons: string[];
}
```

A valid signature from an unpinned key must produce:

```text
cryptographicallyValid = true
trusted = false
```

## Legacy receipt rejection

Add an explicit legacy-receipt failure.

A previous receipt format that did not bind authority environment, transaction ID and correlation ID must never return `trusted: true`, even when its inner Ed25519 signature is mathematically valid.

Return a stable reason such as:

```text
legacy_unbound_receipt
```

Do not silently upgrade, rewrite or re-sign legacy receipts. Preserve them as historical untrusted evidence.

## Crash recovery and reconciliation

Filesystem mutation and SQL state cannot form one atomic distributed transaction.

Handle crashes at every boundary:

- after idempotency claim but before mutation;
- during file writes;
- after mutation but before observation;
- after observation but before receipt signing;
- after receipt signing but before response delivery.

On restart:

1. load the prepared transaction and event chain;
2. re-observe repository state;
3. classify it as exact-before, exact-after, divergent or unreadable;
4. continue only from evidence;
5. sign a success receipt only for exact verified-after state;
6. return the original receipt if it was already signed;
7. require compensation or escalation for divergent state.

Do not rerun the write merely because the last recorded state is `EXECUTING`.

## Compensation

Compensation is a new authenticated action.

It must:

- require the trusted predecessor receipt;
- re-verify the predecessor signature and pinned signer;
- confirm the current repository state matches the predecessor's verified after-state;
- restore the exact prepared before-state when possible;
- independently verify the restoration;
- issue a new signed Receipt V2;
- set `predecessorPayloadDigest` to the predecessor's signed payload digest.

Never mutate or replace the predecessor receipt.

A valid chain is append-only:

```text
original verified receipt
  → compensation receipt
  → optional later successor
```

Reject broken or untrusted predecessor chains.

## CLI

Implement:

```text
agentproof prepare repository-patch --input <request.json>
agentproof approval-request --input <prepared.json> --expires-at <iso> --nonce <nonce>
agentproof execute --input <execution.json> --receipt-key <private.pem>
agentproof status --input <status-query.json>
agentproof reconcile --input <status-query.json> --receipt-key <private.pem>
agentproof compensate --input <status-query.json> --receipt-key <private.pem> --trust-fingerprint <fingerprint> --authority-environment <environment>
agentproof verify-receipt --input <receipt.json> --trust-fingerprint <fingerprint> --required-authority-environment <environment>

agentproof-dev-authority --development keygen --private-key-output <private.pem>
agentproof-dev-authority --development decide --input <approval-request.json> --private-key <private.pem> --decision approved --issuer <issuer>
```

CLI output must be machine-readable JSON on stdout. Human diagnostics go to stderr. Never print private key material.

## SDK exports

Expose only stable public operations:

```ts
export {
  prepareRepositoryPatch,
  createApprovalRequest,
  executeApprovedTransaction,
  getTransactionStatus,
  reconcileRepositoryPatch,
  compensateRepositoryPatchWithReceipt,
  verifyReceipt,
};
```

Keep internal storage, canonicalisation and executor plumbing private unless a public type is required.

## Security constraints

Fail closed for:

- altered prepared transactions;
- altered approval decisions;
- expired approvals;
- replayed approvals;
- reused idempotency keys with different data;
- untrusted authority fingerprints;
- untrusted receipt signer fingerprints;
- development approval presented as production authority;
- before-state drift;
- dirty or wrong repositories;
- detached HEAD;
- path escapes;
- symlinks;
- submodules;
- `.git` writes;
- undeclared changes;
- malformed or duplicate-key JSON;
- oversized patches;
- secret-bearing paths or content;
- missing verification evidence;
- broken predecessor chains.

Document what the system does not prove:

- that the proposer is benevolent;
- that user-selected verification commands are complete;
- that the OS account is uncompromised;
- that process separation is an OS sandbox;
- that a development key is production authority;
- that an embedded public key is a trusted identity;
- that exact-once SQL claiming creates a distributed atomic commit with the filesystem.

## Tests

Write unit, integration and adversarial tests.

At minimum prove:

### Preparation

- clean allowlisted one-file patch prepares successfully;
- dirty repository is rejected;
- path traversal is rejected;
- `.git` path is rejected;
- symlink and submodule cases are rejected;
- before-state drift is detected;
- byte and file limits are enforced.

### Approval

- approval binds transaction ID, correlation ID and request digest;
- changed action data invalidates approval;
- expired approval is rejected;
- altered authority environment is rejected;
- development authority cannot satisfy production policy;
- one approval cannot authorise a different transaction.

### Exactly-once execution

- first execution mutates once;
- identical retry returns byte-for-byte identical signed receipt;
- same idempotency key with different transaction is rejected;
- concurrent identical executions produce one mutation and one terminal receipt;
- approval consumption is durable across process restart.

### Verification

- exit code zero with wrong repository state is not success;
- undeclared file changes fail verification;
- remotes or HEAD drift fail verification;
- verified evidence is assembled by re-observation;
- unresolved state remains unresolved.

### Receipts

- valid receipt verifies cryptographically;
- trusted fingerprint produces `trusted: true`;
- different fingerprint produces valid-but-untrusted;
- changing any signed field breaks verification;
- payload digest is recomputed;
- duplicate-key JSON is rejected;
- legacy unbound receipt never becomes trusted;
- verified identities come only from signed payload.

### Recovery

- crash before mutation resumes without writing twice;
- crash after mutation reconciles exact-after state;
- crash after signing returns the stored original receipt;
- divergent state does not become success.

### Compensation

- compensation requires a trusted predecessor;
- restoration is independently verified;
- successor binds predecessor payload digest;
- predecessor receipt remains unchanged;
- broken chain is rejected.

## Reproducible end-to-end demonstration

Create a disposable Git repository:

```sh
LAB="$(mktemp -d)"
REPO="$LAB/repository"
STATE="$LAB/state"

mkdir -p "$REPO"
git -C "$REPO" init -b main
git -C "$REPO" config user.email agentproof@example.invalid
git -C "$REPO" config user.name "AgentProof Quickstart"

printf 'before\n' > "$REPO/protected.txt"
git -C "$REPO" add protected.txt
git -C "$REPO" commit -m baseline
```

Prepare a request that writes exactly:

```text
after
```

to `protected.txt`, with:

```text
correlationId = "readme-quickstart-001"
maxPatchBytes = 1024
maxFiles = 1
allowedTrackedPaths = ["protected.txt"]
```

Then demonstrate:

1. preparation;
2. approval request with a ten-minute expiry;
3. development authority key generation;
4. signed development approval;
5. receipt signer key generation;
6. execution;
7. offline verification with the pinned receipt fingerprint;
8. identical execution retry;
9. SHA-256 equality of original and retry receipts;
10. compensation;
11. clean repository after compensation.

Expected evidence:

```text
cryptographicallyValid: true
trusted: true
```

The two receipt files must have identical SHA-256 values.

The compensation receipt must contain the original receipt's payload digest as `predecessorPayloadDigest`.

The final command must prove:

```sh
test "$(git -C "$REPO" status --porcelain)" = ""
```

## Documentation

Write:

- a trust model explaining all five roles;
- the exact Receipt V2 signature and canonicalisation protocol;
- the protected repository-patch action;
- recovery and compensation semantics;
- development-versus-production authority limitations;
- an offline verification guide;
- a security limitations section.

Do not describe development authority, shared-user process separation or an embedded public key as production-grade identity security.

## Completion contract

Do not report completion until all of the following are true:

- the package builds from a clean checkout;
- strict type checking passes;
- all unit, integration and adversarial tests pass;
- the disposable repository demonstration passes;
- the retry receipt is byte-for-byte identical;
- offline verification distinguishes validity from trust;
- production policy rejects development authority;
- crash reconciliation is tested after the mutation boundary;
- compensation produces a linked successor receipt;
- no primary CLI bypasses approval;
- no private key is available to the executor;
- no success receipt can be produced from executor claims alone;
- documentation states the remaining trust limitations honestly.

Finish with:

```text
Implemented:
Verified:
Exactly-once evidence:
Trust-boundary evidence:
Recovery evidence:
Compensation evidence:
Known limitations:
Next safe extension:
```

The next safe extension should name one additional bounded action and explain which invariants are reused. Do not claim arbitrary-tool support until that action has its own preparation, authority, execution, observation, verification and receipt contract.
