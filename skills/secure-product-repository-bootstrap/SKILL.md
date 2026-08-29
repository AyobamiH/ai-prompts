---
name: secure-product-repository-bootstrap
description: "Bootstrap a production repository with explicit purpose, boundaries, contracts, persistence, security, validation, CI, packaging, and release controls. Use when starting a product or service from scratch, preparing an experimental repository for external use, or filling missing repository foundations before feature development."
---

# Secure Product Repository Bootstrap

Create a repository that can explain what it is, what it may do, how it is tested, and how it is released before adding broad automation.

## Workflow

1. Inspect organization and repository conventions. Preserve existing instructions when bootstrapping into a non-empty tree.
2. Define the product role, intended users, trust boundary, non-goals, and protected actions.
3. Choose the smallest runtime and persistence model that can satisfy durability and recovery requirements.
4. Create typed schemas before integrating providers. Version external contracts from the first release.
5. Add configuration examples with placeholders. Keep credentials out of source, fixtures, logs, and documentation.
6. Implement a minimal vertical path plus denied and recovery paths.
7. Add formatting, linting, type checks, unit tests, contract tests, and secret scanning as applicable.
8. Configure CI with least privilege, pinned dependencies or actions, and no write authority for untrusted contributions.
9. Add ownership, security policy, changelog, release process, contribution guidance, and operational runbooks.
10. Validate from a clean install, inspect the packaged artifact, and record known gaps honestly.

## Baseline files

Adapt the checklist in [references/repository-baseline.md](references/repository-baseline.md). Do not generate files that the chosen ecosystem will not use.

## Completion gate

Do not call the repository production-ready until clean checkout, dependency installation, validation, tests, packaging, documentation, and CI all agree. A scaffold with placeholder behavior is a bootstrap, not an implemented product.
