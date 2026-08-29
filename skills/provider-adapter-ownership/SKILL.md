---
name: provider-adapter-ownership
description: "Own stable local contracts while keeping discovery, repair, runner, verifier, and other external providers replaceable. Use when integrating open-source agent tools, deciding whether to fork or mirror a dependency, adding provider adapters, avoiding product-authority leakage into a vendor, or preserving a local and self-hosted exit path."
---

# Provider Adapter Ownership

Integrate capabilities behind product-owned interfaces. An external tool may supply discovery, repair, or execution without becoming the authority system.

## Workflow

1. Name the capability needed, not the preferred project. Examples: `MaintenanceSource`, `RepairProvider`, `RunnerProvider`, `VerifierProvider`.
2. Define a minimal local contract with versioned inputs, outputs, errors, timeouts, cancellation, identity, and evidence fields.
3. Implement one reference adapter using the current provider and a deterministic fake for contract tests.
4. Keep admission, policy, audit, and final state transitions in the owning product.
5. Pin provider versions, container digests, schemas, and protocol compatibility.
6. Record licence, provenance, modifications, security posture, release cadence, and support assumptions.
7. Prefer upstream dependencies or thin adapters. Fork or mirror only for availability, security response, or required changes that cannot be maintained upstream.
8. When mirroring, preserve history and notices, document the sync process, and avoid implying authorship.
9. Add compatibility tests before switching providers. Test timeouts, malformed output, partial effects, duplicate delivery, and provider unavailability.
10. Maintain an exit path such as a local process, Docker image, or second provider when lock-in would threaten the product boundary.

## Boundaries

- A discovery provider finds candidates; it does not authorize repairs.
- A repair provider proposes or applies a bounded patch; it does not approve or merge it.
- A runner executes admitted work; it does not decide standing authority.
- A verifier re-observes facts; it must remain independent of the effect when policy requires independence.

Use [references/adapter-contract.md](references/adapter-contract.md) to evaluate an integration before adding it to the runtime.
