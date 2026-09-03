# Terminal Receipt Contract

The receipt must be:

- outside the repository workspace;
- atomically written;
- versioned;
- bound to run ID, action ID, repository, and base subject;
- terminal, not heartbeat-like;
- the only completion oracle;
- free of secret values.

The durable intent records the exact receipt path and launch attempt before effect admission. Missing receipt after the deadline is ambiguous, not retryable success or failure.
