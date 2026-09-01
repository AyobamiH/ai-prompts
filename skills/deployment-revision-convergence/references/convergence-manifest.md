# Deployment Convergence Manifest

Use `deployment-revision-convergence.v1` and bind it to one source SHA, artifact digest, deployment ID, environment, and runtime revision marker.

Record chronological observations with a sanitized timestamp, source (`direct` or `independent`), readiness status, and observed revision marker. The final configured number of observations must all be ready for the expected marker and must cover both source types. A provider success state without that streak is only `WAIT_FOR_CONVERGENCE`.

The authenticated probe must run after convergence and report its expected revision. Do not store response bodies, credentials, tokens, cookies, or secret values. Store only sanitized stage names and remote tool names needed to locate a failure.

Allow no more than one identical-revision retry, require cleanup and reconciliation first, and stop after a repeated failure. A rollback record names the exact known-good source and deployment, proves provenance, and records a successful restoration probe.
