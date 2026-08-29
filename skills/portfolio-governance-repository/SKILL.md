---
name: portfolio-governance-repository
description: "Create a canonical governance repository that keeps product roles, current status, integration contracts, roadmap, and evidence aligned across a multi-repository portfolio. Use when several agentic products have overlapping responsibilities, current and planned integrations are being confused, shared protocols need one owner, or cross-repository documentation drift makes the combined product direction unclear."
---

# Portfolio Governance Repository

Make the portfolio repository the source of truth for cross-product meaning, not a replacement for product-specific implementation documentation.

## Workflow

1. Inventory repositories, customer-facing products, internal protocols, shared services, owners, and release channels.
2. Assign each product one primary role and list explicit non-goals. Keep the customer-facing surface smaller than the implementation graph.
3. Create a versioned product registry with repository, role, lifecycle, current version, status commit, owners, and authority boundary.
4. Define integration contracts with provider, consumer, current state, schema owner, version, subject bindings, failure semantics, and verification responsibility.
5. Separate `live`, `preview`, `experimental`, `planned`, and `retired`. Never let roadmap prose imply runtime dependency.
6. Maintain current-status documents that point to exact product commits or releases.
7. Keep portfolio decisions and a cross-product roadmap in the canonical repository. Link back from each product repository.
8. Run drift checks when product status or integration contracts change. Require coordinated updates in the same reviewed change set when possible.
9. Record evidence for live integrations, including consumer and provider versions and a reproducible compatibility result.

## Suggested structure

```text
proof-and-state/
  CONSTITUTION.md
  products/registry.json
  integrations/registry.json
  contracts/
  status/
  decisions/
  roadmap/
  evidence/
```

Use [references/portfolio-model.md](references/portfolio-model.md) for fields and review rules. Run `python scripts/check_portfolio_status.py PORTFOLIO.json` to detect duplicate identities, missing records, unknown endpoints, contract omissions, and status drift in the compact model.
