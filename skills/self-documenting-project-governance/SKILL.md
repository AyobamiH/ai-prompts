---
name: self-documenting-project-governance
description: "Build a machine-readable project ledger that generates human status views and makes CI reject undocumented governance drift. Use when a long-running autonomous project keeps losing decisions, evidence, deferred work, ownership, or current state across chats, commits, deployments, and provider actions."
---

# Self-Documenting Project Governance

Make durable project state the source of truth. Chat history and manually edited status prose are inputs, not the canonical record.

## Workflow

1. Recover current work from repository history, CI, deployments, provider readback, evidence, and incident records.
2. Store one versioned machine-readable ledger with unique work and evidence identifiers, stream, status, owner, dependencies, exact subject, last update, next action, wait condition, re-entry condition, and stale date.
3. Generate human-readable current status, roadmap, backlog, and evidence views from the ledger. Mark generated files and refuse manual edits that are not reflected in the source ledger.
4. Install a governance-impact CI gate. When product code, workflows, contracts, runtime configuration, or operational behavior changes, require the affected ledger and generated views to change or a specific validated no-impact declaration.
5. Preserve evidence stories as situation, verification, accountability, outcome, content, and measurement. Distinguish observed facts from reported or unproven claims.
6. Keep repository, candidate commit, merge commit, CI, deployment, runtime, credential, provider-review, and publication states separate.
7. Run a scheduled read-only freshness check that reports stale owners and re-entry conditions without mutating product state.
8. Close work only after the exact validated subject and the durable record agree. Defer work only with an owner, reason, next action, re-entry condition, and stale date.

## Boundary with documentation closure

Use this skill to create the durable governance system. Use `documentation-closure-gate` to close an individual change against its exact commit once the system exists.

Read [references/governance-ledger.md](references/governance-ledger.md) for the record contract. Run `python scripts/check_governance_ledger.py LEDGER.json` before enabling the gate.
