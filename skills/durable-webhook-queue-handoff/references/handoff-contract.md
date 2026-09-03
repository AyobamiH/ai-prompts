# Handoff Contract

Record non-secret evidence for one webhook-to-queue transition:

- provider delivery identity and event type;
- authenticated repository and installation or tenant;
- stable deduplication key;
- finding state before and after the atomic claim;
- fresh run ID;
- whether queue setup settled before webhook acceptance;
- whether execution was excluded from the acceptance wait;
- local queue-failure receipt;
- periodic reconciliation configuration;
- duplicate-delivery convergence test result.

Never store webhook secrets, access tokens, or request bodies merely to prove the handoff.
