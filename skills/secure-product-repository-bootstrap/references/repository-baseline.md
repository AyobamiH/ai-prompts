# Secure Repository Baseline

## Root

- `README.md`: role, users, quick start, architecture, limitations.
- `LICENSE`: verified licence choice.
- `SECURITY.md`: reporting, supported versions, secret handling.
- `CHANGELOG.md`: user-visible changes by version.
- `CONTRIBUTING.md`: local validation and review rules.
- `BOUNDARIES.md`: authority constitution for agentic systems.
- `BOT.md` or `AGENTS.md`: automation permissions and stop conditions.
- `.gitignore`: ecosystem outputs, local state, and secrets.
- `.env.example`: names and safe placeholders only.

## Governance

- `.github/CODEOWNERS`
- Pull request template with validation and evidence fields
- Dependency update policy
- CI workflows with minimal permissions
- Release workflow with exact-subject checks
- ADR directory for durable decisions

## Implementation

- Versioned schemas at trust boundaries
- Durable migrations if state is persisted
- Structured errors and redacted logs
- Timeouts, retries, idempotency, and cancellation
- Provider interfaces around external services
- Health checks that do not expose secrets

## Validation

- Format and lint
- Type or compile check
- Unit tests
- Contract and schema tests
- Denial-path tests
- Restart and recovery tests for durable workflows
- Secret and dependency scans
- Clean installation and artifact-content test

## Refusal checks

Stop before release when default credentials exist, an example contains a usable secret, CI needs broad write permissions, state cannot recover after interruption, schemas are implicit, or package contents include local state.
