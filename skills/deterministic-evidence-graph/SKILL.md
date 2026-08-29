---
name: deterministic-evidence-graph
description: "Model exact-subject evidence, detect contradictions, and compute reproducible verdicts without delegating judgment to an LLM. Use when combining repository, commit, CI, artifact, deployment, runtime, signature, or receipt evidence; when generating signed snapshots or state deltas; or when a release or autonomous action must be verified offline."
---

# Deterministic Evidence Graph

Build the evidence graph as deterministic data. Use an LLM to explain the graph, never to decide its verdict.

## Workflow

1. Define the subject tuple before collecting evidence. Include every immutable identity needed by the claim.
2. Normalize evidence into typed observations with source, observed time, status, subject bindings, and provenance.
3. Separate observations from claims and verdicts. Preserve negative and unavailable observations.
4. Reject evidence that omits a required subject field or binds to another value.
5. Detect contradictions before evaluating sufficiency. A pass and fail for the same claim, or different values for a single immutable binding, is a contradiction.
6. Evaluate a versioned deterministic policy. Report missing kinds, mismatches, failures, and contradictions.
7. Canonicalize the graph before hashing or signing. Pin the canonicalization and policy versions.
8. If signing, sign the canonical digest and include signer identity, algorithm, key identifier, and verification instructions.
9. Re-observe mutable facts after execution. Do not reuse pre-execution observations as proof of a later effect.

## Verdict discipline

Use explicit states such as `VERIFIED`, `REFUSED`, `INSUFFICIENT_EVIDENCE`, and `CONTRADICTORY_EVIDENCE`. A transport success or a well-formed response is not evidence that the subject is verified.

Run `python scripts/evaluate_graph.py GRAPH.json` for the compact graph schema described in [references/graph-contract.md](references/graph-contract.md). The helper computes binding and sufficiency only. Add domain-specific checks before using it as a release gate.
