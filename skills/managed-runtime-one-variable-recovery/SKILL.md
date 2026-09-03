---
name: managed-runtime-one-variable-recovery
description: "Diagnose managed sandbox or container reliability with a one-variable production canary ladder. Use when package/image mismatch, transport, lifetime, session defaults, or provider runtime behavior can each plausibly explain the same long-running command failure."
---

# Managed Runtime One-Variable Recovery

When several runtime layers can produce the same interruption, changing them together destroys the evidence needed to know which boundary mattered.

## Workflow

1. Freeze one workload subject: exact agent command, timeout, repository, verifier contract, publication authority, and expected success evidence.
2. First align compatibility invariants such as SDK/package version and runtime image. Add a machine check that prevents drift.
3. Change one runtime variable per repair: transport, keep-alive/lifetime, default-session policy, process primitive, or another single hypothesis.
4. For every repair, list all intentionally unchanged variables in the PR and regression test.
5. Require exact-head validation and deployment before exercising a fresh production canary.
6. Preserve the previous canary as historical evidence. Never rewrite it to fit the new hypothesis.
7. Compare duration, terminal boundary, provider telemetry, and post-command control continuity across canaries.
8. Stop changing higher layers when the current evidence points to a lower runtime boundary.

## Outcomes

- `READY`: the baseline is frozen, compatibility is aligned, each experiment changes one field, and every experiment has a distinct canary and exact deployment.
- `REFUSED`: multiple runtime variables change in one experiment or the workload itself changes between canaries.

Read [references/runtime-ladder.md](references/runtime-ladder.md). Run `python scripts/check_runtime_ladder.py MANIFEST.json` before interpreting a production canary as evidence for one runtime hypothesis.
